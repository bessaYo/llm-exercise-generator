import string


def format_summaries_as_prompt(summaries: list[str]) -> str:
    """Formats slide summaries into a clean, numbered format for LLM prompt."""
    if not summaries:
        return "No relevant slide summaries available."

    formatted = []
    for idx, summary in enumerate(summaries, start=1):
        formatted.append(f"Slide {idx}: {summary.strip()}")

    return "\n".join(formatted)


def format_assignments_as_prompt_text(example_assignments):
    """ "Formats example assignments into a Markdown-formatted string to be used in LLM prompts."""
    lines = []
    for i, ex in enumerate(example_assignments):
        main_type = ex.get("exercise_type", "Unknown")
        main_text = ex.get("exercise_text", "No text provided")

        lines.append(
            f"Example {i+1} - exercise type: {main_type}\nExercise: {main_text}"
        )

        subtasks = ex.get("subtasks", {})
        if isinstance(subtasks, dict):
            for key, value in subtasks.items():
                lines.append(f"    - ({key}) {value}")
    return "\n".join(lines)


def format_assignments_as_list(assignments):
    """Returns a Markdown-formatted list of example exercises including subtasks."""
    texts = []
    for exercise in assignments:
        base_text = exercise.get("exercise_text", "")
        subtasks = exercise.get("subtasks") or exercise.get("subttasks")

        subtask_lines = []
        if subtasks:
            sorted_keys = sorted(subtasks)
            for idx, key in enumerate(sorted_keys):
                value = subtasks[key]
                label = f"{string.ascii_lowercase[idx]})"
                subtask_lines.append(f"{label} {value}")

        subtasks_text = " ".join(subtask_lines)
        full_text = f"{base_text} {subtasks_text}".strip()
        texts.append(full_text)

    return texts
