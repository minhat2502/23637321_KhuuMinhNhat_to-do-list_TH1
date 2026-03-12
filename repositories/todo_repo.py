from typing import Optional
from datetime import date, datetime, timezone
from sqlalchemy.orm import Session
from db.models import Todo, Tag


def _sync_tags(db: Session, todo: Todo, tag_names: list[str]) -> None:
    tags = []
    for name in tag_names:
        name = name.strip().lower()
        tag = db.query(Tag).filter(Tag.name == name).first()
        if tag is None:
            tag = Tag(name=name)
            db.add(tag)
        tags.append(tag)
    todo.tags = tags


def create(db: Session, title: str, description: Optional[str], is_done: bool,
           owner_id: int, due_date: Optional[date] = None, tags: list[str] = []) -> Todo:
    todo = Todo(title=title, description=description, is_done=is_done,
                owner_id=owner_id, due_date=due_date)
    db.add(todo)
    db.flush()
    _sync_tags(db, todo, tags)
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
    query = db.query(Todo).filter(Todo.owner_id == owner_id, Todo.deleted_at == None)

    if is_done is not None:
        query = query.filter(Todo.is_done == is_done)
    if q:
        query = query.filter(Todo.title.ilike(f"%{q}%"))

    total = query.count()
    reverse = sort.startswith("-")
    sort_key = sort.lstrip("-")
    order_col = getattr(Todo, sort_key, Todo.created_at)
    query = query.order_by(order_col.desc() if reverse else order_col.asc())
    return query.offset(offset).limit(limit).all(), total


def get_overdue(db: Session, owner_id: int) -> list[Todo]:
    today = date.today()
    return (
        db.query(Todo)
        .filter(Todo.owner_id == owner_id, Todo.deleted_at == None,
                Todo.is_done == False, Todo.due_date != None, Todo.due_date < today)
        .order_by(Todo.due_date.asc())
        .all()
    )


def get_today(db: Session, owner_id: int) -> list[Todo]:
    today = date.today()
    return (
        db.query(Todo)
        .filter(Todo.owner_id == owner_id, Todo.deleted_at == None,
                Todo.is_done == False, Todo.due_date == today)
        .order_by(Todo.created_at.asc())
        .all()
    )


def get_by_id(db: Session, todo_id: int, owner_id: int) -> Optional[Todo]:
    return db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == owner_id,
                                  Todo.deleted_at == None).first()


def get_deleted(db: Session, owner_id: int) -> list[Todo]:
    return (
        db.query(Todo)
        .filter(Todo.owner_id == owner_id, Todo.deleted_at != None)
        .order_by(Todo.deleted_at.desc())
        .all()
    )


def update(db: Session, todo_id: int, owner_id: int, title: str, description: Optional[str],
           is_done: bool, due_date: Optional[date] = None, tags: list[str] = []) -> Optional[Todo]:
    todo = get_by_id(db, todo_id, owner_id)
    if todo is None:
        return None
    todo.title = title
    todo.description = description
    todo.is_done = is_done
    todo.due_date = due_date
    _sync_tags(db, todo, tags)
    db.commit()
    db.refresh(todo)
    return todo


def patch(db: Session, todo_id: int, owner_id: int, **fields) -> Optional[Todo]:
    todo = get_by_id(db, todo_id, owner_id)
    if todo is None:
        return None
    tags = fields.pop("tags", None)
    for key, value in fields.items():
        setattr(todo, key, value)
    if tags is not None:
        _sync_tags(db, todo, tags)
    db.commit()
    db.refresh(todo)
    return todo


def delete(db: Session, todo_id: int, owner_id: int) -> bool:
    """Soft delete: đánh dấu deleted_at thay vì xóa thật."""
    todo = get_by_id(db, todo_id, owner_id)
    if todo is None:
        return False
    todo.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return True


def restore(db: Session, todo_id: int, owner_id: int) -> Optional[Todo]:
    """Khôi phục todo đã bị soft delete."""
    todo = db.query(Todo).filter(
        Todo.id == todo_id, Todo.owner_id == owner_id, Todo.deleted_at != None
    ).first()
    if todo is None:
        return None
    todo.deleted_at = None
    db.commit()
    db.refresh(todo)
    return todo


