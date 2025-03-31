import streamlit as st
from core.llm_processor import LLMProcessor
from core.pdf_extractor import PDFExtractor
from core.vector_store import VectorStore
from core.bloom_classifier import BloomClassifier
from core.assignment_repository import AssignmentRepository
import tempfile

# Initialize Question Generator and PDF Extractor
llm_processor = LLMProcessor()
pdf_extractor = PDFExtractor()
vector_store = VectorStore()
bloom_classifier = BloomClassifier()
assignment_repository = AssignmentRepository()

st.html("""
    <style>
        .stMainBlockContainer {
            max-width:70rem;
        }
    </style>
    """
)
# Sidebar for Model Selection
st.sidebar.title("⚙️ Settings")
model_options = ["qwen2.5-coder:7b", "llama3.2:latest", "deepseek-r1:latest"]
selected_model = st.sidebar.selectbox("🧠 Open-Source Model:", model_options)
llm_processor.set_model(selected_model)

# **Sidebar: Question History**
if "question_history" not in st.session_state:
    st.session_state["question_history"] = []
if "current_question" not in st.session_state:
    st.session_state["current_question"] = None

st.sidebar.subheader("Questions")

if st.session_state["question_history"]:
    for idx, q in enumerate(st.session_state["question_history"][::-1]):
        with st.sidebar.expander(
            f"{q[11:100]}..."
        ):
            st.write(q)
else:
    st.sidebar.write("No questions generated yet.")


# Page Title
st.title("Generating Programming Exercises with Open-Source LLM's")

st.divider()


# Description
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


# Input fields
topic = st.text_input(
    "📌 Topic:", placeholder="E.g., Introduction to Haskell Programming"
)
learning_objective = st.text_area(
    "🎯 Learning Objective:",
    placeholder="E.g., Students should be able to explain quicksort and its time complexity.",
)

# File uploader for PDFs
uploaded_files = st.file_uploader(
    "📄 Upload Lecture PDFs (optional):", type=["pdf"], accept_multiple_files=True
)

# Process uploaded PDFs with loading spinner
extracted_documents = []
if uploaded_files:
    with st.spinner("📥 Storing PDFs in Database... Please wait."):
        for uploaded_file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(uploaded_file.read())

                # Extract documents
                documents = pdf_extractor.extract_text_pypdf(temp_pdf.name)
                extracted_documents.extend(documents)

        # Speichere alles im VectorStore
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

# Generate Question Button
if st.button("Generate Question"):
    st.divider()
    if not topic.strip() and not learning_objective.strip():
        st.warning("⚠ Please enter a topic and a learning objective.")
    elif not topic.strip():
        st.warning("⚠ Please enter a topic.")
    elif not learning_objective.strip():
        st.warning("⚠ Please enter a learning objective.")
    else:

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

        with st.spinner("Determining corresponding example assignments..."):
            assignments = [
                assignment
                for level in levels
                for assignment in assignment_repository.get_assignments(level)
            ]

        if assignments:
            st.success(f"✅ Corresponding Assignments Sheets found.")

            with st.expander("📂 View Assignment Sheets", expanded=False):
                for i, assignment in enumerate(assignments, 1):
                    st.text_area(
                        f"📄 Assignment {i}:",
                        assignment,
                        height=100,
                    )
        else:
            st.warning("⚠ No assignment sheets found.")

        with st.spinner("🔍 Finding relevant slides and generating summaries..."):
            related_docs = vector_store.find_related_documents(learning_objective, k=2)
            summaries = (
                [
                    llm_processor.generate_summary(doc.page_content)
                    for doc in related_docs
                ]
                if related_docs
                else []
            )

            if related_docs and summaries:
                st.success(
                    f"✅ Found {len(related_docs)} relevant slides. Corresponding summaries successfully generated."
                )
                with st.expander("📂 View Summaries of Related Slides", expanded=False):
                    for summary in summaries:
                        st.text_area(
                            f"📄 Summary of page {summary['page_number']}:",
                            summary["summary"],
                            height=100,
                        )
            elif related_docs:
                st.warning("⚠ Slides were found, but no summaries could be generated.")
            else:
                st.warning("⚠ No relevant slides found.")

        with st.spinner("🧠 Generating question..."):
            summary_contents = [summary["summary"] for summary in summaries]
            response = llm_processor.generate_question(
                topic, learning_objective, summary_contents, assignments, levels[0]
            )

            if response:
                st.success("✅ Question successfully generated.")

                st.session_state["question_history"].append(response)

                st.markdown("### 🧪 Generated Question")
                st.write(response)
    
            else:
                st.warning(
                    "⚠ No question could be generated. Please check your inputs."
                )
