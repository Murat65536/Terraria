from dataclasses import dataclass

from commons import BLOCK_SIZE, TileMaskType, TileStrengthType, TileTag
from pygame import Surface, image, transform


@dataclass
class TileData:
    id: int
    id_str: str
    name: str
    strength: float
    strength_type: TileStrengthType
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    light_reduction: int
    light_emission: int
    tags: list[TileTag]
    item_id_str: str
    item_count_range: tuple[int, int]
    place_sound: str
    hit_sound: str
    image: Surface


@dataclass
class DamagingTileData:
    id: int
    id_str: str
    name: str
    strength: float
    strength_type: TileStrengthType
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    light_reduction: int
    light_emission: int
    tags: list[TileTag]
    item_id_str: str
    item_count_range: tuple[int, int]
    place_sound: str
    hit_sound: str
    tile_damage: int
    tile_damage_name: str
    image: Surface


@dataclass
class MultitileData:
    id: int
    id_str: str
    name: str
    strength: float
    strength_type: TileStrengthType
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    light_reduction: int
    light_emission: int
    tags: list[TileTag]
    item_id_str: str
    item_count_range: tuple[int, int]
    multitile_dimensions: tuple[int, int]
    multitile_required_solids: list[tuple[int, int]]
    place_sound: str
    hit_sound: str
    image: Surface


@dataclass
class DoorTileData:
    id: int
    id_str: str
    name: str
    strength: float
    strength_type: TileStrengthType
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    light_reduction: int
    light_emission: int
    tags: list[TileTag]
    item_id_str: str
    item_count_range: tuple[int, int]
    cycle_facing_left_tile_id_str: str
    cycle_facing_left_tile_offset: list[int]
    cycle_facing_left_sound: str
    cycle_facing_right_tile_id_str: str
    cycle_facing_right_tile_offset: list[int]
    cycle_facing_right_sound: str
    multitile_dimensions: tuple[int, int]
    multitile_required_solids: list[tuple[int, int]]
    place_sound: str
    hit_sound: str
    image: Surface


@dataclass
class LootMultitileData:
    id: int
    id_str: str
    name: str
    strength: float
    strength_type: TileStrengthType
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    light_reduction: int
    light_emission: int
    tags: list[TileTag]
    item_id_str: str
    item_count_range: tuple[int, int]
    loot_group_id_str: str
    multitile_dimensions: tuple[int, int]
    multitile_required_solids: list[tuple[int, int]]
    place_sound: str
    hit_sound: str
    image: Surface


@dataclass
class LootTileData:
    id: int
    id_str: str
    name: str
    strength: float
    strength_type: TileStrengthType
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    light_reduction: int
    light_emission: int
    tags: list[TileTag]
    item_id_str: str
    item_count_range: tuple[int, int]
    loot_group_id_str: str
    place_sound: str
    hit_sound: str
    image: Surface


TILE_DATA: tuple[TileData | DamagingTileData | MultitileData | DoorTileData | LootTileData | LootMultitileData, ...] = (
    TileData(
        id=0,
        id_str="tile.UNNAMED",
        name="UNNAMED",
        strength=0,
        strength_type=TileStrengthType.PICKAXE,
        mask_type=TileMaskType.NOISY,
        mask_merge_ids=[],
        light_reduction=0,
        light_emission=0,
        tags=[],
        item_id_str="item.INVALID",
        item_count_range=(1, 1),
        place_sound="",
        hit_sound="",
        image=Surface((0, 0)),
    ),
    TileData(
        id=1,
        id_str="tile.none",
        name="None",
        strength=0,
        strength_type=TileStrengthType.PICKAXE,
        mask_type=TileMaskType.NONE,
        mask_merge_ids=[],
        light_reduction=10,
        light_emission=0,
        tags=[TileTag.NO_COLLIDE, TileTag.NO_DRAW],
        item_id_str="item.INVALID",
        item_count_range=(0, 0),
        place_sound="",
        hit_sound="",
        image=Surface((0, 0)),
    ),
    TileData(
        id= 2,
        id_str= "tile.dirt",
        name= "Dirt",
        strength= 1,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NOISY,
        mask_merge_ids= [
        "tile.grass",
        "tile.sand",
        "tile.sandstone",
        "tile.snow",
        "tile.stone",
        "tile.trunk",
        "tile.wood",
        ],
        light_reduction= 25,
        light_emission= 0,
        tags= [],
        item_id_str= "item.dirt_block",
        item_count_range= (1, 1),
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/dirt.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 3,
        id_str= "tile.stone",
        name= "Stone",
        strength= 3,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NOISY,
        mask_merge_ids= ["tile.dirt", "tile.wood"],
        light_reduction= 25,
        light_emission= 0,
        tags= [],
        item_id_str= "item.stone_block",
        item_count_range= (1, 1),
        place_sound= "sound.tink",
        hit_sound= "sound.tink",
        image= transform.scale(
        image.load("assets/images/tiles/stone.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 4,
        id_str= "tile.grass",
        name= "Grass",
        strength= 0.5,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NOISY,
        mask_merge_ids= ["tile.dirt", "tile.trunk"],
        light_reduction= 25,
        light_emission= 0,
        tags= [],
        item_id_str= "item.dirt_block",
        item_count_range= (1, 1),
        place_sound= "sound.grass",
        hit_sound= "sound.grass",
        image= transform.scale(
        image.load("assets/images/tiles/grass.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 5,
        id_str= "tile.sand",
        name= "Sand",
        strength= 0.5,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NOISY,
        mask_merge_ids= ["tile.dirt"],
        light_reduction= 25,
        light_emission= 0,
        tags= [],
        item_id_str= "item.sand",
        item_count_range= (1, 1),
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/sand.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 6,
        id_str= "tile.sandstone",
        name= "Sandstone",
        strength= 1.0,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NOISY,
        mask_merge_ids= ["tile.dirt"],
        light_reduction= 25,
        light_emission= 0,
        tags= [],
        item_id_str= "item.sandstone",
        item_count_range= (1, 1),
        place_sound= "sound.tink",
        hit_sound= "sound.tink",
        image= transform.scale(
        image.load("assets/images/tiles/sandstone.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 7,
        id_str= "tile.snow",
        name= "Snow",
        strength= 0,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NOISY,
        mask_merge_ids= ["tile.dirt", "tile.trunk", "tile.copper"],
        light_reduction= 25,
        light_emission= 0,
        tags= [],
        item_id_str= "item.snow",
        item_count_range= (1, 1),
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/snow.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 8,
        id_str= "tile.ice",
        name= "Ice",
        strength= 1.0,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NOISY,
        mask_merge_ids= ["tile.dirt"],
        light_reduction= 25,
        light_emission= 0,
        tags= [],
        item_id_str= "item.ice",
        item_count_range= (1, 1),
        place_sound= "sound.tink",
        hit_sound= "sound.tink",
        image= transform.scale(
        image.load("assets/images/tiles/ice.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 9,
        id_str= "tile.wood",
        name= "Wood",
        strength= 1.0,
        strength_type= TileStrengthType.AXE,
        mask_type= TileMaskType.NOISY,
        mask_merge_ids= ["tile.dirt", "tile.stone"],
        light_reduction= 25,
        light_emission= 0,
        tags= [],
        item_id_str= "item.wood",
        item_count_range= (1, 1),
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/wood.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 10,
        id_str= "tile.trunk",
        name= "Trunk",
        strength= 5.0,
        strength_type= TileStrengthType.AXE,
        mask_type= TileMaskType.NOISY,
        mask_merge_ids= [
        "tile.dirt",
        "tile.grass",
        "tile.leaves",
        "tile.snow",
        ],
        light_reduction= 25,
        light_emission= 0,
        tags= [TileTag.NO_COLLIDE],
        item_id_str= "item.wood",
        item_count_range= (1, 1),
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/trunk.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 11,
        id_str= "tile.leaves",
        name= "Leaves",
        strength= 0.5,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NOISY,
        mask_merge_ids= ["tile.dirt", "tile.trunk"],
        light_reduction= 5,
        light_emission= 0,
        tags= [TileTag.NO_COLLIDE],
        item_id_str= "item.INVALID",
        item_count_range= (1, 1),
        place_sound= "sound.grass",
        hit_sound= "sound.grass",
        image= transform.scale(
        image.load("assets/images/tiles/leaves.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 12,
        id_str= "tile.copper",
        name= "Copper Ore",
        strength= 3.0,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NOISY,
        mask_merge_ids= ["tile.dirt", "tile.stone", "tile.snow"],
        light_reduction= 25,
        light_emission= 0,
        tags= [],
        item_id_str= "item.copper_ore",
        item_count_range= (1, 1),
        place_sound= "sound.tink",
        hit_sound= "sound.tink",
        image= transform.scale(
        image.load("assets/images/tiles/copper_ore.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 13,
        id_str= "tile.silver",
        name= "Silver",
        strength= 0,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NOISY,
        mask_merge_ids= [],
        light_reduction= 25,
        light_emission= 0,
        tags= [],
        item_id_str= "item.silver",
        item_count_range= (1, 1),
        place_sound= "sound.tink",
        hit_sound= "sound.tink",
        image= transform.scale(
        image.load("assets/images/tiles/silver.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    DamagingTileData(
        id= 14,
        id_str= "tile.spike",
        name= "Spike",
        strength= 1.0,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 25,
        light_emission= 0,
        tags= [TileTag.DAMAGING, TileTag.TRANSPARENT],
        item_id_str= "item.spike",
        item_count_range= (1, 1),
        tile_damage= 50,
        tile_damage_name= "spike",
        place_sound= "sound.tink",
        hit_sound= "sound.tink",
        image= transform.scale(
        image.load("assets/images/tiles/spike.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 15,
        id_str= "tile.torch",
        name= "Torch",
        strength= 1.0,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 0,
        light_emission= 200,
        tags= [TileTag.NO_COLLIDE, TileTag.TRANSPARENT],
        item_id_str= "item.torch",
        item_count_range= (1, 1),
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/lamp.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 16,
        id_str= "tile.platform_wood",
        name= "Wood Platform",
        strength= 1.0,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 25,
        light_emission= 0,
        tags= [TileTag.PLATFORM, TileTag.TRANSPARENT],
        item_id_str= "item.wood_platform",
        item_count_range= (1, 1),
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/platform_wood.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    MultitileData(
        id= 17,
        id_str= "tile.chest_wood",
        name= "Chest",
        strength= 2.0,
        strength_type= TileStrengthType.HAMMER,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 25,
        light_emission= 0,
        tags= [
        TileTag.CHEST,
        TileTag.MULTI_TILE,
        TileTag.NO_COLLIDE,
        TileTag.TRANSPARENT,
        ],
        item_id_str= "item.wood_chest",
        item_count_range= (1, 1),
        multitile_dimensions= (2, 2),
        multitile_required_solids= [(0, 2), (1, 2)],
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/chest_wood.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    MultitileData(
        id= 18,
        id_str= "tile.crafting_table_wood",
        name= "Wood Crafting Table",
        strength= 1.0,
        strength_type= TileStrengthType.HAMMER,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 25,
        light_emission= 0,
        tags= [
        TileTag.WORKBENCH,
        TileTag.MULTI_TILE,
        TileTag.NO_COLLIDE,
        TileTag.TRANSPARENT,
        ],
        item_id_str= "item.workbench",
        item_count_range= (1, 1),
        multitile_dimensions= (2, 1),
        multitile_required_solids= [(0, 1), (1, 1)],
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/crafting_table.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    DoorTileData(
        id= 19,
        id_str= "tile.door_wood_open_left",
        name= "Wood Door Open Left",
        strength= 1.0,
        strength_type= TileStrengthType.HAMMER,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 10,
        light_emission= 0,
        tags= [
        TileTag.CYCLABLE,
        TileTag.MULTI_TILE,
        TileTag.NO_COLLIDE,
        TileTag.TRANSPARENT,
        ],
        item_id_str= "item.wood_door",
        item_count_range= (1, 1),
        cycle_facing_left_tile_id_str= "tile.door_wood_closed",
        cycle_facing_left_tile_offset= [1, 0],
        cycle_facing_left_sound= "sound.door_closed",
        cycle_facing_right_tile_id_str= "tile.door_wood_closed",
        cycle_facing_right_tile_offset= [1, 0],
        cycle_facing_right_sound= "sound.door_closed",
        multitile_dimensions= (2, 3),
        multitile_required_solids= [(1, 3), (1, -1)],
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/door_wood_open_left.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    DoorTileData(
        id= 20,
        id_str= "tile.door_wood_closed",
        name= "Closed Wood Door",
        strength= 1.0,
        strength_type= TileStrengthType.HAMMER,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 35,
        light_emission= 0,
        tags= [TileTag.CYCLABLE, TileTag.MULTI_TILE, TileTag.TRANSPARENT],
        item_id_str= "item.wood_door",
        item_count_range= (1, 1),
        cycle_facing_left_tile_id_str= "tile.door_wood_open_left",
        cycle_facing_left_tile_offset= [-1, 0],
        cycle_facing_left_sound= "sound.door_opened",
        cycle_facing_right_tile_id_str= "tile.door_wood_open_right",
        cycle_facing_right_tile_offset= [0, 0],
        cycle_facing_right_sound= "sound.door_opened",
        multitile_dimensions= (1, 3),
        multitile_required_solids= [(0, 3), (0, -1)],
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/door_wood_closed.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    DoorTileData(
        id= 21,
        id_str= "tile.door_wood_open_right",
        name= "Wood Door Open Right",
        strength= 1.0,
        strength_type= TileStrengthType.HAMMER,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 10,
        light_emission= 0,
        tags= [
        TileTag.CYCLABLE,
        TileTag.MULTI_TILE,
        TileTag.NO_COLLIDE,
        TileTag.TRANSPARENT,
        ],
        item_id_str= "item.wood_door",
        item_count_range= (1, 1),
        cycle_facing_left_tile_id_str= "tile.door_wood_closed",
        cycle_facing_left_tile_offset= [0, 0],
        cycle_facing_left_sound= "sound.door_closed",
        cycle_facing_right_tile_id_str= "tile.door_wood_closed",
        cycle_facing_right_tile_offset= [0, 0],
        cycle_facing_right_sound= "sound.door_closed",
        multitile_dimensions= (2, 3),
        multitile_required_solids= [(0, 3), (0, -1)],
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/door_wood_open_right.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    LootMultitileData(
        id= 22,
        id_str= "tile.pot_tall_gray",
        name= "Tall Gray Pot",
        strength= 0.5,
        strength_type= TileStrengthType.DAMAGE,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 25,
        light_emission= 0,
        tags= [
        TileTag.BREAKABLE,
        TileTag.MULTI_TILE,
        TileTag.NO_COLLIDE,
        TileTag.TRANSPARENT,
        ],
        item_id_str= "item.INVALID",
        item_count_range= (0, 0),
        loot_group_id_str= "loot.pot",
        multitile_dimensions= (1, 2),
        multitile_required_solids= [(0, 2)],
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/pot_tall_gray.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    LootMultitileData(
        id= 23,
        id_str= "tile.pot_tall_brown",
        name= "Tall Brown Pot",
        strength= 0.5,
        strength_type= TileStrengthType.DAMAGE,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 25,
        light_emission= 0,
        tags= [
        TileTag.BREAKABLE,
        TileTag.MULTI_TILE,
        TileTag.NO_COLLIDE,
        TileTag.TRANSPARENT,
        ],
        item_id_str= "item.INVALID",
        item_count_range= (0, 0),
        loot_group_id_str= "loot.pot",
        multitile_dimensions= (1, 2),
        multitile_required_solids= [(0, 2)],
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/pot_tall_brown.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    LootMultitileData(
        id= 24,
        id_str= "tile.pot_thick_brown",
        name= "thick Brown Pot",
        strength= 0.5,
        strength_type= TileStrengthType.DAMAGE,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 0,
        light_emission= 0,
        tags= [
        TileTag.BREAKABLE,
        TileTag.MULTI_TILE,
        TileTag.NO_COLLIDE,
        TileTag.TRANSPARENT,
        ],
        item_id_str= "item.INVALID",
        item_count_range= (0, 0),
        multitile_dimensions= (2, 2),
        multitile_required_solids= [(0, 2), (1, 2)],
        loot_group_id_str= "loot.pot",
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/pot_thick_brown.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    LootMultitileData(
        id= 25,
        id_str= "tile.pot_thick_gray",
        name= "thick Gray Pot",
        strength= 0.5,
        strength_type= TileStrengthType.DAMAGE,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 0,
        light_emission= 0,
        tags= [
        TileTag.BREAKABLE,
        TileTag.MULTI_TILE,
        TileTag.NO_COLLIDE,
        TileTag.TRANSPARENT,
        ],
        item_id_str= "item.INVALID",
        item_count_range= (0, 0),
        multitile_dimensions= (2, 2),
        multitile_required_solids= [(0, 2), (1, 2)],
        loot_group_id_str= "loot.pot",
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/pot_thick_brown.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    LootTileData(
        id= 26,
        id_str= "tile.pot_short_gray",
        name= "Short Gray Pot",
        strength= 0.5,
        strength_type= TileStrengthType.DAMAGE,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 25,
        light_emission= 0,
        tags= [TileTag.BREAKABLE, TileTag.NO_COLLIDE, TileTag.TRANSPARENT],
        item_id_str= "item.INVALID",
        item_count_range= (0, 0),
        loot_group_id_str= "loot.pot",
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/pot_short_gray.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    LootTileData(
        id= 27,
        id_str= "tile.pot_short_brown",
        name= "Short Brown Pot",
        strength= 0.5,
        strength_type= TileStrengthType.DAMAGE,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 25,
        light_emission= 0,
        tags= [TileTag.BREAKABLE, TileTag.NO_COLLIDE, TileTag.TRANSPARENT],
        item_id_str= "item.INVALID",
        item_count_range= (0, 0),
        loot_group_id_str= "loot.pot",
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/pot_short_brown.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    MultitileData(
        id= 28,
        id_str= "tile.tree_canopy_a",
        name= "Tree Canopy A",
        strength= 0,
        strength_type= TileStrengthType.DAMAGE,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 0,
        light_emission= 0,
        tags= [TileTag.MULTI_TILE, TileTag.NO_COLLIDE, TileTag.TRANSPARENT],
        item_id_str= "item.wood",
        item_count_range= (4, 20),
        multitile_dimensions= (5, 5),
        multitile_required_solids= [(2, 5)],
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/tree_canopy_a.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    MultitileData(
        id= 29,
        id_str= "tile.painting_a",
        name= "Painting A",
        strength= 0.5,
        strength_type= TileStrengthType.HAMMER,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 25,
        light_emission= 0,
        tags= [TileTag.MULTI_TILE, TileTag.NO_COLLIDE],
        item_id_str= "item.painting_a",
        item_count_range= (0, 0),
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        multitile_dimensions= (3, 2),
        multitile_required_solids= [],
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/painting_a.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    MultitileData(
        id= 30,
        id_str= "tile.painting_b",
        name= "Painting B",
        strength= 0.5,
        strength_type= TileStrengthType.HAMMER,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 25,
        light_emission= 0,
        tags= [TileTag.MULTI_TILE, TileTag.NO_COLLIDE],
        item_id_str= "item.painting_b",
        item_count_range= (0, 0),
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        multitile_dimensions= (2, 2),
        multitile_required_solids= [],
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/painting_b.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    MultitileData(
        id= 31,
        id_str= "tile.painting_c",
        name= "Painting C",
        strength= 0.5,
        strength_type= TileStrengthType.HAMMER,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 25,
        light_emission= 0,
        tags= [TileTag.MULTI_TILE, TileTag.NO_COLLIDE],
        item_id_str= "item.painting_c",
        item_count_range= (0, 0),
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        multitile_dimensions= (3, 2),
        multitile_required_solids= [],
        image= transform.scale(
        image.load("assets/images/tiles/multitiles/painting_c.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
    TileData(
        id= 32,
        id_str= "tile.mushroom",
        name= "Mushroom",
        strength= 0,
        strength_type= TileStrengthType.PICKAXE,
        mask_type= TileMaskType.NONE,
        mask_merge_ids= [],
        light_reduction= 0,
        light_emission= 0,
        tags= [TileTag.NO_COLLIDE, TileTag.TRANSPARENT],
        item_id_str= "item.mushroom",
        item_count_range= (1, 1),
        place_sound= "sound.dig",
        hit_sound= "sound.dig",
        image= transform.scale(
        image.load("assets/images/tiles/mushroom.png").convert_alpha(),
        (BLOCK_SIZE, BLOCK_SIZE),
        ),
    ),
)
