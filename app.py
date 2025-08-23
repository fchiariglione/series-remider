from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

@app.route('/')

def index():
    return render_template("index.html")

@app.route("/<name>")
def tipo(name):
    return render_template("name.html", content=name)

@app.route("/admin")

# Ahi en url_for hay que usar una funcion
def admin():
    return redirect(url_for("hser", name="Admin!"))

if __name__ == "__maiin__":
    app.run(debug=True)