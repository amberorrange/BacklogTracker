""" Models for my backlog Tracking app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(flask_app, db_uri='postgresql:///backlogs', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')



class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    lname - bd.Column(db.String(30), nullable=False)                    
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

    

    def __repr__(self):
        return f'<User user_id={self.user_id} fname={self.fname} lname={self.lname} email={self.email}>'



class Game(db.Model):
    """A game"""

    __tablename__ = 'games'

    game_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text())
    genre_id = db.Column(db.Integer, db.foreign_key('genres.genre_id')) #questions
    igdb_id = db.Column(db.Integer) #uhhhhh


    def __repr__(self):
        return f'<Game game_id={self.game_id} title={self.title} igdb_id={self.igdb_id}>'



class Backlog(db.Model):
    """A user's backlog entry"""

    _tablename__ = 'backlogs'

    backlog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.foreign_key('users.user_id') nullable=False)
    game_id = db.Column(db.Integer, db.foreign_key('games.game_id'), nullable=False)
    ownership_status = db.Column(db.String(30), nullable=False) 
    play_status = db.Column(db.Boolean, nullable=False, default=False) 


    def __repr__(self):
        return f'<Backlog Entry backlog_id={self.backlog_id} game_id={self.game_id}>'



class Genre(db.Model):
    """A genre (of a game)"""

    _tablename__ = 'genres'

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False) 
    

    def __repr__(self):
        return f'<Genre genre_id={self.genre_id} name={self.name}>'




class Review(db.Model):
    """A user's review of a game"""

    _tablename__ = 'reviews'

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.foreign_key('users.user_id') nullable=False)
    game_id = db.Column(db.Integer, db.foreign_key('games.game_id'), nullable=False)
    body = db.Column(db.Text(), nullable=False) 
    score = db.Column(db.Integer, nullable=False) 
    completion_time = db.Column(db.Integer)


    def __repr__(self):
        return f'<Review review_id={self.review_id} score={self.score}>'





if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
