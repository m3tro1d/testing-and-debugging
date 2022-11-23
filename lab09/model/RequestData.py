class RequestData:
    def __init__(self, method, url, body):
        self._method = method
        self._url = url
        self._body = body

    def get_method():
        return self._method

    def get_url():
        return self._url

    def get_body():
        return self._body
