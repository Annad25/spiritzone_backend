import requests

BASE_URL = "http://127.0.0.1:8000"

def test_all_functionalities():
    # Create a user
    user_data = {"name": "John Doe", "email": "john@example.com"}
    user_response = requests.post(f"{BASE_URL}/users/", json=user_data)
    user = user_response.json()
    print("Created User:", user)

    # Create a book
    book_data = {
        "title": "Sample Book",
        "author": "Jane Doe",
        "publication_year": 2022,
        "description": "A sample book description.",
    }
    book_response = requests.post(f"{BASE_URL}/books/", json=book_data)
    book = book_response.json()
    print("Created Book:", book)

    # Check out the book for the user
    checkout_data = {"user_name": "John Doe", "book_title": "Sample Book"}
    checkout_response = requests.post(f"{BASE_URL}/checkout/", json=checkout_data)
    checkout = checkout_response.json()
    print("Checked Out Book:", checkout)

    # Edit the book
    edit_data = {"author": "Updated Author", "publication_year": 2023, "description": "Updated description."}
    edit_response = requests.put(f"{BASE_URL}/books/edit/Sample Book", json=edit_data)
    edited_book = edit_response.json()
    print("Edited Book:", edited_book)

    # Delete the book
    delete_response = requests.delete(f"{BASE_URL}/books/delete/Sample Book")
    deleted_book = delete_response.json()
    print("Deleted Book:", deleted_book)

    # Get all checked-out books
    checked_out_books_response = requests.get(f"{BASE_URL}/checked-out-books/")
    checked_out_books = checked_out_books_response.json()
    print("Checked-out Books:", checked_out_books)

    # Get all books
    all_books_response = requests.get(f"{BASE_URL}/books/all")
    all_books = all_books_response.json()
    print("All Books:", all_books)

    # Get all users
    all_users_response = requests.get(f"{BASE_URL}/users/all")
    all_users = all_users_response.json()
    print("All Users:", all_users)

if __name__ == "__main__":
    test_all_functionalities()
