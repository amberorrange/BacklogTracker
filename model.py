""" Models for my backlog Tracking app"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

import requests

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)                    
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    backlogs = db.relationship('Backlog', backref='user') #primary key to backlogs foreign key
    reviews = db.relationship('Review', backref='user') #primaray key to reviews foreign key

    def get_id(self):
        """Override UserMixin.get_id."""
        
        return str(self.user_id)

    def __repr__(self):
        return f'<User user_id={self.user_id} fname={self.fname} lname={self.lname} email={self.email}>'
    
    def is_game_in_backlog(self, game):
        """Return True if `game` is in `self.backlogs`."""
        
        # Create a list of all games in user's backlog
        backlogged_games = set()
        for log in self.backlogs:
            backlogged_games.add(log.game)

        return game in backlogged_games


class Genre(db.Model):
    """A genre (of a game)"""

    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False) 
    
    def __repr__(self):
        return f'<Genre genre_id={self.genre_id} name={self.name}>'


class Platform(db.Model):
    """A platform(of a game)"""

    __tablename__ = 'platforms'

    platform_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False) 
    
    def __repr__(self):
        return f'<Platform platform_id={self.platform_id} name={self.name}>'


class Game(db.Model):
    """A game"""

    __tablename__ = 'games'

    game_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    rawg_id = db.Column(db.Integer, unique=True) 
    image = db.Column(db.Text)
    
    backlogs = db.relationship("Backlog", backref="game") #primary key to backlogs foreign key
    reviews = db.relationship("Review", backref="game") #primary key to reviews foreign key

    def __repr__(self):
        return f'<Game game_id={self.game_id} title={self.title} igdb_id={self.igdb_id}>'


class Backlog(db.Model):
    """A user's backlog entry"""

    __tablename__ = 'backlogs'

    backlog_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))

    ownership_status = db.Column(db.String(30), nullable=False) 
    play_status = db.Column(db.Boolean, nullable=False) 
    platform = db.Column(db.String(30)) 
    genre = db.Column(db.String(20)) 

    def __repr__(self):
        return f'<Backlog Entry backlog_id={self.backlog_id} user_id={self.user_id} game_id={self.game_id}>'

    #has relationships with user and games


class Review(db.Model):
    """A user's review of a game"""

    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'))
    body = db.Column(db.Text(), nullable=False) 
    score = db.Column(db.Integer, nullable=False) 
    completion_time = db.Column(db.Integer)
    platform = db.Column(db.String(30)) 

    #has relationships with user and games

    def __repr__(self):
        return f'<Review review_id={self.review_id} score={self.score}>'


def connect_to_db(flask_app, db_uri='postgresql:///backlogs', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.
    connect_to_db(app)










