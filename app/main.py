from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
import time
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
from schemas import UserCreate, UserOurt, Post
import models
from database import engine, get_db
from utils import hash
from routers import posts, users

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


app.include_router(posts.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": "Success"}
