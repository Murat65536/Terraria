from dataclasses import dataclass


@dataclass
class ProjectileData:
    id: int
    id_str: str


PROJECTILE_DATA: tuple[ProjectileData, ...] = (
    ProjectileData(id=0, id_str="projectile.INVALID"),
    ProjectileData(id=1, id_str="projectile.arrow"),
    ProjectileData(id=2, id_str="projectile.bullet"),
)
