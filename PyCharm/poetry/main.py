import uuid
from typing import Optional, List

from fastapi import FastAPI, Depends
from fastapi.openapi.models import Response
from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from starlette.status import HTTP_204_NO_CONTENT

from database import engine, get_db

app = FastAPI()

Base = declarative_base()
Base.metadata.create_all(bind=engine)


class RequestMemo(BaseModel):
    title: str
    content: Optional[str] = None
    is_favorite: Optional[bool] = False


class ResponseMemo(BaseModel):
    id: str
    title: str
    content: Optional[str] = None
    is_favorite = bool

    class Config:
        orm_mode = True


@app.get('/memos', response_model=List[ResponseMemo])
async def get_memos(db: Session = Depends(get_db)):
    memos = db.query(Memo).all()
    return memos


@app.post("/memos", response_model=ResponseMemo)
async def register_memo(req: RequestMemo, db: Session = Depends(get_db)):
    memo = Memo(**req.dict())

    db.add(memo)

    db.commit()

    return memo


class Memo(Base):
    __tablename__ = "memos"

    id = Column(String(120), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(80), default='No title', nullable=False, index=True)
    content = Column(Text, nullable=True)
    is_favorite = Column(Boolean, nullable=False, default=False)


class Item(BaseModel):
    user_id: str = Field(title="사용자가 사용할 ID")
    password: str = Field(title="사용자가 사용할 Password")


class PatchItem(BaseModel):
    user_id: Optional[str] = Field(title="사용자가 사용할 ID")
    password: Optional[str] = Field(title="사용자가 사용할 Password")


class ResponseItem(Item):
    success: bool = Field(title="처리 여부/결과")


@app.get("/{name}", name="사용자 ID 생성", description="사용자 이름을 받고 ID를 생성하는 API입니다.")
async def generate_id_for_name(name: str):
    return JSONResponse({
        "id": str(uuid.uuid4()),
        "name": name
    })


@app.post("/register", response_model=ResponseItem)
async def register_item(item: Item):
    global dicted_item
    dicted_item = dict(item)
    dicted_item['success'] = True

    return JSONResponse(dicted_item)


@app.put("/update")
async def update_item(item: Item):
    dicted_item = {k: v for k, v in dict(item).items()}
    dicted_item['success'] = True

    return JSONResponse(dicted_item)


@app.patch("/update")
async def update_item_sub(item: PatchItem):
    dicted_item = {}
    for k, v in dict(item).items():
        dicted_item[k] = v
    dicted_item['success'] = True

    return JSONResponse(dicted_item)


@app.delete("/delete")
async def delete_item():
    dicted_item = None
    return Response(status_code=HTTP_204_NO_CONTENT)
