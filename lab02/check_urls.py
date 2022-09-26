# TODO: implement optional arguments with argparse

from url_checker import UrlChecker
import sys


EXIT_FAILURE = 1
USAGE = 'python3 check_urls.py [root_url]'

VALID_URLS_FILENAME = 'valid_urls.txt'
INVALID_URLS_FILENAME = 'invalid_urls.txt'


def check_urls(root_url):
    checker = UrlChecker(root_url)

    with open(VALID_URLS_FILENAME, 'w') as valid_output, open(INVALID_URLS_FILENAME, 'w') as invalid_output:
        checker.check(valid_output, invalid_output)


def main(args):
    if len(args) != 1:
        print(USAGE)
        sys.exit(EXIT_FAILURE);

    root_url = args[0]
    check_urls(root_url)


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Keyboard interrupt')
        sys.exit(EXIT_FAILURE)
