from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from utils.helper_functions import parse_json_output
from core.prompts.evaluation_prompt import create_evaluation_prompt
from core.prompts.generation_prompts import (
    create_summary_prompt,
    create_exercise_prompt,
)


class LLMProcessor:
    """Class for interacting with local LLM models via Langchain and Ollama."""

    def __init__(self, model_name="qwen2.5-coder:7b", num_ctx=2048):
        """Initializes the LLMProcessor with a default model."""

        self.name = "llm_processor"
        self.model_name = model_name
        self.model = ChatOllama(model=model_name, num_ctx=num_ctx)
        self.parser = StrOutputParser()
        self.chain = self.model | self.parser

    def set_model(self, model_name):
        """Updates the LLM model."""

        self.model_name = model_name
        self.model = ChatOllama(model=model_name, num_ctx=2048)
        self.chain = self.model | self.parser

    def generate_exercise(self, topic, learning_objective, summaries, level):
        """Generates a programming-related exercise based on the given topic, learning objective, and related slide summaries."""
        exercise_prompt = create_exercise_prompt(
            topic, learning_objective, summaries, level
        )
        response = self.chain.invoke(exercise_prompt)
        return parse_json_output(response)

    def generate_summary(self, slide_text):
        summary_prompt = create_summary_prompt(slide_text)
        response = self.chain.invoke(summary_prompt)
        return parse_json_output(response)

    def generate_bloom_level(self, exercise):
        """Generates a Bloom level of a given exercise"""
        evaluation_prompt = create_evaluation_prompt(exercise)
        response = self.chain.invoke(evaluation_prompt)
        return response.strip()
