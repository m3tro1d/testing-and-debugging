import urllib


class RequestData:
    def __init__(self, method, url, params, body):
        self._method = method
        self._url = url
        self._params = params
        self._body = body

    def get_method(self):
        return self._method

    def get_url(self, param_vars):
        params = ''
        if len(self._params) != 0:
            params_list = self._expand_params(self._params, param_vars)
            params = '?' + urllib.parse.urlencode(params_list)

        return self._url + params

    def get_body(self):
        return self._body

    def _expand_params(self, params, param_vars):
        result = dict()

        for key, value in params.items():
            actual_value = value

            if value.startswith('$'):
                var_name = value[1:]
                if var_name not in param_vars:
                    raise RuntimeError("unknown variable: " + var_name)
                actual_value = param_vars[var_name]

            result[key] = actual_value

        return result
