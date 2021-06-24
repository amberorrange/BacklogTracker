import server
import unittest
from model import db, connect_to_db, User, Game, Genre, Review, Backlog, Platform, example_data
import crud


class FlaskTests(unittest.TestCase):
    """Integration tests for Flask server."""

    def setUp(self):
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(server.app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Completes after each test"""

        db.session.close()
        db.drop.all()


    def test_home(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertEqual(result.status_code, 200)



    # def test_login(self):
    #     """Test login page."""

    #     result = self.client.post("/login",
    #                               data={"email": "user1@test.test", "password": "testpw!!"},
    #                               follow_redirects=True)
    #     self.assertIn(b'<li><a href="/add_game">Add a game to your backlog.</a> </li>', result.data)

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