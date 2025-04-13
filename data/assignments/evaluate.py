evaluate_assignments = [
    {
        "question_type": "Evaluate type of function application",
        "question_text": "Given a function `foo` of type `Char -> String` and a value `bar` of type `Char`, determine the type of the expression `(foo bar)` and explain your reasoning.",
        "subtasks": {},
    },
    {
        "question_type": "Evaluate compilation of list comprehensions",
        "question_text": "Consider the following list comprehensions featuring both generators and guards. For each of them, decide whether they are compiling or not compiling, and if they compile, write down the resulting list.",
        "subtasks": {
            "a": "[x `mod` 2 | x <- [0..3]]",
            "b": '[(x,y) | x <- "aBc", isUpper x, y <- "eFgH", isLower y]',
            "c": "[(x,y) | x <- [1..2], y <- ['a'..'b']]",
        },
    },
]
