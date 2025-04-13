analyze_assignments = [
    {
        "question_type": "Analyze Behavior of Empty List Operations",
        "question_text": "Enter the following expressions in GHCi and observe the result: `reverse []`, `head []`, `sum []`. Why does GHCi return what it does in each case?",
        "subtasks": {},
    },
    {
        "question_type": "Compare comprehension-based functions",
        "question_text": "Are the definitions `repeatc` and `repeatn` legal? If so, are they equivalent?",
        "subtasks": {
            "repeatn": "repeatn n xs = [x | x <- xs, i <- [1..n]]",
            "repeatc": "repeatc n xs = [x | i <- [1..n], x <- xs]",
        },
    },
]
