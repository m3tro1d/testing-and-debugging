#!/usr/bin/env python3

from ProductsApi import ProductsApi
from os import path
import json
import jsonschema
import unittest


class TestProductsApi(unittest.TestCase):
    _CONFIG_DIR = path.join(path.dirname(path.realpath(__file__)), 'config')

    _PRODUCTS_FILE = 'products.json'
    _PRODUCTS_SCHEMA_FILE = 'products.schema.json'

    def setUp(self):
        self._api = ProductsApi()
        self._created_product_ids = []
        self._products = self._load_config_json(self._PRODUCTS_FILE)
        self._products_schema = self._load_config_json(self._PRODUCTS_SCHEMA_FILE)

    def tearDown(self):
        for product_id in self._created_product_ids:
            self._api.delete(product_id)

    def test_ListingProducts_ReturnsNonEmptyListWithValidStructure(self):
        products = self._api.list()

        self.assertGreater(len(products), 0, 'products list is not empty')
        self.assertTrue(
                self._json_matches_schema(products, self._products_schema))

    def test_DeletingExistingProduct_RemovesItFromTheList(self):
        product = self._create_product(self._products['valid'])
        response = self._api.delete(product['id'])

        products = self._api.list()
        product = self._find_product(products, product['id'])

        self.assertEqual(response['status'], 1, 'delete response status')
        self.assertIsNone(product, 'product is deleted')

    def test_DeletingNonExistingProduct_ReturnsError(self):
        response = self._api.delete(13371488)

        self.assertEqual(response['status'], 0, 'response status')

    def _load_config_json(self, file_path):
        with open(path.join(self._CONFIG_DIR, file_path)) as f:
            return json.loads(f.read())

    def _json_matches_schema(self, data, schema):
        try:
            jsonschema.validate(data, schema)
            return True
        except:
            return False


    def _create_product(self, body):
        response = self._api.add(body)
        self._created_product_ids.append(response['id'])

        return response

    def _find_product(self, products, id):
        for product in products:
            if product['id'] == id:
                return product

        return None


if __name__ == '__main__':
    unittest.main()
