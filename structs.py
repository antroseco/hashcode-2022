class Skill:
    def __init__(self, name: str, level: int) -> None:
        self.name = name
        self.level = level

    def __repr__(self) -> str:
        return f"Skill({self.name}, {self.level})"


class Person:
    def __init__(self, name, skills: list) -> None:
        self.assigned_tasks = []
        self.name = name
        self.skills = {}
        for skill in skills:
            self.skills[skill.name] = skill

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Person({self.name})"


class Task:
    def __init__(self, name: str, required_skills: list, due_date: int, duration: int, score: int) -> None:
        self.name = name
        self.required_skills = required_skills
        self.assignees = []
        self.reward = 0

        self.due_date = due_date
        self.duration = duration
        self.score = score
        self.latest_start_date = due_date - duration

    def __repr__(self) -> str:
        return f"Task({self.name}, due: {self.due_date})"
