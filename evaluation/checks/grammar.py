import language_tool_python

# Initialize LanguageTool with english (US)
tool = language_tool_python.LanguageTool("en-US")

# List of rule IDs to ignore
IGNORE_RULE_IDS = {
    "MORFOLOGIK_RULE_EN_US",  # allows technical terms and code identifiers
    "EN_QUOTES",  # for quotation marks like “ and ”
    "ARROWS",  # for code arrows like -> and <-
    "EN_UNPAIRED_BRACKETS",  # allows subtask formats like "a.)"
    "COMMA_COMPOUND_SENTENCE_2",  # allows compound sentences without commas
    "DOUBLE_PUNCTUATION",  # to allow double punctuation like [1..10]
    "COMMA_PARENTHESIS_WHITESPACE" # allows for parentheses in code
}


def count_relevant_errors(matches):
    """
    Count the number of relevant grammar errors, ignoring predefined rule IDs.
    """
    return sum(1 for match in matches if match.ruleId not in IGNORE_RULE_IDS)


def check_grammar(text: str) -> int:
    """
    Check the grammar of the given text and return the number of relevant errors.
    """
    matches = tool.check(text)

    # Print relevant grammar errors
    for match in matches:
        if match.ruleId not in IGNORE_RULE_IDS:
            print("\n--- Grammar Error ---")
            print(f"Message       : {match.message}")
            print(
                f"Error Text    : '{text[match.offset:match.offset + match.errorLength]}'"
            )
            print(f"Suggestions   : {match.replacements}")
            print(f"Rule ID       : {match.ruleId}")

    # Return the count of relevant errors
    return count_relevant_errors(matches)
