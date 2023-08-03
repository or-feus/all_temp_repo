from fastapi import FastAPI

from routes.events import event_router
from routes.users import user_router
from database.connection import conn, Settings

app = FastAPI()
settings = Settings()
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.on_event("startup")
async def on_startup():
    await settings.initialize_database()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
