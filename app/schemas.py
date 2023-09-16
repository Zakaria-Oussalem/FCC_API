from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOurt(BaseModel):
    id: int
    email: EmailStr

    class config:
        orm_mode = True


class UserLogIn(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    id: str


class Token(BaseModel):
    access_token: str
    token_type: str
