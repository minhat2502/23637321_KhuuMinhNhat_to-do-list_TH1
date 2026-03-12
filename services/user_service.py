from typing import Optional
from sqlalchemy.orm import Session
from repositories import user_repo
from db.models import User
from core.security import create_access_token


def register(db: Session, email: str, password: str) -> User:
    existing = user_repo.get_by_email(db, email)
    if existing:
        return None
    return user_repo.create(db, email, password)


def login(db: Session, email: str, password: str) -> Optional[str]:
    user = user_repo.authenticate(db, email, password)
    if user is None:
        return None
    return create_access_token(subject=user.id)
