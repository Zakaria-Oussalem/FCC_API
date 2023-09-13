from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOurt(BaseModel):
    id: int
    email: EmailStr

    class config:
        orm_mode = True
