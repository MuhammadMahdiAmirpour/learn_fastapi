import logging
from datetime import datetime

from pydantic import BaseModel, EmailStr
from pydantic.v1 import validator


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    """
    Represents a new post creation with title, content, and published status.
    """

    def __init__(self, title: str, content: str, published: bool = True):
        super().__init__(title=title, content=content, published=published)
        logging.info(f'Post object created with title: {self.title}')
        logging.info(f'Post object created with content: {self.content}')
        logging.info(f'Post object created with published status: {self.published}')

    @validator("title")
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title must not be empty')
        return v

    @validator('content')
    def content_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Content must not be empty')
        return v


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
