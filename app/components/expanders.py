import streamlit as st
from utils.formatters import format_assignments_as_list


def render_slide_content_expander(documents):
    """Displays the extracted content of lecture slides in an expandable section."""
    if not documents:
        return

    with st.expander("📂 View extracted contents of lecture slides", expanded=False):
        for idx, doc in enumerate(documents):
            st.text_area(
                f"📄 Document {doc.metadata.get('page_number', idx + 1)}:",
                doc.page_content,
                height=150,
            )


def render_assignment_expander(assignments):
    """Shows the assignment descriptions in an expandable section."""
    formatted_assignments = format_assignments_as_list(assignments)
    with st.expander(
        "📂 View assignment examples used for exercise generation", expanded=False
    ):
        st.write(formatted_assignments)

    return formatted_assignments


def render_summaries_expander(summaries):
    """Shows the summaries of relevant slides in an expandable section."""
    with st.expander("📂 View generated summaries of relevant slides", expanded=False):
        for summary in summaries:
            if summary and isinstance(summary, dict) and "summary" in summary:
                st.text_area(
                    f"📄 Summary of page {summary.get('page_number', '?')}:",
                    summary["summary"],
                    height=100,
                )
            else:
                st.warning("⚠️ One summary could not be displayed (invalid format).")
