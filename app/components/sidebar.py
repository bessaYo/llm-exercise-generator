import streamlit as st
from utils.helper_functions import get_available_models


def render_sidebar(exercise_model, summary_model):
    """Shows the sidebar for model selection"""
    available_models = get_available_models()

    st.sidebar.title("⚙️ Settings")

    # Select Exercise Model
    selected_exercise_model = st.sidebar.selectbox(
        "Exercise Generation Model:",
        available_models,
        index=available_models.index(exercise_model.model_name),
    )
    exercise_model.set_model(selected_exercise_model)

    # Select Summary Model
    selected_summary_model = st.sidebar.selectbox(
        "Summary Generation Model:",
        available_models,
        index=available_models.index(summary_model.model_name),
    )
    summary_model.set_model(selected_summary_model)

    return exercise_model, summary_model
