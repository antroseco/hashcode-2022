import argparse
import json
from collections import *
from pathlib import Path

import util
from structs import *


def ni(itr):
    return int(next(itr))


def nl(itr):
    # parses the next string of itr as a list of integers
    return [int(v) for v in next(itr).split()]


def nls(itr):
    # Parse the next string of itr as a string preceding a list of integers.
    string, ints = next(itr).split(maxsplit=1)
    return [string] + [int(v) for v in ints.split()]


def parse(inp):
    itr = (line for line in inp.split('\n'))
    ns = argparse.Namespace()

    # Contributors, Projects.
    ns.C, ns.P = nl(itr)
    assert 1 <= ns.C <= 10**5
    assert 1 <= ns.P <= 10**5

    ns.contributors = []
    # C sections describing individual contributors.
    for _ in range(ns.C):
        # Name, number of skills.
        name, N = nls(itr)
        assert 1 <= len(name) <= 20
        assert 1 <= N <= 100

        skills = []
        # The next N lines describe individual skills of the contributor.
        for _ in range(N):
            # Skill name, level.
            skill_name, L = nls(itr)
            assert 1 <= len(skill_name) <= 20
            assert 1 <= L <= 10

            skills.append(Skill(skill_name, L))

        ns.contributors.append(Person(name, skills))

    ns.projects = []
    # This is followed by P sections describing individual projects.
    for _ in range(ns.P):
        # Project name, Days needed, Score, Best before day, number of roles.
        name, Di, Si, Bi, Ri = nls(itr)
        assert 1 <= Di <= 10**5
        assert 1 <= Si <= 10**5
        assert 1 <= Bi <= 10**5
        assert 1 <= Ri <= 100

        skills = []
        # The next Ri lines describe the skills in the project.
        for _ in range(Ri):
            # Skill name, required skill level.
            Xk, Lk = nls(itr)
            assert 1 <= len(Xk) <= 20
            assert 1 <= Lk <= 100

            skills.append(Skill(Xk, Lk))

        ns.projects.append(Task(name, skills, Bi, Di, Si))

    return ns


def parse_cached(inp, tc, overwrite=False):
    return util.getCachedObj('inputNameSpace', tc, lambda: parse(inp), overwrite)


class FlexibleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, argparse.Namespace):
            return vars(obj)
        return json.JSONEncoder.default(self, obj)


def parse2json(inp):
    ns = parse(inp)
    return json.dumps(ns, cls=FlexibleEncoder)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('inp', nargs='?')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    if args.inp:
        file_list = [args.inp]
    else:
        file_list = Path('in').glob('*.in')

    for inp in file_list:
        data = parse2json(inp.read_text())
        with inp.with_suffix('.json').open('w') as f:
            f.write(data)
