from util import get_in_file_content
from structs import Skill
from dump_solution import dump_to_str
from dataparser import parse
import argparse
import random
import sys
from collections import *

sys.path.extend(['..', '.'])


def sort_tasks_by_start_date(tasks: list):
    return sorted(tasks, key=lambda task: task.latest_start_date)


def register_person_as_mentor(mentoring_skills: dict, person_skills: dict):
    for skill_name in person_skills:
        skill = person_skills[skill_name]

        if skill_name not in mentoring_skills:
            mentoring_skills[skill_name] = Skill(skill.name, skill.level)
        else:
            # Check to see if our guy is the best mentor
            if skill.level > mentoring_skills[skill_name].level:
                mentoring_skills[skill_name] = Skill(skill.name, skill.level)

    # Lets pretend we're functional
    return mentoring_skills


def find_people_to_fill_single_task(people, task):
    remaining_people = [*people]
    mentoring_skills = {}
    assigned_people = []

    for required_skill in task.required_skills:
        if required_skill.name in mentoring_skills:
            mentor_skill = mentoring_skills[required_skill.name]
            if mentor_skill.level >= required_skill.level:
                required_skill = Skill(required_skill.name, required_skill.level - 1)

        for person_index, person in enumerate(remaining_people):
            # Budget default dict
            person_skill = Skill(required_skill.name, 0)
            if required_skill.name in person.skills:
                person_skill = person.skills[required_skill.name]

            # TODO: check for learnings here
            if person_skill.level >= required_skill.level:
                # Yay! We can use this person
                remaining_people.pop(person_index)
                assigned_people.append(person)
                register_person_as_mentor(mentoring_skills, person.skills)
                break
        else:
            # We failed to assign any people
            return False

    for skill, person in zip(task.required_skills, assigned_people):
        task.assignees.append(person.name)
        person.assigned_tasks.append(task)

        person_skill_level = 0
        if skill.name in person.skills:
            person_skill_level = person.skills[skill.name].level

        if skill.level >= person_skill_level:
            person.skills[skill.name] = Skill(skill.name, person_skill_level)

    return True


def solve_tasks(people: list, tasks: list):
    tasks: deque = deque(sort_tasks_by_start_date(tasks))
    finished_tasks = []

    for _ in range(100000):
        if not tasks:
            break

        task = tasks.popleft()

        if find_people_to_fill_single_task(people, task):
            finished_tasks.append(task)
        else:
            tasks.append(task)

    return dump_to_str(finished_tasks)


# inp is an input file as a single string
# return your output as a string
def solve(inp, args):
    # TODO: Solve the problem
    random.seed(args['seed'])
    # ns = parse_cached(inp, args['testcase'])
    ns = parse(inp)
    # ns.tasks = [
    #     Task('YACK', [Skill('c++', 10), Skill('python', 5)], 10, 5, 1),
    #     Task('YACK2', [Skill('c++', 10), Skill('python', 5)], 5, 5, 1),
    # ]
    # ns.people = [
    #     Person('tom', [Skill('c++', 10), Skill('python', 6)]),
    #     Person('wex', [Skill('python', 4)])
    # ]

    return solve_tasks(ns.contributors, ns.projects)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    args = parser.parse_args()
    inp = get_in_file_content(args.in_file)
    out = solve(inp, {'seed': 0})
    print('\n'.join(['OUT:', '=========', out]))
