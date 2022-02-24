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
    
    def __repr__(self) -> str:
        return f"Person({self.name})"

class Task:
    def __init__(self, name: str, required_skills: list, due_date: int, duration: int) -> None:
        self.name = name
        self.required_skills = {}
        for skill in required_skills:
            self.required_skills[skill.name] = skill

        self.due_date = due_date
        self.duration = duration
        self.latest_start_date = due_date - duration

    def __repr__(self) -> str:
        return f"Task({self.name}, due: {self.due_date})"
