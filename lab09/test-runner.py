#!/usr/bin/env python3

from Runner import Runner
from args import parse_arguments
from config import parse_config
import sys


def main(args):
    tests = parse_config(args.config_file)
    runner = Runner()
    runner.run(tests)


if __name__ == '__main__':
    args = parse_arguments()
    try:
        main(args)
    except KeyboardInterrupt:
        print("\nUserInterrupt", file=sys.stderr)
        sys.exit(1)
