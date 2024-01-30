from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    """Pydantic model for creating a post."""
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    """Pydantic model for creating a user."""
    username: str

class UserResponse(BaseModel):
    """Pydantic model for user response."""
    id: int
    username: str

class PostResponse(BaseModel):
    """Pydantic model for post response."""
    id: int
    title: str
    content: str
    user_id: int

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/posts/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    """Endpoint to create a new post."""
    db_post = models.Post(**post.__dict__)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get('/posts/{post_id}', response_model=PostResponse, status_code=status.HTTP_200_OK)
async def read_posts(post_id: int, db: db_dependency):
    """Endpoint to get a specific post by ID."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get('/posts/', response_model=List[PostResponse])
async def read_all_posts(db: db_dependency):
    """Endpoint to get all posts."""
    posts = db.query(models.Post).all()
    return posts

@app.post('/users/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    """Endpoint to create a new user."""
    db_user = models.User(**user.__dict__)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get('/users/{user_id}', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    """Endpoint to get a specific user by ID."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get('/users/', response_model=List[UserResponse])
async def get_all_users(db: db_dependency):
    """Endpoint to get all users."""
    users = db.query(models.User).all()
    return users

@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency):
    """Endpoint to delete a post by ID."""
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    db.delete(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
