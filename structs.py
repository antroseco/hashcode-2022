from collections import namedtuple
Skill = namedtuple('Skill', ['name', 'level'])

class Person:
    def __init__(self, name, skills: list) -> None:
        self.assigned_task_names = []
        self.name = name
        self.skills = {}
        for skill in skills:
            self.skills[skill.name] = skill
        self.earliest_available = 0
        self.busy_till = 0

    def get_skill(self, skill_name)-> Skill:
        if skill_name in self.skills:
            return self.skills[skill_name]
        return Skill(skill_name, 0)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Person({self.name})"


class Task:
    def __init__(self, name: str, required_skills: list, due_date: int, duration: int, score: int) -> None:
        self.name = name
        self.required_skills = required_skills
        self.assignee_names = []
        self.reward = 0

        self.due_date = due_date
        self.duration = duration
        self.score = score
        self.latest_start_date = due_date - duration

    def __repr__(self) -> str:
        return f"Task({self.name}, due: {self.due_date})"
