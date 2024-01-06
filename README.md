# spiritzone_backend
# FastAPI Library Management System

This is a simple FastAPI project for a library management system. It includes functionality to manage books, users, and book checkouts.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Annad25/spiritzone_backend.git
   cd spiritzone_backend
Install dependencies:

pip install -r requirements.txt
Run the FastAPI application:

uvicorn main:app --reload
The API will be available at http://127.0.0.1:8000.

API Endpoints
Create a New Book
URL: POST /books/
Request Body:
```
{
  "title": "Example Book",
  "author": "John Doe",
  "publication_year": 2022,
  "description": "A sample book description."
}
```
Response:
```
{
  "title": "Example Book",
  "author": "John Doe",
  "publication_year": 2022,
  "description": "A sample book description."
}
```
Create a New User
URL: POST /users/
Request Body:
```
{
  "name": "John Doe",
  "email": "john@example.com"
}
```
Response:
```
{
  "name": "John Doe",
  "email": "john@example.com"
}
```
Checkout a Book for a User
URL: POST /checkout/
Request Body:
```
{
  "user_name": "John Doe",
  "book_title": "Example Book"
}
```
Response:
```
{
  "user_id": 1,
  "book_id": 1,
  "checked_out_date": "2022-01-01T12:00:00"
}
```
Edit an Existing Book
URL: PUT /books/edit/{book_title}
Path Parameter: {book_title} is the title of the book to be edited.
Request Body:
```
{
  "author": "Updated Author",
  "publication_year": 2023,
  "description": "Updated description."
}
Response:
```
{
  "title": "Example Book",
  "author": "Updated Author",
  "publication_year": 2023,
  "description": "Updated description."
}
Delete an Existing Book
URL: DELETE /books/delete/{book_title}
Path Parameter: {book_title} is the title of the book to be deleted.
Response:
```
{
  "title": "Example Book",
  "author": "Updated Author",
  "publication_year": 2023,
  "description": "Updated description."
}
```
Get All Checked-out Books
URL: GET /checked-out-books/
Response:
```
[
  {
    "user_id": 1,
    "book_id": 1,
    "checked_out_date": "2022-01-01T12:00:00"
  },
  {
    "user_id": 2,
    "book_id": 3,
    "checked_out_date": "2022-01-02T12:00:00"
  }
]
```
Get All Books
URL: GET /books/all
Response:
```
[
  {
    "title": "Example Book",
    "author": "Updated Author",
    "publication_year": 2023,
    "description": "Updated description."
  },
  {
    "title": "Another Book",
    "author": "Jane Doe",
    "publication_year": 2021,
    "description": "A different book."
  }
]
```
Get All Users
URL: GET /users/all
Response:
```
[
  {
    "name": "John Doe",
    "email": "john@example.com"
  },
  {
    "name": "Jane Doe",
    "email": "jane@example.com"
  }
]
```
```
