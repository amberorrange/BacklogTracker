"""CRUD Operations"""

from model import db, User, Game, Genre, Review, Backlog, Platform, connect_to_db


def check_login(email, password):
    """Returns a user if their login information exists in db"""

    user = User.query.filter( (User.email == email) & (User.password == password) ).first()
    return user
     
def create_user(fname, lname, email, password):
    """Creates and returns a new user"""

    if fname == "" or lname == "" or email == "" or password == "":
        return None

    user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_user_by_email(email):
    """Returns a user by their email"""

    return User.query.filter(User.email == email).first()

def delete_account(email):
    """Deletes a user's account"""

    user= User.query.filter(User.email==email).first()
    db.session.delete(user)
    db.session.commit()

def change_account_info(current_email, fname, lname, email, password):
    """Changes a user's account information"""

    if fname == "" or lname == "" or email == "" or password == "":
        return None

    user = User.query.filter(User.email==current_email).update({User.fname: fname, User.lname: lname, User.email: email, User.password: password})
    db.session.commit()

    return user

def get_genres():
    """Returns names of the genres in db (must be lowercase to use in requests to RAWG API)"""

    genres = Genre.query.all()
    genre_names = []
    for genre in genres:
        genre_names.append(genre.name.lower())

    return genre_names

def create_game(title, description, rawg_id, image):
    """Creates a game and returns it"""

    game = Game(title=title, description=description, rawg_id=rawg_id, image=image)

    db.session.add(game)
    db.session.commit()

    return game

def delete_game(id):
    """Deletes a game(based on its id)"""

    game = Game.query.get(id)

    db.session.delete(game)
    db.session.commit()

def create_backlog(user_id, game_id, ownership_status, play_status, platform, genre):
    """Creates a Backlog entry and returns it"""

    backlog = Backlog(user_id=user_id, game_id=game_id, ownership_status=ownership_status, play_status=play_status, platform=platform, genre=genre)

    db.session.add(backlog)
    db.session.commit()

    return backlog

def get_game_by_id(id):
    """Returns game with the given id"""

    return  Game.query.get(id)

def get_game_by_rawg_id(rawg_id):
    """Checks for a game by rawg_id and returns it"""

    return Game.query.filter(Game.rawg_id == rawg_id).first()

def get_backlog_by_user(user_id):
    """Returns backlog entries of a user"""

    return Backlog.query.filter(Backlog.user_id==user_id).all()

def check_backlogs(game_id):
    """Returns Backlog searched by game_id"""

    return Backlog.query.filter(Backlog.game_id==game_id).first()

def change_backlog_entry(backlog_id, ownership_status, play_status, platform, genre):
    """Changes info for a backlog entry"""

    backlog_entry = Backlog.query.filter(Backlog.backlog_id==backlog_id).update({Backlog.ownership_status: ownership_status, Backlog.play_status: play_status, Backlog.platform: platform, Backlog.genre: genre})
    db.session.commit()

    return backlog_entry

def delete_backlog_entry_by_id(id):
    """Deletes a backlog entry from db"""

    backlog = Backlog.query.get(id)
    db.session.delete(backlog)
    db.session.commit()

def get_backlog_by_id(id):
    """Returns backlog entry with given id"""

    return Backlog.query.get(id)

def create_review(user_id, game_id, body, score, completion_time, platform, genre):
    """Creates and returns a review"""

    review = Review(user_id=user_id, game_id=game_id, body=body, score=score, completion_time=completion_time, platform=platform, genre=genre)

    db.session.add(review)
    db.session.commit()

    return review

def get_reviews_by_user_id(user_id):
    """Returns all reviews from a user"""

    return Review.query.filter(Review.user_id==user_id).all()

def get_review_by_id(id):
    """Returns a review by its id """

    return Review.query.get(id)

def change_review_info(review_id, body, score, completion_time, platform, genre):
    """Changes information for a review"""

    review = Review.query.filter(Review.review_id==review_id).update({Review.body: body, Review.score: score, Review.completion_time: completion_time, Review.platform: platform, Review.genre: genre})
    db.session.commit()

    return review

def delete_review(id):
    """Deletes a review from db"""

    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()

def check_play_status(status):
    """Checks play status of game and returns boolean"""
    if status == "Yes":
            return True
    return False

def get_completion_time(reviews):
    """Returns sum of completion times in a user's reviews """
    completion_time = 0
    for review in reviews:
        completion_time += review.completion_time 
    
    return completion_time

def get_sums_of_genres(rows):
    """Gets sums of hours played for each genre of a user and reformats it"""
    dict1 = {}
    for review in rows:
        dict1[review.genre] = dict1.get(review.genre, 0) + review.completion_time
    
    genres_lst = []
    hours_lst = []

    for genre in dict1.keys():
        genres_lst.append(genre)
    
    for hours in dict1.values():
        hours_lst.append(hours)

    final_dict = { "labels": genres_lst,
                    "data": {"quantity": hours_lst} }

    return final_dict

def get_sums_of_platforms(rows):
    """Gets sums of hours played for each platform of a user and reformats it"""
    dict1 = {}
    for review in rows:
        dict1[review.platform] = dict1.get(review.platform, 0) + review.completion_time
    
    genres_lst = []
    hours_lst = []

    for genre in dict1.keys():
        genres_lst.append(genre)
    
    for hours in dict1.values():
        hours_lst.append(hours)

    final_dict = { "labels": genres_lst,
                    "data": {"quantity": hours_lst} }

    return final_dict


if __name__ == '__main__':
    from server import app
    connect_to_db(app)


