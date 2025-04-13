understand_assignments = [
    {
        "question_type": "Identify general types of expressions",
        "question_text": "What are the most general types of the following expressions? Answer using Haskell type notation.",
        "subtasks": {
            "i": '"404"',
            "ii": '([404,4], ["HTTP", "Tires"])',
            "iii": '[[], ""]',
            "iv": "[filter not]",
        },
    },
    {
        "question_type": "Explain type errors",
        "question_text": "Explain why the expression (not 'a') results in a type error in Haskell. Provide an informal argument for how the error arises.",
        "subtasks": {},
    },
    {
        "question_type": "Explain well-typed expressions",
        "question_text": "Which of the following Haskell expressions are well typed?",
        "subttasks": {
            "a": "['1', '2', '3']",
            "b": "[1] ++ ['a']",
            "c": '("1, 2",("3"))',
            "d": "[tail, init, reverse]",
        },
    },
    {
        "question_type": "Explain result of functions",
        "question_text": "Explain the result of the following functions:",
        "subtasks": {
            "a": "foo xs = map (+1) (map (+1) xs)",
            "b": "bar xs = sum (map (\_ -> 1) (filter (> 7) (filter (< 13) xs)))",
            "c": "baz xss = map (map (+1)) xss",
        },
    },
]
