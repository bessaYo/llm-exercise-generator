#!/usr/bin/env python
import json
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from core.prompts.evaluation_prompt import create_evaluation_prompt
from core.prompts.generation_prompts import (
    create_summary_prompt,
    create_answer_prompt,
    create_question_prompt,
)


class LLMProcessor:
    """Handles interaction with the LLM model for generating programming-related questions and summarizing lecture slides."""

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
        self.model = ChatOllama(model=model_name)
        self.chain = self.model | self.parser

    def generate_question(
        self, topic, learning_objective, summaries, assignments, level
    ):
        """Generates a programming-related question based on the given topic, learning objective, and related slide summaries."""

        prompt = create_question_prompt(
            topic, learning_objective, summaries, assignments, level
        )
        # response = self.chain.stream(prompt)
        response = self.chain.invoke(prompt)
        return response

    def generate_answer(self, generated_question):
        prompt = create_answer_prompt(generated_question)
        response = self.chain.stream(prompt)
        return response

    def generate_summary(self, slide_text):
        """Generates a summary of a lecture slide, including extracting the page number."""

        summary_prompt = create_summary_prompt(slide_text)
        response = self.chain.invoke(summary_prompt)
        cleaned_response = response.strip().strip("```json").strip("```")

        try:
            summary_data = json.loads(cleaned_response)
            return summary_data
        except json.JSONDecodeError:
            print("⚠️ LLM Response was not valid JSON:", response)
            return None

    def generate_bloom_level(self, question):
        """Generates a Bloom level of a given question"""
        evaluation_prompt = create_evaluation_prompt(question)
        response = self.chain.invoke(evaluation_prompt)
        return response
