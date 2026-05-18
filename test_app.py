import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_content(self):
        response = self.client.get('/')
        # Accepts either the fallback or the ContentSlot tag
        self.assertTrue(
            b'Welcome to the Monorepo' in response.data or
            b'content-key="index_html.welcome_to_the_monorepo"' in response.data
        )
        self.assertTrue(
            b'Get Started' in response.data or
            b'content-key="index_html.get_started"' in response.data
        )

if __name__ == '__main__':
    unittest.main()
