import json
from model.ExpectedData import ExpectedData
from model.RequestData import RequestData
from model.Test import Test


def parse_config(path):
    data = json.loads(path.read())
    base_url = data['base_url']

    result = []
    for test_data in data['tests']:
        description = test_data['description']
        request_data = create_request_data(test_data, base_url)
        expected_data = create_expected_data(test_data['expected'])

        result.append(Test(description, request_data, expected_data))

    return result


def create_request_data(data, base_url):
    method = data['method']
    url = base_url + data['uri']
    body = json.dumps(data['request'])

    return RequestData(method, url, body)


def create_expected_data(data):
    status = data['status']
    response = json.dumps(data['response'])

    return ExpectedData(status, response)
