class Test:
    def __init__(self, description, request_data, response_data):
        self._description = description
        self._request_data = request_data
        self._response_data = response_data

    def get_description(self):
        return self._description

    def get_request_data(self):
        return self._request_data

    def get_response_data(self):
        return self._response_data
