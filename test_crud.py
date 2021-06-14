import unittest
import crud
from model import db, User, Game, Genre, Review, Backlog, Platform, connect_to_db

class usersTestCase(unittest.TestCase):
    """Unit tests about User class"""

    def test_check_login(self):
        self.assertIsInstance(crud.check_login("test1@test.test", "testpw!!"), object)

    def test_create_user(self): 
        self.assertIsInstance(crud.create_user("test11", "test11", "test11@test.test", "testpw!!" ), object)

    def test_create_user_2(self):
        self.assertIsNone(crud.create_user("", "", "", "" )) 

    def test_change_account_info(self): 
        self.assertIsInstance(crud.change_account_info("test11@test.test","test12", "test12", "test12@test.test", "testpw!!" ), object)

    def test_delete_created_user(self):
        self.assertIsNone(crud.delete_account("test12@test.test")) 

    def test_get_user_by_email(self):
        self.assertIsInstance(crud.get_user_by_email("test1@test.test"), object)


class genresTestCase(unittest.TestCase):
    """Unit tests about Genre class"""

    def test_get_genres(self):
        self.assertIsInstance(crud.get_genres(), list)

    def test_get_genres_2(self):
        self.assertNotEqual(crud.get_genres(), [])


# class gamesTestCase(unittest.TestCase):
#     """Unit tests about Game class"""









if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    unittest.main()