from pydantic import BaseModel, field_validator
from datetime import datetime, date
from typing import Optional


def _validate_title(v: str) -> str:
    v = v.strip()
    if len(v) < 3:
        raise ValueError("title phải có ít nhất 3 ký tự")
    if len(v) > 100:
        raise ValueError("title không được vượt quá 100 ký tự")
    return v


class TagResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: bool = False
    due_date: Optional[date] = None
    tags: list[str] = []

    @field_validator("title")
    @classmethod
    def title_must_be_valid(cls, v: str) -> str:
        return _validate_title(v)


class TodoUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: bool
    due_date: Optional[date] = None
    tags: list[str] = []

    @field_validator("title")
    @classmethod
    def title_must_be_valid(cls, v: str) -> str:
        return _validate_title(v)


class TodoPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None

    @field_validator("title")
    @classmethod
    def title_must_be_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return _validate_title(v)
        return v


class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_done: bool
    due_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    tags: list[TagResponse] = []

    model_config = {"from_attributes": True}


class PaginatedTodos(BaseModel):
    items: list[TodoResponse]
    total: int
    limit: int
    offset: int
