apply_assignments = [
    {
        "question_type": "Filter divisible numbers",
        "question_text": "Provide a Haskell expression that returns a list of all integers between 1 and 99 that are divisible by 3.",
        "subtasks": {},
    },
    {
        "question_type": "Combine two lists in reverse order",
        "question_text": "Given two lists [4, 1] and [3, 2], provide a Haskell expression that returns the list [1, 2, 3, 4] using head, tail, !!, ++, take, drop, reverse, or init.",
        "subtasks": {},
    },
    {
        "question_type": "Use map and filter to express a list comprehension",
        "question_text": "Express [x * x | x <- [1..], even x] using map and filter.",
        "subtasks": {},
    },
    {
        "question_type": "Reimplement functions using pattern matching",
        "question_text": "Reimplement the following third function using pattern matching. You are not allowed to use the head or tail functions.",
        "subtasks": {"a": "third xs = head (tail (tail xs))"},
    },
    {
        "question_type": "Rewrite without list comprehension",
        "question_text": "Translate the following function to an equivalent one that does NOT use list comprehension:",
        "subtasks": {"a": "charCount ch str = sum [1 | x <- str, x == ch]"},
    },
]
