import streamlit as st
import tempfile
import os
from core.llm_processor import LLMProcessor
from core.vector_store import VectorStore
from core.bloom_classifier import BloomClassifier
from utils.formatters import format_summaries_as_prompt
from utils.helper_functions import (
    extract_text_from_pdf,
    clean_markdown_json,
    get_available_models,
)
from evaluation.evaluation_pipeline import evaluation_pipeline
from components.sidebar import render_sidebar
from components.displays import (
    render_exercise,
    render_input_fields,
    render_instructions,
)
from components.expanders import (
    render_assignment_expander,
    render_summaries_expander,
    render_slide_content_expander,
)
from core.example_assignments import exercise_types

# Disable parallel tokenizers warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# --- Check for local models ---
available_models = get_available_models()
if not available_models:
    st.warning(
        "No models found in the local Ollama environment.\n\n"
        "Please install the required models by running the following commands in your terminal:\n\n"
        "`ollama pull qwen2.5-coder:7b`\n\n"
        "`ollama pull gemma3:4b`\n\n"
        "Restart the app after installation.\n\n"
    )
    st.stop()

# Fallback for default models
# These models should be available in the local Ollama environment
default_exercise_model = "qwen2.5-coder:7b"
default_summary_model = "gemma3:4b"

# If the default models are not available, select the first available model
if default_exercise_model not in available_models:
    default_exercise_model = available_models[0]
if default_summary_model not in available_models:
    default_summary_model = available_models[0]

# --- Session State Initialization ---
if "vector_store" not in st.session_state:
    st.session_state["vector_store"] = VectorStore()
if "extracted_documents" not in st.session_state:
    st.session_state["extracted_documents"] = []
if "uploaded_files_names" not in st.session_state:
    st.session_state["uploaded_files_names"] = []
if "topic" not in st.session_state:
    st.session_state["topic"] = ""
if "learning_objective" not in st.session_state:
    st.session_state["learning_objective"] = ""
if "summaries" not in st.session_state:
    st.session_state["summaries"] = []
if "summaries_topic" not in st.session_state:
    st.session_state["summaries_topic"] = ""
if "summaries_learning_objective" not in st.session_state:
    st.session_state["summaries_learning_objective"] = ""
if "summaries_uploaded_files" not in st.session_state:
    st.session_state["summaries_uploaded_files"] = []

vector_store = st.session_state["vector_store"]

# --- Initialize LLMs and Bloom Classifier ---
exercise_model = LLMProcessor(model_name=default_exercise_model)
summary_model = LLMProcessor(model_name=default_summary_model)
bloom_classifier = BloomClassifier()

# --- HTML Styling ---
st.html(
    """
    <style>
        .stMainBlockContainer {
            max-width:70rem;
        }
    </style>
    """
)

# --- Sidebar and Inputs ---
exercise_model, summary_model = render_sidebar(exercise_model, summary_model)

render_instructions()
topic_input, learning_objective_input, uploaded_files = render_input_fields()

# Update Session State for Topic and Learning Objective
if topic_input:
    st.session_state["topic"] = topic_input
if learning_objective_input:
    st.session_state["learning_objective"] = learning_objective_input

# --- Process Uploaded PDFs ---
if uploaded_files:
    new_documents = []
    new_upload_detected = False

    for uploaded_file in uploaded_files:
        if uploaded_file.name not in st.session_state["uploaded_files_names"]:
            new_upload_detected = True
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(uploaded_file.read())
                documents = extract_text_from_pdf(temp_pdf.name)
                new_documents.extend(documents)
                st.session_state["uploaded_files_names"].append(uploaded_file.name)

    if new_upload_detected:
        with st.spinner("Storing PDFs in Database... Please wait."):
            vector_store.add_documents(new_documents)
            st.session_state["extracted_documents"].extend(new_documents)
            st.success(
                f"Successfully stored {len(new_documents)} slide(s) from uploaded files."
            )

# --- Show Extracted Slides ---
render_slide_content_expander(st.session_state["extracted_documents"])

# --- Exercise Generation Pipeline ---
if st.button("Generate Exercise"):
    st.divider()

    # Validate inputs
    if (
        not st.session_state["topic"].strip()
        or not st.session_state["learning_objective"].strip()
        or not st.session_state["extracted_documents"]
    ):
        st.warning(
            "Missing input detected. Please make sure to provide a Topic, a Learning Objective, and at least one Lecture Slide."
        )
    else:

        # --- Step 1: Classify Bloom's Taxonomy Level ---
        with st.spinner(
            "🔍 Determining the Bloom’s Taxonomy level for the learning objective..."
        ):
            levels = bloom_classifier.classify(st.session_state["learning_objective"])

        if levels != None:
            st.success(
                f"Successfully identified Bloom's Taxonomy Level: **{', '.join(levels)}**"
            )
            # Show example assignments for the detected Bloom level
            assignments = exercise_types.get(levels[0], {}).get(
                "example_assignments", []
            )
            if assignments:
                render_assignment_expander(assignments)
        else:
            st.warning(
                "⚠ No matching Bloom level found. Please refine the learning objective."
            )

        # --- Step 2: Find Relevant Slides and Generate Summaries ---
        need_new_summaries = (
            st.session_state["summaries_topic"] != st.session_state["topic"]
            or st.session_state["summaries_learning_objective"]
            != st.session_state["learning_objective"]
            or st.session_state["summaries_uploaded_files"]
            != st.session_state["uploaded_files_names"]
        )

        if need_new_summaries or not st.session_state["summaries"]:

            related_docs = []

            if st.session_state["extracted_documents"]:
                with st.spinner(
                    "🔍 Finding relevant slides and generating summaries..."
                ):
                    related_docs = vector_store.find_related_documents(
                        st.session_state["learning_objective"], k=3
                    )
                    if related_docs is None:
                        st.warning(
                            "No related documents found for this learning objective."
                        )
                    else:
                        # Generate summaries for each related document
                        try:
                            summaries = [
                                summary_model.generate_summary(doc.page_content)
                                for doc in related_docs
                            ]
                            st.session_state["summaries"] = summaries
                            st.session_state["summaries_topic"] = st.session_state[
                                "topic"
                            ]
                            st.session_state["summaries_learning_objective"] = (
                                st.session_state["learning_objective"]
                            )
                            st.session_state["summaries_uploaded_files"] = list(
                                st.session_state["uploaded_files_names"]
                            )
                        except Exception as e:
                            st.error(
                                "Could not generate summaries. Make sure the model is available."
                                f"Error: {e}"
                            )

                if related_docs and st.session_state["summaries"]:
                    st.success(
                        f"Found {len(related_docs)} relevant slides. Summaries generated."
                    )
                    render_summaries_expander(st.session_state["summaries"])
                elif related_docs:
                    st.warning(
                        "Slides were found, but no summaries could be generated."
                    )
                else:
                    st.warning("No relevant slides found.")

            else:
                st.warning("No slides available to match against.")
        else:
            st.success("Using previously generated summaries.")
            render_summaries_expander(st.session_state["summaries"])

        # --- Step 3: Generate Exercise ---
        with st.spinner("🧠 Generating exercise..."):
            extracted_summary_texts = [
                s["summary"]
                for s in st.session_state["summaries"]
                if isinstance(s, dict)
            ]
            summaries_for_prompt = format_summaries_as_prompt(extracted_summary_texts)

            exercise_json = exercise_model.generate_exercise(
                st.session_state["topic"],
                st.session_state["learning_objective"],
                summaries_for_prompt,
                levels[0],
            )

        if not exercise_json:
            st.warning(
                "No exercise could be generated. Please check your inputs and try again."
            )
        else:
            rendered = render_exercise(exercise_json)
            if rendered is None:
                st.error("Failed to render the generated exercise. Please try again.")
            else:
                st.session_state["generated_exercise"] = exercise_json

                # --- Step 4: Evaluate ---
                with st.spinner("📊 Evaluating generated exercise..."):
                    evaluation_pipeline(
                        exercise_json,
                        levels[0],
                        extracted_summary_texts,
                        assignments,
                    )
