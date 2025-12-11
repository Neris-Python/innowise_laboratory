from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Book Collection API",
    description="A simple API to manage your book collection",
    version="1.0.0"
)


# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Book Collection API"}


# 1. POST /books/ - Add a new book
@app.post("/books/", response_model=schemas.Book, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    # Check if book already exists
    existing_book = db.query(models.Book).filter(
        models.Book.title == book.title,
        models.Book.author == book.author
    ).first()

    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    # Create new book
    db_book = models.Book(
        title=book.title,
        author=book.author,
        year=book.year
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


# 2. GET /books/ - Get all books (with optional pagination)
@app.get("/books/", response_model=List[schemas.Book])
def read_books(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(100, ge=1, le=100, description="Number of records to return"),
        db: Session = Depends(get_db)
):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books


# 3. GET /books/{book_id} - Get a specific book
@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


# 4. PUT /books/{book_id} - Update book details
@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(
        book_id: int,
        book_update: schemas.BookUpdate,
        db: Session = Depends(get_db)
):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Update only provided fields
    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


# 5. DELETE /books/{book_id} - Delete a book by ID
@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return


# 6. GET /books/search/ - Search books by title, author, or year
@app.get("/books/search/", response_model=List[schemas.Book])
def search_books(
        title: Optional[str] = Query(None, description="Search by title (partial match)"),
        author: Optional[str] = Query(None, description="Search by author (partial match)"),
        year: Optional[int] = Query(None, description="Search by exact year"),
        db: Session = Depends(get_db)
):
    query = db.query(models.Book)

    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    if year:
        query = query.filter(models.Book.year == year)

    books = query.all()
    return books


# 7. Additional endpoint: Count total books
@app.get("/books/count/")
def count_books(db: Session = Depends(get_db)):
    count = db.query(models.Book).count()
    return {"total_books": count}