from typing import Callable, TypedDict


class Query(TypedDict):
    sql: Callable[..., str]
    item_type: str
    fields: list[str]