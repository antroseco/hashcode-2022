from util import get_in_file_content
from dataparser import parse
from collections import *
import argparse
import random
import sys
sys.path.extend(['..', '.'])


def solve(inp, args):
    # inp is an input file as a single string
    # return your output as a string
    random.seed(args['seed'])
    # ns = parse_cached(inp, args['testcase'])
    ns = parse(inp)

    return '0'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file')
    args = parser.parse_args()
    inp = get_in_file_content(args.in_file)
    out = solve(inp, {'seed': 0})
    print('\n'.join(['OUT:', '=========', out]))
