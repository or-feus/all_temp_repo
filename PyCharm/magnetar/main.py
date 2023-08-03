from typing import Any, List

from fastapi import FastAPI, Header, Path, Query

from model import Human

app = FastAPI()

human_dict: List[Human] = list()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: Any = Path(...)):
    return {"message": f"Hello {name}"}


@app.get("/feus")
async def header_test(head=Header(default=None)) -> dict:
    return {"success": head}


@app.get("/query")
async def query_test(zz: str = Query(default=None)):
    return {"query": zz}


@app.post("/register")
async def human_register(human: Human):
    human_dict.append(human)
    print(human_dict)
    return {"human": human_dict[human.id]}


@app.get("/register/{human_id}")
async def get_human_data(human_id: int):
    print(human_dict[human_id])
    return human_dict[human_id]
