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

        flash(f"Currently logged in as {current_user.fname}.")
        return redirect("/view_backlog")
    else:
        return redirect("/login")
   

@app.route('/login')
def login():
    """Allows users to enter their login information"""

    #figure out how to not repeat this in both routes(line 33)?
    if current_user.is_authenticated:

        flash(f"Currently logged in as {current_user.fname}.")
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
    """Allows user to create a new account."""
    #displays form to enter new account information
    return render_template("create_account.html")


@app.route("/register_account", methods=["POST"])
def register_user():
    """Register a new user"""

    if current_user.is_authenticated:
        flash("Already logged in.")
        return redirect("/view_backlog")

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
        if created_user == None: #if some of the fields are left empty, the function create_user will return none
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


    user = crud.get_user_by_email(email)
    if user and user.email != current_user.email:
        flash('A user with that email already exists. Log in or Try again with a different email.')
        return redirect("/change_account_info_form")

    if pw_confirm != password:
        flash("Your passwords don't match. Please try again.")
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


@app.route('/show_game/<rawg_id>')
@login_required
def show_game_info(rawg_id):
    """Shows user individual game info and option to add game to backlog."""

    url = f'https://api.rawg.io/api/games/{rawg_id}'
    payload =  {'key': API_KEY}
    res = requests.get(url, params=payload)
    data = res.json()

    #checks for esrb rating(name error prevention)
    esrb_rating = data['esrb_rating']
    if esrb_rating == None:
        esrb_rating = ""
    else:
        esrb_rating = data['esrb_rating']['name']
    
    return render_template("game_details.html", 
                            data=data,
                            esrb=esrb_rating) 










@app.route('/view_backlog')
def view_backlog():
    """Displays users to see their backlog entries."""
    #hyperlinks to the add_game route and add_review routes

    if current_user.is_authenticated == False:
        flash('Please Log In.')
        return redirect("/")

    backlogs = crud.get_backlogs()
    
  
    return render_template('backlogs.html', backlogs=backlogs)



@app.route("/backlog_validation", methods=["POST"])
@login_required
def add_game_and_backlog():
    """Adds game into db if not there already and creates a backlog entry for the user"""

    title = request.form.get("title")
    description = request.form.get("description")
    rawg_id = request.form.get("rawg_id")
    image = request.form.get("game_image")

    ownership_status = request.form.get("ownership_status")
    play_status = request.form.get("play_status")
    if play_status == "Yes":
        playing = True
    else:
        playing = False


    user = crud.get_user_by_email(current_user.email)
    game = crud.get_game_by_rawg_id(rawg_id)

    #check if there is already a backlog entry
    if game is not None:
        checked_entry = crud.check_backlogs(game.game_id)
    else:
        checked_entry = None
    
    if checked_entry and checked_entry is not None:
        flash("That game is already in your backlog.") 
        return redirect("/view_backlog")



    if game is None:
        #adds game to db if not there and creates backlog entry
        new_game = crud.create_game(title, description, rawg_id, image) 
        crud.create_backlog(user.user_id, new_game.game_id, ownership_status, playing)  
    else:
        #creates backlog entry if game already in db
        crud.create_backlog(user.user_id, game.game_id, ownership_status, playing)

    flash("Game added.")
    return redirect("/view_backlog") 
                            
                        
       


@app.route('/delete_backlog')
@login_required
def delete_backlog():
    """Shows form to delete a backlog entry. """

    backlogs = crud.get_backlogs()

    return render_template("delete_backlog.html", backlogs=backlogs)


@app.route('/delete_backlog_confirmation', methods=["POST"])
@login_required
def confirm_delete_backlog():
    """Delete's a backlog entry selected from form. """

    backlog_entry = request.form.get("deleted_backlog")

    db_backlog_entry = crud.get_backlog_by_id(backlog_entry)

    crud.delete_backlog_entry_by_id(db_backlog_entry.backlog_id)

    flash("Your entry has been deleted.")

    return redirect("/view_backlog")




@app.route('/add_review')
@login_required
def select_game_to_review():
    """Users choose which game they want to review."""

    backlogs = crud.get_backlogs()

    return render_template("add_review.html", backlogs=backlogs)


@app.route('/review_game')
@login_required
def review_game_form():
    """Users can add a review for games they've played."""

    game_id = request.args.get("game_to_review")
    game = crud.get_game_by_id(game_id)

    return render_template("add_review_form.html", game=game)


@app.route('/review_confirmation', methods=["POST"])
@login_required
def add_review_to_db():
    """Adds review to the db """

    game_id = request.form.get("game_id")
    user_id = current_user.user_id
    body = request.form.get("body")
    score =request.form.get("score")
    completion_time =request.form.get("completion_time")


    crud.create_review(user_id, game_id, body, score, completion_time)
    flash("Your review has been added.")

    return redirect("/view_reviews")


@app.route('/view_reviews')
@login_required
def show_reviews():
    """Displays all a users reviews. """

    reviews = crud.get_reviews()

    return render_template("show_reviews.html", reviews=reviews)


if __name__ == '__main__':
    connect_to_db(app)
    app.debug = True
    app.run(host='0.0.0.0', debug=True)
