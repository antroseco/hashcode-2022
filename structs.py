class Skill:
    def __init__(self, name: str, level: int) -> None:
        self.name = name
        self.level = level
    
    def __repr__(self) -> str:
        return f"Skill({self.name}, {self.level})"

class Person:
    def __init__(self, name, skills: list) -> None:
        self.name = name
        self.skills = {}
        for skill in skills:
            self.skills[skill.name] = skill

class Task:
    def __init__(self, required_skills, due_date, duration) -> None:
        self.skills = {}
        for skill in required_skills:
            self.required_skills[skill.name] = skill

        self.due_date = due_date
        self.duration = duration
        self.latest_start_date = due_date - duration