""" Models for my backlog Tracking app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer,
                        autoincrement= True,
                        primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)                    
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    #has 2 relationships
    backlogs = db.relationship('Backlog', backref='user') #primary key to backlogs foreign key
    reviews = db.relationship('Review', backref='user') #primaray key to reviews foreign key

    

    def __repr__(self):
        return f'<User user_id={self.user_id} fname={self.fname} lname={self.lname} email={self.email}>'



class Genre(db.Model):
    """A genre (of a game)"""

    __tablename__ = 'genres'

    genre_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False) 
    

    def __repr__(self):
        return f'<Genre genre_id={self.genre_id} name={self.name}>'

    #has relationship with game
    games = db.relationship("Game", backref="genres") #primary key to games foreign key



class Game(db.Model):
    """A game"""

    __tablename__ = 'games'

    game_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id')) #questions
    igdb_id = db.Column(db.Integer) #uhhhhh

    
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
    play_status = db.Column(db.Boolean, nullable=False, default=False) 


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


    # if len(User.query.all())
    # test_user = User(fname='testfname', lname='testlname', email='test@test.test', password='testpw')
    # test_game= Game(title='testtitle')







