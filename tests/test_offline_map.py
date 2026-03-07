import unittest
import os
import sqlite3
from offline_map.app import app

class TestOfflineMap(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Offline Map App', response.data)

    def test_tile_serving(self):
        # We know 0/0/0.png exists in our sample mbtiles
        response = self.app.get('/tiles/0/0/0.png')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, 'image/png')

    def test_tile_not_found(self):
        # High zoom level tile that should not exist
        response = self.app.get('/tiles/10/0/0.png')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
