from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from core.prompts import create_question_prompt, create_summary_prompt
import json

class LLMProcessor:
    """
    Handles interaction with the LLM model for generating programming-related questions and summarizing lecture slides.
    """

    def __init__(self, model_name="qwen2.5-coder:7b"):
        """
        Initializes the LLMProcessor with a default model.

        Args:
            model_name (str): Name of the LLM model to be used (default is "qwen2.5-coder:7b").
        """
        
        self.name = "llm_processor"
        self.model_name = model_name
        self.model = ChatOllama(model=model_name)
        self.parser = StrOutputParser()
        self.chain = self.model | self.parser

    def set_model(self, model_name):
        """
        Updates the LLM model.

        Args:
            model_name (str): Name of the new model to be used.
        """
        self.model_name = model_name
        self.model = ChatOllama(model=model_name)
        self.chain = self.model | self.parser

    def generate_question(self, topic, learning_objective, summaries, assignments, level):
        """
        Generates a programming-related question based on the given topic, learning objective, and related slide summaries.

        Args:
            topic (str): The topic of the question.
            learning_objective (str): The learning objective that the question should align with.
            summaries (list): A list of summarized lecture slides to provide context for the question.
            assignments (list): A list of corresponding assignments

        Returns:
            str: The generated question.
        """
        prompt = create_question_prompt(topic, learning_objective, summaries, assignments, level)  
        print(f"Question Generation prompt {prompt}")
        response = self.chain.invoke(prompt)  
        return response 

    def generate_summary(self, slide_text):
        """
        Generates a summary of a lecture slide, including extracting the page number.

        Args:
            slide_text (str): The full text of a single lecture slide.

        Returns:
            dict or None: A dictionary containing:
                - "page_number" (int): The extracted page number.
                - "summary" (str): The summarized content of the slide.
              Returns None if the response is not valid JSON.
        """
        summary_prompt = create_summary_prompt(slide_text) 
        response = self.chain.invoke(summary_prompt) 
        cleaned_response = response.strip().strip("```json").strip("```")

        try:
            summary_data = json.loads(cleaned_response) 
            return summary_data  
        except json.JSONDecodeError:
            print("⚠️ LLM Response was not valid JSON:", response)
            return None