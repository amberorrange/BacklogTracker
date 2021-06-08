"""Server for my app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from model import connect_to_db, User
import os
import crud 
import requests
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"


login_manager = LoginManager()
login_manager.init_app(app)

app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['RAWG_KEY']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def homepage():
    """View Homepage of Backlog Tracker-they can login or create an account"""

    if current_user.is_authenticated:

        flash("Already logged in.")
        return redirect("/view_backlog")
    else:
        return redirect("/login")
   


@app.route('/login')
def login():
    """Allows users to enter their login information"""

    #figure out how to not repeat this in both routes(line 33)?
    if current_user.is_authenticated:

        flash("Already logged in.")
        return redirect("/view_backlog")


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
        flash("You have successfully logged in.")
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



@app.route("/show_user_details")
@login_required
def show_user_details():
    """Shows user's account info. Gives them options to delete or alter their account. """

    return render_template("user_details.html")

@app.route("/delete_account")
@login_required
def delete_account():
    """Delete's a user's account"""
    email = current_user.email
    crud.delete_account(email)
    flash("Your account has been deleted.")
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
    pw_confirm = request.form.get("pw_confirmation")

    user = crud.get_user_by_email(email)

    if user:
        flash('A user with that email already exists. Log in or Try again with a different email.')
        return redirect("/create_account")
    elif  password != pw_confirm: #make sure passwords are the same
        flash("Your passwords don't match. Please try again.")
        return redirect("/create_account")

    else:
        created_user = crud.create_user(fname, lname, email, password)
        if created_user == None: #if some of the fields are left empty, the function will return none
            flash("Please fill out all required fields.")
            return redirect("/create_account")
        else:   
            flash('Account created successfully. Please log in.')
            return redirect("/login")



@app.route("/change_account_info_form")
@login_required
def change_account_info_form():
    """Shows user form to change account information"""

    return render_template("change_account.html")


@app.route("/change_account_info", methods=["POST"])
@login_required
def change_account_info():
    """Changes a user's account information"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    email = request.form.get("email")
    password = request.form.get("password")
    pw_confirm = request.form.get("pw_confirm")

    if pw_confirm != password:
        flash("Passwords do not match.")
        return redirect("/change_account_info_form")

    current_email = current_user.email

    user = crud.change_account_info(current_email, fname, lname, email, password)
    if user == None:
        flash("Please fill all fields.")
        return redirect("/change_account_info_form")
    else:    
        logout_user()
        flash("Your account information is changed. Please log in again.")

    return redirect("/")
  






@app.route('/view_backlog')
def view_backlog():
    """Displays users to see their backlog entries."""
    #also includes hyperlinks to the add_game route and add_review routes

    if current_user.is_authenticated == False:
        flash('Please Log In.')
        return redirect("/")

    return render_template('backlogs.html')


@app.route('/add_game')
@login_required
def add_game():
    """Allow users to add a new entry to their backlog"""

    genres = crud.get_genres()
   
    return render_template("add_game.html", genres=genres)

@app.route("/search_results")
@login_required
def search_results(): 
    """Searches for user's game and displays results"""

    user_query = request.args.get("game", "")
    genre = request.args.get("genres", "")

    if genre == "":
        #add ability to search without genre field
        payload =  {'key': API_KEY,'search': user_query}
    else:
        payload = {'key': API_KEY,'search': user_query, 'genres': genre}

    url = 'https://api.rawg.io/api/games'
    res = requests.get(url, params=payload)
    data = res.json()
    results = data['results']

    return render_template("search_results.html", results=results)


# @app.route('/add_game/rawg_id')
# @login_required
# def show_game_info():
#     """Shows user individual game info and option to add game to backlog."""

#     # game_info = session['results'][]
   
#     # pass



@app.route('/add_review')
@login_required
def add_review():
    """Users can add a review for games they've played."""
    return render_template("add_review.html")


if __name__ == '__main__':
    connect_to_db(app)
    app.debug = True
    app.run(host='0.0.0.0', debug=True)
