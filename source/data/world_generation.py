from typing import TypedDict


class WorldGenerationData(TypedDict):
    id: int
    id_str: str


WORLD_GENERATION_DATA: list[WorldGenerationData] = [
    {"id": 0, "id_str": "world_gen.INVALID"},
    {"id": 1, "id_str": "world_gen.default"},
]
