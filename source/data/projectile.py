from typing import TypedDict

class ProjectileData(TypedDict):
    id: int
    id_str: str

PROJECTILE_DATA: list[ProjectileData] = [
    {"id": 0, "id_str": "projectile.INVALID"},
    {"id": 1, "id_str": "projectile.arrow"},
    {"id": 2, "id_str": "projectile.bullet"},
]