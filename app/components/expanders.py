import streamlit as st
from utils.formatters import format_assignments_as_list


def render_slide_content_expander(documents):
    """Displays the extracted content of lecture slides in an expandable section."""
    if not documents:
        st.info("No Lecture Slides Found.")
        return

    with st.expander("📂 View Extracted Contents of Lecture Slides", expanded=False):
        for idx, doc in enumerate(documents):
            page_number = getattr(doc, "metadata", {}).get("page_number", idx + 1)
            content = getattr(doc, "page_content", "[No content available]")
            st.text_area(f"📄 Document {page_number}:", content, height=150)


def render_assignment_expander(assignments):
    """Shows the assignment descriptions in an expandable section."""
    if not assignments:
        st.info("No Assignment Examples Available.")
        return

    formatted_assignments = format_assignments_as_list(assignments)
    with st.expander(
        "📂 View Assignment Examples Used for Exercise Generation", expanded=False
    ):
        st.write(formatted_assignments)

    return formatted_assignments


def render_summaries_expander(summaries):
    """Shows the summaries of relevant slides in an expandable section."""
    if not summaries:
        st.info("No Slide Summaries Available.")
        return

    with st.expander("📂 View Generated Summaries of Relevant Slides", expanded=False):
        for idx, summary in enumerate(summaries):
            if isinstance(summary, dict) and summary.get("summary"):
                page_number = summary.get("page_number", idx + 1)
                text = summary.get("summary", "[No summary available]")
                st.text_area(f"📄 Summary of page {page_number}:", text, height=100)
            else:
                st.warning(
                    f"⚠️ Summary {idx + 1} could not be displayed (invalid format)."
                )
