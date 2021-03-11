import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, abort)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["Mongo_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    """
    Home Page for the Website. Invites users to Start Browsing
    Sign-In or Register a new account
    """
    return render_template("index.html")


@app.route("/get_movies")
def get_movies():
    "Movies Page displays all movies to the users"
    movies = list(mongo.db.movies.find().sort("movie_title", 1))
    review = list(mongo.db.review.find())
    return render_template("get_movies.html", movies=movies, review=review)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Search bar that uses the indexes created in MongoDB's allows the users to
    search for any movie title, director or actor name. The results are then
    displayed. If there are no results for the user's query, then message
    displayed telling user no matches.
    """
    query = request.form.get("query")
    movies = list(mongo.db.movies.find({"$text": {"$search": query}}))
    return render_template("get_movies.html", movies=movies)


@app.route("/movie_details/<movie_id>")
def movie_details(movie_id):
    """ Movie Details page. Displays the movie details stored in
    MongoDB after users clicks view more button
    """
    # identifies the current movie and returns the movie details
    movie = mongo.db.movies.find_one({'_id': ObjectId(movie_id)})
    # Finds and returns all reviews stored on the MongoDB
    review = mongo.db.review.find().sort("review_date", 1)
    return render_template("movie_details.html", movie=movie, review=review)


# User functions #
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Registers new users to the website.
    """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # Check if username is already registered
        if existing_user:
            flash("Username exists try another")
            return redirect(url_for("register"))
        # Creates a new user with a hashed password
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "favourite_movies": []
        }
        mongo.db.users.insert_one(register)
        # logs user into session cookie called 'register'
        session["register"] = request.form.get("username").lower()
        flash("Successfully registered, welcome!")
        return redirect(url_for("profile", username=session["register"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs the user into the website.
    """
    if request.method == "POST":
        # Check if user is registered
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # if existing user, redirects user to profile page
        if existing_user:
            # ensures hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["register"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["register"]))

            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # if not an existing user, redirects user to login page
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Logs the users out of the session
    """
    flash("You have been logged out")
    session.pop("register")
    return redirect(url_for("login"))


# User Profile #

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Users Profile page displays the users reviews and Favourite movies.
    """
    username = mongo.db.users.find_one(
        {"username": session["register"]})["username"]

    if session["register"]:
        # Displays the reviews the user created
        review = mongo.db.review.find()

        user_in_db = mongo.db.users.find_one({"username": session["register"]})
        favourites = mongo.db.users.find(user_in_db)

        # Defines favourite_movies array from current User document
        favourites_movies = user_in_db["favourite_movies"]

        favs = mongo.db.movies.find({"_id": {
                                    "$in": favourites_movies}
                            })

        return render_template(
            "profile.html", username=username, review=review, user=user_in_db,
            favourites=favourites, favourites_movies=favourites_movies,
            favs=favs)

    return redirect(url_for("login"))


# CRUD Movie Functions #

@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    """
    Inserts new movie to the movies collection when user submits
    the form from the add_movie page.
    """
    if request.method == "POST":
        movies = {
            "movie_title": request.form.get("movie_title"),
            "director": request.form.get("director"),
            "genre_type": request.form.get("genre_type"),
            "release_date": request.form.get("release_date"),
            "actors": request.form.getlist("actors[]"),
            "classification": request.form.get("classification"),
            "run_time": request.form.get("run_time"),
            "plot": request.form.get("plot"),
            "poster_image": request.form.get("poster_image"),
            "trailer": request.form.get("trailer"),
            "created_by": session["register"],
            "itunes": request.form.get("itunes"),
            "amazon": request.form.get("amazon")
        }
        mongo.db.movies.insert_one(movies)
        flash("Movie Added")
        return redirect(url_for("get_movies"))

    movie = mongo.db.movies.find()
    genre = mongo.db.genre.find().sort("genre_type", 1)
    return render_template("add_movie.html", movie=movie, genre=genre)


@app.route("/edit_movie/<movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    """
    Allows users to edit the movie currently being viewed.
    User is brought to a form page based on the movies current fields.
    """
    if request.method == "POST":
        # captures current forms data and allows users to update details
        edit = {
            "movie_title": request.form.get("movie_title"),
            "director": request.form.get("director"),
            "genre_type": request.form.get("genre_type"),
            "release_date": request.form.get("release_date"),
            "actors": request.form.getlist("actors[]"),
            "classification": request.form.get("classification"),
            "run_time": request.form.get("run_time"),
            "plot": request.form.get("plot"),
            "poster_image": request.form.get("poster_image"),
            "trailer": request.form.get("trailer"),
            "created_by": session["register"],
            "itunes": request.form.get("itunes"),
            "amazon": request.form.get("amazon")
        }
        mongo.db.movies.update({"_id": ObjectId(movie_id)}, edit)
        flash("Movie Successfully Edited")

    movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    genre = mongo.db.genre.find().sort("genre_type", 1)
    return render_template("edit_movie.html", movie=movie, genre=genre)


@app.route("/delete_movie/<movie_id>")
def delete_movie(movie_id):
    """
    Allows users to delete the current movie
    """
    mongo.db.movies.remove({"_id": ObjectId(movie_id)})
    flash("Movie Succesfully Deleted")
    return redirect(url_for("get_movies"))


# CRUD Movie Review functions #

@app.route("/movie_review/<movie_id>", methods=["GET", "POST"])
def movie_review(movie_id):
    """
    Path that allows users to add a review to the current movie
    """
    if request.method == "POST":
        review = {
            "movie_title": request.form.get("movie_title"),
            "rating": request.form.get("rating"),
            "review_title": request.form.get("review-title"),
            "review": request.form.get("review"),
            "review_date": request.form.get("review_date"),
            "created_by": session["register"]
        }
        mongo.db.review.insert_one(review)
        flash("Movie Successfully Reviewed")
        return redirect(url_for("get_movies"))
    # finds the current movie
    movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    genre = mongo.db.genre.find().sort("genre_type", 1)
    return render_template("movie_review.html", movie=movie, genre=genre)


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    """
    Allows users to add a review to the movie
    via the form on the add_review page
    """
    if request.method == "POST":
        review = {
            "movie_title": request.form.get("movie_title"),
            "rating": request.form.get("rating"),
            "review_title": request.form.get("review-title"),
            "review": request.form.get("review"),
            "review_date": request.form.get("review_date"),
            "created_by": session["register"]
        }
        mongo.db.review.insert_one(review)
        flash("Movie Successfully Reviewed")
        return redirect(url_for("get_movies"))

    movie = mongo.db.movies.find().sort("movie_title", 1)
    return render_template("add_review.html", movie=movie)


@app.route("/delete_review/<reviews_id>")
def delete_review(reviews_id):
    """
    Allows users to delete reviews they have created
    """
    mongo.db.review.remove({"_id": ObjectId(reviews_id)})
    flash("Review Succesfully Deleted")

    reviews = mongo.db.review.find_one({"_id": ObjectId(reviews_id)})
    username = mongo.db.users.find_one(
        {"username": session["register"]})["username"]
    return render_template("profile.html", username=username, reviews=reviews)


# Add Favourites #

@app.route('/add_favourites/<movie_id>', methods=["GET", "POST"])
def add_favourites(movie_id):
    """
    Allows users the ability to add movies to their favourites
    """
    # Checks if user is in session
    if 'register' in session:
        # Identifies the current user
        user = mongo.db.users.find_one({"username": session['register']})

        favourites = user['favourite_movies']
        # Makes sure the movie is not already in the user's
        # favourites and then adds to favourites
        if ObjectId(movie_id) not in favourites:

            mongo.db.users.update_one(
                {"username": session['register']},
                {"$push": {"favourite_movies": ObjectId(movie_id)}})

            mongo.db.movies.update(
                {'_id': ObjectId(movie_id)},
                {'$inc': {'favourite_count': 1}})

        else:
            # If the movie is already in the User's favourites,
            # the below message is displayed
            flash("You have already added this Movie to your Favourites")
            return redirect(url_for('movie_details',
                                    user=user['username'], movie_id=movie_id))

    flash('Added to My Favourites.')
    return redirect(url_for(
        'movie_details', user=user['username'], movie_id=movie_id))


@app.route('/remove_favourites/<movie_id>', methods=["GET", "POST"])
def remove_favourites(movie_id):
    """
    Allows users to remove favourites
    """
    # identifies the current user
    username = mongo.db.users.find_one({"username": session['register']})
    user = mongo.db.users.find_one({"username": session['register']})

    favourites = user['favourite_movies']
    # checks if Movie is in users favourites and remove it from favourites
    if ObjectId(movie_id) in favourites:
        mongo.db.users.update(
            {"username": session['register']},
            {"$pull": {"favourite_movies": ObjectId(movie_id)}})

        mongo.db.movies.update(
            {'_id': ObjectId(movie_id)},
            {'$inc': {'favourite_count': -1}})

        flash('Removed from My Favourites.')
        return redirect(url_for(
            'profile', user=user['username'],
            username=username, movie_id=movie_id))

    else:
        flash('Removed from My Favourites.')
        return redirect(url_for(
            'profile', user=user['username'],
            username=username, movie_id=movie_id))


# Errors #
"""
Path to customised error pages
"""


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(410)
def page_gone(e):
    return render_template('410.html'), 410


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
