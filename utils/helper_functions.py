from langchain_community.document_loaders import PyPDFLoader
import ollama
import re


def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file and returns a list of LangChain Documents (one per page)."""
    print("Starting PDF text extraction...")
    loader = PyPDFLoader(file_path)
    return loader.load()


def clean_markdown(text):
    """Removes common Markdown formatting from a text string."""
    text = re.sub(r"#+ ", "", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"^- ", "", text)
    return text.strip()


def clean_markdown_json(text):
    """Removes surrounding ```json ... ``` markers if present, otherwise returns the text unchanged."""
    text = text.strip()

    if text.startswith("```json") and text.endswith("```"):
        lines = text.splitlines()
        return "\n".join(lines[1:-1]).strip()
    else:
        return text


def get_available_models():
    """Returns a tuple of all model names currently available in the local Ollama environment."""
    models_info = ollama.list()
    available_models = tuple(model.model for model in models_info["models"])
    return available_models
