"""
Headless batch runner that reproduces the evaluation experiment from the paper.

For each (topic, learning objective) pair it mirrors the Streamlit app flow:
classify the Bloom level, retrieve the top-k lecture slides, summarize them,
generate N exercises, and run each through the automated evaluation pipeline
(results are written to evaluation/results/ by the pipeline).

Usage:
    python run_evaluation.py --slides "FP Lecture Notes.pdf" --per-lo 10
    python run_evaluation.py --per-lo 1 --only remember   # quick smoke test
"""

import argparse
import glob
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

from core.llm_processor import LLMProcessor
from core.vector_store import VectorStore
from core.bloom_classifier import BloomClassifier
from core.example_assignments import exercise_types
from utils.helper_functions import extract_text_from_pdf
from utils.formatters import format_summaries_as_prompt
from evaluation.evaluation_pipeline import evaluation_pipeline

# The six (intended Bloom level, topic, learning objective) triples used in the
# original project-thesis experiment (Table 5.7). The learning-objective wording
# is taken verbatim from the thesis. Each level has exactly one designed LO, so
# the intended level is authoritative and drives generation directly; the keyword
# classifier is only run for transparency (see note on `understand` below).
#
# Note: the `understand` LO contains the word "using", which the rule-based
# classifier stems to "use" and matches against the `apply` keyword list, so it
# classifies ambiguously as {apply, understand}. This is why generation must be
# anchored on the intended level rather than the classifier's (set-ordered,
# non-deterministic) first pick.
LEARNING_OBJECTIVES = [
    (
        "remember",
        "Haskell Syntax and Prelude Overview",
        "Students should be able to recognize and recall basic Haskell syntax, "
        "keywords, and built-in functions.",
    ),
    (
        "understand",
        "Type Inference and Haskell Type Signatures",
        "Students should be able to describe the types of Haskell expressions and "
        "explain how type inference works using standard type notation.",
    ),
    (
        "apply",
        "Rewriting Haskell Functions using Recursion",
        "Students should be able to reimplement given Haskell expressions embedded "
        "in the task as equivalent recursive functions, without relying on "
        "higher-order functions.",
    ),
    (
        "analyze",
        "Analyzing Variants of Haskell Functions",
        "Students should be able to analyze provided Haskell functions by breaking "
        "down its structure.",
    ),
    (
        "evaluate",
        "Functional Equivalence and Evaluation Behavior in Haskell",
        "Students should be able to evaluate multiple Haskell implementations of the "
        "same function based on provided code examples, and justify which "
        "implementation is more appropriate under specific evaluation conditions.",
    ),
    (
        "create",
        "User-defined Data Types and Instances in Haskell",
        "Students should be able to design custom data types and implement "
        "appropriate type class instances for them.",
    ),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--slides", default="FP Lecture Notes.pdf")
    parser.add_argument("--per-lo", type=int, default=10,
                        help="Number of exercises to generate per learning objective.")
    parser.add_argument("--only", default=None,
                        help="Run only this Bloom level (for smoke tests).")
    parser.add_argument("--skip", default=None,
                        help="Comma-separated Bloom levels to skip (e.g. 'remember').")
    parser.add_argument("--top-up", action="store_true",
                        help="Only generate the exercises missing to reach --per-lo "
                             "per level (counts existing result JSONs).")
    parser.add_argument("--exercise-model", default="qwen2.5-coder:7b")
    parser.add_argument("--summary-model", default="gemma3:4b")
    parser.add_argument("--num-ctx", type=int, default=4096,
                        help="Context window; the paper uses 4096.")
    parser.add_argument("--k", type=int, default=3,
                        help="Number of slides retrieved per learning objective.")
    args = parser.parse_args()

    print(f"Loading slides from {args.slides!r} ...")
    documents = extract_text_from_pdf(args.slides)
    print(f"Loaded {len(documents)} slide pages.")

    print("Building vector store and embedding slides (first run downloads the model)...")
    vector_store = VectorStore()
    vector_store.add_documents(documents)

    bloom_classifier = BloomClassifier()
    exercise_model = LLMProcessor(model_name=args.exercise_model, num_ctx=args.num_ctx)
    summary_model = LLMProcessor(model_name=args.summary_model, num_ctx=args.num_ctx)

    objectives = LEARNING_OBJECTIVES
    if args.only:
        objectives = [o for o in objectives if o[0] == args.only.lower()]
        if not objectives:
            raise SystemExit(f"Unknown Bloom level: {args.only}")
    if args.skip:
        skip = {s.strip().lower() for s in args.skip.split(",")}
        objectives = [o for o in objectives if o[0] not in skip]
        print(f"Skipping levels: {sorted(skip)}")

    total_generated = 0
    for expected_level, topic, learning_objective in objectives:
        print("\n" + "=" * 80)
        print(f"LEARNING OBJECTIVE [{expected_level}] - {topic}")
        print("=" * 80)

        # Each LO is designed for exactly one Bloom level, so the intended level is
        # authoritative and drives generation + evaluation. The rule-based classifier
        # is run only for transparency (it is non-deterministic when an LO matches
        # several levels, e.g. the `understand` LO also matching `apply`).
        level = expected_level
        classifier_levels = bloom_classifier.classify(learning_objective)
        note = "" if classifier_levels == [level] else "  (classifier ambiguous/diverges)"
        print(f"  Intended Bloom level: '{level}' | classifier: {classifier_levels}{note}")

        assignments = exercise_types.get(level, {}).get("example_assignments", [])

        # Step 2: retrieve related slides + summarize (once per learning objective)
        related_docs = vector_store.find_related_documents(learning_objective, k=args.k)
        print(f"  Retrieved {len(related_docs)} related slides.")
        summaries = [summary_model.generate_summary(d.page_content) for d in related_docs]
        summary_texts = [s["summary"] for s in summaries if isinstance(s, dict) and "summary" in s]
        summaries_for_prompt = format_summaries_as_prompt(summary_texts)
        print(f"  Generated {len(summary_texts)} slide summaries.")

        # Step 3 + 4: generate exercises until per_lo *valid* ones exist for this
        # level. Generation can fail when the model emits unparseable JSON (more
        # likely at temperature=1.0), so we retry rather than skip. With --top-up
        # only the count missing to reach per_lo is generated.
        level_dir = os.path.join("evaluation", "results", "exercises", level)
        existing = len(glob.glob(os.path.join(level_dir, "*.json"))) if args.top_up else 0
        need = max(0, args.per_lo - existing)
        if existing:
            print(f"  {existing} already present; generating {need} more.")

        produced = 0
        attempts = 0
        max_attempts = need * 5 + 5
        while produced < need and attempts < max_attempts:
            attempts += 1
            print(f"\n  --- {level} exercise {produced + 1}/{need} (attempt {attempts}) ---")
            exercise_json = exercise_model.generate_exercise(
                topic, learning_objective, summaries_for_prompt, level
            )
            if not exercise_json:
                print("  Generation failed (no parseable JSON) - retrying.")
                continue
            evaluation_pipeline(exercise_json, level, summary_texts, assignments)
            produced += 1
            total_generated += 1

        if produced < need:
            print(f"  WARNING: only produced {produced}/{need} for '{level}' "
                  f"after {attempts} attempts.")

    print(f"\nDone. Evaluated {total_generated} exercises. "
          f"Results written under evaluation/results/.")


if __name__ == "__main__":
    main()
