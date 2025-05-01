import textstat


def check_readability(exercise: str) -> int:
    """
    Check the readability of the given text using the Flesch-Kincaid Grade Level.
    """
    # Calculate the flesch-kincaid grade level
    score = textstat.flesch_reading_ease(exercise)

    return score
