#!/usr/bin/env python3

from args import parse_arguments
from config import parse_config
from runner import run_tests
import sys


def main(args):
    tests = parse_config(args.config_file)
    run_tests(tests)


if __name__ == '__main__':
    args = parse_arguments()
    try:
        main(args)
    except KeyboardInterrupt:
        print("\nUserInterrupt", file=sys.stderr)
        sys.exit(1)
