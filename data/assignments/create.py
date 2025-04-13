create_assignments = [
    {
        "question_type": "Design Function Type Signatures",
        "question_text": "Based on given descriptions, propose reasonable type signatures (contracts) for isCapital, average, getMax, and det, using knowledge of type classes.",
        "subtasks": {
            "a": "isCapital: Determine whether the specified letter is a capital letter.",
            "b": "Return the mean value from a given list.",
            "c": "Return the greatest element of a given list.",
            "d": "Returns the determinant of a given square matrix.",
        },
    },
    {
        "question_type": "Design a data structure",
        "question_text": "Define a Haskell data type to represent arithmetic expressions involving addition and multiplication. Then, write a function that evaluates such expressions.",
        "subtasks": {},
    },
    {
        "question_type": "Construct contract, purpose, and example",
        "question_text": "Provide a contract (type signature), a purpose (short description), and one example for the following function:",
        "subtasks": {
            "a": "lwr a xs = foldr (\\x (lwrs, upprs) -> if (x < a) then (x:lwrs, upprs) else (lwrs, x:upprs)) ([],[]) xs"
        },
    },
]
