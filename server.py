"""Server for my app."""


from flask import (Flask, render_template, request, flash, session,
                   redirect)


from model import connect_to_db
# import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined




@app.route('/')
def homepage():
    """View Homepage of Backlog Tracker"""

    return render_template('homepage.html')



@app.route('/login')
def login():
    """Allows users to login to their account with their account info/shows form to login"""

    return render_template('login.html')
    

@app.route('/login_confirmation')
def login_confirmation():
    """Confirms a user has successfully logged in and either
    redirects to view their backlog or redirects back to the login page"""





@app.route("/create_account")
def create_account():
    """Allows user to create new accounts"""
    #after creating account- an alert will confirm their account
    # they will be directed to the view_backlog route



@app.route('/view_backlog')
def view_backlog():
    """Displays users to see their backlog entries."""
    #also includes hyperlinks to the add_game route and add_review routes


@app.route('/add_game')
def add_game():
    """Allow users to add a new entry to their backlog"""



@app.route('/add_review')
def add_review():
    """Users can add a review for games they've played."""






if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
