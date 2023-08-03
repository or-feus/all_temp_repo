import asyncio

from model import Human

human_test = {
    "id": 1,
    "age": 29,
    "name": "feus",
    "height": 180,
    "weight": 70
}


def test_human_model_check():
    instance = Human(
        id=1,
        age=29,
        name="feus",
        height=180,
        weight=70
    )

    assert human_test["id"] == instance.id
    assert human_test["age"] == instance.age
    assert human_test["name"] == instance.name
    assert human_test["height"] == instance.height
    assert human_test["weight"] == instance.weight


loop = asyncio.get_event_loop()
