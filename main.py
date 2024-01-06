# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, declarative_base, relationship
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SQLAlchemy Models
Base = declarative_base()

class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)

    books = relationship("Book", secondary="user_books")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    publication_year = Column(Integer)
    description = Column(String)

class UserBook(Base):
    __tablename__ = "user_books"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    checked_out_date = Column(DateTime, default=datetime.utcnow)

class UserBookResponse(OurBaseModel):
    user_id: int
    book_id: int
    checked_out_date: datetime

# Database initialization
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Pydantic models for request/response bodies
class BookBase(OurBaseModel):
    title: str
    author: str
    publication_year: int
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class UserBase(OurBaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserCheckout(OurBaseModel):
    user_name: str
    book_title: str


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create a new book
@app.post("/books/", response_model=BookBase)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    try:
        db_book = Book(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    # Convert the SQLAlchemy model to a dictionary
    response_model = BookBase(**db_book.__dict__)
    return response_model

# Function to create a new user
@app.post("/users/", response_model=UserBase)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Function to check out a book for a user based on names and update using IDs
@app.post("/checkout/", response_model=UserBookResponse)
def checkout_book(checkout: UserCheckout, db: Session = Depends(get_db)):
    user_name = checkout.user_name
    book_title = checkout.book_title

    # Get user and book using names
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    book = db.query(Book).filter(Book.title == book_title).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if the book is already checked out by the user
    existing_checkout = db.query(UserBook).filter(
        UserBook.user_id == user.id, UserBook.book_id == book.id
    ).first()

    if existing_checkout:
        raise HTTPException(
            status_code=400,
            detail="This book is already checked out by the user.",
        )

    # Create a new UserBook entry
    user_book = UserBook(user_id=user.id, book_id=book.id, checked_out_date=datetime.utcnow())
    db.add(user_book)
    db.commit()
    db.refresh(user_book)

    response_model = UserBookResponse(
        user_id=user_book.user_id,
        book_id=user_book.book_id,
        checked_out_date=user_book.checked_out_date,
    )
    return response_model

# Function to edit an existing book by title
@app.put("/books/edit/{book_title}", response_model=BookBase)
def edit_book(book_title: str, book_update: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.title == book_title).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    for field, value in book_update.dict().items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)

    response_model = BookBase(
        title=db_book.title,
        author=db_book.author,
        publication_year=db_book.publication_year,
        description=db_book.description,
    )
    return response_model

# Function to delete an existing book by title
@app.delete("/books/delete/{book_title}", response_model=BookBase)
def delete_book(book_title: str, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.title == book_title).first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()

    response_model = BookBase(
        title=db_book.title,
        author=db_book.author,
        publication_year=db_book.publication_year,
        description=db_book.description,
    )
    return response_model


# Function to get all checked-out books by users
@app.get("/checked-out-books/", response_model=List[UserBookResponse])
def get_checked_out_books(db: Session = Depends(get_db)):
    checked_out_books = db.query(UserBook).all()

    # Convert the UserBook objects to UserBookResponse models
    response_models = [
        UserBookResponse(
            user_id=user_book.user_id,
            book_id=user_book.book_id,
            checked_out_date=user_book.checked_out_date,
        )
        for user_book in checked_out_books
    ]

    return response_models

# Function to get all books
@app.get("/books/all", response_model=List[BookBase])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

# Function to get all users
@app.get("/users/all", response_model=List[UserBase])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

