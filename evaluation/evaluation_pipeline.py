import os
import textstat
import json
import uuid
from sentence_transformers import SentenceTransformer, util
from evaluation.hs_compilation import check_haskell_code
from utils.text_helpers import split_question
from core.llm_processor import LLMProcessor

# Disable parallelism for tokenizers
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Initiliaze embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize evaluation models
evaluation_models = [
    "gemma3:4b",
    "qwen2.5-coder:7b",
    "llama3.2:latest",
    "mistral:latest",
]

# Set paths
questions_path = "evaluation/questions"
results_path = "evaluation/results"


# Evaluation pipeline
def evaluation_pipeline(question, assignments, target_bloom):
    print("Evaluating generated question...")

    question_json = split_question(question)

    question_embedding = embedding_model.encode(question, convert_to_tensor=True)
    assignments_embeddings = embedding_model.encode(assignments, convert_to_tensor=True)

    # Readability (Only Text Parts)
    text_only = " ".join(question_json["text_parts"])
    readability_score = textstat.flesch_kincaid_grade(text_only)

    # Word Count (Complete Question)
    word_count = len(question_json["full_markdown"].split())

    # Assignment Similarity
    question_similarity = util.pytorch_cos_sim(
        question_embedding, assignments_embeddings
    ).tolist()
    question_similarity = [float(x) for x in question_similarity[0]]

    # Code Compilation
    haskell_code = question_json["code"]
    compilation_result = check_haskell_code(haskell_code)

    # Bloom Classification by LLM models
    evaluation_results = {}
    for model in evaluation_models:
        eval_model = LLMProcessor(model)
        evaluation_result = eval_model.generate_bloom_level(question)
        evaluation_results[model] = evaluation_result

    # Export results
    export_results(
        results_path,
        question,
        haskell_code,
        target_bloom,
        readability_score,
        word_count,
        sum(question_similarity) / len(question_similarity),
        compilation_result,
        evaluation_results,
    )


def export_results(
    results_path,
    question,
    code_part,
    target_bloom,
    readability_score,
    word_count,
    avg_similarity,
    compilation_result,
    evaluation_results,
):
    # Generate a unique ID for the question
    entry_id = str(uuid.uuid4().hex[:8])

    # Create a new entry with the provided data
    new_entry = {
        "id": entry_id,
        "question": question,
        "code_part": code_part,
        "target_bloom": target_bloom,
        "readability_score": readability_score,
        "word_count": word_count,
        "avg_similarity": avg_similarity,
        "compilation_result": compilation_result,
        "evaluation_results": evaluation_results,
    }

    # Check if the results path exists, if not create it
    os.makedirs(results_path, exist_ok=True)

    # Create the file name using the entry ID
    file_name = f"question_{entry_id}.json"
    file_path = os.path.join(results_path, file_name)

    # Save the new entry to a JSON file
    with open(file_path, "w", encoding="utf-8") as outfile:
        json.dump(new_entry, outfile, ensure_ascii=False, indent=4)

    print(f"Generated question has been evaluated. Exported result to {file_path}")
