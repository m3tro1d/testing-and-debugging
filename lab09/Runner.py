import sys
import requests
from model.ResponseData import ResponseData


class Runner:
    def __init__(self):
        self._remember_vars = dict()

    def run(self, tests):
        test_count = len(tests)
        passed_count = 0
        if test_count == 0:
            print('No tests found :(')

        for number, test in enumerate(tests, start=1):
            try:
                self.run_test(test)
                passed_count += 1
                print('[{}/{}] \'{}\' PASSED'.format(number,
                    test_count,
                    test.get_description()))
            except Exception as e:
                print('[{}/{}] \'{}\' FAILED\n{}'.format(number,
                    test_count,
                    test.get_description(),
                    str(e)))

        print('\nPassed {}/{} {:.2%}'.format(passed_count,
            test_count,
            passed_count / test_count))

    def run_test(self, test):
        actual_response = self.make_request(test.get_request_data())
        expected_response = test.get_response_data()

        if actual_response.get_status() != expected_response.get_status():
            raise RuntimeError('expected status: {}, actual: {}'.format(expected_response.get_status(), actual_response.get_status()))

        if not self.body_contains(expected_response.get_body(), actual_response.get_body()):
            raise RuntimeError('expected body:\n{}\nactual\n{}'.format(expected_response.get_body(), actual_response.get_body()))

        self.save_remember_vars(test.get_remember_vars(), actual_response.get_body())


    def make_request(self, request_data):
        if request_data.get_method() == 'GET':
            response = requests.get(request_data.get_url(self._remember_vars))
        else:
            response = requests.post(request_data.get_url(self._remember_vars), json=request_data.get_body())

        body = response.content
        try:
            body = response.json()
        except Exception:
            pass

        return ResponseData(response.status_code, body)


    def body_contains(self, expected, actual):
        for key, value in expected.items():
            if actual[key] != value:
                return False

        return True

    def save_remember_vars(self, remember_vars, body):
        for var_name, response_key in remember_vars.items():
            if response_key not in body:
                raise RuntimeError('remember variable {} not found in response'.format(var_name))

            self._remember_vars[var_name] = body[response_key]
