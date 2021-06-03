"""Server for my app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)

from flask_login import LoginManager, login_user, login_required, logout_user

from model import connect_to_db, User

import crud 

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"


login_manager = LoginManager()
login_manager.init_app(app)

app.jinja_env.undefined = StrictUndefined


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def homepage():
    """View Homepage of Backlog Tracker-they can login or create an account"""

    return render_template('homepage.html')


@app.route('/login')
def login():
    """Allows users to enter their login information"""

    return render_template('login.html')
    

@app.route('/login_confirmation', methods=['POST'])
def login_confirmation():
    """Confirms a user has successfully logged in and either
    redirects to view their backlog or redirects back to the login page"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.check_login(email, password)
    if user:

        # Call flask_login.login_user to login a user
        login_user(user)
        flash("You have successfully logged in!")
        return redirect("/view_backlog")

    else:
        flash('Email or Password not found. Please try again or create an account.')
        return redirect('/login')


@app.route("/logout")
@login_required
def logout():
    """Logs a user out of their account. """
    logout_user()
    flash("Successfully logged out of account.")

    return redirect("/")




@app.route("/create_account")
def create_account():
    """Allows user to create new accounts"""
    #displays form to enter new account information
    return render_template("create_account.html")


@app.route("/register_account", methods=["POST"])
def register_user():
    """Register a new user"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")


    user = crud.get_user_by_email(email)
    if user:
        flash('A user with that email already exists. Log in or Try again with a different email.')
        return redirect("/create_account")
    else:
        crud.create_user(fname, lname, email, password)
        flash('Account created successfully. Please log in.')
    
        return redirect("/login")


@app.route('/view_backlog')
@login_required
def view_backlog():
    """Displays users to see their backlog entries."""
    #also includes hyperlinks to the add_game route and add_review routes

    return render_template('backlogs.html')


@app.route('/add_game')
@login_required
def add_game():
    """Allow users to add a new entry to their backlog"""



@app.route('/add_review')
@login_required
def add_review():
    """Users can add a review for games they've played."""


if __name__ == '__main__':
    connect_to_db(app)
    app.debug = True
    app.run(host='0.0.0.0', debug=True)
