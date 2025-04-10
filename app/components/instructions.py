import streamlit as st


def render_instructions():
    """Shows the instructions for the app."""
    st.title("Generating Programming Exercises with Open-Source LLM's")
    st.divider()
    st.write(
        """ 
        This tool leverages Open-Source LLMs to generate **programming-related questions** based on **lecture slides**, a **topic**, and a **learning objective**.
        
        The learning objective is classified according to a cognitive level of **Bloom’s Taxonomy** and forms the basis for the question generation. 
        
        1️⃣ **Define the topic** – Specifies the subject area of the generated question  
        2️⃣ **Set the learning objective** – Describes what students should learn or achieve through the question    
        3️⃣ **Upload lecture slides (PDF format only)** – Extraction of key concepts and programming examples    
        """
    )
    st.divider()


def render_input_fields():
    """Shows the input fields for the topic, learning objective, and file upload."""
    topic = st.text_input(
        "📌 Topic:",
        value="Introduction to Haskell Programming",
        placeholder="E.g., Introduction to Haskell Programming",
    )
    learning_objective = st.text_area(
        "🎯 Learning Objective:",
        value="Students should be able to explain quicksort",
        placeholder="E.g., Students should be able to explain quicksort and its time complexity.",
    )
    uploaded_files = st.file_uploader(
        "📄 Upload Lecture PDFs (optional):", type=["pdf"], accept_multiple_files=True
    )

    return topic, learning_objective, uploaded_files
