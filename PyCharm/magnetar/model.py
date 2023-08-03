from typing import Optional

from pydantic import BaseModel


class Human(BaseModel):
    id: int
    age: Optional[int]
    name: str
    height: Optional[int]
    weight: Optional[int]