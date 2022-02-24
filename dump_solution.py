from typing import List

from simplejson import dump

from structs import Task

nl = "\n"


def dump_to_str(tasks: List[Task]):
    buffer = ""

    tasks = [task for task in tasks if task.assignee_names]

    # Number of tasks we are execting.
    E = len(tasks)
    buffer += str(E) + nl

    # Assume that these are sorted in chronological order.
    for task in tasks:
        buffer += task.name + nl
        buffer += " ".join(task.assignee_names) + nl

    return buffer


if __name__ == "__main__":
    tasks = [
        Task("WebServer", [], 0, 0, 0),
        Task("Logging", [], 0, 0, 0),
        Task("WebChat", [], 0, 0, 0),
    ]

    tasks[0].assignee_names = ["Bob", "Anna"]
    tasks[1].assignee_names = ["Anna"]
    tasks[2].assignee_names = ["Maria", "Bob"]

    print(dump_to_str(tasks), end="")
