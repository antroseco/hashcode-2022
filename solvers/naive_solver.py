import argparse
import random
import sys
sys.path.extend(['..', '.'])
from collections import *
from dataparser import parse
from util import get_in_file_content
from structs import Task, Person, Skill
from collections import defaultdict

def sort_tasks_by_start_date(tasks: list):
    return sorted(tasks, key = lambda task: task.latest_start_date)


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

    for required_skill in task.required_skills:
        required_skill_before_mentor = required_skill

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
                register_person_as_mentor(mentoring_skills, person.skills)
                task.assignees.append(person)
                person.assigned_tasks.append(task)
                remaining_people.pop(person_index)

                if required_skill_before_mentor.level >= person_skill.level:
                    person.skills[person_skill.name] = Skill(person_skill.name, person_skill.level)
            
                break
        else:
            # We failed to assign any people
            assert(False)
        


def solve_tasks(people, tasks):
    tasks = sort_tasks_by_start_date(tasks)
    for task in tasks:
        find_people_to_fill_single_task(people, task)




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

    solve_tasks(ns.people, ns.tasks)

    return '0'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    args = parser.parse_args()
    inp = get_in_file_content(args.in_file)
    out = solve(inp, {'seed': 0})
    print('\n'.join(['OUT:', '=========', out]))
