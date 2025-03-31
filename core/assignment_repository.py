class AssignmentRepository:
    """
    Repository holding assignments examples for each Bloom's taxonomy level
    """

    def __init__(self):
        self.name ="assignment_repository"
        self.assignments = {
            "remember": [
                """List five common data types in Python. For each data type:
                - Provide a clear definition.
                - Include a code example demonstrating the data type.
                - Briefly explain typical use cases.""",
                """Define what a function is in programming. In your answer:
                - Explain the syntax for defining a function in Python (including parameters and return value).
                - Describe the main components of a function.
                - Provide a concrete example where using a function is appropriate.""",
            ],
            "understand": [
                "Explain the difference between a list and a tuple in Python, and give an example where each is appropriate.",
                "Describe how a conditional (if-else) statement works in a programming language of your choice.",
            ],
            "apply": [
                "Write a Python function that takes a list of integers and returns a new list containing only the even numbers. Explain your implementation.",
                "Implement a simple sorting algorithm (e.g., bubble sort) in Python and test it with an example list.",
            ],
            "analyze": [
                "Compare two Python functions that perform similar tasks by analyzing their time complexity. Discuss which function is more efficient and why.",
                "Examine a provided code snippet and identify potential inefficiencies. Explain your reasoning and suggest improvements.",
            ],
            "evaluate": [
                "Review two different implementations of quicksort in Python. Evaluate their performance in terms of time and space complexity, and justify which one would be more suitable for large datasets.",
                "Critically assess the advantages and drawbacks of using recursion versus iteration in Python for processing large data sets. Support your evaluation with examples.",
            ],
            "create": [
                "Design and implement your own variation of the quicksort algorithm in Python that includes logging for each recursive call. Explain how your approach enhances the standard implementation.",
                "Develop a Python program that integrates sorting functionality with user input validation. Detail your design decisions and explain how your program handles invalid inputs gracefully.",
            ],
        }

    def get_assignments(self, level):
        """
        Returns example assignments for the given Bloom level

        Args:
            level (str): Bloom's taxonomy level

        Returns:
            list: A list of assignment strings
        """

        return self.assignments.get(level)
