"""Server for my app."""


from flask import (Flask, render_template, request, flash, session,
                   redirect)


from model import connect_to_db

import crud 

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


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
    
        # session["user"] = user
        flash("You have successfully logged in!")
        return redirect("/view_backlog")
    else:
        flash('Email or Password not found. Please try again or create an account.')
        return redirect('/login')




@app.route("/create_account")
def create_account():
    """Allows user to create new accounts"""
    #displays form to enter new account information
    return render_template("create_account.html")


@app.route("/register_account", methods=["POST"])
def show_user():
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
def view_backlog():
    """Displays users to see their backlog entries."""
    #also includes hyperlinks to the add_game route and add_review routes

    return render_template('backlogs.html')


@app.route('/add_game')
def add_game():
    """Allow users to add a new entry to their backlog"""



@app.route('/add_review')
def add_review():
    """Users can add a review for games they've played."""


if __name__ == '__main__':
    connect_to_db(app)
    app.debug = True
    app.run(host='0.0.0.0', debug=True)
