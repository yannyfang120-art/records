import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session

import config
import db
import items
import users

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
    classes = items.get_classes(item_id)
    return render_template("show_item.html", item=item, classes=classes) 

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

    review_points = float(request.form["review_points"])
    if review_points < 1 or review_points > 10:
        return "VIRHE: arvostelun pitää olla 1-10"

    review_points = round(review_points, 1)



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

    classes = []
    section = request.form["section"]
    if section:
        classes.append(("Genre", section))

    items.add_item(album, artist, review, review_points, user_id, classes)

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

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "Virhe: tunnus on jo varattu"

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


#käyttäjän linkki

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=items) 




#kirjautuminen

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"



#kirjautuminen ulos

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session ["user_id"]
        del session["username"]
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
  