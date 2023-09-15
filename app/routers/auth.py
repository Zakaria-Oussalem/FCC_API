from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
import models
from schemas import UserLogIn
from database import get_db
from utils import hash, verify

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials: UserLogIn, db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    # Check if password is correct
    print(user.password)
    print(hash(user_credentials.password))
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    # Create a token
    return {"token": "example token"}
