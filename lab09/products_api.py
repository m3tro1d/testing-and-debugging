import config.endpoints as ep
import requests


class ProductsApi:
    _METHOD_GET = 'GET'
    _METHOD_POST = 'POST'

    _ID_PARAM = 'id'

    def list(self):
        response = requests.request(
                self._METHOD_GET,
                ep.BASE_URL + ep.LIST_PRODUCTS_URI)

        return response.json()

    def add(self, product):
        response = requests.request(
                self._METHOD_POST,
                ep.BASE_URL + ep.ADD_PRODUCT_URI,
                json=product)

        try:
            return response.json()
        except:
            return { 'status': 0 }

    def edit(self, product):
        response = requests.request(
                self._METHOD_POST,
                ep.BASE_URL + ep.EDIT_PRODUCT_URI,
                json=product)

        try:
            return response.json()
        except:
            return { 'status': 0 }

    def delete(self, id):
        params = { self._ID_PARAM: id }

        response = requests.request(
                self._METHOD_GET,
                ep.BASE_URL + ep.DELETE_PRODUCT_URI,
                params=params)

        return response.json()
