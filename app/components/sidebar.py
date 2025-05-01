#!/usr/bin/env python
import streamlit as st
from utils.helper_functions import get_available_models


def render_sidebar(exiercise_model, answer_model, summary_model):
    """Shows the sidebar for model selection and settings."""
    available_models = get_available_models()

    st.sidebar.title("⚙️ Settings")

    # Select Exercise Model
    selected_exercise_model = st.sidebar.selectbox(
        "Exercise Generation Model:",
        available_models,
        index=available_models.index(exiercise_model.model_name),
    )
    exiercise_model.set_model(selected_exercise_model)

    # # Select Answer Model
    # selected_answer_model = st.sidebar.selectbox(
    #     "Answer Generation Model:",
    #     available_models,
    #     index=available_models.index(answer_model.model_name),
    # )
    # answer_model.set_model(selected_answer_model)

    # Select Summary Model
    selected_summary_model = st.sidebar.selectbox(
        "Summary Generation Model:",
        available_models,
        index=available_models.index(summary_model.model_name),
    )
    summary_model.set_model(selected_summary_model)

    return exiercise_model, answer_model, summary_model
