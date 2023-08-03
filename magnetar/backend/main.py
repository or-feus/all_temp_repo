from fastapi import FastAPI, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from db.config import logger
from db.connect import get_db, engine, Base
from db.model import Post
from db.schema.post import PostResponse, PostRequest

app = FastAPI(title="Ordinary Space", version="0.1")

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(payload: PostRequest, db: AsyncSession = Depends(get_db)):
    post = Post(**payload.dict())
    db.add(post)

    return await db.commit()


async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")
    await start_db()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")