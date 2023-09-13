from datetime import datetime
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from random import randrange
import time
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import engine, get_db
from utils import hash

models.Base.metadata.create_all(bind=engine)


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True


app = FastAPI()


# connecting to postgre database
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapidb",
            user="fastapi_user",
            password="255241",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection succesful")
        break
    except Exception as error:
        print("connection to database failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": "Success"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts  """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
        """ INSERT INTO posts (title, content, published) 
    VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.publish),
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"new_post": new_post}


# @app.get('/posts/latest')
# def get_latest_post():
#     return {"post_detail": my_posts[-1]}

# @app.get("/posts/{id}")
# def get_post(id: int):
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
#         detail = f"post with id: {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": f"post with id: {id} was not found"}
#     return {"post_detail": post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """ UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.publish, str(id)),
    )

    updated_post = cursor.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return {"data": updated_post}


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOurt(BaseModel):
    id: int
    email: EmailStr

    class config:
        orm_mode = True


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOurt)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashedPassword = hash(user.password)
    user.password = hashedPassword

    # Add to DB
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
