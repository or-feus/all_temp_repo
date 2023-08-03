from datetime import datetime

from pydantic import BaseModel, Field


class PostRequest(BaseModel):

    author_id: int = Field(title="작성자의 이름")
    title: str = Field(title="")
    current_time: datetime = Field(title="", default=datetime.now())
    content: str = Field(title="")
    status: str = Field(title="")
    like_count: int = Field(title="", default=0)
    comment_count: int = Field(title="", default=0)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "author_id": "orfeus",
                "title": "Ordinary Title",
                "content": "Ordinary Graffiti",
                "status": "Ordinary Cool",
                "like_count": 0,
                "comment_count": 0
            }
        }


class PostResponse(BaseModel):
    title: str = Field(title="")
    current_time: datetime = Field(title="", default=datetime.now())
    content: str = Field(title="")
    status: str = Field(title="")
    like_count: int = Field(title="", default=0)
    comment_count: str = Field(title="", default=0)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Ordinary Title",
                "content": "Ordinary Graffiti",
                "status": "Ordinary Cool",
                "like_count": 0,
                "comment_count": 0
            }
        }
