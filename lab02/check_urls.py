from args import parse_arguments
from logger import Logger
from url_checker import LinkChecker
import sys


EXIT_FAILURE = 1
USAGE = 'python3 check_urls.py [root_url]'

VALID_URLS_FILENAME = 'valid_urls.txt'
INVALID_URLS_FILENAME = 'invalid_urls.txt'


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
