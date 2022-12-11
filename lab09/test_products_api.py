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
        self._products_schema = self._load_config_json(
                self._PRODUCTS_SCHEMA_FILE)

    def tearDown(self):
        for product_id in self._created_product_ids:
            self._api.delete(product_id)

    def test_ListingProducts_ReturnsNonEmptyListWithValidStructure(self):
        products = self._api.list()

        self.assertGreater(len(products), 0, 'products list is not empty')
        self.assertTrue(
                self._json_matches_schema(products, self._products_schema))

    def test_CreatingValidProduct_AddsItToTheList(self):
        response = self._create_product(self._products['valid'])

        products = self._api.list()
        list_product = self._find_product(products, response['id'])

        self.assertTrue(
                self._products['valid'].items() <= list_product.items(),
                'product in list')
        self.assertEqual(list_product['alias'], 'creeping-death', 'alias')
        self.assertEqual(list_product['img'], 'no_image.jpg', 'img')
        self.assertEqual(list_product['cat'], 'Men', 'cat')

    def test_CreatingWithTheSameAlias_AddsPostfix(self):
        response1 = self._create_product(self._products['valid_for_alias'])
        response2 = self._create_product(self._products['valid_for_alias'])

        products = self._api.list()
        list_product1 = self._find_product(products, response1['id'])
        list_product2 = self._find_product(products, response2['id'])

        self.assertEqual(
                list_product1['alias'],
                self._products['valid_for_alias']['alias'],
                'first alias')
        self.assertEqual(
                list_product2['alias'],
                self._products['valid_for_alias']['alias'] + '-0',
                'second alias')

    def test_CreatingWithEmptyProduct_ReturnsError(self):
        response = self._create_product(self._products['empty'])

        self.assertEqual(response['status'], 0, 'response status')

    def test_CreatingWithNullProduct_ReturnsError(self):
        response = self._create_product(self._products['null'])

        self.assertEqual(response['status'], 0, 'response status')

    def test_EditingProduct_ChangesItInTheList(self):
        pass

    def test_EditingProduct_DoesntChangeItsAlias(self):
        pass

    def test_DeletingExistingProduct_RemovesItFromTheList(self):
        response = self._create_product(self._products['valid'])
        delete_response = self._api.delete(response['id'])

        products = self._api.list()
        list_product = self._find_product(products, response['id'])

        self.assertEqual(delete_response['status'], 1, 'delete response status')
        self.assertIsNone(list_product, 'product is deleted')

    def test_DeletingNonExistingProduct_ReturnsError(self):
        response = self._api.delete(13371488)

        self.assertEqual(response['status'], 0, 'response status')

    def _load_config_json(self, file_path):
        full_path = path.join(self._CONFIG_DIR, file_path)
        with open(full_path, encoding='utf-8') as f:
            return json.loads(f.read())

    def _json_matches_schema(self, data, schema):
        try:
            jsonschema.validate(data, schema)
            return True
        except:
            return False

    def _create_product(self, body):
        try:
            response = self._api.add(body)
            self._created_product_ids.append(response['id'])
        except:
            response = { 'status': 0 }

        return response

    def _find_product(self, products, id):
        for product in products:
            if int(product['id']) == id:
                return product

        return None


if __name__ == '__main__':
    unittest.main()
