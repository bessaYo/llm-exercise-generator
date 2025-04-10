def create_evaluation_prompt(question):
    return f"""
You are an expert in computer science education. Your task is to analyze a programming-related question and assign it to the most appropriate level of Bloom’s Taxonomy.

Choose exactly **one** of the following Bloom levels, based on the cognitive process the question demands from the student.

Definitions for each level:

- **Remember**: Retrieving, recognizing, and recalling relevant knowledge from long-term memory.
- **Understand**: Constructing meaning from oral, written, and graphic messages through interpreting, exemplifying, classifying, summarizing, inferring, comparing, and explaining.
- **Apply**: Carrying out or using a procedure for executing or implementing.
- **Analyze**: Breaking material into constituent parts and determining how the parts relate to one another and to an overall structure or purpose through differentiating, organizing, and attributing.
- **Evaluate**: Making judgments based on criteria and standards through checking and critiquing.
- **Create**: Putting elements together to form a coherent or functional whole; reorganizing elements into a new pattern or structure through generating, planning, or producing.

---

### Instructions:
- Read the question carefully.
- Identify the **main mental operation** the student is expected to perform.
- Choose **only one** Bloom level from the list.
- Return **only the level name**, like: `Understand` (no explanation, no formatting, no punctuation).

---

### Question:
{question}

### Output:
Single Bloom level name (no explanation, no formatting, no punctuation).
"""
