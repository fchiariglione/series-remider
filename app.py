from flask import Flask, redirect, url_for, render_template, request, session, flash
import sqlalchemy
from datetime import timedelta

app = Flask(__name__)

#Se necesita para usar sesiones
app.secret_key = "hello"
#Tiempo de vida de la sesion
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/')

def index():
    return render_template("index.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user
        flash(f"Logged in as {user}")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash(f"Already logged in")
            return redirect(url_for("user")) 
        return render_template("login.html")


@app.route('/user', methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash(f"Email saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash(f"You are not logged in")
        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    flash("You have been logged out", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)