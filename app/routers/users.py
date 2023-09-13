from fastapi import Body, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from schemas import UserCreate, UserOurt, Post
import models
from database import get_db
from utils import hash

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOurt)
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


@router.get("/users/{id}", response_model=UserOurt)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )
    return user
