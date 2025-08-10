from dataclasses import dataclass

from commons import BLOCK_SIZE, TileMaskType
from pygame import Surface, image, transform


@dataclass
class WallData:
    id: int
    id_str: str
    name: str
    mask_type: TileMaskType
    mask_merge_ids: tuple[str, ...]
    item_id_str: str
    place_sound: str
    hit_sound: str
    surface: Surface


WALL_DATA: tuple[WallData, ...] = (
    WallData(
        id=0,
        id_str="wall.INVALID",
        name="INVALID",
        mask_type=TileMaskType.NONE,
        mask_merge_ids=(),
        item_id_str="item.INVALID",
        place_sound="sound.dig",
        hit_sound="sound.dig",
        surface=Surface((0, 0)),
    ),
    WallData(
        id=1,
        id_str="wall.none",
        name="None",
        mask_type=TileMaskType.NOISY,
        mask_merge_ids=(),
        item_id_str="item.INVALID",
        place_sound="sound.dig",
        hit_sound="sound.dig",
        surface=Surface((0, 0)),
    ),
    WallData(
        id=2,
        id_str="wall.dirt",
        name="Dirt Wall",
        mask_type=TileMaskType.NOISY,
        mask_merge_ids=(
            "wall.dirt",
            "wall.ice",
            "wall.hardened_sand",
            "wall.sandstone",
            "wall.snow",
            "wall.stone",
            "wall.wood",
        ),
        item_id_str="item.dirt_wall",
        place_sound="sound.dig",
        hit_sound="sound.dig",
        surface=transform.scale(
            image.load("assets/images/walls/dirt.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    WallData(
        id=3,
        id_str="wall.stone",
        name="Stone",
        mask_type=TileMaskType.NOISY,
        mask_merge_ids=("wall.dirt", "wall.snow", "wall.wood"),
        item_id_str="item.stone_wall",
        place_sound="sound.dig",
        hit_sound="sound.dig",
        surface=transform.scale(
            image.load("assets/images/walls/stone.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    WallData(
        id=4,
        id_str="wall.ice",
        name="Ice",
        mask_type=TileMaskType.NOISY,
        mask_merge_ids=("wall.snow",),
        item_id_str="item.ice_wall",
        place_sound="sound.dig",
        hit_sound="sound.dig",
        surface=transform.scale(
            image.load("assets/images/walls/ice.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    WallData(
        id=5,
        id_str="wall.snow",
        name="Snow",
        mask_type=TileMaskType.NOISY,
        mask_merge_ids=(
            "wall.dirt",
            "wall.ice",
            "wall.sandstone",
            "wall.snow",
            "wall.stone",
            "wall.wood",
        ),
        item_id_str="item.snow_wall",
        place_sound="sound.dig",
        hit_sound="sound.dig",
        surface=transform.scale(
            image.load("assets/images/walls/snow.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    WallData(
        id=6,
        id_str="wall.sandstone",
        name="Sandstone",
        mask_type=TileMaskType.NOISY,
        mask_merge_ids=("wall.dirt", "wall.hardened_sand", "wall.snow"),
        item_id_str="item.sandstone_wall",
        place_sound="sound.dig",
        hit_sound="sound.dig",
        surface=transform.scale(
            image.load("assets/images/walls/sandstone.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    WallData(
        id=7,
        id_str="wall.hardened_sand",
        name="Sand",
        mask_type=TileMaskType.NOISY,
        mask_merge_ids=(
            "wall.dirt",
            "wall.sandstone",
            "wall.snow",
            "wall.stone",
            "wall.wood",
        ),
        item_id_str="item.hardened_sand_wall",
        place_sound="sound.dig",
        hit_sound="sound.dig",
        surface=transform.scale(
            image.load("assets/images/walls/hardened_sand.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    WallData(
        id=8,
        id_str="wall.wood",
        name="Wood",
        mask_type=TileMaskType.NOISY,
        mask_merge_ids=(
            "wall.dirt",
            "wall.hardened_sand",
            "wall.snow",
            "wall.stone",
        ),
        item_id_str="item.wood_wall",
        place_sound="sound.dig",
        hit_sound="sound.dig",
        surface=transform.scale(
            image.load("assets/images/walls/wood.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
)
