from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class StoriesBase(BaseModel):
    user: str
    file: str

class StoriesCreate(StoriesBase):
    pass

class Stories(StoriesBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_date: datetime


class StoriesLikeBase(BaseModel):
    user: str
    story: int
    like: bool = True

class StoriesLikeCreate(StoriesLikeBase):
    pass

class StoriesLike(StoriesLikeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class StoriesCommentBase(BaseModel):
    user: str
    story: int
    text: str

class StoriesCommentCreate(StoriesCommentBase):
    pass

class StoriesCommentUpdate(BaseModel):
    text: Optional[str] = None

class StoriesComment(StoriesCommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int