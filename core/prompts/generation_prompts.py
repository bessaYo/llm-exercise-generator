def create_summary_prompt(slide_text):
    return f"""
You are an AI assistant summarizing a single lecture slide from a programming course.

---
**Slide Text:**
{slide_text}

**Your Task:**
1. Extract the page number (usually at the end of the slide).
2. Summarize the slide in 1–2 concise sentences.
- Focus on technical content and key concepts.
- Include all code snippets **verbatim** (unchanged).
- Do not add explanations or background knowledge.

**Output Format (strict JSON, very important!):**
```json
{{
"page_number": <Extracted Page Number>,
"summary": "<Concise, code-focused summary>"
}}
"""


def create_question_prompt(
    topic, learning_objective, summaries, example_assignments, bloom_level
):
    bloom_level_descriptions = {
        "remember": (
            "Retrieving, recognizing, and recalling relevant knowledge from long-term memory.\n"
        ),
        "understand": (
            "Constructing meaning from oral, written, and graphic messages through interpreting, "
            "exemplifying, classifying, summarizing, inferring, comparing, and explaining.\n"
        ),
        "apply": ("Carrying out or using a procedure for executing or implementing.\n"),
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
        ),
    }

    level_text = bloom_level_descriptions.get(
        bloom_level, "No matching Bloom level provided."
    )
    return f"""
### SYSTEM
You are a university instructor. Your task is to generate exactly **one** high-quality, self-contained programming exercise. Do **not** generate multiple questions.

---

**Topic:** {topic}  
**Learning Objective:** {learning_objective}  
**Bloom's Level:** {bloom_level} — {level_text}

**Context (internal use only – do NOT reference directly):**  
{summaries}

**Example Assignments (for inspiration):**  
{example_assignments}

---

### TASK INSTRUCTIONS

- The **primary goal** is designing a task explicitly tailored to help students **achieve the provided learning objective**.
- Strictly align the complexity, depth, and scope of the exercise with the given **Bloom level** (e.g., understanding, applying, evaluating, creating).
- Use the provided **example assignments** to guide:
    - Wording, style, and instructional tone
    - Complexity and depth of the task
    - Overall structure and format

- The internal context is exclusively for your inspiration. Do **not** directly reference any internal context in the question. The exercise must stand alone and be fully understandable without external context.

---

**IMPORTANT GUIDELINES:**  
- Do **not** include answers or explanations.
- Avoid concluding remarks such as “Good luck!”, “Have fun!”, or similar.
- Only output the programming question formatted **exactly** as follows (no additional headings, numbering, or markdown elements):

---

### OUTPUT FORMAT (strict Markdown only):
### Question:  
<Insert the programming question here>
"""


def create_answer_prompt(generated_question):
    return f"""
### SYSTEM
You are a programming assistant. Your task is to provide a correct and complete answer to the following programming question.

---
**Question:**  
{generated_question}

---
**Guidelines:**
- Be clear, concise, and technically correct.
- Prefer code where applicable.
- Focus only on what is needed to solve the question.

---
Only output in the following markdown format:**

### Answer:  
<Insert the correct answer here, including code if relevant>
"""
