import sys
import subprocess


EXIT_FAILURE = 1
USAGE = 'usage: python triangle_test.py triangle.py test_cases.txt result.txt'
STRIP_CHARS = ' \n\r'
TEST_DELIMITER = ':'
COMMENT_INDICATOR = '#'

SUCCESS = 'success'
ERROR = 'error'


class TestCase:
    def __init__(self, args, expected_output):
        self._args = args.split(' ')
        self._expected_output = expected_output.strip(STRIP_CHARS)

    def get_args(self):
        return self._args

    def get_expected_output(self):
        return self._expected_output


def parse_test_file(filename):
    result = []

    with open(filename, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip(STRIP_CHARS)

            if len(line) == 0 or line.startswith(COMMENT_INDICATOR):
                continue

            args, output = line.split(TEST_DELIMITER)
            result.append(TestCase(args, output))

    return result


def get_output(args):
    result = subprocess.run(args, stdout=subprocess.PIPE)
    return result.stdout.decode('1251').strip(STRIP_CHARS)


def run_tests(test_cases, script_name, result_file):
    total_cases = len(test_cases)
    passed_cases = 0

    with open(result_file, mode='w', encoding='utf-8') as f:
        for test_case in test_cases:
            output = get_output(['python', script_name, *test_case.get_args()])

            if output == test_case.get_expected_output():
                print(SUCCESS, file=f)
                passed_cases += 1
            else:
                print(ERROR, file=f)

        result_str = '\npassed {}/{} - {:.2%}'.format(
                passed_cases,
                total_cases,
                passed_cases / total_cases)
        print(result_str, file=f)


def main(args):
    if len(args) != 3:
        print(USAGE)
        sys.exit(EXIT_FAILURE)

    script_name = args[0]
    test_file = args[1]
    result_file = args[2]

    test_cases = parse_test_file(test_file)
    run_tests(test_cases, script_name, result_file)


if __name__ == '__main__':
    main(sys.argv[1:])
