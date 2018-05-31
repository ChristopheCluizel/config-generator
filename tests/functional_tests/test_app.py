from unittest2 import TestCase
from app import app
import json


class AppTests(TestCase):
    def test_status(self):
        expected_response = json.dumps({'success': True})
        with app.test_client() as c:
            response = c.get('/health')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode("utf-8"), expected_response)

    def test_home(self):
        expected_response = json.dumps({'success': True})
        with app.test_client() as c:
            response = c.get('/')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode("utf-8"), expected_response)

    def test_generate_conf_valid(self):
        expected_response = "This is a text with a test-value in the middle."
        with app.test_client() as c:
            response = c.post('/generate-conf',
                              data="This is a text with a {{ all_test_config__generator_test__key }} in the middle.",
                              content_type='text/plain')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode("utf-8"), expected_response)
