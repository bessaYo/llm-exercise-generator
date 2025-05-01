from core.example_assignments import exercise_types
from utils.formatters import format_assignments_as_prompt_text


def create_summary_prompt(slide_text):
    return f"""
You are an AI assistant summarizing content extracted from a single lecture slide of a programming course.

---

### Input Description:
The input text is the complete textual content extracted from one single slide using the PyPDF library. It typically includes the slide's main text, headings, bullet points, code snippets, and a page number (usually at the end).

---

### Slide Text:
{slide_text}

---

### Task:
Create a concise, strictly code-focused summary of the entire slide content.

Your summary will serve as a foundation for generating programming exercises later. Thus, it must strictly contain:

- Relevant technical definitions and concepts related directly to code.
- All code snippets copied verbatim (exactly as they appear).

### OUTPUT GUIDELINES

- Extract and provide the page number from the slide (typically found at the end).
- Summarize the slide content in concise sentences:
   - Include all original code snippets exactly as given.
   - Strictly focus on programming-related content, concepts, or definitions.
   - If the slide lacks any relevant technical concepts or code snippets, the summary should be an empty string ("").
- The output must strictly be a valid JSON object matching the structure defined below.

---

### OUTPUT FORMAT:

{{
  "page_number": "<Extracted page number>",
  "summary": "<Concise, code-focused summary or empty string if no relevant content>"
}}
"""


def create_answer_prompt(generated_exercise):
    return f"""
### SYSTEM
You are a programming assistant. Your task is to provide a correct and complete answer to the following programming exercise.

---
**Exercise:**
{generated_exercise}

---
**Guidelines:**
- Be clear, concise, and technically correct.
- Prefer code where applicable.
- Focus only on what is needed to solve the exercise.

---
Only output in the following markdown format:**

### Answer:
<Insert the correct answer here, including code if relevant>
"""


def create_exercise_prompt(topic, learning_objective, summaries, bloom_level):
    bloom_level = bloom_level.lower()
    guidance = exercise_types[bloom_level]["guidance"]
    example_assignments = exercise_types[bloom_level]["example_assignments"]
    examples = format_assignments_as_prompt_text(example_assignments)

    return f"""You are a learning engineer support bot tasked with creating high-quality, self-contained programming exercises.

---

The programming exercise must be well aligned with the learning objective it is intended to assess.
This means it must target the correct cognitive complexity as defined by Bloom’s Taxonomy.
Below are the six levels of Bloom’s Taxonomy, each corresponding to a specific type of thinking skill:

- Remember: Recall facts, syntax, or basic concepts.
- Understand: Explain ideas, interpret code, or summarize behavior.
- Apply: Implement knowledge in new contexts or complete given code tasks.
- Analyze: Decompose code structures or critically compare different implementations.
- Evaluate: Judge code quality, correctness, or efficiency based on defined criteria.
- Create: Design and produce original code or creatively reorganize existing solutions.

---

### CONTEXTUAL INPUT

- The topic of the exercise should lie within the field of: {topic}  
- The exercise must be aligned with the following learning objective: {learning_objective}

Learnning objectives are specific statements that describe what students should be able to do after completing the exercise.

Use the following summaries of lecture slides as internal context to generate the exercise. They are taken from real course materials and provide relevant terminology, code snippets, and examples that can be used in the exercise.
Do not reference lecture slides in you generated exercise. Students have no access to the slides when solving the exercise. Only use the content of the summaries if it is relevant to the exercise.

Lecture Slide Summaries:
{summaries}

---

### EXERCISE SPECIFICATIONS

- The target Bloom Level is: {bloom_level}  
{guidance}

Use the example assignments below to guide the structure, complexity, and tone of the generated exercise.  

Example Exercises:
{examples}

---
### OUTPUT GUIDELINES

- Follow the structure and tone of the example assignments provided above.
- The output must strictly be a valid JSON object matching the structure defined below.
- Use Markdown formatting for all code elements (e.g., function names, expressions, type annotations). Enclose all such elements in backticks (`` ` ``).
- If the task consists of multiple parts, include a `"subtasks"` field with subtasks labeled as `"subtask_1"`, `"subtask_2"`, etc.
- If the task only contains a single step, omit the `"subtasks"` field and include the full instruction in `"exercise_text"`.
- Do not include any explanations, meta-comments, formatting instructions, or additional text outside the JSON object.

---

### OUTPUT FORMAT

{{
  "exercise_type": "<Short name describing the task type, e.g. 'Explain function behavior'>",
  "exercise_text": "<Introductory instruction describing the main task. Follow the style of the examples. Use Markdown formatting for all code elements.>",
  "subtasks": {{
    "subtask_1": "<First expression or question. Use backticks for any Haskell code or notation.>",
    "subtask_2": "<Second expression or question.>"
  }}
}}
"""
