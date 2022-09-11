import sys
import subprocess


EXIT_FAILURE = 1
USAGE = 'usage: python triangle_test.py triangle.py test_cases.txt result.txt'

SUCCESS = 'success'
ERROR = 'error'


class TestCase:
    def __init__(self, args, expected_output):
        self._args = args
        self._expected_output = expected_output

    def get_args(self):
        return self._args

    def get_expected_output(self):
        return self._expected_output


def parse_test_file(filename):
    result = []

    with open(filename, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            elements = line.strip(' \n\r').split(' ')
            result.append(TestCase(elements[:3], elements[-1]))

    return result


def main(args):
    if len(args) != 3:
        print(USAGE)
        sys.exit(EXIT_FAILURE)

    script_name = args[0]
    test_file = args[1]
    result_file = args[2]

    with open(result_file, mode='w', encoding='utf-8') as f:
        test_cases = parse_test_file(test_file)
        for test_case in test_cases:
            result = subprocess.run(
                ['python', script_name, *test_case.get_args()],
                stdout=subprocess.PIPE
            )
            output = result.stdout.decode('1251').strip(' \n\r')

            if output == test_case.get_expected_output():
                print(SUCCESS, file=f)
            else:
                print(ERROR, file=f)


if __name__ == '__main__':
    main(sys.argv[1:])
