import unittest
import crud
from model import db, User, Game, Genre, Review, Backlog, Platform, connect_to_db


class userTestCase(unittest.TestCase):
    """Unit tests about user class"""

    def test_check_login(self):
        self.assertIsInstance(crud.check_login("test1@test.test", "testpw!!"), object)

    def test_create_user(self):
        self.assertIsInstance(crud.create_user("test14", "test14", "test14@test.test", "testpw!!" ), object)

    def test_create_user_2(self):
        assert crud.create_user("", "", "", "" ) == None   

    def test_get_user_by_email(self):
        self.assertIsInstance(crud.get_user_by_email("test@test1.test"), object)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    unittest.main()