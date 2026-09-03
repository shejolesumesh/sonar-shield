from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorResponse(BaseModel):
    detail: str


class ListResponse(BaseModel, Generic[T]):
    total: int
    items: list[T]


class MessageResponse(BaseModel):
    message: str
    data: dict | None = None
