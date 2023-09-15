from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True


class PostCreate(BaseModel):
    title: str
    content: str
    publish: bool = True
    id: int


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
