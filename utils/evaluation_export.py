import os
import json
import uuid
from datetime import datetime
from collections import defaultdict
import pandas as pd


def export_evaluation_results(
    base_results_path,
    exercise,
    target_bloom_level,
    grammar_errors,
    readability_score,
    compilation_result,
    bloom_consistency_results,
    lecture_slide_similarity,
    assignment_similarity,
):
    # Generate unique ID
    entry_id = str(uuid.uuid4().hex[:8])

    # Prepare entry
    new_entry = {
        "id": entry_id,
        "timestamp": datetime.now().isoformat(),
        "exercise": exercise,
        "target_bloom_level": target_bloom_level,
        "grammar_errors": grammar_errors,
        "readability_score": readability_score,
        "compilation_result": compilation_result,
        "bloom_consistency_results": bloom_consistency_results,
        "lecture_slide_similarity": lecture_slide_similarity,
        "assignment_similarity": assignment_similarity,
    }

    # Create subdirectory path by bloom level
    subfolder = os.path.join(base_results_path, "exercises", target_bloom_level)
    os.makedirs(subfolder, exist_ok=True)

    # Full file path
    file_name = f"exercise_{entry_id}.json"
    file_path = os.path.join(subfolder, file_name)

    # Save as JSON
    with open(file_path, "w", encoding="utf-8") as outfile:
        json.dump(new_entry, outfile, ensure_ascii=False, indent=4)

    print(f"Updating tables at {base_results_path}/tables/...")
    update_bloom_consistency_table(base_results_path)
    update_rq1_metrics_table(base_results_path)
    update_similarity_metrics_table(base_results_path)
    update_compilation_table(base_results_path)

    print(f"Exported the results of the evaluated exercise to {file_path}")
    print("--" * 75)


def update_bloom_consistency_table(base_path):
    output_csv_path = os.path.join(base_path, "tables", "bloom_consistency.csv")
    aggregate_bloom_consistency_table(base_path, output_csv_path)


def aggregate_bloom_consistency_table(input_base_path, output_csv_path):
    """
    Aggregates Bloom consistency results across all models per Bloom level.
    Saves a CSV file with average accuracy (%) for each model.
    """
    exercises_path = os.path.join(input_base_path, "exercises")
    bloom_levels = ["remember", "understand", "apply", "analyze", "evaluate", "create"]
    model_scores = defaultdict(lambda: defaultdict(list))

    for level in bloom_levels:
        level_path = os.path.join(exercises_path, level)
        if not os.path.isdir(level_path):
            continue

        for filename in os.listdir(level_path):
            if filename.endswith(".json"):
                file_path = os.path.join(level_path, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    target = data.get("target_bloom_level", "").lower()
                    predictions = data.get("bloom_consistency_results", {})

                    for model, prediction in predictions.items():
                        is_correct = int(prediction.lower() == target)
                        model_scores[level][model].append(is_correct)

    # Build table rows
    rows = []
    for level in bloom_levels:
        row = {"Bloom Level": level}
        for model in sorted(
            {m for level_data in model_scores.values() for m in level_data}
        ):
            scores = model_scores[level].get(model, [])
            avg = round(sum(scores) / len(scores) * 100, 1) if scores else 0.0
            row[model] = avg
        rows.append(row)

    df = pd.DataFrame(rows).fillna(0.0)
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    return df


def aggregate_rq1_metrics_table(input_base_path, output_csv_path):
    """
    Aggregates RQ1 metrics (grammar correctness, readability, and compilation success)
    across Bloom levels from JSON evaluation results and writes a CSV table.
    """
    exercises_path = os.path.join(input_base_path, "exercises")
    bloom_levels = ["remember", "understand", "apply", "analyze", "evaluate", "create"]

    # Collect metrics
    metrics = defaultdict(
        lambda: {
            "grammar_total": 0,
            "grammar_correct": 0,
            "readability_scores": [],
            "compilation_total": 0,
            "compilation_success": 0,
        }
    )

    for level in bloom_levels:
        level_path = os.path.join(exercises_path, level)
        if not os.path.isdir(level_path):
            continue

        for filename in os.listdir(level_path):
            if filename.endswith(".json"):
                with open(
                    os.path.join(level_path, filename), "r", encoding="utf-8"
                ) as f:
                    data = json.load(f)
                    level_data = metrics[level]

                    # Grammar check
                    grammar_errors = data.get("grammar_errors", None)
                    if grammar_errors is not None:
                        level_data["grammar_total"] += 1
                        if grammar_errors == 0:
                            level_data["grammar_correct"] += 1

                    # Readability
                    readability = data.get("readability_score", None)
                    if readability is not None:
                        level_data["readability_scores"].append(readability)

                    # Compilation check. The stored value may be the full result
                    # dict (with status/reason/stderr) or, for older runs, just the
                    # status string. Exercises without Haskell code are excluded.
                    compilation_result = data.get("compilation_result", "")
                    if isinstance(compilation_result, dict):
                        status = compilation_result.get("status", "")
                    else:
                        status = compilation_result
                    status = (status or "").lower()
                    if status == "success" or status.startswith("fail"):
                        level_data["compilation_total"] += 1
                        if status == "success":
                            level_data["compilation_success"] += 1

    # Build rows
    rows = []
    for level in bloom_levels:
        level_data = metrics[level]
        grammar_pct = (
            round(level_data["grammar_correct"] / level_data["grammar_total"] * 100, 1)
            if level_data["grammar_total"] > 0
            else 0.0
        )
        readability_avg = (
            round(
                sum(level_data["readability_scores"])
                / len(level_data["readability_scores"]),
                1,
            )
            if level_data["readability_scores"]
            else 0.0
        )
        # Levels whose exercises contain no Haskell code have nothing to compile;
        # report "-" rather than a misleading 0%.
        compile_pct = (
            round(
                level_data["compilation_success"]
                / level_data["compilation_total"]
                * 100,
                1,
            )
            if level_data["compilation_total"] > 0
            else "-"
        )

        rows.append(
            {
                "Bloom Level": level,
                "Grammar Correct (%)": grammar_pct,
                "Avg. Flesch Score": readability_avg,
                "Code Compiles (%)": compile_pct,
            }
        )

    # Save table
    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    return df


def update_rq1_metrics_table(base_path):
    output_csv_path = os.path.join(base_path, "tables", "rq1_metrics.csv")
    return aggregate_rq1_metrics_table(base_path, output_csv_path)


def aggregate_similarity_table(base_path, output_csv_path):
    """
    Aggregates the max similarity scores between exercises and:
    - their example assignments
    - their relevant lecture slides

    Saves a table with one row per Bloom level containing the average max similarities.
    """
    exercises_path = os.path.join(base_path, "exercises")
    bloom_levels = ["remember", "understand", "apply", "analyze", "evaluate", "create"]

    results = []

    for level in bloom_levels:
        level_path = os.path.join(exercises_path, level)
        if not os.path.isdir(level_path):
            continue

        assignment_max_values = []
        summary_max_values = []

        for filename in os.listdir(level_path):
            if filename.endswith(".json"):
                file_path = os.path.join(level_path, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                    assignment_sims = data.get("assignment_similarity", [])
                    summary_sims = data.get("lecture_slide_similarity", [])

                    if assignment_sims:
                        assignment_max_values.append(max(assignment_sims))
                    if summary_sims:
                        summary_max_values.append(max(summary_sims))

        avg_assign_sim = (
            round(sum(assignment_max_values) / len(assignment_max_values), 3)
            if assignment_max_values
            else 0.0
        )
        avg_summary_sim = (
            round(sum(summary_max_values) / len(summary_max_values), 3)
            if summary_max_values
            else 0.0
        )

        results.append(
            {
                "Bloom Level": level,
                "Max Similarity to Assignment (avg)": avg_assign_sim,
                "Max Similarity to Slide Summary (avg)": avg_summary_sim,
            }
        )

    df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    return df


def update_similarity_metrics_table(base_path):
    output_csv_path = os.path.join(base_path, "tables", "similarity_metrics.csv")
    return aggregate_similarity_table(base_path, output_csv_path)


def aggregate_compilation_table(base_path, output_csv_path):
    """
    Builds a compilation failure taxonomy across all evaluated exercises.

    For every Haskell code block it counts passes and failures, splitting the
    failures into 'incomplete' (truncated/missing-definition fragments) and
    'genuine' (complete code with a real type/semantic error). It reports both
    the overall success rate and the rate restricted to complete code (i.e. with
    incomplete fragments removed from the denominator), the latter being the more
    meaningful indicator of the model's ability to produce correct Haskell.
    Requires result JSONs that store the full compilation_result dict.
    """
    exercises_path = os.path.join(base_path, "exercises")
    bloom_levels = ["remember", "understand", "apply", "analyze", "evaluate", "create"]

    rows = []
    tot = {"snippets": 0, "passed": 0, "incomplete": 0, "genuine": 0}
    for level in bloom_levels:
        level_path = os.path.join(exercises_path, level)
        if not os.path.isdir(level_path):
            continue

        snippets = passed = incomplete = genuine = 0
        for filename in os.listdir(level_path):
            if not filename.endswith(".json"):
                continue
            with open(os.path.join(level_path, filename), "r", encoding="utf-8") as f:
                comp = json.load(f).get("compilation_result", {})
            if not isinstance(comp, dict):
                continue  # older run without detailed compilation data
            blocks = comp.get("compiled_blocks", 0)
            if blocks == 0:
                continue
            snippets += blocks
            errors = comp.get("errors", [])
            passed += blocks - len(errors)
            for e in errors:
                if e.get("reason") == "incomplete":
                    incomplete += 1
                else:
                    genuine += 1

        if snippets == 0:
            continue
        complete = snippets - incomplete
        rows.append({
            "Bloom Level": level,
            "Code Snippets": snippets,
            "Passed": passed,
            "Failed (incomplete)": incomplete,
            "Failed (genuine)": genuine,
            "Success (all) %": round(100 * passed / snippets, 1),
            "Success (complete only) %": round(100 * passed / complete, 1) if complete else "-",
        })
        for k, v in zip(tot, (snippets, passed, incomplete, genuine)):
            tot[k] += v

    if rows:
        complete = tot["snippets"] - tot["incomplete"]
        rows.append({
            "Bloom Level": "ALL",
            "Code Snippets": tot["snippets"],
            "Passed": tot["passed"],
            "Failed (incomplete)": tot["incomplete"],
            "Failed (genuine)": tot["genuine"],
            "Success (all) %": round(100 * tot["passed"] / tot["snippets"], 1),
            "Success (complete only) %": round(100 * tot["passed"] / complete, 1) if complete else "-",
        })

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    return df


def update_compilation_table(base_path):
    output_csv_path = os.path.join(base_path, "tables", "compilation_taxonomy.csv")
    return aggregate_compilation_table(base_path, output_csv_path)
