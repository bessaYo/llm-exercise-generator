def create_evaluation_prompt(exercise):
    return f"""
You are an expert in computer science education. Your task is to analyze a programming-related exercise and assign it to the most appropriate level of Bloom’s Taxonomy.

Choose exactly one of the following Bloom levels, based on the cognitive process the exercise demands from the student.

Focus especially on the main **mental operation** required, and look for **keywords** that signal typical tasks at each level. Below are concise definitions and key verbs per Bloom level:

- **Remember**: Recall facts, definitions, or syntax without deeper interpretation.  
  Typical verbs: *recall, name, list, identify, define, match*

- **Understand**: Explain concepts, code behavior, or interpret functionality in own words.  
  Typical verbs: *explain, describe, summarize, interpret, discuss*

- **Apply**: Use known techniques, functions, or concepts in a new situation or context.  
  Typical verbs: *apply, use, demonstrate, solve, illustrate*

- **Analyze**: Examine structure or behavior, compare implementations, identify problems.  
  Typical verbs: *analyze, differentiate, compare, contrast, categorize*

- **Evaluate**: Judge code quality, correctness, efficiency, or style based on criteria.  
  Typical verbs: *evaluate, justify, defend, argue, critique*

- **Create**: Design original code, structures, or solutions from scratch.  
  Typical verbs: *design, create, develop, formulate, invent*

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