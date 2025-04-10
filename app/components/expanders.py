#!/usr/bin/env python
import streamlit as st
from utils.text_helpers import format_assignment_descriptions


def render_assignment_expander(assignments):
    """Shows the assignment descriptions in an expandable section."""
    formatted_assignments = format_assignment_descriptions(assignments)
    with st.expander("📂 View Assignment Sheets", expanded=False):
        st.write(formatted_assignments)

    return formatted_assignments


def render_summaries_expander(summaries):
    """Shows the summaries of relevant slides in an expandable section."""
    with st.expander("📂 View Summaries of Relevant Slides", expanded=False):
        for summary in summaries:
            if summary and isinstance(summary, dict) and "summary" in summary:
                st.text_area(
                    f"📄 Summary of page {summary.get('page_number', '?')}:",
                    summary["summary"],
                    height=100,
                )
            else:
                st.warning("⚠️ One summary could not be displayed (invalid format).")
