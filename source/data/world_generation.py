from dataclasses import dataclass


@dataclass
class WorldGenerationData:
    id: int
    id_str: str


WORLD_GENERATION_DATA: tuple[WorldGenerationData, ...] = (
    WorldGenerationData(id=0, id_str="world_gen.INVALID"),
    WorldGenerationData(id=1, id_str="world_gen.default"),
)
