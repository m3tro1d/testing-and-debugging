import json
from model.ResponseData import ResponseData
from model.RequestData import RequestData
from model.Test import Test


def parse_config(path):
    data = json.loads(path.read())
    base_url = data['base_url']

    result = []
    for test_data in data['tests']:
        description = test_data['description']
        request_data = create_request_data(test_data, base_url)
        response_data = create_response_data(test_data['expected'])
        
        remember_vars = None
        if 'remember' in test_data:
            remember_vars = test_data['remember']

        result.append(Test(description, request_data, response_data, remember_vars))

    return result


def create_request_data(data, base_url):
    method = data['method']
    url = base_url + data['uri']
    body = data['request']

    return RequestData(method, url, body)


def create_response_data(data):
    status = data['status']
    response = data['response']

    return ResponseData(status, response)
