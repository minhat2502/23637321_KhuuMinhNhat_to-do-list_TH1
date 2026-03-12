from typing import Optional
from sqlalchemy.orm import Session
from repositories import todo_repo
from db.models import Todo


def create_todo(db: Session, title: str, description: Optional[str], is_done: bool, owner_id: int) -> Todo:
    return todo_repo.create(db, title, description, is_done, owner_id)


def get_todos(
    db: Session,
    owner_id: int,
    is_done: Optional[bool],
    q: Optional[str],
    sort: str,
    limit: int,
    offset: int,
) -> dict:
    items, total = todo_repo.get_all(db, owner_id, is_done, q, sort, limit, offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


def get_todo(db: Session, todo_id: int, owner_id: int) -> Optional[Todo]:
    return todo_repo.get_by_id(db, todo_id, owner_id)


def update_todo(db: Session, todo_id: int, owner_id: int, title: str, description: Optional[str], is_done: bool) -> Optional[Todo]:
    return todo_repo.update(db, todo_id, owner_id, title, description, is_done)


def patch_todo(db: Session, todo_id: int, owner_id: int, **fields) -> Optional[Todo]:
    return todo_repo.patch(db, todo_id, owner_id, **fields)


def complete_todo(db: Session, todo_id: int, owner_id: int) -> Optional[Todo]:
    return todo_repo.patch(db, todo_id, owner_id, is_done=True)


def delete_todo(db: Session, todo_id: int, owner_id: int) -> bool:
    return todo_repo.delete(db, todo_id, owner_id)

