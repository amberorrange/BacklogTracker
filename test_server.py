import server
import unittest
import model


class FlaskTests(unittest.TestCase):
    """Integration tests for Flask server."""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    # Connect to test database
    model.connect_to_db(server.app, "postgresql:///testdb")

    # Create tables and add sample data
    model.db.create_all()
    model.example_data()

    
    # def tearDown(self):
    #   """Stuff to do after each test."""









    
    # def test_home(self):
    #     client = server.app.test_client()
    #     result = client.get('/')
    #     self.assertEqual(result.status_code, 200)

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email": "user1@test.test", "password": "testpw!!"},
                                  follow_redirects=True)
        self.assertIn(b'<li><a href="/add_game">Add a game to your backlog.</a> </li>', result.data)

    # def test_show_user_details(self):
    #     result = self.client.post('/show_user_details', data={})
    #     self.assertIn(b'<h1> Account Information </h1>', result.data)


    #   def test_some_flask_route(self):
    #   """Some non-database test..."""

    #   result = self.client.get("/my-route")
    #   self.assertEqual(result.status_code, 200)
    #   self.assertIn('<h1>Test</h1>', result.data)





if __name__ == '__main__':
    unittest.main()