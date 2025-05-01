from utils.formatters import format_assignments_as_list
from utils.evaluation_export import export_evaluation_results
from evaluation.checks.grammar import check_grammar
from evaluation.checks.readability import check_readability
from evaluation.checks.code_compilation import check_code_compilation
from evaluation.checks.bloom_consistency import check_bloom_consistency
from evaluation.checks.vector_similarity import (
    check_assignments_similarity,
    check_summaries_similarity,
)


# Set export path
results_path = "evaluation/results"


# Automated evaluation pipeline
def evaluation_pipeline(exercise: dict, target_bloom_level: str, summaries: list, assignments: list) -> None:
    """Evaluates the generated exercise based on various automated checks."""

    exercise = format_assignments_as_list([exercise])[0]
    assignments = format_assignments_as_list(assignments)

    print(f"Automatically evaluating generated {target_bloom_level} - exercise...")
    print("--" * 100)

    # Check grammar
    grammar_errors = check_grammar(exercise)
    print(f"Grammar Errors: {grammar_errors}")
    print("--" * 100)

    # Check readability
    readability_score = check_readability(exercise)
    print(f"Flesch Reading Ease Readability Score: {readability_score}")
    print("--" * 100)

    # Check code compilation
    compilation_result = check_code_compilation(exercise)
    print(f"Code Compilation Result: {compilation_result}")
    print("--" * 100)

    # Check bloom's consistency
    bloom_consistency_results = check_bloom_consistency(exercise)
    print(f"Bloom Classifcation Results by LLM Models: {bloom_consistency_results}")
    print("--" * 100)

    # Check similarity to summaries
    summary_similarity = check_summaries_similarity(exercise, summaries)
    print(f"Similarity to Lecture Slide Summaries: {summary_similarity}")
    print("--" * 100)

    # Check assignment similarity
    assignment_similarity = check_assignments_similarity(exercise, assignments)
    print(f"Similarity to Example Assignments: {assignment_similarity}")
    print("--" * 100)

    # Export results to specified path
    export_evaluation_results(
        results_path,
        exercise,
        target_bloom_level,
        grammar_errors,
        readability_score,
        compilation_result.get("status"),
        bloom_consistency_results,
        summary_similarity,
        assignment_similarity,
    )
