from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import DateTime, select
from sqlalchemy.orm import Mapped, mapped_column

from adapters.database import db as database


class Session(database.db.Model):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True)
    client_ip: Mapped[str] = mapped_column()
    key: Mapped[str] = mapped_column(unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class SessionRepo:
    db: SQLAlchemy

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def save(self, s: Session):
        self.db.session.add(s)
        self.db.session.commit()

    def select_by_key(self, key: str) -> Session | None:
        stmt = select(Session).where(Session.key == key)
        row = self.db.session.execute(stmt).first()
        return row[0] if row else None
