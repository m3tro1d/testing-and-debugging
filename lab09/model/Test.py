class Test:
    def __init__(self, description, request_data, response_data, remember_vars):
        self._description = description
        self._request_data = request_data
        self._response_data = response_data
        self._remember_vars = remember_vars

    def get_description(self):
        return self._description

    def get_request_data(self):
        return self._request_data

    def get_response_data(self):
        return self._response_data

    def get_remember_vars(self):
        return self._remember_vars
