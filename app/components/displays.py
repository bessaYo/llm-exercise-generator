import streamlit as st
import json
import string


def render_instructions():
    """Shows the instructions for the app."""
    st.title("Generating Programming Exercises with LLM's")
    st.divider()
    st.write(
        """ 
        This tool leverages Open-Source LLMs to generate **programming-related exercises** based on a **topic**, a **learning objective**, and **lecture slides**.
        
        The learning objective is classified according to a cognitive level of **Bloom’s Taxonomy** and forms the basis for the exercise generation. 
        
        The following three inputs are required to generate a programming exercise:
        
        1️⃣ **Topic** – Specifies the subject area of the generated exercise.\n 
        2️⃣ **Learning Objective** – Describes what students should learn or achieve through the exercise.\n    
        3️⃣ **Lecture Slides** – Provide contextual input to ground the exercise.   
        """
    )
    st.divider()


def render_input_fields():
    """Shows the input fields for the topic, learning objective, and file upload."""

    topic = st.text_input(
        "📌 **Enter a topic:**",
        placeholder="E.g., Introduction to Haskell Programming",
    )
    learning_objective = st.text_area(
        "🎯 **Define the learning objective:**",
        placeholder="E.g., Students should be able to explain quicksort and its time complexity.",
    )
    uploaded_files = st.file_uploader(
        "📄 **Upload Lecture PDFs:**",
        type=["pdf"],
        accept_multiple_files=True,
    )

    return topic.strip(), learning_objective.strip(), uploaded_files


def render_exercise(exercise_input):
    """Displays exercise text and subtasks from a given JSON object or JSON string."""

    if isinstance(exercise_input, str):
        try:
            exercise_json = json.loads(exercise_input)
        except json.JSONDecodeError:
            return None
    else:
        exercise_json = exercise_input

    # Display main exercise text
    exercise_text = exercise_json.get("exercise_text", "No exercise found.")
    st.write("### Generated Exercise")
    st.markdown(exercise_text)

    subtasks = exercise_json.get("subtasks")
    if isinstance(subtasks, dict) and subtasks:
        sorted_keys = sorted(subtasks)
        for idx, key in enumerate(sorted_keys):
            value = subtasks[key]
            label = f"{string.ascii_lowercase[idx]}.)"
            st.markdown(f"{label} {value}")

    return exercise_json
