from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)

# Se necesita para usar sesiones
app.secret_key = "hello"
# SQLAlchemy Config
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Users.sqlite3"
# No trackea modificaciones
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Tiempo de vida de la sesion
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)



class Users(db.Model):
    # Si no se define el nombre entre comillas se usa el nombre de la variable
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

# asegura que la tabla exista
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template("index.html")

# Muestra todos los usuarios
@app.route('/view')
def view():
    return render_template("view.html", values=Users.query.all())

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user

        found_user = Users.query.filter_by(name=user).first()

        if found_user:
            session["email"] = found_user.email
        else:
            usr = Users(user, "")
            db.session.add(usr)
            db.session.commit()

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
            # cambia el mail
            found_user = Users.query.filter_by(name=user).first()
            found_user.email = email
            # guarda en db
            db.session.commit()

            flash("Email saved")
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
