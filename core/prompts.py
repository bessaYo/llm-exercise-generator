def create_question_prompt(topic, learning_objective, summaries, example_assignments, bloom_level):
    bloom_level_descriptions = {
        "remember": (
            "Retrieving, recognizing, and recalling relevant knowledge from long-term memory.\n"
        ),
        "understand": (
            "Constructing meaning from oral, written, and graphic messages through interpreting, "
            "exemplifying, classifying, summarizing, inferring, comparing, and explaining.\n"
        ),
        "apply": (
            "Carrying out or using a procedure for executing or implementing.\n"
        ),
        "analyze": (
            "Breaking material into constituent parts and determining how the parts relate to one another "
            "and to an overall structure or purpose through differentiating, organizing, and attributing.\n"
        ),
        "evaluate": (
            "Making judgments based on criteria and standards through checking and critiquing.\n"
        ),
        "create": (
            "Putting elements together to form a coherent or functional whole; reorganizing elements into a new pattern "
            "or structure through generating, planning, or producing.\n"
        )
    }
    
    level_text = bloom_level_descriptions.get(bloom_level, "No matching Bloom level provided.")
    
    return f"""
    You are an university professor that creates clear, stand-alone programming exercise questions. Given the following inputs, generate exactly one self-contained question-answer pair.

    Inputs:
    - **Topic:** {topic}
    - **Learning Objective:** {learning_objective}
    - **Summaries (for your background only):** {summaries}
    - **Example Assignments (style reference):** {format_example_assignments(example_assignments)}
    - **Bloom's Level:** {bloom_level} {level_text}

    Requirements:
    1. The question and answer must be fully understandable without extra context.
    2. The question should be on univeristy difficulty level.
    2. They must directly align with the topic and learning objective.
    3. Use the example assignments as a style and difficulty guide.
    4. Incorporate a creative twist that prompts deeper thought. Students should not be able to just copy a solution.
    5. Do not reference the background info, Bloom's level, or example assignments in your final output.
    6. Output exactly one question-answer pair in the following Markdown format:

    **Question:** <Your question here>

    **Answer:**  
    <Your answer here> (code blocks should be formatted using triple backticks if applicable)
    """


def create_summary_prompt(slide_text):
    return f"""
    You are provided with the text of a **single lecture slide** that typically ends with a **page number**.

    ---
    **Slide Text:**
    {slide_text}
    
    **Your Task:**
    1. **Extract the Page Number:** Identify and extract the page number, which is usually located at the end of the slide text.
    2. **Summarize the Slide:** Write a summary in at least 3-4 sentences that captures all the key ideas and concepts from the slide.
       - If the slide includes **code snippets**, include them in the summary **verbatim** without any modifications.
    3. **Accuracy:** Ensure that your summary only reflects the information explicitly provided in the slide and does not add any new information.

    **Important Guidelines:**
    - Do **NOT** invent or add information; summarize **only** what is stated in the slide.
    - All key points must be included in the summary.
    - Retain and include all code snippets exactly as they appear.

    **Output Format (strictly follow this JSON structure):**
    ```
    {{
        "page_number": <Extracted Page Number>,
        "summary": "<Detailed summary of the slide, including all relevant code snippets>"
    }}
    ```
    ---
    """

def format_example_assignments(assignments: list[str]) -> str:
    return "\n".join([f"- {a}" for a in assignments])