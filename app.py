import secrets
import sqlite3
from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session

import config
import db
import items
import re
import users


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

#csfr
def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
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
    bids = items.get_bids(item_id)
    image = items.get_image_by_item(item_id)
    return render_template("show_item.html", item=item, classes=classes, bids=bids, image=image)

#kuvan näyttäminen
@app.route("/images/<int:item_id>")
def edit_images(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    image = items.get_image_by_item(item_id)

    return render_template("images.html", item=item, image=image)

#kuvan lisääminen
@app.route("/add_image", methods=["POST"])
def add_image():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)


    file = request.files["image"]
    if not file.filename.endswith(".png"):
        flash("VIRHE: väärä tiedostomuoto")
        return redirect("/images/" + str(item_id))

    image = file.read()
    if len(image) > 100 * 1024:
        flash("VIRHE: liian suuri kuva")
        return redirect("/images/" + str(item_id))

    items.delete_images(item_id)

    items.add_image(item_id, image)
    return redirect("/images/" + str(item_id))


@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = items.get_image(image_id)
    if not image:
        abort(404)

    response = make_response(image)
    response.headers.set("Content-Type", "image/png")
    return response

#lisäys image-item sivulle
@app.route("/item/<int:item_id>")
def item(item_id):
    item = items.get_item(item_id)
    image = items.get_image_by_item(item_id)
    return render_template("item.html", item=item, image=image)

#kuvan poistaminen

@app.route("/remove_image", methods=["POST"])
def remove_image():
    require_login()
    check_csrf()

    item_id = int(request.form["item_id"])
    image_id = int(request.form["image_id"])

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    items.remove_image(image_id)

    return redirect(f"/images/{item_id}")


#arvostelun muokkaus

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    classes = items.get_all_classes()

    return render_template("edit_item.html",
                           item=item,
                           classes=classes)


@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    check_csrf()

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
        flash("VIRHE: arvostelun pitää olla 1-10")
        return redirect("/item/" + str(item_id))

    review_points = round(review_points, 1)
    review_points_str = f"{review_points:.1f}"

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            classes.append((parts[0], parts[1]))


    items.update_item(item_id, album, artist, review, review_points, classes)

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
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))


#uusi arvostelu
@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_classes()
    return render_template("new_item.html", classes=classes)

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()

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
        flash("VIRHE: arvostelun pitää olla 1-10")
        return redirect(f"/item/{item_id}")

    user_id = session["user_id"]

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            classes.append((parts[0], parts[1]))

    item_id = items.add_item(album, artist, review, review_points, user_id, classes)
    return redirect(f"/item/{item_id}")


#tunnus

@app.route("/register")
def register():
    session["csrf_token"] = secrets.token_hex(16)
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    check_csrf()

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("Virhe: tunnus on jo varattu")
        return redirect("/register")

    return redirect("/")

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


#kommentin käsittelijä
@app.route("/create_bid", methods=["POST"])
def create_bid():
    require_login()
    check_csrf()

    comment_review = request.form["comment_review"]
    if not comment_review or len(comment_review) > 1000:
        abort(403)

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(403)

    user_id = session["user_id"]

    items.add_bid(item_id, user_id, comment_review)

    return redirect("/item/" + str(item_id))


#kirjautuminen

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        session["csrf_token"] = secrets.token_hex(16)
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")



#kirjautuminen ulos

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session ["user_id"]
        del session["username"]
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
  