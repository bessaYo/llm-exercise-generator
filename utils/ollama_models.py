import ollama

def get_available_models():
    """Returns a tuple of all model names currently available in the local Ollama environment."""
    models_info = ollama.list()
    available_models = tuple(model.model for model in models_info["models"])
    return available_models