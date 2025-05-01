from sentence_transformers import SentenceTransformer, util

# Initialize the embedding model to compute vector similarity
# This model is a smaller version of the BERT model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_similarity(base_text: str, comparison_texts: list) -> list:
    """Computes cosine similarity between a base text and a list of texts."""
    base_embedding = embedding_model.encode(base_text, convert_to_tensor=True)
    comparison_embeddings = embedding_model.encode(
        comparison_texts, convert_to_tensor=True
    )
    similarities = util.cos_sim(base_embedding, comparison_embeddings)[0]

    return [round(sim.item(), 3) for sim in similarities]


def check_summaries_similarity(exercise_text: str, summaries: list) -> list:
    """Returns a list of similarity scores between the exercise and each summary."""
    return compute_similarity(exercise_text, summaries)


def check_assignments_similarity(exercise_text: str, assignments: list) -> list:
    """Returns a list of similarity scores between the exercise and each assignment."""
    return compute_similarity(exercise_text, assignments)
