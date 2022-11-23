class RequestData:
    def __init__(self, method, url, body):
        self._method = method
        self._url = url
        self._body = body

    def get_method(self):
        return self._method

    def get_url(self):
        return self._url

    def get_body(self):
        return self._body
