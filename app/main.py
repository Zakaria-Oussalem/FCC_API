from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
import time
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
from schemas import UserCreate, UserOurt, Post
import models
from database import engine, get_db
from utils import hash

models.Base.metadata.create_all(bind=engine)


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


@app.get("/users/{id}", response_model=UserOurt)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )
    return user
