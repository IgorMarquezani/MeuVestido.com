import uuid
from datetime import datetime, timedelta
from flask import Request, Response, json
from sqlalchemy.exc import IntegrityError

from application import hasher
from application import validator
from models.session import Session, SessionRepo
from models.user import User, UserRepo
from adapters.database import db as database


def signup(req: Request) -> Response:
    form = req.form

    u = User(form)

    v = validator.Validator()

    if not v.validate_name(u.name):
        resp = json.jsonify({
            "message": "invalid name length",
            "details": ["name needs to bet between 2 to 55 characters"],
        })
        resp.status_code = 400
        return resp

    if not v.validate_email(u.email):
        resp = json.jsonify({
            "message": "invalid email address",
        })
        resp.status_code = 400
        return resp

    if not v.validate_passwd(u.password):
        resp = json.jsonify({
            "message": "invalid password",
            "details": [
                "passwords needs to have at least 8 characters",
                "passwords needs to have a numeric character",
                "passwords needs to have a special character",
                "passwords needs to have a uppercase character",
            ],
        })
        resp.status_code = 400
        return resp

    h = hasher.Hasher()

    u.password = h.hash_passwd(u.password)

    repo = UserRepo(database.db)

    try:
        repo.save(u)
    except IntegrityError:
        err = {"message": "email already in use"}
        resp = json.jsonify(err)
        resp.status_code = 208
        return resp

    resp = Response()
    resp.set_data("ok")
    resp.status_code = 200

    return resp


def login(req: Request) -> Response:
    form = req.form

    email = form.get("email", default="")
    passwd = form.get("password", default="")

    user_repo = UserRepo(database.db)

    u = user_repo.select_by_email(email)
    if not u:
        resp = Response("invalid email or password")
        resp.status_code = 400
        return resp

    h = hasher.Hasher()

    if not h.compare_hash_and_passwd(u.password, passwd):
        resp = Response("invalid email or password")
        resp.status_code = 400
        return resp

    s = Session()
    s.user_id = u.id
    s.client_ip = req.remote_addr if req.remote_addr else ""
    s.expires_at = datetime.utcnow() + timedelta(hours=24)
    s.key = str(uuid.uuid4())

    session_repo = SessionRepo(database.db)

    try:
        session_repo.save(s)
    except IntegrityError:
        return Response("ok")
    except Exception as e:
        resp = Response()
        resp.status_code = 500
        resp.set_data("internal server error")
        print(e)
        return resp

    resp = Response("ok")
    resp.set_cookie("_Secure1", s.key, expires=s.expires_at, httponly=True)
    return resp
