from url_checker import UrlChecker
from args import parse_arguments
import sys


EXIT_FAILURE = 1
USAGE = 'python3 check_urls.py [root_url]'

VALID_URLS_FILENAME = 'valid_urls.txt'
INVALID_URLS_FILENAME = 'invalid_urls.txt'


def main(args):
    checker = UrlChecker()
    with (open(args.valid, 'w') as valid_output,
          open(args.invalid, 'w') as invalid_output):
        checker.check(args.url, valid_output, invalid_output)


if __name__ == '__main__':
    args = parse_arguments()
    try:
        main(args)
    except KeyboardInterrupt:
        print('Keyboard interrupt', file=sys.stderr)
        sys.exit(EXIT_FAILURE)
