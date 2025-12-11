from pydantic import BaseModel
from typing import Optional


# Base schema for Book
class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None


# Schema for creating a book
class BookCreate(BookBase):
    pass


# Schema for updating a book
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None


# Schema for returning a book
class Book(BookBase):
    id: int

    class Config:
        from_attributes = True