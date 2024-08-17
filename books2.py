import datetime
from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


class Book():
    id: int
    title: str
    author: str
    description: str
    rating: str
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None, title="Id is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=0, lt=datetime.datetime.now().year)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "a new book",
                "author": "codingwithroby",
                "description": "a new description of a book",
                "rating": 5,
                "published_date": 2012
            }
        }

BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book", 5, 2012),
    Book(2, "Be fast with FastAPI", "codingwithroby", "A great book", 5, 2013),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book", 5, 2014),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2015),
    Book(5, "HP2 Science Pro", "Author 2", "Book Description", 3, 2016),
    Book(6, "HP3", "Author 3", "Book Description", 1, 2017)
]


@app.get("/books", status_code=status.HTTP_200_OK)
def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
    raise HTTPException(status_code=404, detail="Item not found")
        
@app.get("/books/", status_code=status.HTTP_200_OK)
def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
def update_book(book_request: BookRequest):
    
    book_changed = False
    
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_request.id:
            BOOKS[i] = book_request
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/books/delete/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(gt=0)):
    book_changed = False

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/books/by_published_date/{published_date}", status_code=status.HTTP_200_OK)
def get_by_published_date(published_date: int = Path(gt=1999, lt=2031)):
    return [book for book in BOOKS if book.published_date == published_date]


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1

    return book