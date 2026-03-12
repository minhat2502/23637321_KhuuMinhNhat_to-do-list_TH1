from typing import Optional
from sqlalchemy.orm import Session
from db.models import Todo


def create(db: Session, title: str, description: Optional[str], is_done: bool, owner_id: int) -> Todo:
    todo = Todo(title=title, description=description, is_done=is_done, owner_id=owner_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_all(
    db: Session,
    owner_id: int,
    is_done: Optional[bool],
    q: Optional[str],
    sort: str,
    limit: int,
    offset: int,
) -> tuple[list[Todo], int]:
    query = db.query(Todo).filter(Todo.owner_id == owner_id)

    if is_done is not None:
        query = query.filter(Todo.is_done == is_done)

    if q:
        query = query.filter(Todo.title.ilike(f"%{q}%"))

    total = query.count()

    reverse = sort.startswith("-")
    sort_key = sort.lstrip("-")
    order_col = getattr(Todo, sort_key, Todo.created_at)
    query = query.order_by(order_col.desc() if reverse else order_col.asc())

    items = query.offset(offset).limit(limit).all()
    return items, total


def get_by_id(db: Session, todo_id: int, owner_id: int) -> Optional[Todo]:
    return db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == owner_id).first()


def update(db: Session, todo_id: int, owner_id: int, title: str, description: Optional[str], is_done: bool) -> Optional[Todo]:
    todo = get_by_id(db, todo_id, owner_id)
    if todo is None:
        return None
    todo.title = title
    todo.description = description
    todo.is_done = is_done
    db.commit()
    db.refresh(todo)
    return todo


def patch(db: Session, todo_id: int, owner_id: int, **fields) -> Optional[Todo]:
    todo = get_by_id(db, todo_id, owner_id)
    if todo is None:
        return None
    for key, value in fields.items():
        setattr(todo, key, value)
    db.commit()
    db.refresh(todo)
    return todo


def delete(db: Session, todo_id: int, owner_id: int) -> bool:
    todo = get_by_id(db, todo_id, owner_id)
    if todo is None:
        return False
    db.delete(todo)
    db.commit()
    return True


