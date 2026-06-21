import re
import language_tool_python

# Initialize LanguageTool with english (US)
tool = language_tool_python.LanguageTool("en-US")


def strip_code(text: str) -> str:
    """
    Removes embedded code from an exercise so that grammar checking only runs
    on natural-language prose.

    Instead of disabling LanguageTool rules that misfire on code (which weakens
    the checker and leaves residual false positives), we remove the code itself:
      1. fenced Markdown code blocks (```...```),
      2. inline code spans (`...`),
      3. enumeration labels such as "a)" or "a.)" used for subtasks,
    and finally normalize whitespace around punctuation left behind by removal.
    """
    # 1) fenced code blocks are block-level -> drop them entirely
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    # 2) inline code spans are woven into sentences -> replace with a neutral
    #    placeholder noun so the surrounding grammar stays intact. Deleting them
    #    instead would leave artifacts such as ",," (from "`a`, `b`,") or "( )".
    text = re.sub(r"`[^`]*`", "code", text)
    # 3) subtask enumeration labels (a), b), a.) ...) at the start of a token
    text = re.sub(r"(?:(?<=\s)|^)[a-zA-Z]\.?\)\s*", "", text)
    # 4) collapse runs of adjacent placeholders (e.g. a list of code subtasks),
    #    done after label removal so "code a) code b) code" also collapses
    text = re.sub(r"\bcode(?:\s+code\b)+", "code", text)
    # 5) pull punctuation back to the preceding word and collapse whitespace
    text = re.sub(r"\s+([.,;:?!])", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    # 6) a placeholder that starts a sentence must be capitalized so it does not
    #    trip the "sentence should start with a capital" rule (a code artifact)
    text = re.sub(r"(^|[.?!]\s+)code\b", lambda m: m.group(1) + "Code", text)
    return text


# The only LanguageTool rule we disable. After stripping embedded code, all
# grammatical rules stay active; we only suppress the spell-checker, because the
# prose legitimately contains Haskell keywords and identifiers (e.g. "newtype",
# "Int", "sumEvenNumbers") that the model did not wrap in code formatting. These
# are domain vocabulary, not misspellings, and are not grammatical errors.
IGNORE_RULE_IDS = {"MORFOLOGIK_RULE_EN_US"}


def check_grammar(text: str) -> int:
    """
    Check the grammar of the prose in the given exercise and return the number
    of errors. Embedded code is stripped beforehand so that all grammatical
    LanguageTool rules can stay active without code-related false positives; only
    the spell-checking rule (IGNORE_RULE_IDS) is suppressed for domain vocabulary.
    """
    prose = strip_code(text)
    matches = [m for m in tool.check(prose) if m.rule_id not in IGNORE_RULE_IDS]

    # Print detected grammar errors for inspection
    for match in matches:
        print("\n--- Grammar Error ---")
        print(f"Message       : {match.message}")
        print(
            f"Error Text    : '{prose[match.offset:match.offset + match.error_length]}'"
        )
        print(f"Suggestions   : {match.replacements}")
        print(f"Rule ID       : {match.rule_id}")

    return len(matches)
