from typing import TypedDict

class AIData(TypedDict):
    id: int
    id_str: str

AI_DATA: list[AIData] = [
    {"id": 0, "id_str": "loot.INVALID"},
    {"id": 1, "id_str": "loot.slime"},
    {"id": 2, "id_str": "loot.bunny"},
]