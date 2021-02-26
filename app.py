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
    movies = list(mongo.db.movies.find())
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
            "password": generate_password_hash(request.form.get("password"))
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
                    flash("Welcome, {}".format(request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["register"]))

            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["register"]})["username"]

    if session["register"]:
        review = mongo.db.review.find()
        return render_template("profile.html", username=username, review=review)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("register")
    return redirect(url_for("login"))


@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        movies = {
            "movie_title": request.form.get("movie_title"),
            "director": request.form.get("director"),
            "genre_type": request.form.get("genre_type"),
            "release_date": request.form.get("release_date"),
            "actors": request.form.getlist("actors[]"),
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


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
