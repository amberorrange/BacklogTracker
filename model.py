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


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Game.query.delete()
    Backlog.query.delete()
    Review.query.delete()
    Genre.query.delete()
    Platform.query.delete()

    #sample data
    user1 = User(fname='user1',lname='luser1', email="user1@test.test", password='testpw!!')
    user2 = User(fname='user2',lname='luser2', email="user2@test.test", password='testpw!!')
    user3 = User(fname='user3',lname='luser3', email="user3@test.test", password='testpw!!')
    user4 = User(fname='user4',lname='luser4', email="user4@test.test", password='testpw!!')

    game1 = Game(title="Persona 5",description="Fun JRPG with dungeons.", rawg_id=11, image= "")
    game2 = Game(title="Quantum Break",description="Freeze Time and save the world.", rawg_id=2, image= "")
    game3 = Game(title="Ace Attorney",description="Protect your clients and defend their innocence.", rawg_id=224, image= "")
   
    bl1 = Backlog(user_id=1, game_id=1, ownership_status="Owned", play_status=False, platform="PlayStation 4", genre="RPG")
    bl2 = Backlog(user_id=2, game_id=2, ownership_status="Not Owned", play_status=False, platform="Xbox One", genre="Action")
    bl3 = Backlog(user_id=3, game_id=3, ownership_status="Owned", play_status=True, platform="Nintendo Switch", genre="Action")
    bl4 = Backlog(user_id=4, game_id=3, ownership_status="Not Owned", play_status=True, platform="Xbox One", genre="Puzzle")

    review1 = Review(user_id=1, game_id=1, body="Fun", score=8, completion_time=11, platform="PlayStation 4")
    review2 = Review(user_id=2, game_id=2, body="Boring", score=4, completion_time=4, platform="Nintendo Switch")
    review3 = Review(user_id=3, game_id=3, body="Okay", score=7, completion_time=22, platform="Xbox One")
    
    genre1 = Genre(name="RPG")
    genre2 = Genre(name="Action")
    genre3 = Genre(name="Puzzle")

    pf1 = Platform(name="PlayStation 4")
    pf2 = Platform(name="Nintendo Switch")
    pf3 = Platform(name="Xbox One")
    
    db.session.add_all([user1, user2, user3, user4, game1, game2, game3, bl1, bl2, bl3, bl4, review1, review2, review3, genre1, genre2, genre3, pf1, pf2, pf3])
    db.session.commit()


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.
    connect_to_db(app)










