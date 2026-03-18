import unittest
import os
import io
import json
import sqlite3
from app import app
from database import init_db

TEST_DATABASE = os.path.join(os.path.dirname(__file__), 'test_app_store.db')

class AppStoreApiTestCase(unittest.TestCase):
    def setUp(self):
        # Set environment variable before any imports that might use it
        os.environ['APP_STORE_DB'] = TEST_DATABASE
        app.config['TESTING'] = True
        self.app = app.test_client()
        # Ensure fresh database for each test
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)
        init_db()

    def tearDown(self):
        if os.path.exists(TEST_DATABASE):
            os.remove(TEST_DATABASE)
        if 'APP_STORE_DB' in os.environ:
            del os.environ['APP_STORE_DB']

    def test_auth_and_reviews(self):
        # 1. Signup
        signup_data = {'username': 'testuser', 'password': 'password123', 'email': 'test@example.com'}
        response = self.app.post('/api/signup', json=signup_data)
        self.assertEqual(response.status_code, 201)

        # 2. Login
        login_data = {'username': 'testuser', 'password': 'password123'}
        response = self.app.post('/api/login', json=login_data)
        self.assertEqual(response.status_code, 200)

        # 3. Upload App
        upload_data = {
            'name': 'Test App',
            'package_name': 'com.test.app',
            'description': 'A test application',
            'version': '1.0.0',
            'category': 'Tools',
            'apk': (io.BytesIO(b"fake apk content"), 'test.apk')
        }
        response = self.app.post('/api/apps', data=upload_data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 201)

        # 4. Search and List
        response = self.app.get('/api/apps?search=Test')
        self.assertEqual(response.status_code, 200)
        apps = json.loads(response.data)
        self.assertEqual(len(apps), 1)
        app_id = apps[0]['id']

        # 5. Post Review
        review_data = {'rating': 5, 'comment': 'Great app!'}
        response = self.app.post(f'/api/apps/{app_id}/reviews', json=review_data)
        self.assertEqual(response.status_code, 201)

        # 6. Get Details (with review)
        response = self.app.get(f'/api/apps/{app_id}')
        self.assertEqual(response.status_code, 200)
        app_details = json.loads(response.data)
        self.assertEqual(len(app_details['reviews']), 1)
        self.assertEqual(app_details['reviews'][0]['comment'], 'Great app!')

if __name__ == '__main__':
    unittest.main()
