import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash

import config
import db
import items

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)


@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items=all_items)


#tiedon hankinta
@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    return render_template("show_item.html", item=item) 

#arvostelun muokkaus

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_item.html",item=item)


@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    album = request.form["album"]
    if not album or len(album) > 50:
        abort(403)
    artist = request.form["artist"]
    if not artist or len(artist) > 50:
        abort(403)
    review = request.form["review"]
    if not review or len(review) > 1000:
        abort(403)

    review_points = int(request.form["review_points"])
    if review_points < 1 or review_points > 10:
        return "VIRHE: arvostelun pitää olla 1-10"



    items.update_item(item_id, album, artist, review, review_points)

    return redirect("/item/" + str(item_id))


#arvostelun poisto

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html",item=item)

    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))





#uusi arvostelu
@app.route("/new_item")
def new_item():
    require_login()
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()

    album = request.form["album"]
    if not album or len(album) > 50:
        abort(403)
    artist = request.form["artist"]
    if not artist or len(artist) > 50:
        abort(403)
    review = request.form["review"]
    if not review or len(review) > 1000:
        abort(403)

    review_points = int(request.form["review_points"])
    if review_points < 1 or review_points > 10:
        return "VIRHE: arvostelun pitää olla 1-10"

    user_id = session["user_id"]

    items.add_item(album, artist, review, review_points, user_id)

    return redirect("/")



#tunnus

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

#tiedon etsiminen

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_item(query)

    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)






#kirjautuminen

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]

        user_id = result["id"]
        password_hash = result["password_hash"]
        password_input = request.form["password"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session ["user_id"]
        del session["username"]
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
  