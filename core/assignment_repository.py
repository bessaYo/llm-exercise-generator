from data.assignments.remember import remember_assignments
from data.assignments.understand import understand_assignments
from data.assignments.apply import apply_assignments
from data.assignments.analyze import analyze_assignments
from data.assignments.evaluate import evaluate_assignments
from data.assignments.create import create_assignments

class AssignmentRepository:
    """
    Repository holding assignments examples for each Bloom's taxonomy level
    """

    def __init__(self):
        self.name = "assignment_repository"
        self.assignments = {
            "remember": remember_assignments,
            "understand": understand_assignments,
            "apply": apply_assignments,
            "analyze": analyze_assignments,
            "evaluate": evaluate_assignments,
            "create": create_assignments,
        }

    def get_assignments(self, level):
        """
        Returns example assignments for the given Bloom level.

        Args:
            level (str): Bloom's taxonomy level

        Returns:
            list[dict]: A list of assignment dicts
        """
        return self.assignments.get(level, [])