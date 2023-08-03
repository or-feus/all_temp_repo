from pathlib import Path

from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.models import mongodb
from app.models.book import BookModel

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")
print(templates)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    book = BookModel(keyword="파이썬", publisher="BJPublic", price=1200, image="me.png")
    print(await mongodb.engine.save(book))
    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": "콜렉터 북북이"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, s: str):
    return templates.TemplateResponse(
        "./item.html",
        {"request": request, "title": "콜렉터 북북이"},
    )


@app.on_event("startup")
def on_app_start():
    print("hello server")

    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    print("good bye server")
    mongodb.close()
