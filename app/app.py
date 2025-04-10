#!/usr/bin/env python
import streamlit as st
import tempfile
from core.llm_processor import LLMProcessor
from core.vector_store import VectorStore
from core.bloom_classifier import BloomClassifier
from core.assignment_repository import AssignmentRepository
from utils.text_helpers import (
    format_slide_summaries,
    extract_text_from_pdf,
)
from evaluation.evaluation_pipeline import evaluation_pipeline
from components.sidebar import render_sidebar
from components.instructions import render_instructions, render_input_fields
from components.expanders import render_assignment_expander, render_summaries_expander


# Initialize Classes
question_model = LLMProcessor(model_name="qwen2.5-coder:7b", num_ctx=8192)
answer_model = LLMProcessor(model_name="qwen2.5-coder:7b", num_ctx=8192)
summary_model = LLMProcessor(model_name="gemma3:4b", num_ctx=4096)
vector_store = VectorStore()
bloom_classifier = BloomClassifier()
assignment_repository = AssignmentRepository()


st.html(
    """
    <style>
        .stMainBlockContainer {
            max-width:70rem;
        }
    </style>
    """
)

# Sidebar for model selection
question_model, answer_model, summary_model = render_sidebar(
    question_model, answer_model, summary_model
)

# Render instructions
render_instructions()
topic, learning_objective, uploaded_files = render_input_fields()

# Process uploaded PDFs
extracted_documents = []
if uploaded_files:
    with st.spinner("📥 Storing PDFs in Database... Please wait."):
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(uploaded_file.read())

                # Extract documents
                documents = extract_text_from_pdf(temp_pdf.name)
                extracted_documents.extend(documents)

        # Save extracted documents to vector store
        vector_store.add_documents(extracted_documents)

        st.success(
            f"✅ Successfully stored {len(documents)} slide(s) from **{uploaded_file.name}**"
        )

    # Show extracted Documents
    with st.expander("📂 View Extracted Slide Content", expanded=False):
        for idx, doc in enumerate(extracted_documents):
            st.text_area(
                f"📄 Document {doc.metadata.get('page_number', idx + 1)}:",
                doc.page_content,
                height=150,
            )

# Generate question pipeline
if st.button("Generate Question"):
    st.divider()

    # Validate inputs
    if not topic.strip() and not learning_objective.strip():
        st.warning("⚠ Please enter a topic and a learning objective.")
    elif not topic.strip():
        st.warning("⚠ Please enter a topic.")
    elif not learning_objective.strip():
        st.warning("⚠ Please enter a learning objective.")
    else:
        # 1: Classify Bloom's Taxonomy level
        with st.spinner(
            "🔍 Determining the Bloom’s Taxonomy level for the learning objective..."
        ):
            levels = bloom_classifier.classify(learning_objective)

        if levels and levels != ["No match found"]:
            st.success(
                f"✅ Successfully identified Bloom's Taxonomy Level: **{', '.join(levels)}**"
            )
        else:
            st.warning(
                "⚠ No matching Bloom level found. Please refine the learning objective."
            )

        # 2: Determine corresponding assignment sheets
        with st.spinner("Determining corresponding example assignments..."):
            assignments = [
                assignment
                for level in levels
                for assignment in assignment_repository.get_assignments(level)
            ]

        # Show assignment descriptions in an expander
        if assignments:
            st.success("✅ Corresponding Assignment Sheets found.")
            formatted_assignments = render_assignment_expander(assignments)
        else:
            st.warning("⚠ No assignment sheets found.")

        # 3: Find relevant slides and generate summaries
        with st.spinner("🔍 Finding relevant slides and generating summaries..."):
            related_docs = vector_store.find_related_documents(learning_objective, k=2)
            summaries = []
            if related_docs:
                try:
                    summaries = [
                        summary_model.generate_summary(doc.page_content)
                        for doc in related_docs
                    ]
                except Exception as e:
                    st.error(
                        "Could not generate summaries. Make sure the model is available. Try running `ollama list` to check the model status."
                        f"Error: {e}"
                    )
            # Show summaries in an expander
            if related_docs and summaries:
                st.success(
                    f"✅ Found {len(related_docs)} relevant slides. Corresponding summaries successfully generated."
                )
                render_summaries_expander(summaries)
            elif related_docs:
                st.warning("⚠ Slides were found, but no summaries could be generated.")
            else:
                st.warning("⚠ No relevant slides found.")

        # 4: Generate question
        with st.spinner("🧠 Generating question..."):
            summary_contents = [s["summary"] for s in summaries if isinstance(s, dict)]
            formatted_summaries = format_slide_summaries(summary_contents)

            question = question_model.generate_question(
                topic,
                learning_objective,
                formatted_summaries,
                formatted_assignments,
                levels[0],
            )

            if not question:
                st.warning(
                    "⚠ No question could be generated. Please check your inputs."
                )
            else:
                st.success("✅ Question successfully generated.")
                st.write(question)

        if question:
            evaluation_pipeline(
                question,
                formatted_assignments,
                levels[0],
            )
