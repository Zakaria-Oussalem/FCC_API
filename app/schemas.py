from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr

    class config:
        orm_mode = True


class UserLogIn(BaseModel):
    email: EmailStr
    password: str


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    owner_id: int
    owner: UserOut


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class TokenData(BaseModel):
    id: str


class Token(BaseModel):
    access_token: str
    token_type: str
