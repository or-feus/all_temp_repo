from typing import List

import strawberry


@strawberry.type
class TodoType:
    name: str
    done: bool


todos = [
    TodoType(name="Todo #1", done=False),
    TodoType(name="Todo #2", done=False),
    TodoType(name="Todo #3", done=True),
]


@strawberry.type
class Query:
    @strawberry.field
    def todos(self, info, done: bool = None) -> List[TodoType]:
        if done is not None:
            return filter(lambda todo: todo.done == done, todos)
        else:
            return todos


schema = strawberry.Schema(query=Query)
