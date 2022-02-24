from collections import OrderedDict

from dataparser import *
from collections import *
from structs import Person, Task


def parse_output(out: list):
    parsed = OrderedDict()
    n = int(out[0])

    for i in range(1, 2 * n, 2):
        parsed[out[i]] = out[i + 1].split()

    return parsed


# inp: the input file as a single string
# out: the answer file produced by your solver, as a single string
# return the score of the output as an integer
def score(inp, out):
    ns = parse(inp)
    out = parse_output(out.split('\n'))
    people = ns.contributors
    tasks = ns.projects

    person_table = {person.name: person for person in people}
    task_table = {task.name: task for task in tasks}
    for task, people in out.items():
        task: Task = task_table[task]
        task.start_date = 0
        people = [person_table[person] for person in people]

        for person in people:
            if not hasattr(person, "earliest_available"):
                person.earliest_available = 0

            task.start_date = max(task.start_date, person.earliest_available)

        task.end_date = task.start_date + task.duration  # this is one day after the last day people work on the task

        for person in people:
            person.earliest_available = task.end_date

        task.reward = max(task.score - max(task.end_date - task.due_date, 0), 0)

    return sum(task.reward for task in task_table.values())


if __name__ == "__main__":
    inp = "3 3\nAnna 1\nC++ 2\nBob 2\nHTML 5\nCSS 5\nMaria 1\nPython 3\nLogging 5 10 5 1\nC++ 3\nWebServer 7 10 7 2\nHTML 3\nC++ 2\nWebChat 10 20 20 2\nPython 3\nHTML 3"
    out = "3\nWebServer\nBob Anna\nLogging\nAnna\nWebChat\nMaria Bob"
    print(score(inp, out))
