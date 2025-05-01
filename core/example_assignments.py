exercise_types = {
    "remember": {
        "guidance": (
            "Remember-level exercises require students to recall specific facts, definitions, or syntax. "
            "Exercises should prompt precise retrieval of knowledge, such as exact syntax, keywords, or function names, without requiring deeper interpretation."
        ),
        "example_assignments": [
            {
                "exercise_type": "Recall function type signatures",
                "exercise_text": "What are the type signatures of the following standard functions?",
                "subttasks": {
                    "subtask_1": "length",
                    "subtask_2": "head",
                    "subtask_3": "tail",
                    "subtask_4": "map",
                },
            },
            {
                "exercise_type": "Identify keywords",
                "exercise_text": "Which of the following are reserved keywords?",
                "subttasks": {
                    "subtask_1": "if",
                    "subtask_2": "loop",
                    "subtask_3": "where",
                    "subtask_4": "define",
                },
            },
        ],
    },
    "understand": {
        "guidance": (
            "Understand-level exercises ask students to clearly explain concepts, interpret code behaviors, or describe functionalities using their own words. "
            "Exercises must prompt detailed explanations or illustrative examples, encouraging deep comprehension rather than simple recall."
        ),
        "example_assignments": [
            {
                "exercise_type": "Identify general types of expressions",
                "exercise_text": "What are the most general types of the following expressions? Answer using Haskell type notation.",
                "subtasks": {
                    "subtask_1": '"404"',
                    "subtask_2": '([404,4], ["HTTP", "Tires"])',
                    "subtask_3": '[[], ""]',
                    "subtask_4": "[filter not]",
                },
            },
            {
                "exercise_type": "Explain type errors",
                "exercise_text": "Explain why the expression (not 'a') results in a type error in Haskell. Provide an informal argument for how the error arises.",
                "subtasks": {},
            },
            {
                "exercise_type": "Explain well-typed expressions",
                "exercise_text": "Which of the following Haskell expressions are well typed?",
                "subttasks": {
                    "subtask_1": "['1', '2', '3']",
                    "subtask_2": "[1] ++ ['a']",
                    "subtask_3": '("1, 2",("3"))',
                    "subtask_4": "[tail, init, reverse]",
                },
            },
            {
                "exercise_type": "Explain result of functions",
                "exercise_text": "Explain the result of the following functions:",
                "subtasks": {
                    "subtask_1": "foo xs = map (+1) (map (+1) xs)",
                    "subtask_2": "bar xs = sum (map (\_ -> 1) (filter (> 7) (filter (< 13) xs)))",
                    "subtask_3": "baz xss = map (map (+1)) xss",
                },
            },
        ],
    },
    "apply": {
        "guidance": (
            "Apply-level exercises require students to demonstrate their ability to use known concepts or functions in new and practical contexts. "
            "Tasks should clearly specify novel scenarios or data, demanding active application of previously learned methods rather than direct repetition."
        ),
        "example_assignments": [
            {
                "exercise_type": "Filter divisible numbers",
                "exercise_text": "Provide a Haskell expression that returns a list of all integers between 1 and 99 that are divisible by 3.",
                "subtasks": {},
            },
            {
                "exercise_type": "Combine two lists in reverse order",
                "exercise_text": "Given two lists [4, 1] and [3, 2], provide a Haskell expression that returns the list [1, 2, 3, 4] using head, tail, !!, ++, take, drop, reverse, or init.",
                "subtasks": {},
            },
            {
                "exercise_type": "Use map and filter to express a list comprehension",
                "exercise_text": "Express [x * x | x <- [1..], even x] using map and filter.",
                "subtasks": {},
            },
            {
                "exercise_type": "Reimplement functions using pattern matching",
                "exercise_text": "Reimplement the following third function using pattern matching. You are not allowed to use the head or tail functions.",
                "subtasks": {"subtask_1": "third xs = head (tail (tail xs))"},
            },
            {
                "exercise_type": "Rewrite without list comprehension",
                "exercise_text": "Translate the following function to an equivalent one that does NOT use list comprehension:",
                "subtasks": {
                    "subtask_1": "charCount ch str = sum [1 | x <- str, x == ch]"
                },
            },
        ],
    },
    "analyze": {
        "guidance": (
            "Analyze-level exercises prompt students to critically examine code structures, behaviors, or logic. "
            "Tasks must involve detailed investigation or comparisons, clearly requiring identification of patterns, differences, or potential issues in code."
        ),
        "example_assignments": [
            {
                "exercise_type": "Analyze Behavior of Empty List Operations",
                "exercise_text": "Enter the following expressions in GHCi and observe the result: `reverse []`, `head []`, `sum []`. Why does GHCi return what it does in each case?",
                "subtasks": {},
            },
            {
                "exercise_type": "Compare comprehension-based functions",
                "exercise_text": "Are the definitions `repeatc` and `repeatn` legal? If so, are they equivalent?",
                "subtasks": {
                    "subtask_1": "repeatn: repeatn n xs = [x | x <- xs, i <- [1..n]]",
                    "subtask_2": "repeatc: repeatc n xs = [x | i <- [1..n], x <- xs]",
                },
            },
        ],
    },
    "evaluate": {
        "guidance": (
            "Evaluate-level exercises require students to judge the correctness, efficiency, readability, or quality of provided code. "
            "Exercises must clearly set criteria for evaluation, guiding students to substantiate their judgments with precise reasoning."
        ),
        "example_assignments": [
            {
                "exercise_type": "Evaluate type of function application",
                "exercise_text": "Given a function `foo` of type `Char -> String` and a value `bar` of type `Char`, determine the type of the expression `(foo bar)` and explain your reasoning.",
                "subtasks": {},
            },
            {
                "exercise_type": "Evaluate compilation of list comprehensions",
                "exercise_text": "Consider the following list comprehensions featuring both generators and guards. For each of them, decide whether they are compiling or not compiling, and if they compile, write down the resulting list.",
                "subtasks": {
                    "subtask_1": "[x `mod` 2 | x <- [0..3]]",
                    "subtask_2": '[(x,y) | x <- "aBc", isUpper x, y <- "eFgH", isLower y]',
                    "subtask_3": "[(x,y) | x <- [1..2], y <- ['a'..'b']]",
                },
            },
        ],
    },
    "create": {
        "guidance": (
            "Create-level exercises challenge students to design new solutions, data structures, or significant code reorganizations. "
            "Tasks must clearly prompt original and creative production, encouraging novel designs rather than modifications of provided examples."
        ),
        "example_assignments": [
            {
                "exercise_type": "Design Function Type Signatures",
                "exercise_text": "Based on given descriptions, propose reasonable type signatures (contracts) for isCapital, average, getMax, and det, using knowledge of type classes.",
                "subtasks": {
                    "subtask_1": "isCapital: Determine whether the specified letter is a capital letter.",
                    "subtask_2": "Return the mean value from a given list.",
                    "subtask_3": "Return the greatest element of a given list.",
                    "subtask_4": "Returns the determinant of a given square matrix.",
                },
            },
            {
                "exercise_type": "Design a data structure",
                "exercise_text": "Define a Haskell data type to represent arithmetic expressions involving addition and multiplication. Then, write a function that evaluates such expressions.",
                "subtasks": {},
            },
            {
                "exercise_type": "Construct contract, purpose, and example",
                "exercise_text": "Provide a contract (type signature), a purpose (short description), and one example for the following function:",
                "subtasks": {
                    "subtask_1": "lwr a xs = foldr (\\x (lwrs, upprs) -> if (x < a) then (x:lwrs, upprs) else (lwrs, x:upprs)) ([],[]) xs"
                },
            },
        ],
    },
}
