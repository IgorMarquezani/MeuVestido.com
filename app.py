from flask import Flask, render_template, request, send_file

from adapters.controllers import users
from adapters.database import db as database
from application.authenticator import Authenticator
from models.user import User

app = Flask(__name__, static_folder="./public")

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:root@localhost:5432/root"

database.db.init_app(app)

with app.app_context():
    database.db.create_all()

auth = Authenticator(database.db)


@app.get("/")
@auth.set_user_decorator
def index(user: User):
    return render_template("index.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return send_file("./public/html/login.html")

    return users.login(request)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return send_file("./public/html/signup.html")

    return users.signup(request)


@app.route("/product-register", methods=["GET"])
@auth.set_user_decorator
def product_register(user: User):
    return render_template("product-register.html", user=user)


@app.get("/product/<id>")
def product(id: str):
    return render_template("product.html")
