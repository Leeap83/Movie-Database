import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
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
    return render_template("index.html")


@app.route("/get_movies")
def get_movies():
    movies = list(mongo.db.movies.find().sort("movie_title", 1))
    review = list(mongo.db.review.find())
    return render_template("get_movies.html", movies=movies, review=review)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    movies = list(mongo.db.movies.find({"$text": {"$search": query}}))
    return render_template("get_movies.html", movies=movies)


@app.route("/movie_details/<movie_id>")
def movie_details(movie_id):
    movie = mongo.db.movies.find_one({'_id': ObjectId(movie_id)})
    review = mongo.db.review.find().sort("review_date", 1)
    return render_template("movie_details.html", movie=movie, review=review)


# User functions #

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username exists try another")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "favourite_movies": []
        }
        mongo.db.users.insert_one(register)

        session["register"] = request.form.get("username").lower()
        flash("Successfully registered, welcome!")
        return redirect(url_for("profile", username=session["register"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:

            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["register"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["register"]))

            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("register")
    return redirect(url_for("login"))


# User Profile #

@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["register"]})["username"]

    if session["register"]:
        review = mongo.db.review.find()

        user_in_db = mongo.db.users.find_one({"username": session["register"]})
        favourites = mongo.db.users.find(user_in_db)

        # Defines favourite_recipes array from current User document
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
            "created_by": session["register"]
        }
        mongo.db.movies.insert_one(movies)
        flash("Movie Added")
        return redirect(url_for("get_movies"))

    movie = mongo.db.movies.find()
    genre = mongo.db.genre.find().sort("genre_type", 1)
    return render_template("add_movie.html", movie=movie, genre=genre)


@app.route("/edit_movie/<movie_id>", methods=["GET", "POST"])
def edit_movie(movie_id):
    if request.method == "POST":
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
            "created_by": session["register"]
        }
        mongo.db.movies.update({"_id": ObjectId(movie_id)}, edit)
        flash("Movie Successfully Edited")

    movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    genre = mongo.db.genre.find().sort("genre_type", 1)
    return render_template("edit_movie.html", movie=movie, genre=genre)


@app.route("/delete_movie/<movie_id>")
def delete_movie(movie_id):
    mongo.db.movies.remove({"_id": ObjectId(movie_id)})
    flash("Movie Succesfully Deleted")
    return redirect(url_for("get_movies"))


# CRUD Movie Review functions #

@app.route("/movie_review/<movie_id>", methods=["GET", "POST"])
def movie_review(movie_id):
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

    movie = mongo.db.movies.find_one({"_id": ObjectId(movie_id)})
    genre = mongo.db.genre.find().sort("genre_type", 1)
    return render_template("movie_review.html", movie=movie, genre=genre)


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
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
    mongo.db.review.remove({"_id": ObjectId(reviews_id)})
    flash("Review Succesfully Deleted")

    reviews = mongo.db.review.find_one({"_id": ObjectId(reviews_id)})
    username = mongo.db.users.find_one(
        {"username": session["register"]})["username"]
    return render_template("profile.html", username=username, reviews=reviews)


# Add Favourites #

@app.route('/add_favourites/<movie_id>', methods=["GET", "POST"])
def add_favourites(movie_id):
    # Checks if user is in session
    if 'register' in session:
        # Identifies the current user
        user = mongo.db.users.find_one({"username": session['register']})

        favourites = user['favourite_movies']

        if ObjectId(movie_id) not in favourites:
            mongo.db.users.update_one(
                {"username": session['register']},
                {"$push": {"favourite_movies": ObjectId(movie_id)}})

            mongo.db.movies.update(
                {'_id': ObjectId(movie_id)},
                {'$inc': {'favourite_count': 1}})

        else:

            flash("You have already added this Movie to your Favourites")
            return redirect(url_for('movie_details',
                                    user=user['username'], movie_id=movie_id))

    flash('Added to My Favourites.')
    return redirect(url_for(
        'movie_details', user=user['username'], movie_id=movie_id))


@app.route('/remove_favourites/<movie_id>', methods=["GET", "POST"])
def remove_favourites(movie_id):

    # Identifies the current user
    user = mongo.db.users.find_one({"username": session['register']})

    favourites = user['favourite_movies']

    # Removes movie from user's favourites
    if ObjectId(movie_id) in favourites:
        mongo.db.users.update(
            {"username": session['register']},
            {"$pull": {"favourite_movies": ObjectId(movie_id)}})

        mongo.db.movies.update(
            {'_id': ObjectId(movie_id)},
            {'$inc': {'favourite_count': -1}})

    flash('Removed from My Favourites.')
    return redirect(url_for("profile", user=user['username'], movie_id=movie_id))



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
