from pydantic import BaseModel, Field


class AuthorRequest(BaseModel):
    name: str = Field(title="작성자 이름")
    avatar: str = Field(title="")
    description: str = Field(title="작성자 설명")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Feus",
                "avatar": "zz",
                "description": "Ordinary Space"
            }
        }


class AuthorResponse(BaseModel):
    id: int = Field(title="작성자 ID")
    name: str = Field(title="작성자 이름")
    avatar: str = Field(title="")
    description: str = Field(title="작성자 설명")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1423,
                "name": "Feus",
                "avatar": "zz",
                "description": "Ordinary Space"
            }
        }

