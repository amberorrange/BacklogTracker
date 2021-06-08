"""CRUD Operations"""

from model import db, User, Game, Genre, Review, Backlog, connect_to_db


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

    user = User.query.filter(User.email==current_email).update({User.fname: fname, User.lname: lname, User.email: email, User.password: password})
    db.session.commit()

    return user











# def create_review(user, game, body, score):
#     """Create and Retrun a review."""

#     review = Review(user=user, game=game, body=body, score=score)

#     db.session.add(review)
#     db.session.commit()

#     return review




if __name__ == '__main__':
    from server import app
    connect_to_db(app)


