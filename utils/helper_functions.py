from langchain_community.document_loaders import PyPDFLoader
import json
import ollama
import re


def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file and returns a list of LangChain Documents (one per page)."""
    loader = PyPDFLoader(file_path)
    return loader.load()


def clean_markdown(text):
    """Removes common Markdown formatting from a text string."""
    text = re.sub(r"#+ ", "", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"^- ", "", text)
    return text.strip()

def clean_markdown_json(text: str) -> str:
    """Extracts JSON from LLM output, removing Markdown formatting like ```json ... ``` or any other noise."""
    text = text.strip()
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    return ""


def parse_json_output(llm_output: str) -> dict | None:
    """Cleans and parses LLM output into a JSON object. Returns None if parsing fails."""
    cleaned = clean_markdown_json(llm_output)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        print("Could not parse LLM output as JSON:")
        print(llm_output)
        return None

def get_available_models():
    """Returns a tuple of all model names currently available in the local Ollama environment."""
    models_info = ollama.list()
    models = models_info.get("models", [])
    
    return tuple(model["model"] for model in models)
