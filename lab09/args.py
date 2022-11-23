from textwrap import dedent
import argparse
import os

class CustomArgumentParser(argparse.ArgumentParser):
    def format_help(self):
        help_text = dedent(f"""\
        Shop test suite.

        Usage: {self.prog} [OPTIONS] CONFIG_FILE

        CONFIG_FILE:
          Thread's URL

        Options:
          -h,  --help     show help
        """)

        return help_text


def parse_arguments():
    parser = CustomArgumentParser(usage="%(prog)s [OPTIONS] CONFIG_FILE")

    parser.add_argument("config_file", type=argparse.FileType('r'))

    return parser.parse_args()
