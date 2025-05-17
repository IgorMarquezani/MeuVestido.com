from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.datastructures import ImmutableMultiDict

from adapters.database import db as database


class User(database.db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    def __init__(self, form: ImmutableMultiDict) -> None:
        self.name = form.get("name", default="")
        self.email = form.get("email", default="")
        self.password = form.get("password", default="")


class UserRepo:
    db: SQLAlchemy

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def save(self, u: User):
        self.db.session.add(u)
        self.db.session.commit()

    def select_by_id(self, id: int) -> User | None:
        stmt = select(User).where(User.id == id)
        row = self.db.session.execute(stmt).first()
        return row[0] if row else None

    def select_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        row = self.db.session.execute(stmt).first()
        return row[0] if row else None
