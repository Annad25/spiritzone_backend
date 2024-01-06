import unittest
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_create_book():
    book_data = {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "publication_year": 1951,
        "description": "A story about teenage angst and rebellion."
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 201
    assert response.json() == book_data
    print (response.json())

def test_update_book():
    book_id = 1
    book_update_data = {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publication_year": 1960,
        "description": "A story about racism and injustice in the American South."
    }
    response = client.put(f"/books/{book_id}", json=book_update_data)
    assert response.status_code == 200
    assert response.json() == book_update_data
    print (response.json)
def test_delete_book():
    book_id = 1
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}
    print(response.json)
def test_checkout_book():
    checkout_info = {
        "user_id": 1,
        "book_id": 1
    }
    response = client.post("/checkout/", json=checkout_info)
    assert response.status_code == 200
    print(response.status_code)
def test_get_checked_out_users():
    response = client.get("/checked-out-users/")
    assert response.status_code == 200
    print(response.status_code)
