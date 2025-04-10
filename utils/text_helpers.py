#!/usr/bin/env python
from langchain_community.document_loaders import PyPDFLoader
import re

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file and returns a list of LangChain Documents (one per page)."""
    print("Starting PDF text extraction...")
    loader = PyPDFLoader(file_path)
    return loader.load()

def format_assignment_descriptions(assignments: list[dict]) -> str:
    """Formats assignment descriptions into numbered examples for LLM prompts."""
    if not assignments:
        return "No example assignments available."

    formatted = []
    for idx, assignment in enumerate(assignments, start=1):
        description = assignment.get("description", "").strip()
        if description:
            formatted.append(f"**Example {idx}:**\n{description}")

    return "\n\n".join(formatted)

def format_slide_summaries(summaries: list[str]) -> str:
    """Formats slide summaries into a clean, numbered format for LLM input."""
    if not summaries:
        return "No relevant slide summaries available."

    formatted = []
    for idx, summary in enumerate(summaries, start=1):
        formatted.append(f"Slide {idx}: {summary.strip()}")

    return "\n".join(formatted)

def clean_markdown(text):
    """Removes common Markdown formatting from a text string."""
    text = re.sub(r"#+ ", "", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text) 
    text = re.sub(r"`([^`]*)`", r"\1", text)  
    text = re.sub(r"^- ", "", text)  
    return text.strip()

def extract_code(markdown_text):
    """Extracts and concatenates all Haskell code blocks from a Markdown string."""
    code_blocks = re.findall(r"```haskell\n(.*?)```", markdown_text, re.DOTALL)
    return "\n\n".join([block.strip() for block in code_blocks]) if code_blocks else ""

def split_question(markdown_text):
    """Splits a Markdown question into full markdown, text parts, and Haskell code."""
    code = extract_code(markdown_text)
    text_without_code = re.sub(r"```haskell\n.*?```", "", markdown_text, flags=re.DOTALL)
    lines = [line.strip() for line in text_without_code.split("\n") if line.strip()]
    text_parts = [clean_markdown(line) for line in lines if not line.startswith("###")]

    return {
        "full_markdown": markdown_text.strip(),
        "text_parts": text_parts,
        "code": code
    }