"""Server for my app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect, jsonify)

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from model import connect_to_db, User, db, Platform, Genre, Review, Backlog, Game
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
    
    return redirect("/login")


@app.route('/login')
def login():
    """Allows users to enter their login information"""

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

@app.route("/delete_account_confirmation")
@login_required
def delete_account_confirmation():
    """Confirms user wants to delete their account."""
    return render_template("delete_account.html")

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
    
    if current_user.is_authenticated:
        flash("Already logged in.")
        return redirect("/view_backlog")

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

    elif password != pw_confirm: #make sure passwords are the same
        flash("Your passwords don't match. Please try again.")
        return redirect("/create_account")
    elif len(password) < 8:
        flash("Password must be 8 or more characters.")
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

    if len(password) < 8:
        flash("Password must be 8 or more characters.")
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
    """Takes user to form to search for game to add to their backlog"""

    genres = crud.get_genres()
    return render_template("add_game.html", genres=genres)


@app.route("/search_results")
@login_required
def search_results(): 
    """Searches for user's game and displays results."""

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
    if data['esrb_rating'] == None:
        esrb_rating = ""
    else:
        esrb_rating = data['esrb_rating']['name']

    #for form in game_details.html
    platforms = Platform.query.all() 
    genres = Genre.query.all()
    return render_template("game_details.html", 
                            data=data,
                            esrb=esrb_rating,
                            platforms=platforms,
                            genres=genres) 


@app.route('/view_backlog')
def view_backlog():
    """Displays user's backlog entries."""
    
    if current_user.is_authenticated == False:
        flash('Please Log In.')
        return redirect("/")

    return render_template('backlogs.html', backlogs=current_user.backlogs)


@app.route("/backlog_validation", methods=["POST"])
@login_required
def add_game_and_backlog():
    """Adds game into db if not there already and creates a backlog entry for the user"""

    title = request.form.get("title")
    description = request.form.get("description")
    rawg_id = request.form.get("rawg_id")
    image = request.form.get("game_image")
    genre = request.form.get("genres")

    ownership_status = request.form.get("ownership_status")     
    play_status = crud.check_play_status(request.form.get("play_status"))
    platform = request.form.get("platforms")

   #get user object and all its data 
    user = User.query.options(
        db.joinedload('backlogs').joinedload('game')
    ).filter_by(
        email=current_user.email
    ).first()

    game = crud.get_game_by_rawg_id(rawg_id)

    #check if there is already a backlog entry of that game
    if user.is_game_in_backlog(game):
        flash("That game is already in your backlog.") 
        return redirect("/view_backlog")

    #checks if game is in our db or not
    if game is None:
        #if game isn't in db, adds the game to db and then creates backlog entry
        new_game = crud.create_game(title, description, rawg_id, image) 
        crud.create_backlog(user.user_id, new_game.game_id, ownership_status, play_status, platform, genre)  
    else:
        #creates backlog entry of a game that's already in our db
        crud.create_backlog(user.user_id, game.game_id, ownership_status, play_status, platform, genre)

    flash("Game added.")
    return redirect("/view_backlog") 

@app.route('/edit_backlog_selection')
@login_required
def edit_backlog_selection():
    """Shows form to select which backlog entry to edit. """
    return render_template("edit_backlog_selection.html", backlogs=current_user.backlogs)

@app.route('/edit_backlog', methods=['POST'])
@login_required
def edit_backlog():
    """Shows form to edit backlog entry"""
    
    backlog_to_edit = request.form.get('edited_backlog')
    backlog_to_edit = crud.get_backlog_by_id(backlog_to_edit)

    platforms = Platform.query.all() 
    genres = Genre.query.all()

    return render_template("edit_backlog_form.html", 
                            backlog=backlog_to_edit,
                            platforms=platforms, 
                            genres=genres)

@app.route('/confirm_backlog_change', methods=['POST'])
@login_required
def confirm_backlog_change():
    """Updates/comfirms a backlog entries changes"""

    backlog_id = request.form.get('backlog_id')
    backlog_to_edit = crud.get_backlog_by_id(backlog_id)

    ownership_status = request.form.get("ownership_status")     
    play_status = crud.check_play_status(request.form.get("play_status"))
    platform = request.form.get("platforms")
    genre = request.form.get("genres")

    crud.change_backlog_entry(backlog_id, ownership_status, play_status, platform, genre)
    flash(f" Information for {backlog_to_edit.game.title} was changed.")

    return redirect("/view_backlog")
                      
@app.route('/delete_backlog')
@login_required
def delete_backlog():
    """Shows form to delete a backlog entry. """

    return render_template("delete_backlog.html", backlogs=current_user.backlogs)


@app.route('/delete_backlog_confirmation', methods=["POST"])
@login_required
def confirm_delete_backlog():
    """Delete's a backlog entry selected from form. """

    backlog_entry = request.form.get("deleted_backlog")

    db_backlog_entry = crud.get_backlog_by_id(backlog_entry)
    crud.delete_backlog_entry_by_id(db_backlog_entry.backlog_id)

    flash("Your entry has been deleted.")
    return redirect("/view_backlog")


@app.route('/organize_backlogs')
@login_required
def organize_backlogs():
    """Displays backlogs organized by genre, platform, ownership status, play status, or ABC order."""

    organized_by = request.args.get("backlog_organization")

    if organized_by == "Play Status":
        backlogs = Backlog.query.filter(Backlog.user_id==current_user.user_id).order_by(Backlog.play_status).all()
    elif organized_by == "Ownership Status":
       backlogs = Backlog.query.filter(Backlog.user_id==current_user.user_id).order_by(Backlog.ownership_status).all()
    elif organized_by == "Genre":
        backlogs = Backlog.query.filter(Backlog.user_id==current_user.user_id).order_by(Backlog.genre).all()
    elif organized_by == "Platform":
          backlogs = Backlog.query.filter(Backlog.user_id==current_user.user_id).order_by(Backlog.platform).all()
    elif organized_by == "Alphabetical":
        backlogs = Backlog.query.join(Game).filter(Backlog.user_id==current_user.user_id).order_by(Game.title).all()
    else: 
        flash("Please choose an option")
        return redirect("/view_backlog")

    return render_template("organized_backlogs.html", backlogs=backlogs)

@app.route('/add_review')
@login_required
def select_game_to_review():
    """Users choose which game they want to review."""

    return render_template("add_review.html", backlogs=current_user.backlogs)


@app.route('/review_game')
@login_required
def review_game_form():
    """Users can add a review for games they've played."""

    game_id = request.args.get("game_to_review")
    game = crud.get_game_by_id(game_id)

    platforms = Platform.query.all()
    genres = Genre.query.all()

    return render_template("add_review_form.html", game=game, platforms=platforms, genres=genres)


@app.route('/review_confirmation', methods=["POST"])
@login_required
def add_review_to_db():
    """Adds review to the db """

    game_id = request.form.get("game_id")
    body = request.form.get("body")
    score =request.form.get("score")
    completion_time = request.form.get("completion_time")
    platform = request.form.get("platforms")
    genre = request.form.get("genres")

    if score == "" or completion_time == "":
        flash("Please fill out all fields.")
        return redirect("/add_review")

    crud.create_review(current_user.user_id, game_id, body, score, completion_time, platform, genre)
    flash("Your review has been added.")

    return redirect("/view_reviews")


@app.route('/view_reviews')
@login_required
def show_reviews():
    """Displays all a users reviews. """

    reviews = current_user.reviews
    return render_template("show_reviews.html", reviews=reviews)

@app.route('/edit_review_form', methods=["POST"])
@login_required
def show_edit_review_form():
    """Displays form to edit a review."""

    review_to_edit = request.form.get("review")
    review_to_edit = crud.get_review_by_id(review_to_edit)

    genres = Genre.query.all()
    platforms = Platform.query.all()

    return render_template("edit_review_form.html", 
                            review=review_to_edit, 
                            platforms=platforms, 
                            genres=genres)


@app.route('/edit_review_confirmation', methods=["POST"])
@login_required
def confirm_edited_review():
    """Edits a review and confirms the changes."""

    review_id = request.form.get("review_id")
    review_to_edit = crud.get_review_by_id(review_id)

    body = request.form.get("body")
    score =request.form.get("score")
    completion_time = request.form.get("completion_time")
    platform = request.form.get("platforms")
    genre = request.form.get("genres")

    if score == "" or completion_time == "":
        flash("Please fill out all fields.")
        return redirect("/view_reviews")

    crud.change_review_info(review_id, body, score, completion_time, platform, genre)
    flash(f"Review for {review_to_edit.game.title} changed.")

    return redirect("/view_reviews")


@app.route('/delete_review', methods=["POST"])
@login_required
def delete_review():
    """Delete's a review. """

    review_id = request.form.get("review")
    crud.delete_review(review_id)
    flash("Your review has been deleted.")
    
    return redirect("/view_reviews")

@app.route("/show_charts")
@login_required
def show_charts():
    """Display a user's data."""

    reviews = Review.query.filter(Review.user_id == current_user.user_id).all()
    total_completion_time = crud.get_completion_time(reviews)

    return render_template("user_charts.html", completion_time=total_completion_time)

#route to send chart information (ajax request)
@app.route("/get_hours_by_genre.json")
@login_required
def get_hours_by_genre():
    """Returns hours played by genres of a user as json"""

    #get dictionary of genres and sum of hours played per genre of the user
    hours_played_by_genre = db.session.query(Review.genre, Review.completion_time).filter(Review.user_id==current_user.user_id).all() 
    data = crud.get_sums_of_genres(hours_played_by_genre)

    return jsonify(data)

@app.route("/get_hours_by_platform.json")
@login_required
def get_hours_by_platform():
    """Returns hours played by plaforms of a user as json"""

    hours_played_by_platform = db.session.query(Review.platform, Review.completion_time).filter(Review.user_id==current_user.user_id).all() 
    data = crud.get_sums_of_platforms(hours_played_by_platform)

    return jsonify(data)

if __name__ == '__main__':
    connect_to_db(app)
    app.debug = True
    app.run(host='0.0.0.0', debug=True)
