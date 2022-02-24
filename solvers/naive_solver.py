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
    random.shuffle(tasks)
    return tasks
    return sorted(tasks, key=lambda task: task.score, reverse=True)
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


def get_viable_candidates_to_fill_role(remaining_people, required_skill, true_skill):
    candidates = []
    for person in remaining_people:
        person_skill = person.get_skill(required_skill.name)

        # TODO: check for learnings here
        if person_skill.level >= true_skill.level:
            candidates.append(person)

    return candidates


def sort_candidates(candidates, _1, _2):
    return sorted(candidates, key=lambda c: c.busy_till)


def find_people_to_fill_single_task(people, task):
    remaining_people = set(people)
    mentoring_skills = {}
    assigned_people = []

    earliest_start_time = 0
    for true_skill in task.required_skills:
        # Check if mentor exists
        skill_threshold_with_mentor = Skill(true_skill.name, true_skill.level)
        if true_skill.name in mentoring_skills:
            mentor_skill = mentoring_skills[true_skill.name]
            if mentor_skill.level >= true_skill.level:
                skill_threshold_with_mentor = Skill(true_skill.name, true_skill.level - 1)

        candidates = get_viable_candidates_to_fill_role(remaining_people, skill_threshold_with_mentor, true_skill)
        candidates = sort_candidates(candidates, skill_threshold_with_mentor, true_skill)

        if not candidates:
            return False

        best_candidate = candidates[0]
        earliest_start_time = max(earliest_start_time, best_candidate.busy_till)
        assigned_people.append(best_candidate)
        remaining_people.remove(best_candidate)
        register_person_as_mentor(mentoring_skills, best_candidate.skills)

    # Check that we don't loose points by attempting a task
    # TODO: assign start time to task so we can sort it later
    if earliest_start_time + task.duration > task.due_date + task.score:
        return False

    for skill, person in zip(task.required_skills, assigned_people):
        task.assignee_names.append(person.name)
        task.actual_start_time = earliest_start_time
        person.assigned_task_names.append(task.name)
        person.busy_till = earliest_start_time + task.duration

        person_skill_level = person.get_skill(skill.name).level
        if skill.level >= person_skill_level:
            person.skills[skill.name] = Skill(skill.name, person_skill_level + 1)

    return True


def solve_tasks(people: list, tasks: list):
    tasks: deque = deque(sort_tasks_by_start_date(tasks))
    finished_tasks = []

    for _ in range(5000):
        if not tasks:
            break

        task = tasks.popleft()

        if find_people_to_fill_single_task(people, task):
            finished_tasks.append(task)
        else:
            tasks.append(task)

    finished_tasks = sorted(finished_tasks, key = lambda task: task.actual_start_time)
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
