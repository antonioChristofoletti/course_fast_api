from fastapi import Body, FastAPI

app = FastAPI()


BOOKS = [
    {"title": "title one", "author": "Author one", "category": "Science"},
    {"title": "title two", "author": "Author two", "category": "Science"},
    {"title": "title three", "author": "Author three", "category": "History"},
    {"title": "title four", "author": "Author four", "category": "Math"},
]


@app.get("/books")
def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book


@app.get("/books/")
def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/")
def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)

    return books_to_return


@app.get("/books/search_by_author/{book_author_path}/")
def read_author_or_category_by_query(book_author_path: str, book_author_query):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author_path.casefold()
            or book.get("author").casefold() == book_author_query.casefold()
        ):
            books_to_return.append(book)

    return books_to_return


@app.post("/books/create_book")
def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == update_book.get("title").casefold():
            BOOKS[i] = update_book


@app.delete("/books/delete_book/{book_title}")
def delete_book(delete_book_title):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == delete_book_title:
            BOOKS.pop(delete_book)
