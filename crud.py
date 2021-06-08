"""CRUD Operations"""

from model import db, User, Game, Genre, Review, Backlog, connect_to_db
import re


def check_login(email, password):
    """returns a user if their login information exists in db"""

    user = User.query.filter( (User.email == email) & (User.password == password) ).first()

    return user

    
def create_user(fname, lname, email, password):
    """Create and return a new user."""

    if fname == "" or lname == "" or email == "" or password == "":

        return None

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_email(email):
    """Return a user by their email"""

    return User.query.filter(User.email == email).first()


def delete_account(email):

    """Delete's a user's account."""

    user= User.query.filter(User.email== email).first()
    db.session.delete(user)
    db.session.commit()



def change_account_info(current_email, fname, lname, email, password):
    """Changes a user's account information. """

    if fname == "" or lname == "" or email == "" or password == "":

        return None

    user = User.query.filter(User.email==current_email).update({User.fname: fname, User.lname: lname, User.email: email, User.password: password})
    db.session.commit()

    return user


def get_genres():
    """Returns all the names of the genres in db. """

    genres = Genre.query.all()
    genre_names = []
    for genre in genres:
        genre_names.append(genre.name.lower())

    return genre_names


def create_game(title, description, rawg_id):
    """Creates a game and returns it."""

    game = Game(title=title, description=description, rawg_id=rawg_id)

    db.session.add(game)
    db.session.commit()

    return game


def create_backlog(user_id, game_id, ownership_status, play_status):
    """ Creates a Backlog entry and returns it."""

    backlog = Backlog(user_id=user_id, game_id=game_id, ownership_status=ownership_status, play_status=play_status)

    db.session.add(backlog)
    db.session.commit()

    return backlog




def get_game_by_rawg_id(rawg_id):
    """Checks for a game by rawg_id and returns it."""

    return Game.query.filter(Game.rawg_id == rawg_id).first()


def get_backlogs():

    return Backlog.query.all()

def check_backlogs(game_id):

    return Backlog.query.filter(Backlog.game.game_id==game_id)






# def create_review(user, game, body, score):
#     """Create and Retrun a review."""

#     review = Review(user=user, game=game, body=body, score=score)

#     db.session.add(review)
#     db.session.commit()

#     return review




if __name__ == '__main__':
    from server import app
    connect_to_db(app)


