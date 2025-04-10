#!/usr/bin/env python
import streamlit as st
from utils.ollama_models import get_available_models


def render_sidebar(question_model, answer_model, summary_model):
    """Shows the sidebar for model selection and settings."""
    available_models = get_available_models()

    st.sidebar.title("⚙️ Settings")

    # Select Question Model
    selected_question_model = st.sidebar.selectbox(
        "Question Model:",
        available_models,
        index=available_models.index(question_model.model_name),
    )
    question_model.set_model(selected_question_model)

    # Select Answer Model
    selected_answer_model = st.sidebar.selectbox(
        "Answer Model:",
        available_models,
        index=available_models.index(answer_model.model_name),
    )
    answer_model.set_model(selected_answer_model)

    # Select Summary Model
    selected_summary_model = st.sidebar.selectbox(
        "Summary Model:",
        available_models,
        index=available_models.index(summary_model.model_name),
    )
    summary_model.set_model(selected_summary_model)

    return question_model, answer_model, summary_model
