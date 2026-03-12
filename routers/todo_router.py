from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from sqlalchemy.orm import Session
from schemas.todo import TodoCreate, TodoUpdate, TodoPatch, TodoResponse, PaginatedTodos
from services import todo_service
from db.session import get_db

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db)):
    return todo_service.create_todo(db, payload.title, payload.description, payload.is_done)


@router.get("", response_model=PaginatedTodos)
def list_todos(
    is_done: Optional[bool] = Query(default=None, description="Lọc theo trạng thái"),
    q: Optional[str] = Query(default=None, description="Tìm kiếm theo title"),
    sort: str = Query(default="created_at", description="created_at hoặc -created_at"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return todo_service.get_todos(db, is_done, q, sort, limit, offset)


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = todo_service.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db)):
    todo = todo_service.update_todo(db, todo_id, payload.title, payload.description, payload.is_done)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return todo


@router.patch("/{todo_id}", response_model=TodoResponse)
def patch_todo(todo_id: int, payload: TodoPatch, db: Session = Depends(get_db)):
    fields = payload.model_dump(exclude_unset=True)
    todo = todo_service.patch_todo(db, todo_id, **fields)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return todo


@router.post("/{todo_id}/complete", response_model=TodoResponse)
def complete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = todo_service.complete_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return todo


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    if not todo_service.delete_todo(db, todo_id):
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
