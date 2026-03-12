from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


def _validate_title(v: str) -> str:
    v = v.strip()
    if len(v) < 3:
        raise ValueError("title phải có ít nhất 3 ký tự")
    if len(v) > 100:
        raise ValueError("title không được vượt quá 100 ký tự")
    return v


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: bool = False

    @field_validator("title")
    @classmethod
    def title_must_be_valid(cls, v: str) -> str:
        return _validate_title(v)


class TodoUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: bool

    @field_validator("title")
    @classmethod
    def title_must_be_valid(cls, v: str) -> str:
        return _validate_title(v)


class TodoPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None

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
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaginatedTodos(BaseModel):
    items: list[TodoResponse]
    total: int
    limit: int
    offset: int
