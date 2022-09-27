from args import parse_arguments
from logger import Logger
from url_checker import LinkChecker
import sys


EXIT_FAILURE = 1


def main(args):
    logger = Logger(args.valid, args.invalid)
    checker = LinkChecker(logger)

    checker.check(args.url)


if __name__ == '__main__':
    args = parse_arguments()
    try:
        main(args)
    except KeyboardInterrupt:
        print('Keyboard interrupt')
