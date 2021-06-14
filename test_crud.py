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


class creationsTestCase(unittest.TestCase):
    """Unit tests about creating instances of Game, Backlog, and Review classes"""

    # def test_create_game(self): 
    #     self.assertIsInstance(crud.create_game("Test", "", "0", ""), object)

    # def test_create_backlog(self):
    #     self.assertIsInstance(crud.create_backlog(1, 1, "Owned", True, "PlayStation 4", "RPG"), object)

    # def test_create_review(self):
    #     self.assertIsInstance(crud.create_review(1, 1, "Great", 10, 100, "RPG"), object)

    # next three tests are to delete fake data previously created-problem: they can only be repeated once
    def test_delete_review(self): 
        self.assertIsNone(crud.delete_review(1))

    def test_delete_backlog_entry_by_id(self):
        self.assertIsNone(crud.delete_backlog_entry_by_id(1))

    def test_delete_game(self):
        self.assertIsNone(crud.delete_game(1))


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    unittest.main()