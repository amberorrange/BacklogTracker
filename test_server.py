mport server
import unittest


class MyAppIntegrationTestCase(unittest.TestCase):
    """Examples of integration tests: testing Flask server."""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True


    def test_(self):
        result = self.client.get('/')
        self.assertIn(b'', result.data)

    def test_m(self):
        result = self.client.post('/', data={})
        self.assertIn(b'', result.data)
##
if __name__ == '__main__':
    unittest.main()