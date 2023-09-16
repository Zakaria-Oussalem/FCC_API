from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
import time
from sqlalchemy.orm import Session
import psycopg2
from psycopg2.extras import RealDictCursor
from schemas import UserCreate, UserOut, Post
import models
from database import engine, get_db
from utils import hash
from routers import posts, users, auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status": "Success"}
