import sys


def run_tests(tests):
    test_count = len(tests)
    if test_count == 0:
        print("No tests found :(")

    for number, test in enumerate(tests, start=1):
        try:
            run_test(test)
            print("[{}/{}] Test passed".format(number, test_count))
        except Exception as e:
            print("[{}/{}] Test failed: {}".format(number, test_count, str(e)))


def run_test(test):
    pass
