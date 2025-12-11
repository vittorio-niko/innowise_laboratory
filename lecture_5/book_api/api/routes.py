"""
Routes API module for books collection management.

- GET /books/ : get all books list
- POST /books/ : create a book
- GET /books/{book_id} : get book info
- PUT /books/{book_id} : update book info
- DELETE /books/{book_id} : delete book by id
"""


from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import models
import schemes
from database import get_db

router = APIRouter()

@router.post("/books/", response_model=schemes.BookResponse, summary="Add new book")
def create_book(book: schemes.BookCreate, db: Session = Depends(get_db)):
    """
    Add new book to collection.

    - **title**: Book title (mandatory)
    - **author**: Book author name (mandatory)
    - **year**: Publication year (mandatory)

    Pydantic schemes validate data.
    """
    db_book = models.Book(
        title=book.title,
        author=book.author,
        year=book.year
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


@router.get("/books/", response_model=List[schemes.BookResponse], summary="Get all books")
def get_books(
        skip: int = Query(0, ge=0, description="Entries skipped"),
        limit: int = Query(100, ge=1, le = 1000, description="Entries returned"),
        db: Session = Depends(get_db)
):
    """
    Get all books list with pagination.

    - **skip**: Entries to skip (for pagination purposes)
    - **limit**: Entries to return (max 1000)
    """
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books


@router.get("/books/search/", response_model=List[schemes.BookResponse], summary="Book search")
def search_books(
        title: Optional[str] = Query(None, description="Title search (partial match)"),
        author: Optional[str] = Query(None, description="Author name search (partial match)"),
        year: Optional[int] = Query(None, ge=0, le=9999, description="Publication year search"),
        db: Session = Depends(get_db)
):
    """
    Search by book title, author name and publication year (all combinations allowed).

    - **title**: Title search (partial match)
    - **author**: Author name search (partial match)
    - **year**: Publication year search
    """
    query = db.query(models.Book)

    if title:
        query = query.filter(models.Book.title.contains(title))
    if author:
        query = query.filter(models.Book.author.contains(author))
    if year:
        query = query.filter(year == models.Book.year)

    books = query.all()
    return books


@router.get("/books/{book_id}", response_model=schemes.BookResponse, summary="Get book by id")
def read_book(book_id: int, db: Session = Depends(get_db)):
    """
    Get book info by ID.

    - **book_id**: book id in DB
    """
    book = db.query(models.Book).filter(book_id == models.Book.id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book is not found")

    return book


@router.put("/books/{book_id}", response_model=schemes.BookResponse, summary="Update book info")
def update_book(
        book_id: int,
        book_update: schemes.BookUpdate,
        db: Session = Depends(get_db)
):
    """
    Update book info.
    All fields can be updated.
    All parameters are optional, validated by pydantic schemes.
    """
    # Book search
    db_book = db.query(models.Book).filter(book_id == models.Book.id).first()

    if db_book is None:
        raise HTTPException(status_code=404, detail="Book is not found")

    # Get new data to update
    update_data = book_update.model_dump(exclude_unset=True)

    # Update data
    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)

    return db_book


@router.delete("/books/{book_id}", summary="Delete book")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete book from collection.

    - **book_id**: book id to delete
    """
    # Book search
    book = db.query(models.Book).filter(book_id == models.Book.id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book is not found")

    # Delete book
    db.delete(book)
    db.commit()

    return {"message": f"Book with id {book_id} successfully deleted"}


@router.get("/", summary="API information")
def root():
    """Root endpoint with API information"""
    return {
        "message": "Book Collection API",
        "docs": "/docs",
        "version": "1.0.0",
        "endpoints": {
            "POST /books/": "Add new book",
            "GET /books/": "Get all books",
            "GET /books/{id}": "Get book by id",
            "PUT /books/{id}": "Update book info",
            "DELETE /books/{id}": "Delete book",
            "GET /books/search/": "Book search"
        }
    }
