from functools import wraps
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from adapters.database import db as database
from models.session import Session, SessionRepo
from models.user import UserRepo


class Authenticator:
    def __init__(self, db: SQLAlchemy) -> None:
        self.db = db

    def authenticate(self, raw_cookie: str) -> bool:
        cookie = raw_cookie.split(" ")
        if len(cookie) < 1:
            return False

        key_value = cookie[0]

        v = key_value.split("=")

        stmt = select(Session).where(Session.key == v)

        row = self.db.session.execute(stmt).first()

        return True if row else False

    def set_user_decorator(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = request.cookies.get("_Secure1")
            if not key:
                return func(*args, **kwargs, user=None)

            session_repo = SessionRepo(database.db)

            s = session_repo.select_by_key(key)
            if not s:
                return func(*args, **kwargs, user=None)

            user_repo = UserRepo(database.db)

            u = user_repo.select_by_id(s.user_id)
            if not u:
                return func(*args, **kwargs, user=None)

            return func(*args, **kwargs, user=u)

        return wrapper
