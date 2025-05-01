from core.llm_processor import LLMProcessor

# List of models to evaluate Bloom's consistency
evaluation_models = [
    "gemma3:4b",
    "qwen2.5-coder:7b",
    "mistral:latest",
    "llama3.2:latest",
]


def check_bloom_consistency(exercise: str) -> dict:
    """Check the consistency of the exercise with the target Bloom level."""

    evaluation_results = {}

    # Initialize the LLM processor for each model and generate the Bloom level for the exercise
    for model in evaluation_models:
        eval_model = LLMProcessor(model)
        evaluation_result = eval_model.generate_bloom_level(exercise)
        if isinstance(evaluation_result, str):
            evaluation_results[model] = evaluation_result.lower().strip()
        else:
            evaluation_results[model] = "unknown"

    return evaluation_results
