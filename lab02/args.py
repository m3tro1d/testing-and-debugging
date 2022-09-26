from textwrap import dedent
import argparse
import os


class CustomArgumentParser(argparse.ArgumentParser):
    def format_help(self):
        help_text = dedent(f"""\
        A simple web crawler which checks links for availability and
        collects them in corresponding files.

        Usage: {self.prog} [options] url

        url:
          URL to process

        Options:
          -h,  --help                 show help
          -v,  --valid   [filename]   specify output file for valid URLs (def: {self.get_default('valid')})
          -i,  --invalid [filename]   specify output file for invalid URLs (def: {self.get_default('invalid')})
        """)
        return help_text


def parse_arguments():
    parser = CustomArgumentParser(usage="%(prog)s [options] url")
    parser.add_argument('-v', '--valid', default='valid_urls.txt')
    parser.add_argument('-i', '--invalid', default='invalid_urls.txt')
    parser.add_argument('url')

    return parser.parse_args()
