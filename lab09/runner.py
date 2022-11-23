import sys
import requests
from model.ResponseData import ResponseData


def run_tests(tests):
    test_count = len(tests)
    passed_count = 0
    if test_count == 0:
        print('No tests found :(')

    for number, test in enumerate(tests, start=1):
        try:
            run_test(test)
            passed_count += 1
            print('[{}/{}] Test passed'.format(number, test_count))
        except Exception as e:
            print('[{}/{}] Test failed: {}'.format(number, test_count, str(e)))

    print('\nPassed {}/{} {:.2}%'.format(passed_count, test_count, passed_count / test_count * 100))


def run_test(test):
    actual_response = make_request(test.get_request_data())
    expected_response = test.get_response_data()

    if actual_response.get_status() != expected_response.get_status():
        raise RuntimeError('expected status: {}, actual: {}'.format(expected_response.get_status(), actual_response.get_status()))

    if not body_contains(expected_response.get_body(), actual_response.get_body()):
        raise RuntimeError('expected body:\n{}\nactual\n{}'.format(expected_response.get_body(), actual_response.get_body()))


def make_request(request_data):
    response = requests.post(request_data.get_url(), json=request_data.get_body())

    body = response.content
    try:
        body = response.json()
    except Exception:
        pass

    return ResponseData(response.status_code, body)


def body_contains(expected, actual):
    for key, value in expected.items():
        if actual[key] != value:
            return False

    return True
