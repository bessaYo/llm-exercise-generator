def create_evaluation_prompt(exercise):
    return f"""
You are an expert in computer science education. Your task is to analyze a programming-related exercise and assign it to the most appropriate level of Bloom’s Taxonomy.

Choose exactly one of the following Bloom levels, based on the cognitive process the exercise demands from the student.

Identify the main mental operation required from the student by using the following definitions per level:

- Remember: Remember-level exercises require students to recall specific facts, definitions, or syntax. Exercises should prompt precise retrieval of knowledge, such as exact syntax, keywords, or function names, without requiring deeper interpretation.

- Understand: Understand-level exercises ask students to clearly explain concepts, interpret code behaviors, or describe functionalities using their own words. Exercises must prompt detailed explanations or illustrative examples, encouraging deep comprehension rather than simple recall.

- Apply: Apply-level exercises require students to demonstrate their ability to use known concepts or functions in new and practical contexts. Tasks should clearly specify novel scenarios or data, demanding active application of previously learned methods rather than direct repetition.

- Analyze: Analyze-level exercises prompt students to critically examine code structures, behaviors, or logic. Tasks must involve detailed investigation or comparisons, clearly requiring identification of patterns, differences, or potential issues in code.

- Evaluate: Evaluate-level exercises require students to judge the correctness, efficiency, readability, or quality of provided code. Exercises must clearly set criteria for evaluation, guiding students to substantiate their judgments with precise reasoning.

- Create: Create-level exercises challenge students to design new solutions, data structures, or significant code reorganizations. Tasks must clearly prompt original and creative production, encouraging novel designs rather than modifications of provided examples.

---

### Instructions:
- Read the exercise carefully.
- Choose only one Bloom level from the list above.
- Return only the level name, like: `Understand` (no explanation, no formatting, no punctuation).

---

### Exercise:
{exercise}

### Output:
Single Bloom level name.
"""
