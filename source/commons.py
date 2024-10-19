import pygame
from typing import TextIO, TypedDict
from datetime import datetime
from enum import Enum


class ItemTag(Enum):
    TILE = 0
    WALL = 1
    MATERIAL = 2
    WEAPON = 3
    TOOL = 4
    LONGSWORD = 5
    RANGED = 6
    MAGICAL = 7
    AMMO = 8
    PICKAXE = 9
    AXE = 10
    HAMMER = 11
    GRAPPLE = 12  # TODO The code for the grappling hook is incomplete.
    COIN = 13
    SHORTSWORD = 14


class ItemPrefixGroup(Enum):
    UNIVERSAL = 0
    COMMON = 1
    LONGSWORD = 2
    RANGED = 3
    MAGICAL = 4
    SHORTSWORD = 5


class TileTag(Enum):
    TRANSPARENT = 0
    NO_DRAW = 1
    NO_COLLIDE = 2
    MULTITILE = 3
    CYCLABLE = 4
    CHEST = 5
    BREAKABLE = 6
    WORKBENCH = 7
    PLATFORM = 8
    DAMAGING = 9


class TileStrengthType(Enum):
    PICKAXE = 0
    HAMMER = 1
    AXE = 2
    DAMAGE = 3


class TileMaskType(Enum):
    NONE = 0
    NOISY = 1


class PlayerData(TypedDict):
    name: str
    model: object
    hotbar: list[tuple[int, str, int, str]]
    inventory: list[tuple[int, str, int, str]]
    hp: int
    max_hp: int
    playtime: int
    creation_date: datetime
    last_played_date: datetime


class AIData(TypedDict):
    id: int
    id_str: str


class CraftingRecipeData(TypedDict):
    id: int
    id_str: str


class EntityItemData(TypedDict):
    item_name: str
    item_minimum_drops: int
    item_maximum_drops: int
    item_weight: int


class EntityData(TypedDict):
    id: int
    id_str: str
    name: str
    type: str
    health: int
    defense: int
    knockback_resistance: float
    attack_damage: int
    color: tuple[int, int, int]
    item_drops: list[EntityItemData]
    coin_drop_range: tuple[int, int]


class PlacableTileItemData(TypedDict):
    id: int
    id_str: int
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    hold_offset: float
    tile_id_str: str
    pickup_sound: str
    drop_sound: str
    image: pygame.Surface


class ImplacableTileItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    tile_id_str: str
    pickup_sound: str
    drop_sound: str
    hold_offset: float
    image: pygame.Surface


class MaterialItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    pickup_sound: str
    drop_sound: str
    hold_offset: float
    image: pygame.Surface


class WallItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    hold_offset: float
    pickup_sound: str
    drop_sound: str
    wall_id_str: str
    image: pygame.Surface


class PickaxeItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    attack_speed: int
    attack_damage: int
    knockback: int
    crit_chance: float
    prefixes: list[ItemPrefixGroup]
    pickaxe_power: float
    pickup_sound: str
    drop_sound: str
    use_sound: str
    hold_offset: float
    image: pygame.Surface
    world_override_image: pygame.Surface | None


class HammerItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    attack_speed: int
    attack_damage: int
    knockback: float
    crit_chance: float
    prefixes: list[ItemPrefixGroup]
    pickup_sound: str
    drop_sound: str
    use_sound: str
    hammer_power: float
    hold_offset: float
    image: pygame.Surface
    world_override_image: pygame.Surface | None


class AxeItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    attack_speed: int
    attack_damage: int
    knockback: float
    crit_chance: float
    prefixes: list[ItemPrefixGroup]
    axe_power: float
    pickup_sound: str
    drop_sound: str
    use_sound: str
    hold_offset: float
    image: pygame.Surface
    world_override_image: pygame.Surface | None


class SwordItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    attack_speed: int
    attack_damage: int
    knockback: float
    crit_chance: float
    prefixes: list[ItemPrefixGroup]
    pickup_sound: str
    drop_sound: str
    use_sound: str
    hold_offset: float
    image: pygame.Surface
    world_override_image: pygame.Surface | None


class RangedItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    attack_speed: int
    attack_damage: int
    knockback: float
    crit_chance: float
    prefixes: list[ItemPrefixGroup]
    ranged_projectile_id_str: str
    ranged_ammo_type: list[str]
    ranged_projectile_speed: float
    ranged_accuracy: float
    ranged_num_projectiles: int
    pickup_sound: str
    drop_sound: str
    use_sound: str
    hold_offset: float
    image: pygame.Surface
    world_override_image: pygame.Surface | None


class AmmunitionItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    ammo_damage: float
    ammo_drag: float
    ammo_gravity_modifier: float
    ammo_knockback_modifier: float
    pickup_sound: str
    drop_sound: str
    hold_offset: float
    ricochet_amount: int
    image: pygame.Surface
    ammo_image: pygame.Surface


class GrapplingHookItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    grapple_speed: float
    grapple_chain_length: float
    grapple_max_chains: int
    pickup_sound: str
    drop_sound: str
    hold_offset: float
    image: pygame.Surface
    grapple_chain_image: pygame.Surface
    grapple_claw_image: pygame.Surface


class MagicalWeaponItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    pickup_sound: str
    drop_sound: str
    prefixes: list[ItemPrefixGroup]
    attack_speed: int
    attack_damage: int
    knockback: float
    crit_chance: float
    hold_offset: float
    use_sound: str
    mana_cost: int
    image: pygame.Surface
    world_override_image: pygame.Surface | None


class ItemLootData(TypedDict):
    item_id_str: str
    item_spawn_weight: int
    item_spawn_depth_range: tuple[int, int]
    item_stack_count_range: tuple[int, int]
    item_slot_priority: int
    once_per_instance: bool


class LootData(TypedDict):
    id: int
    id_str: str
    name: str
    item_spawn_count_range: tuple[int, int]
    item_list_data: list[ItemLootData]
    coin_spawn_range: tuple[int, int]


class ProjectileData(TypedDict):
    id: int
    id_str: str


class SoundData(TypedDict):
    id: int
    id_str: str
    variation_paths: list[str]
    volume: float


class StructureData(TypedDict):
    id: int
    id_str: str
    name: str
    width: int
    height: int
    spawn_weight: int
    tile_data: list[str]


class TileData(TypedDict):
    id: int
    id_str: str
    name: str
    strength: float
    strength_type: str
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    light_reduction: int
    light_emission: int
    tags: list[str]
    item_id_str: str
    item_count_range: tuple[int, int]
    place_sound: str
    hit_sound: str
    image: pygame.Surface


class DamagingTileData(TypedDict):
    id: int
    id_str: str
    name: str
    strength: float
    strength_type: str
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    light_reduction: int
    light_emission: int
    tags: list[str]
    item_id_str: str
    item_count_range: tuple[int, int]
    place_sound: str
    hit_sound: str
    tile_damage: int
    tile_damage_name: str
    image: pygame.Surface


class MultitileData(TypedDict):
    id: int
    id_str: str
    name: str
    strength: float
    strength_type: str
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    light_reduction: int
    light_emission: int
    tags: list[str]
    item_id_str: str
    item_count_range: tuple[int, int]
    multitile_dimensions: tuple[int, int]
    multitile_required_solids: list[tuple[int, int]]
    place_sound: str
    hit_sound: str
    image: pygame.Surface


class DoorTileData(TypedDict):
    id: int
    id_str: str
    name: str
    strength: float
    strength_type: str
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    light_reduction: int
    light_emission: int
    tags: list[str]
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
    image: pygame.Surface


class LootMultitileData(TypedDict):
    id: int
    id_str: str
    name: str
    strength: float
    strength_type: str
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    light_reduction: int
    light_emission: int
    tags: list[str]
    item_id_str: str
    item_count_range: tuple[int, int]
    loot_group_id_str: str
    multitile_dimensions: tuple[int, int]
    multitile_required_solids: list[tuple[int, int]]
    place_sound: str
    hit_sound: str
    image: pygame.Surface


class LootTileData(TypedDict):
    id: int
    id_str: str
    name: str
    strength: float
    strength_type: str
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    light_reduction: int
    light_emission: int
    tags: list[str]
    item_id_str: str
    item_count_range: tuple[int, int]
    loot_group_id_str: str
    place_sound: str
    hit_sound: str
    image: pygame.Surface


class WallData(TypedDict):
    id: int
    id_str: str
    name: str
    mask_type: TileMaskType
    mask_merge_ids: list[str]
    item_id_str: str
    place_sound: str
    hit_sound: str
    image: pygame.Surface


class WorldGenData(TypedDict):
    id: int
    id_str: str


pygame.init()

BLOCK_SIZE: int = 16
TARGET_FPS: int = 60
MOUSE_POSITION: tuple[int, int] = (0, 0)
HOVERED_TILE: tuple[int, int] = (0, 0)
SHIFT_ACTIVE: bool = False

game_state: str = "MAIN_MENU"
game_sub_state: str = "MAIN"

# Config loading
CONFIG: TextIO = open("CONFIG.txt", "r")
CONFIG_DATA: list[str] = CONFIG.readlines()
configData: list[str] = []
for item in CONFIG_DATA:
    item = item.split("=")
    configData.append(item[1][:-1])
WINDOW_WIDTH: int = int(configData[0].split(",")[0])
WINDOW_HEIGHT: int = int(configData[0].split(",")[1])
GRAVITY: float = 9.8 * BLOCK_SIZE * 0.666 * float(configData[1])  # 3 tiles = 1 metre
RUN_FULLSCREEN: bool = bool(int(configData[2]))
PARTICLES: bool = bool(int(configData[3]))
PARTICLE_DENSITY: float = float(configData[4])
MUSIC: bool = bool(int(configData[5]))
CONFIG_MUSIC_VOLUME: float = float(configData[6])
SOUND: bool = bool(int(configData[7]))
CONFIG_SOUND_VOLUME: float = float(configData[8])
CREATIVE: bool = bool(int(configData[9]))
BACKGROUND: bool = bool(int(configData[10]))
PARALLAX_AMOUNT: float = float(configData[11])
PASSIVE: bool = bool(int(configData[12]))
MAX_ENEMY_SPAWNS: int = int(configData[13])
FANCY_TEXT: bool = bool(int(configData[14]))
HITBOXES: bool = bool(int(configData[15]))
SPLASHSCREEN: bool = bool(int(configData[16]))
AUTO_SAVE_FREQUENCY: float = float(configData[17])
EXPERIMENTAL_LIGHTING: bool = bool(int(configData[18]))
SMOOTH_CAM: bool = bool(int(configData[19]))
DRAW_UI: bool = bool(int(configData[20]))

if RUN_FULLSCREEN:
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

FONT_FILE_PATH: str = r"assets/fonts/AndyBold.ttf"
SMALL_FONT: pygame.font.Font = pygame.font.Font(FONT_FILE_PATH, 10)
DEFAULT_FONT: pygame.font.Font = pygame.font.Font(FONT_FILE_PATH, 16)
MEDIUM_FONT: pygame.font.Font = pygame.font.Font(FONT_FILE_PATH, 22)
LARGE_FONT: pygame.font.Font = pygame.font.Font(FONT_FILE_PATH, 40)
EXTRA_LARGE_FONT: pygame.font.Font = pygame.font.Font(FONT_FILE_PATH, 50)

WAIT_TO_USE: bool = False

ENEMY_SPAWN_TICK: int = 0

MIN_ENEMY_SPAWN_TILES_X: int = int((WINDOW_WIDTH // BLOCK_SIZE) * 0.5)
MAX_ENEMY_SPAWN_TILES_X: int = int(MIN_ENEMY_SPAWN_TILES_X * 2)
MIN_ENEMY_SPAWN_TILES_Y: int = int((WINDOW_HEIGHT // BLOCK_SIZE) * 0.5)
MAX_ENEMY_SPAWN_TILES_Y: int = int(MIN_ENEMY_SPAWN_TILES_Y * 2)

PLAYER_DATA: PlayerData = {
    "name": "",
    "model": None,
    "hotbar": [],
    "inventory": [],
    "hp": 0,
    "max_hp": 0,
    "playtime": 0,
    "creation_date": datetime(1, 1, 1),
    "last_played_date": datetime(1, 1, 1),
}

PLAYER_SAVE_OPTIONS: list[list[PlayerData]] = []

PLAYER_WIDTH: int = 26
PLAYER_HEIGHT: int = 48
PLAYER_ARM_LENGTH: int = 20

PLAYER_MODEL_DATA: list[list[int]] = []
PLAYER_MODEL: object = None
PLAYER_FRAMES: list[list[pygame.Surface]] = []
PLAYER_REACH: int = 8
PLAYER_MODEL_COLOR_INDEX: int = 0
TEXT_INPUT: str = ""

is_holding_item: bool = False
item_holding: object = None


OLD_TIME_MILLISECONDS: int = pygame.time.get_ticks()
DELTA_TIME: int = 0

CURRENT_SKY_LIGHTING: int = 255

GAME_BACKGROUND: pygame.Surface = pygame.Surface((WINDOW_WIDTH + 2048, WINDOW_HEIGHT + 838))
GAME_BACKGROUND.blit(pygame.image.load("assets/images/backgrounds/game_backgrounds/forest_background.png"), (0, 0))

WORLD_SAVE_OPTIONS: list[tuple[str, pygame.Surface]] = []

AI_DATA: list[AIData] = [
    {"id": 0, "id_str": "loot.INVALID"},
    {"id": 1, "id_str": "loot.slime"},
    {"id": 2, "id_str": "loot.bunny"},
]

CRAFTING_RECIPES: list[CraftingRecipeData] = [
    {"id": 0, "id_str": "crafting_recipe.INVALID"},
    {"id": 1, "id_str": "crafting_recipe.work_bench"},
]

ENTITY_DATA: list[EntityData] = [
    {
        "id": 0,
        "id_str": "entity.INVALID",
        "name": "INVALID",
        "type": "Slime",
        "health": 0,
        "defense": 0,
        "knockback_resistance": 0,
        "attack_damage": 0,
        "color": (0, 0, 0),
        "item_drops": [
            {
                "item_name": "item.INVALID",
                "item_minimum_drops": 0,
                "item_maximum_drops": 0,
                "item_weight": 0,
            }
        ],
        "coin_drop_range": (0, 0),
    },
    {
        "id": 1,
        "id_str": "entity.green_slime",
        "name": "Green Slime",
        "type": "Slime",
        "health": 14,
        "defense": 0,
        "knockback_resistance": -2,
        "attack_damage": 6,
        "color": (10, 200, 10),
        "item_drops": [
            {
                "item_name": "item.gel",
                "item_minimum_drops": 1,
                "item_maximum_drops": 2,
                "item_weight": 100,
            }
        ],
        "coin_drop_range": (5, 30),
    },
    {
        "id": 2,
        "id_str": "entity.blue_slime",
        "name": "Blue Slime",
        "type": "Slime",
        "health": 25,
        "defense": 2,
        "knockback_resistance": 0,
        "attack_damage": 7,
        "color": (10, 10, 200),
        "item_drops": [
            {
                "item_name": "item.gel",
                "item_minimum_drops": 1,
                "item_maximum_drops": 2,
                "item_weight": 100,
            }
        ],
        "coin_drop_range": (15, 50),
    },
    {
        "id": 3,
        "id_str": "entity.red_slime",
        "name": "Red Slime",
        "type": "Slime",
        "health": 35,
        "defense": 4,
        "knockback_resistance": 0,
        "attack_damage": 12,
        "color": (200, 10, 10),
        "item_drops": [
            {
                "item_name": "item.gel",
                "item_minimum_drops": 2,
                "item_maximum_drops": 5,
                "item_weight": 100,
            }
        ],
        "coin_drop_range": (25, 75),
    },
    {
        "id": 4,
        "id_str": "entity.purple_slime",
        "name": "Purple Slime",
        "type": "Slime",
        "health": 40,
        "defense": 6,
        "knockback_resistance": 0.1,
        "attack_damage": 12,
        "color": (200, 10, 200),
        "item_drops": [
            {
                "item_name": "item.gel",
                "item_minimum_drops": 2,
                "item_maximum_drops": 5,
                "item_weight": 100,
            }
        ],
        "coin_drop_range": (35, 110),
    },
    {
        "id": 5,
        "id_str": "entity.yellow_slime",
        "name": "Yellow Slime",
        "type": "Slime",
        "health": 45,
        "defense": 7,
        "knockback_resistance": 0,
        "attack_damage": 15,
        "color": (200, 150, 100),
        "item_drops": [
            {
                "item_name": "item.gel",
                "item_minimum_drops": 2,
                "item_maximum_drops": 5,
                "item_weight": 100,
            }
        ],
        "coin_drop_range": (45, 130),
    },
]

ITEM_DATA: list[
    PlacableTileItemData
    | ImplacableTileItemData
    | MaterialItemData
    | WallItemData
    | PickaxeItemData
    | HammerItemData
    | AxeItemData
    | SwordItemData
    | RangedItemData
    | AmmunitionItemData
    | GrapplingHookItemData
    | MagicalWeaponItemData
] = [
    {
        "id": 0,
        "id_str": "item.INVALID",
        "name": "INVALID",
        "tags": [],
        "tier": 0,
        "max_stack": 9999,
        "buy_price": 0,
        "sell_price": 0,
        "hold_offset": 0.0,
        "tile_id_str": "tile.UNNAMED",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "image": pygame.Surface((0, 0)),
    },
    {
        "id": 1,
        "id_str": "item.iron_pickaxe",
        "name": "Iron Pickaxe",
        "tags": [ItemTag.PICKAXE, ItemTag.TOOL, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 0,
        "sell_price": 40,
        "attack_speed": 20,
        "attack_damage": 7,
        "knockback": 2,
        "crit_chance": 0.04,
        "prefixes": [ItemPrefixGroup.COMMON, ItemPrefixGroup.UNIVERSAL],
        "pickaxe_power": 40.0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": pygame.image.load(
            "assets/images/items/iron_pickaxe.png"
        ).convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 2,
        "id_str": "item.dirt_block",
        "name": "Dirt",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 1,
        "sell_price": 0,
        "hold_offset": 0.0,
        "tile_id_str": "tile.dirt",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "image": pygame.image.load(
            "assets/images/items/dirt_block.png"
        ).convert_alpha(),
    },
    {
        "id": 3,
        "id_str": "item.stone_block",
        "name": "Stone",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 2,
        "sell_price": 0,
        "hold_offset": 0.0,
        "tile_id_str": "tile.stone",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "image": pygame.image.load(
            "assets/images/items/stone_block.png"
        ).convert_alpha(),
    },
    {
        "id": 4,
        "id_str": "item.iron_broadsword",
        "name": "Iron Broadsword",
        "tags": [ItemTag.LONGSWORD, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 200,
        "sell_price": 20,
        "attack_speed": 20,
        "attack_damage": 12,
        "knockback": 5.5,
        "crit_chance": 0.04,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.LONGSWORD,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": pygame.image.load(
            "assets/images/items/iron_broadsword.png"
        ).convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 5,
        "id_str": "item.mushroom",
        "name": "Mushroom",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 1,
        "tile_id_str": "tile.mushroom",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/mushroom.png").convert_alpha(),
    },
    {
        "id": 6,
        "id_str": "item.iron_ore",
        "name": "Iron Ore",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 20,
        "sell_price": 10,
        "tile_id_str": "tile.pot_thick_brown",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/iron_ore.png").convert_alpha(),
    },
    {
        "id": 7,
        "id_str": "item.dirt_wall",
        "name": "Dirt Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 2,
        "sell_price": 0,
        "hold_offset": 0.0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "wall_id_str": "wall.dirt",
        "image": pygame.image.load("assets/images/items/dirt_wall.png").convert_alpha(),
    },
    {
        "id": 8,
        "id_str": "item.stone_wall",
        "name": "Stone Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 2,
        "sell_price": 0,
        "hold_offset": 0.0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "wall_id_str": "wall.stone",
        "image": pygame.image.load(
            "assets/images/items/stone_wall.png"
        ).convert_alpha(),
    },
    {
        "id": 9,
        "id_str": "item.snow",
        "name": "Snow",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 2,
        "tile_id_str": "tile.snow",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/snow.png").convert_alpha(),
    },
    {
        "id": 10,
        "id_str": "item.snow_wall",
        "name": "Snow Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 2,
        "sell_price": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "wall_id_str": "wall.snow",
        "image": pygame.image.load("assets/images/items/snow_wall.png").convert_alpha(),
    },
    {
        "id": 11,
        "id_str": "item.ice",
        "name": "Ice",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 0,
        "tile_id_str": "tile.none",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/ice.png").convert_alpha(),
    },
    {
        "id": 12,
        "id_str": "item.ice_wall",
        "name": "Ice Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 2,
        "sell_price": 5,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "wall_id_str": "wall.ice",
        "image": pygame.image.load("assets/images/items/ice_wall.png").convert_alpha(),
    },
    {
        "id": 13,
        "id_str": "item.wood",
        "name": "Wood",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 1,
        "tile_id_str": "tile.wood",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/wood.png").convert_alpha(),
    },
    {
        "id": 14,
        "id_str": "item.wood_wall",
        "name": "Wood Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 2,
        "sell_price": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "wall_id_str": "wall.wood",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/wood_wall.png").convert_alpha(),
    },
    {
        "id": 15,
        "id_str": "item.copper_ore",
        "name": "Copper Ore",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 10,
        "sell_price": 5,
        "tile_id_str": "tile.copper",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load(
            "assets/images/items/copper_ore.png"
        ).convert_alpha(),
    },
    {
        "id": 16,
        "id_str": "item.silver_ore",
        "name": "Silver Ore",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 20,
        "sell_price": 10,
        "tile_id_str": "tile.pot_thick_brown",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load(
            "assets/images/items/silver_ore.png"
        ).convert_alpha(),
    },
    {
        "id": 17,
        "id_str": "item.sand",
        "name": "Sand",
        "tags": [ItemTag.MATERIAL, ItemTag.TILE],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 10,
        "sell_price": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "tile_id_str": "tile.sand",
        "image": pygame.image.load("assets/images/items/sand.png").convert_alpha(),
    },
    {
        "id": 18,
        "id_str": "item.hardened_sand_wall",
        "name": "Hardened Sand Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 10,
        "sell_price": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "wall_id_str": "wall.hardened_sand",
        "image": pygame.image.load(
            "assets/images/items/hardened_sand_wall.png"
        ).convert_alpha(),
    },
    {
        "id": 19,
        "id_str": "item.sandstone",
        "name": "Sandstone",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 0,
        "tile_id_str": "tile.sandstone",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/sandstone.png").convert_alpha(),
    },
    {
        "id": 20,
        "id_str": "item.sandstone_wall",
        "name": "Sandstone Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "wall_id_str": "wall.sandstone",
        "image": pygame.image.load(
            "assets/images/items/sandstone_wall.png"
        ).convert_alpha(),
    },
    {
        "id": 21,
        "id_str": "item.wood_platform",
        "name": "Wood Platform",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 20,
        "sell_price": 5,
        "tile_id_str": "tile.platform_wood",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load(
            "assets/images/items/wood_platform.png"
        ).convert_alpha(),
    },
    {
        "id": 22,
        "id_str": "item.copper_broadsword",
        "name": "Copper Broadsword",
        "tags": [ItemTag.LONGSWORD, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 200,
        "sell_price": 20,
        "attack_speed": 45,
        "attack_damage": 5,
        "knockback": 10,
        "crit_chance": 0.03,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.LONGSWORD,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": pygame.image.load(
            "assets/images/items/copper_broadsword.png"
        ).convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 23,
        "id_str": "item.excalibur",
        "name": "Excalibur",
        "tags": [ItemTag.LONGSWORD, ItemTag.WEAPON],
        "tier": 10,
        "max_stack": 1,
        "buy_price": 100000000,
        "sell_price": 20000000,
        "attack_speed": 35,
        "attack_damage": 1337,
        "knockback": 0,
        "crit_chance": 0.0,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.LONGSWORD,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.9,
        "image": pygame.image.load("assets/images/items/excalibur.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 24,
        "id_str": "item.wood_broadsword",
        "name": "Wooden Sword",
        "tags": [ItemTag.LONGSWORD, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 100,
        "sell_price": 10,
        "attack_speed": 50,
        "attack_damage": 3,
        "knockback": 6,
        "crit_chance": 0.03,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.LONGSWORD,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": pygame.image.load(
            "assets/images/items/wood_broadsword.png"
        ).convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 25,
        "id_str": "item.wood_bow",
        "name": "Wooden Bow",
        "tags": [ItemTag.RANGED, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 150,
        "sell_price": 20,
        "attack_speed": 50,
        "attack_damage": 4,
        "knockback": 2,
        "crit_chance": 0.03,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.RANGED,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "ranged_projectile_id_str": "projectile.arrow",
        "ranged_ammo_type": ["item.wooden_arrow"],
        "ranged_projectile_speed": 75.0,
        "ranged_accuracy": 0.9,
        "ranged_num_projectiles": 1,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.bow",
        "hold_offset": 0.8,
        "image": pygame.image.load("assets/images/items/wood_bow.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 26,
        "id_str": "item.wooden_arrow",
        "name": "Wooden Arrow",
        "tags": [ItemTag.MATERIAL, ItemTag.AMMO],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 1,
        "ammo_damage": 4.0,
        "ammo_drag": 0.05,
        "ammo_gravity_modifier": 1.2,
        "ammo_knockback_modifier": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "ricochet_amount": 1,
        "image": pygame.image.load(
            "assets/images/items/wooden_arrow.png"
        ).convert_alpha(),
        "ammo_image": pygame.image.load("assets/images/projectiles/wooden_arrow.png").convert_alpha()
    },
    {
        "id": 27,
        "id_str": "item.musket",
        "name": "Musket",
        "tags": [ItemTag.RANGED, ItemTag.WEAPON],
        "tier": 1,
        "max_stack": 1,
        "buy_price": 5000,
        "sell_price": 250,
        "attack_speed": 75,
        "attack_damage": 12,
        "knockback": 4,
        "crit_chance": 0.03,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.RANGED,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "ranged_projectile_id_str": "projectile.bullet",
        "ranged_ammo_type": ["item.musket_ball"],
        "ranged_projectile_speed": 100.0,
        "ranged_accuracy": 0.95,
        "ranged_num_projectiles": 1,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.gun_shot",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/musket.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 28,
        "id_str": "item.musket_ball",
        "name": "Musket Ball",
        "tags": [ItemTag.MATERIAL, ItemTag.AMMO],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 7,
        "sell_price": 1,
        "ammo_damage": 7.0,
        "ammo_drag": 0.05,
        "ammo_gravity_modifier": 0.5,
        "ammo_knockback_modifier": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "ricochet_amount": 1,
        "image": pygame.image.load(
            "assets/images/items/musket_ball.png"
        ).convert_alpha(),
        "ammo_image": pygame.image.load("assets/images/projectiles/musket_ball.png").convert_alpha()
    },
    {
        "id": 29,
        "id_str": "item.copper_coin",
        "name": "Copper Coin",
        "tags": [ItemTag.AMMO, ItemTag.COIN],
        "tier": 0,
        "max_stack": 100,
        "buy_price": 0,
        "sell_price": 0,
        "ammo_damage": 2.0,
        "ammo_drag": 5.0,
        "ammo_gravity_modifier": 1.0,
        "ammo_knockback_modifier": 0,
        "pickup_sound": "sound.coins",
        "drop_sound": "sound.coins",
        "hold_offset": 0.0,
        "ricochet_amount": 1,
        "image": pygame.image.load(
            "assets/images/items/copper_coin.png"
        ).convert_alpha(),
        "ammo_image": pygame.image.load("assets/images/projectiles/musket_ball.png").convert_alpha()
    },
    {
        "id": 30,
        "id_str": "item.silver_coin",
        "name": "Silver Coin",
        "tags": [ItemTag.AMMO, ItemTag.COIN],
        "tier": 0,
        "max_stack": 100,
        "buy_price": 0,
        "sell_price": 0,
        "ammo_damage": 5.0,
        "ammo_drag": 2.5,
        "ammo_gravity_modifier": 0.75,
        "ammo_knockback_modifier": 0,
        "pickup_sound": "sound.coins",
        "drop_sound": "sound.coins",
        "hold_offset": 0.0,
        "ricochet_amount": 1,
        "image": pygame.image.load(
            "assets/images/items/silver_coin.png"
        ).convert_alpha(),
        "ammo_image": pygame.image.load("assets/images/projectiles/musket_ball.png").convert_alpha()
    },
    {
        "id": 31,
        "id_str": "item.gold_coin",
        "name": "Gold Coin",
        "tags": [ItemTag.AMMO, ItemTag.COIN],
        "tier": 0,
        "max_stack": 100,
        "buy_price": 0,
        "sell_price": 0,
        "ammo_damage": 50.0,
        "ammo_drag": 1.25,
        "ammo_gravity_modifier": 0.5,
        "ammo_knockback_modifier": 0,
        "pickup_sound": "sound.coins",
        "drop_sound": "sound.coins",
        "hold_offset": 0.0,
        "ricochet_amount": 1,
        "image": pygame.image.load("assets/images/items/gold_coin.png").convert_alpha(),
        "ammo_image": pygame.image.load("assets/images/projectiles/musket_ball.png").convert_alpha()
    },
    {
        "id": 32,
        "id_str": "item.platinum_coin",
        "name": "Platinum Coin",
        "tags": [ItemTag.AMMO, ItemTag.COIN],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 0,
        "sell_price": 0,
        "ammo_damage": 100.0,
        "ammo_drag": 0.625,
        "ammo_gravity_modifier": 0.25,
        "ammo_knockback_modifier": 0,
        "pickup_sound": "sound.coins",
        "drop_sound": "sound.coins",
        "hold_offset": 0.0,
        "ricochet_amount": 1,
        "image": pygame.image.load(
            "assets/images/items/platinum_coin.png"
        ).convert_alpha(),
        "ammo_image": pygame.image.load("assets/images/projectiles/musket_ball.png").convert_alpha()
    },
    {
        "id": 33,
        "id_str": "item.copper_pickaxe",
        "name": "Copper Pickaxe",
        "tags": [ItemTag.PICKAXE, ItemTag.TOOL, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 150,
        "sell_price": 10,
        "attack_speed": 50,
        "attack_damage": 2,
        "knockback": 10,
        "crit_chance": 0.03,
        "prefixes": [ItemPrefixGroup.COMMON, ItemPrefixGroup.UNIVERSAL],
        "pickaxe_power": 35.0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": pygame.image.load(
            "assets/images/items/copper_pickaxe.png"
        ).convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 34,
        "id_str": "item.copper_hammer",
        "name": "Copper Hammer",
        "tags": [ItemTag.HAMMER, ItemTag.TOOL, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 150,
        "sell_price": 10,
        "attack_speed": 50,
        "attack_damage": 2,
        "knockback": 10,
        "crit_chance": 0.03,
        "prefixes": [ItemPrefixGroup.COMMON, ItemPrefixGroup.UNIVERSAL],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hammer_power": 0,
        "hold_offset": 0.8,
        "image": pygame.image.load(
            "assets/images/items/copper_hammer.png"
        ).convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 35,
        "id_str": "item.wood_hammer",
        "name": "Wood Hammer",
        "tags": [ItemTag.HAMMER, ItemTag.TOOL, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 150,
        "sell_price": 10,
        "attack_speed": 35,
        "attack_damage": 2,
        "knockback": 10,
        "crit_chance": 0.03,
        "prefixes": [ItemPrefixGroup.COMMON, ItemPrefixGroup.UNIVERSAL],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hammer_power": 0,
        "hold_offset": 0.8,
        "image": pygame.image.load(
            "assets/images/items/wood_hammer.png"
        ).convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 36,
        "id_str": "item.gel",
        "name": "Blue Gel",
        "tags": [ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 1,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/gel.png").convert_alpha(),
    },
    {
        "id": 37,
        "id_str": "item.wood_chest",
        "name": "Wooden Chest",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 99,
        "buy_price": 50,
        "sell_price": 5,
        "tile_id_str": "tile.chest_wood",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load(
            "assets/images/items/wood_chest.png"
        ).convert_alpha(),
    },
    {
        "id": 38,
        "id_str": "item.workbench",
        "name": "Workbench",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 99,
        "buy_price": 50,
        "sell_price": 5,
        "tile_id_str": "tile.crafting_table_wood",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/workbench.png").convert_alpha(),
    },
    {
        "id": 39,
        "id_str": "item.wood_door",
        "name": "Wooden Door",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 99,
        "buy_price": 50,
        "sell_price": 5,
        "tile_id_str": "tile.door_wood_closed",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/wood_door.png").convert_alpha(),
    },
    {
        "id": 40,
        "id_str": "item.torch",
        "name": "Torch",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 20,
        "sell_price": 2,
        "tile_id_str": "tile.torch",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/torch.png").convert_alpha(),
    },
    {
        "id": 41,
        "id_str": "item.spike",
        "name": "Spike",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 15,
        "sell_price": 0,
        "tile_id_str": "tile.spike",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load("assets/images/items/spike.png").convert_alpha(),
    },
    {
        "id": 42,
        "id_str": "item.grappling_hook",
        "name": "Grappling Hook",
        "tags": [ItemTag.GRAPPLE, ItemTag.TOOL],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 10000,
        "sell_price": 500,
        "grapple_speed": 10.0,
        "grapple_chain_length": 100.0,
        "grapple_max_chains": 1,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": pygame.image.load(
            "assets/images/items/grappling_hook.png"
        ).convert_alpha(),
        "grapple_chain_image": pygame.image.load(
            "assets/images/grappling_hook_chain.png"
        ).convert_alpha(),
        "grapple_claw_image": pygame.image.load(
            "assets/images/grappling_hook_claw.png"
        ).convert_alpha(),
    },
    {
        "id": 43,
        "id_str": "item.water_bolt",
        "name": "Water Bolt",
        "tags": [ItemTag.MAGICAL, ItemTag.WEAPON],
        "tier": 3,
        "max_stack": 999,
        "buy_price": 10000,
        "sell_price": 750,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "prefixes": [],
        "attack_speed": 12,
        "attack_damage": 5,
        "knockback": 0,
        "crit_chance": 0.03,
        "hold_offset": 0.0,
        "use_sound": "sound.swing",
        "mana_cost": 20,
        "image": pygame.image.load(
            "assets/images/items/water_bolt.png"
        ).convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 44,
        "id_str": "item.painting_a",
        "name": "Painting A",
        "tags": [ItemTag.TILE],
        "tier": 3,
        "max_stack": 999,
        "buy_price": 1000,
        "sell_price": 100,
        "hold_offset": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "tile_id_str": "tile.painting_a",
        "image": pygame.image.load(
            "assets/images/items/painting_a.png"
        ).convert_alpha(),
    },
    {
        "id": 45,
        "id_str": "item.painting_b",
        "name": "Painting B",
        "tags": [ItemTag.TILE],
        "tier": 3,
        "max_stack": 999,
        "buy_price": 1000,
        "sell_price": 100,
        "hold_offset": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "tile_id_str": "tile.painting_b",
        "image": pygame.image.load(
            "assets/images/items/painting_b.png"
        ).convert_alpha(),
    },
    {
        "id": 46,
        "id_str": "item.painting_c",
        "name": "Painting C",
        "tags": [ItemTag.TILE],
        "tier": 3,
        "max_stack": 999,
        "buy_price": 1000,
        "sell_price": 100,
        "hold_offset": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "tile_id_str": "tile.painting_c",
        "image": pygame.image.load(
            "assets/images/items/painting_c.png"
        ).convert_alpha(),
    },
    {
        "id": 47,
        "id_str": "item.copper_axe",
        "name": "Copper Axe",
        "tags": [ItemTag.AXE, ItemTag.TOOL, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 150,
        "sell_price": 10,
        "attack_speed": 50,
        "attack_damage": 2,
        "knockback": 10,
        "crit_chance": 0.03,
        "prefixes": [ItemPrefixGroup.COMMON, ItemPrefixGroup.UNIVERSAL],
        "axe_power": 55.0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": pygame.image.load(
            "assets/images/items/copper_axe.png"
        ).convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 48,
        "id_str": "item.iron_shortsword",
        "name": "Iron Shortsword",
        "tags": [ItemTag.SHORTSWORD, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 200,
        "sell_price": 20,
        "attack_speed": 20,
        "attack_damage": 12,
        "knockback": 5.5,
        "crit_chance": 0.04,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.SHORTSWORD,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": pygame.image.load(
            "assets/images/items/iron_shortsword.png"
        ).convert_alpha(),
        "world_override_image": None,
    },
]

LOOT_DATA: list[LootData] = [
    {
        "id": 0,
        "id_str": "loot.INVALID",
        "name": "INVALID",
        "item_spawn_count_range": (0, 0),
        "item_list_data": [
            {
                "item_id_str": "item.INVALID",
                "item_spawn_weight": 100,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (0, 0),
                "item_slot_priority": 0,
                "once_per_instance": False,
            }
        ],
        "coin_spawn_range": (0, 0),
    },
    {
        "id": 1,
        "id_str": "loot.pot",
        "name": "Pot",
        "item_spawn_count_range": (1, 2),
        "item_list_data": [
            {
                "item_id_str": "item.torch",
                "item_spawn_weight": 100,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (3, 15),
                "item_slot_priority": 3,
                "once_per_instance": False,
            },
            {
                "item_id_str": "item.wood_platform",
                "item_spawn_weight": 50,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (5, 15),
                "item_slot_priority": 3,
                "once_per_instance": False,
            },
            {
                "item_id_str": "item.spike",
                "item_spawn_weight": 50,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (2, 6),
                "item_slot_priority": 2,
                "once_per_instance": False,
            },
            {
                "item_id_str": "item.musket_ball",
                "item_spawn_weight": 25,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (5, 20),
                "item_slot_priority": 1,
                "once_per_instance": False,
            },
            {
                "item_id_str": "item.copper_coin",
                "item_spawn_weight": 5,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (1, 1),
                "item_slot_priority": 0,
                "once_per_instance": True,
            },
            {
                "item_id_str": "item.wooden_arrow",
                "item_spawn_weight": 35,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (7, 25),
                "item_slot_priority": 1,
                "once_per_instance": False,
            },
        ],
        "coin_spawn_range": (75, 150),
    },
    {
        "id": 2,
        "id_str": "loot.chest_wood",
        "name": "Wood Chest",
        "item_spawn_count_range": (2, 6),
        "item_list_data": [
            {
                "item_id_str": "item.musket",
                "item_spawn_weight": 100,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (1, 1),
                "item_slot_priority": 0,
                "once_per_instance": True,
            },
            {
                "item_id_str": "item.wood_bow",
                "item_spawn_weight": 100,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (1, 1),
                "item_slot_priority": 0,
                "once_per_instance": True,
            },
            {
                "item_id_str": "item.water_bolt",
                "item_spawn_weight": 100,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (1, 1),
                "item_slot_priority": 0,
                "once_per_instance": False,
            },
            {
                "item_id_str": "item.wooden_arrow",
                "item_spawn_weight": 600,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (5, 20),
                "item_slot_priority": 2,
                "once_per_instance": False,
            },
            {
                "item_id_str": "item.musket_ball",
                "item_spawn_weight": 600,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (5, 20),
                "item_slot_priority": 2,
                "once_per_instance": False,
            },
        ],
        "coin_spawn_range": (750, 2000),
    },
    {
        "id": 3,
        "id_str": "loot.chest_gold",
        "name": "Gold Chest",
        "item_spawn_count_range": (2, 5),
        "item_list_data": [
            {
                "item_id_str": "item.dirt_block",
                "item_spawn_weight": 100,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (0, 0),
                "item_slot_priority": 0,
                "once_per_instance": False,
            }
        ],
        "coin_spawn_range": (5000, 15000),
    },
]

PROJECTILE_DATA: list[ProjectileData] = [
    {"id": 0, "id_str": "projectile.INVALID"},
    {"id": 1, "id_str": "projectile.arrow"},
    {"id": 2, "id_str": "projectile.bullet"},
]

SOUND_DATA: list[SoundData] = [
    {"id": 0, "id_str": "sound.INVALID", "variation_paths": [], "volume": 1},
    {
        "id": 1,
        "id_str": "sound.tink",
        "variation_paths": [
            "assets/sounds/tink_0.wav",
            "assets/sounds/tink_1.wav",
            "assets/sounds/tink_2.wav",
        ],
        "volume": 1,
    },
    {
        "id": 2,
        "id_str": "sound.dig",
        "variation_paths": [
            "assets/sounds/dig_0.wav",
            "assets/sounds/dig_1.wav",
            "assets/sounds/dig_2.wav",
        ],
        "volume": 1,
    },
    {
        "id": 3,
        "id_str": "sound.jump",
        "variation_paths": ["assets/sounds/jump.wav"],
        "volume": 1,
    },
    {
        "id": 4,
        "id_str": "sound.player_hurt",
        "variation_paths": [
            "assets/sounds/player_hit_0.wav",
            "assets/sounds/player_hit_1.wav",
            "assets/sounds/player_hit_2.wav",
        ],
        "volume": 1,
    },
    {
        "id": 5,
        "id_str": "sound.grass",
        "variation_paths": ["assets/sounds/grass.wav"],
        "volume": 1,
    },
    {
        "id": 6,
        "id_str": "sound.player_death",
        "variation_paths": ["assets/sounds/player_killed.wav"],
        "volume": 1,
    },
    {
        "id": 7,
        "id_str": "sound.mirror",
        "variation_paths": ["assets/sounds/mirror.wav"],
        "volume": 0.1,
    },
    {
        "id": 8,
        "id_str": "sound.slime_hurt",
        "variation_paths": ["assets/sounds/npc_hit_0.wav"],
        "volume": 1,
    },
    {
        "id": 9,
        "id_str": "sound.slime_death",
        "variation_paths": ["assets/sounds/npc_killed_0.wav"],
        "volume": 1,
    },
    {
        "id": 10,
        "id_str": "sound.swing",
        "variation_paths": ["assets/sounds/swing.wav"],
        "volume": 1,
    },
    {
        "id": 11,
        "id_str": "sound.bow",
        "variation_paths": ["assets/sounds/bow.wav"],
        "volume": 1,
    },
    {
        "id": 12,
        "id_str": "sound.gun_shot",
        "variation_paths": ["assets/sounds/gun_shot.wav"],
        "volume": 0.2,
    },
    {
        "id": 13,
        "id_str": "sound.bullet_hit",
        "variation_paths": ["assets/sounds/bullet_hit.wav"],
        "volume": 1,
    },
    {
        "id": 14,
        "id_str": "sound.grab",
        "variation_paths": ["assets/sounds/grab.wav"],
        "volume": 1,
    },
    {
        "id": 15,
        "id_str": "sound.run",
        "variation_paths": [
            "assets/sounds/run_0.wav",
            "assets/sounds/run_1.wav",
            "assets/sounds/run_2.wav",
        ],
        "volume": 1,
    },
    {
        "id": 16,
        "id_str": "sound.coins",
        "variation_paths": ["assets/sounds/coins.wav"],
        "volume": 0.3,
    },
    {
        "id": 17,
        "id_str": "sound.menu_open",
        "variation_paths": ["assets/sounds/menu_open.wav"],
        "volume": 0.3,
    },
    {
        "id": 18,
        "id_str": "sound.menu_close",
        "variation_paths": ["assets/sounds/menu_close.wav"],
        "volume": 0.3,
    },
    {
        "id": 19,
        "id_str": "sound.menu_select",
        "variation_paths": ["assets/sounds/menu_select.wav"],
        "volume": 0.3,
    },
    {
        "id": 20,
        "id_str": "sound.chat",
        "variation_paths": ["assets/sounds/chat.wav"],
        "volume": 0.3,
    },
    {
        "id": 21,
        "id_str": "sound.door_opened",
        "variation_paths": ["assets/sounds/door_opened.wav"],
        "volume": 1,
    },
    {
        "id": 22,
        "id_str": "sound.door_closed",
        "variation_paths": ["assets/sounds/door_closed.wav"],
        "volume": 1,
    },
]

STRUCTURE_DATA: list[StructureData] = [
    {
        "id": 0,
        "id_str": "structure.INVALID",
        "name": "INVALID",
        "width": 0,
        "height": 0,
        "spawn_weight": 0,
        "tile_data": [],
    },
    {
        "id": 1,
        "id_str": "structure.mineshaft_top",
        "name": "Mineshaft Top",
        "width": 7,
        "height": 7,
        "spawn_weight": 0,
        "tile_data": [
            "--[0:tile.stone]----",
            "-[0:tile.stone][0:tile.stone;3:wall.wood][0:tile.door_wood_closed;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][1:0,-2;3:wall.wood][0:tile.stone;3:wall.stone]",
            "[0:tile.stone][0:tile.stone;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.stone][0:tile.stone;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood;4:mineshaft,Down]",
            "[0:tile.stone][0:tile.stone;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "-[0:tile.stone][0:tile.stone;3:wall.wood][0:tile.door_wood_closed;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][1:0,-2;3:wall.wood][0:tile.stone;3:wall.stone]",
            "--[0:tile.stone]----",
        ],
    },
    {
        "id": 2,
        "id_str": "structure.mineshaft_top_inner",
        "name": "Mineshaft Inner Top",
        "width": 5,
        "height": 10,
        "spawn_weight": 400,
        "tile_data": [
            "-[0:tile.stone][3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.wood][0:tile.stone;3:wall.wood][0:tile.stone;3:wall.wood][0:tile.stone;3:wall.wood][0:tile.stone;3:wall.stone]",
            "[0:tile.none]--[0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[3:wall.wood][3:wall.wood][0:tile.none][0:tile.none;3:wall.wood][0:tile.none][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood;4:mineshaft,Down]",
            "-[0:tile.none;3:wall.wood][3:wall.wood]-[0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.stone]-[3:wall.stone][0:tile.stone][3:wall.stone][0:tile.stone;3:wall.wood][0:tile.stone;3:wall.wood][0:tile.stone;3:wall.wood][0:tile.stone;3:wall.wood][0:tile.stone;3:wall.stone]",
        ],
    },
    {
        "id": 3,
        "id_str": "structure.mineshaft_main",
        "name": "Mineshaft Main",
        "width": 5,
        "height": 9,
        "spawn_weight": 500,
        "tile_data": [
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood;4:mineshaft,Up][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood;4:mineshaft,Down]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]",
        ],
    },
    {
        "id": 4,
        "id_str": "structure.mineshaft_door_left",
        "name": "Mineshaft Door Left",
        "width": 7,
        "height": 9,
        "spawn_weight": 100,
        "tile_data": [
            "----[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone;4:mineshaft,Left][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "----[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.door_wood_closed;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][1:0,-2;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood;4:mineshaft,Up][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood;4:mineshaft,Down]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]",
        ],
    },
    {
        "id": 5,
        "id_str": "structure.mineshaft_door_right",
        "name": "Mineshaft Door Right",
        "width": 7,
        "height": 9,
        "spawn_weight": 100,
        "tile_data": [
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood;4:mineshaft,Up][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood;4:mineshaft,Down]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.door_wood_closed;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][1:0,-2;3:wall.stone][0:tile.stone;3:wall.stone]",
            "----[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "----[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone;4:mineshaft,Right][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
        ],
    },
    {
        "id": 6,
        "id_str": "structure.mineshaft_room_left",
        "name": "Mineshaft Room Left",
        "width": 12,
        "height": 7,
        "spawn_weight": 100,
        "tile_data": [
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;2:loot.pot;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.chest_wood;1:0,0;2:loot.chest_wood;3:wall.stone][1:0,-1;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][1:-1,0;3:wall.stone][1:-1,-1;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.door_wood_closed;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][1:0,-2;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]-",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone;4:mineshaft,Right][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]-",
        ],
    },
    {
        "id": 7,
        "id_str": "structure.mineshaft_room_right",
        "name": "Mineshaft Room Right",
        "width": 12,
        "height": 7,
        "spawn_weight": 100,
        "tile_data": [
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone;4:mineshaft,Left][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]-",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]-",
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.door_wood_closed;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][1:0,-2;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.chest_wood;1:0,0;2:loot.chest_wood;3:wall.stone][1:0,-1;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][1:-1,0;3:wall.stone][1:-1,-1;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]",
        ],
    },
    {
        "id": 8,
        "id_str": "structure.mineshaft_corridor_a",
        "name": "Mineshaft Corridor A",
        "width": 14,
        "height": 7,
        "spawn_weight": 100,
        "tile_data": [
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone;4:mineshaft,Left][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]--",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]--",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]-",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.stone;3:wall.stone]-",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_tall_gray;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][0:tile.stone;3:wall.stone]-",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]-",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;2:loot.chest_wood;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_short_gray;3:wall.stone][0:tile.stone;3:wall.stone]-",
            "[0:tile.stone;3:wall.stone][0:tile.torch;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_thick_brown;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][1:-1,0;3:wall.stone][1:-1,-1;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_short_brown;3:wall.stone][0:tile.stone;3:wall.stone]",
            "--[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_tall_brown;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][0:tile.stone;3:wall.stone]",
            "--[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone;4:mineshaft,Right][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
        ],
    },
    {
        "id": 9,
        "id_str": "structure.mineshaft_corridor_b",
        "name": "Mineshaft Corridor B",
        "width": 14,
        "height": 7,
        "spawn_weight": 100,
        "tile_data": [
            "--[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone;4:mineshaft,Left][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "--[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_thick_brown;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][1:-1,0;3:wall.stone][1:-1,-1;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.torch;3:wall.stone][0:tile.none;2:loot.chest_wood;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]-",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_tall_gray;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][0:tile.stone;3:wall.stone]-",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_short_brown;3:wall.stone][0:tile.stone;3:wall.stone]-",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.stone;3:wall.stone]-",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]-",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]--",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone;4:mineshaft,Right][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]--",
        ],
    },
    {
        "id": 10,
        "id_str": "structure.mineshaft_corridor_c",
        "name": "Mineshaft Corridor C",
        "width": 17,
        "height": 6,
        "spawn_weight": 100,
        "tile_data": [
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone;4:mineshaft,Left][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_short_brown;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_thick_gray;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][1:-1,0;3:wall.stone][1:-1,-1;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.stone;2:loot.chest_wood;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_tall_gray;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.torch;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_tall_brown;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_gray;3:wall.wood][0:tile.wood;3:wall.wood]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone;4:mineshaft,Right][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]",
        ],
    },
    {
        "id": 11,
        "id_str": "structure.mineshaft_corridor_d",
        "name": "Mineshaft Corridor Trap",
        "width": 17,
        "height": 14,
        "spawn_weight": 100,
        "tile_data": [
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone;4:mineshaft,Left][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]--------",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_thick_gray;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][0:tile.stone;3:wall.stone]--------",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][1:-1,0;3:wall.stone][1:-1,-1;3:wall.stone][0:tile.stone;3:wall.stone]--------",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_tall_brown;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][0:tile.stone;3:wall.stone]--------",
            "-[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]--------",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]--------",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_short_gray;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.stone;2:loot.chest_wood;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.spike;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone]",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]--------",
            "-[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_tall_gray;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]--------",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_short_gray;3:wall.stone][0:tile.stone;3:wall.stone]--------",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.pot_tall_gray;1:0,0;3:wall.stone][1:0,-1;3:wall.stone][0:tile.stone;3:wall.stone]--------",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]--------",
            "-[0:tile.stone;3:wall.stone][0:tile.none;3:wall.stone][0:tile.none;3:wall.stone;4:mineshaft,Right][0:tile.none;3:wall.stone][0:tile.stone;3:wall.stone]--------",
        ],
    },
    {
        "id": 12,
        "id_str": "structure.mineshaft_bottom",
        "name": "Mineshaft Bottom",
        "width": 5,
        "height": 10,
        "spawn_weight": 100,
        "tile_data": [
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone]--[3:wall.stone][0:tile.stone]-",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none][3:wall.wood][0:tile.none]-[3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood;4:mineshaft,Up][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none][0:tile.none][3:wall.wood]--",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none]-[0:tile.none;3:wall.wood]-[0:tile.none;3:wall.wood]-",
            "[0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone;3:wall.stone][0:tile.stone][0:tile.stone;3:wall.stone]-[3:wall.stone]-",
        ],
    },
    {
        "id": 13,
        "id_str": "structure.tree_canopy_a",
        "name": "Tree Canopy A",
        "width": 5,
        "height": 5,
        "spawn_weight": 100,
        "tile_data": [
            "[0:tile.tree_canopy_a;1:0,0;2:loot.chest_wood][1:0,-1][1:0,-2][1:0,-3][1:0,-4]",
            "[1:-1,0][1:-1,-1][1:-1,-2][1:-1,-3][1:-1,-4]",
            "[1:-2,0][1:-2,-1][1:-2,-2][1:-2,-3][1:-2,-4;4:tree_trunk,Down]",
            "[1:-3,0][1:-3,-1][1:-3,-2][1:-3,-3][1:-3,-4]",
            "[1:-4,0][1:-4,-1][1:-4,-2][1:-4,-3][1:-4,-4]",
        ],
    },
    {
        "id": 14,
        "id_str": "structure.tree_trunk_a",
        "name": "Tree Trunk A",
        "width": 1,
        "height": 2,
        "spawn_weight": 100,
        "tile_data": ["[0:tile.trunk;4:tree_trunk,Up][0:tile.trunk;4:tree_trunk,Down]"],
    },
    {
        "id": 15,
        "id_str": "structure.tree_trunk_b",
        "name": "Tree Trunk B",
        "width": 5,
        "height": 3,
        "spawn_weight": 100,
        "tile_data": [
            "[0:tile.trunk;4:tree_trunk,Up][0:tile.trunk][0:tile.trunk;4:tree_trunk,Down]",
            "-[0:tile.leaves]-",
            "[0:tile.leaves][0:tile.leaves][0:tile.leaves]",
            "[0:tile.leaves][0:tile.leaves][0:tile.leaves]",
            "[0:tile.leaves][0:tile.leaves][0:tile.leaves]",
        ],
    },
    {
        "id": 16,
        "id_str": "structure.tree_trunk_c",
        "name": "Tree Trunk C",
        "width": 5,
        "height": 3,
        "spawn_weight": 100,
        "tile_data": [
            "[0:tile.leaves][0:tile.leaves][0:tile.leaves]",
            "[0:tile.leaves][0:tile.leaves][0:tile.leaves]",
            "[0:tile.leaves][0:tile.leaves][0:tile.leaves]",
            "-[0:tile.leaves]-",
            "[0:tile.trunk;4:tree_trunk,Up][0:tile.trunk][0:tile.trunk;4:tree_trunk,Down]",
        ],
    },
    {
        "id": 17,
        "id_str": "structure.tree_foot",
        "name": "Tree Foot",
        "width": 3,
        "height": 2,
        "spawn_weight": 100,
        "tile_data": [
            "-[0:tile.trunk]",
            "[0:tile.trunk;4:tree_trunk,Up][0:tile.trunk;4:tree_root,Down]",
            "-[0:tile.trunk]",
        ],
    },
    {
        "id": 18,
        "id_str": "structure.tree_root_a",
        "name": "Tree Root A",
        "width": 6,
        "height": 5,
        "spawn_weight": 100,
        "tile_data": [
            "--[0:tile.trunk]-[0:tile.trunk]",
            "-[0:tile.trunk]-[0:tile.trunk][0:tile.trunk]",
            "[0:tile.trunk;4:tree_root,Up][0:tile.trunk][0:tile.trunk]--",
            "--[0:tile.trunk]--",
            "-[0:tile.trunk]-[0:tile.trunk]-",
            "---[0:tile.trunk][0:tile.trunk]",
        ],
    },
    {
        "id": 19,
        "id_str": "structure.tree_root_b",
        "name": "Tree Root B",
        "width": 6,
        "height": 6,
        "spawn_weight": 100,
        "tile_data": [
            "-[0:tile.trunk]----",
            "--[0:tile.trunk][0:tile.trunk]--",
            "[0:tile.trunk;4:tree_root,Up][0:tile.trunk][0:tile.trunk]-[0:tile.trunk][0:tile.trunk]",
            "--[0:tile.trunk][0:tile.trunk]--",
            "--[0:tile.trunk]-[0:tile.trunk]-",
            "-[0:tile.trunk]-[0:tile.trunk]--",
        ],
    },
    {
        "id": 20,
        "id_str": "structure.tree_root_chest",
        "name": "Tree Root Chest",
        "width": 7,
        "height": 9,
        "spawn_weight": 100,
        "tile_data": [
            "---[0:tile.trunk]--[0:tile.trunk]--",
            "-[0:tile.trunk]--[0:tile.trunk][0:tile.trunk]---",
            "--[0:tile.trunk][0:tile.trunk][0:tile.trunk]-[0:tile.trunk][0:tile.trunk][0:tile.trunk]",
            "[0:tile.trunk;4:tree_root,Up][0:tile.trunk]-[0:tile.trunk][0:tile.chest_wood;1:0,0;2:loot.chest_wood][1:0,-1][0:tile.trunk]--",
            "-[0:tile.trunk][0:tile.trunk][0:tile.trunk][1:-1,0][1:-1,-1][0:tile.trunk]--",
            "[0:tile.trunk]-[0:tile.trunk]-[0:tile.trunk][0:tile.trunk]-[0:tile.trunk]-",
            "---[0:tile.trunk]--[0:tile.trunk]-[0:tile.trunk]",
        ],
    },
    {
        "id": 21,
        "id_str": "structure.underground_cabin_a",
        "name": "Underground Cabin A",
        "width": 20,
        "height": 8,
        "spawn_weight": 10,
        "tile_data": [
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_tall_gray;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood;4:underground_cabin,Up][0:tile.none;3:wall.wood][0:tile.painting_b;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.chest_wood;1:0,0;2:loot.chest_wood;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_brown;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_tall_gray;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_thick_brown;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.crafting_table_wood;1:0,0;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_c;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_brown;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][1:-2,0;3:wall.wood][1:-2,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood;4:underground_cabin,Down]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.door_wood_closed;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][1:0,-2;3:wall.wood][0:tile.wood;3:wall.wood]",
            "--[0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none]-",
            "-[0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none]-",
            "--[0:tile.none][0:tile.none][0:tile.none][0:tile.none]--",
        ],
    },
    {
        "id": 22,
        "id_str": "structure.underground_cabin_b",
        "name": "Underground Cabin B",
        "width": 20,
        "height": 8,
        "spawn_weight": 100,
        "tile_data": [
            "---[0:tile.none][0:tile.none][0:tile.none]--",
            "--[0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none]-",
            "---[0:tile.none][0:tile.none][0:tile.none][0:tile.none]-",
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.door_wood_closed;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][1:0,-2;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_brown;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_thick_gray;1:0,0;2:loot.chest_wood;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_gray;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_tall_gray;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_b;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood;4:underground_cabin,Down]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood]",
        ],
    },
    {
        "id": 23,
        "id_str": "structure.underground_cabin_c",
        "name": "Underground Cabin C",
        "width": 14,
        "height": 17,
        "spawn_weight": 10,
        "tile_data": [
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood;4:underground_cabin,Up][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_c;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_b;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-2,0;3:wall.wood][1:-2,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_a;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.door_wood_closed;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][1:0,-2;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][1:-2,0;3:wall.wood][1:-2,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood;4:underground_cabin,Down]",
            "--[0:tile.none][0:tile.none][0:tile.wood][0:tile.none][0:tile.none][0:tile.none][0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "--[0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood]",
            "-[0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none]--------",
            "-[0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none]--------",
            "--[0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none]---------",
        ],
    },
    {
        "id": 24,
        "id_str": "structure.underground_cabin_d",
        "name": "Underground Cabin D",
        "width": 16,
        "height": 11,
        "spawn_weight": 100,
        "tile_data": [
            "------[0:tile.none][0:tile.none][0:tile.none][0:tile.none]-",
            "-----[0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none]",
            "----[0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none]",
            "---[0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none]",
            "---[0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.none][0:tile.platform_wood][0:tile.none]-",
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.door_wood_closed;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][1:0,-2;3:wall.wood][0:tile.wood;3:wall.wood]--",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]--",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_b;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]--",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]--",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]--",
            "[0:tile.platform_wood;3:wall.wood;4:underground_cabin,Up][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_gray;3:wall.wood][0:tile.wood;3:wall.wood]--",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_a;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_tall_gray;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]--",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]--",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][1:-2,0;3:wall.wood][1:-2,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_brown;3:wall.wood][0:tile.wood;3:wall.wood]--",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]--",
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood]--",
        ],
    },
    {
        "id": 25,
        "id_str": "structure.underground_cabin_e",
        "name": "Underground Cabin E",
        "width": 17,
        "height": 9,
        "spawn_weight": 35,
        "tile_data": [
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_b;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.pot_short_gray;3:wall.wood][0:tile.platform_wood;3:wall.wood;4:underground_cabin,Down]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_tall_gray;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_a;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_thick_gray;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][1:-2,0;3:wall.wood][1:-2,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_gray;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_c;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.chest_wood;1:0,0;2:loot.chest_wood;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood;4:underground_cabin,Up][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-2,0;3:wall.wood][1:-2,-1;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_tall_gray;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood]",
        ],
    },
    {
        "id": 26,
        "id_str": "structure.underground_cabin_f",
        "name": "Underground Cabin F",
        "width": 13,
        "height": 8,
        "spawn_weight": 100,
        "tile_data": [
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_thick_gray;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_b;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood;4:underground_cabin,Down]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_tall_gray;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.crafting_table_wood;1:0,0;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_gray;3:wall.wood][1:-1,0;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_gray;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.door_wood_closed;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][1:0,-2;3:wall.wood][0:tile.wood;3:wall.wood]",
        ],
    },
    {
        "id": 27,
        "id_str": "structure.underground_cabin_g",
        "name": "Underground Cabin G",
        "width": 13,
        "height": 15,
        "spawn_weight": 20,
        "tile_data": [
            "-------[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood]",
            "-------[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_thick_gray;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "-------[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "-------[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_b;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood;4:underground_cabin,Down]",
            "-------[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_tall_gray;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_gray;3:wall.wood][0:tile.pot_short_gray;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.crafting_table_wood;1:0,0;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood;4:underground_cabin,Up][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_gray;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_gray;3:wall.wood][1:-1,0;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.painting_c;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-1,0;3:wall.wood][1:-1,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.pot_short_gray;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][1:-2,0;3:wall.wood][1:-2,-1;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.platform_wood;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.none;3:wall.wood][0:tile.wood;3:wall.wood]",
            "[0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.wood;3:wall.wood][0:tile.door_wood_closed;1:0,0;3:wall.wood][1:0,-1;3:wall.wood][1:0,-2;3:wall.wood][0:tile.wood;3:wall.wood]",
        ],
    },
]

TILE_DATA: list[
    TileData
    | DamagingTileData
    | MultitileData
    | DoorTileData
    | LootTileData
    | LootMultitileData
] = [
    {
        "id": 0,
        "id_str": "tile.UNNAMED",
        "name": "UNNAMED",
        "strength": 0,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": [],
        "light_reduction": 0,
        "light_emission": 0,
        "tags": [],
        "item_id_str": "item.INVALID",
        "item_count_range": (1, 1),
        "place_sound": "",
        "hit_sound": "",
        "image": pygame.Surface((0, 0)),
    },
    {
        "id": 1,
        "id_str": "tile.none",
        "name": "None",
        "strength": 0,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 10,
        "light_emission": 0,
        "tags": ["NO_COLLIDE", "NO_DRAW"],
        "item_id_str": "item.INVALID",
        "item_count_range": (0, 0),
        "place_sound": "",
        "hit_sound": "",
        "image": pygame.Surface((0, 0)),
    },
    {
        "id": 2,
        "id_str": "tile.dirt",
        "name": "Dirt",
        "strength": 1,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": [
            "tile.grass",
            "tile.sand",
            "tile.sandstone",
            "tile.snow",
            "tile.stone",
            "tile.trunk",
            "tile.wood",
        ],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": [],
        "item_id_str": "item.dirt_block",
        "item_count_range": (1, 1),
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/dirt.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 3,
        "id_str": "tile.stone",
        "name": "Stone",
        "strength": 3,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": ["tile.dirt", "tile.wood"],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": [],
        "item_id_str": "item.stone_block",
        "item_count_range": (1, 1),
        "place_sound": "sound.tink",
        "hit_sound": "sound.tink",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/stone.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 4,
        "id_str": "tile.grass",
        "name": "Grass",
        "strength": 0.5,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": ["tile.dirt", "tile.trunk"],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": [],
        "item_id_str": "item.dirt_block",
        "item_count_range": (1, 1),
        "place_sound": "sound.grass",
        "hit_sound": "sound.grass",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/grass.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 5,
        "id_str": "tile.sand",
        "name": "Sand",
        "strength": 0.5,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": ["tile.dirt"],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": [],
        "item_id_str": "item.sand",
        "item_count_range": (1, 1),
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/sand.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 6,
        "id_str": "tile.sandstone",
        "name": "Sandstone",
        "strength": 1.0,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": ["tile.dirt"],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": [],
        "item_id_str": "item.sandstone",
        "item_count_range": (1, 1),
        "place_sound": "sound.tink",
        "hit_sound": "sound.tink",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/sandstone.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 7,
        "id_str": "tile.snow",
        "name": "Snow",
        "strength": 0,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": ["tile.dirt", "tile.trunk", "tile.copper"],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": [],
        "item_id_str": "item.snow",
        "item_count_range": (1, 1),
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/snow.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 8,
        "id_str": "tile.ice",
        "name": "Ice",
        "strength": 1.0,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": ["tile.dirt"],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": [],
        "item_id_str": "item.ice",
        "item_count_range": (1, 1),
        "place_sound": "sound.tink",
        "hit_sound": "sound.tink",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/ice.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 9,
        "id_str": "tile.wood",
        "name": "Wood",
        "strength": 1.0,
        "strength_type": "AXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": ["tile.dirt", "tile.stone"],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": [],
        "item_id_str": "item.wood",
        "item_count_range": (1, 1),
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/wood.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 10,
        "id_str": "tile.trunk",
        "name": "Trunk",
        "strength": 5.0,
        "strength_type": "AXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": [
            "tile.dirt",
            "tile.grass",
            "tile.leaves",
            "tile.snow",
        ],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": ["NO_COLLIDE"],
        "item_id_str": "item.wood",
        "item_count_range": (1, 1),
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/trunk.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 11,
        "id_str": "tile.leaves",
        "name": "Leaves",
        "strength": 0.5,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": ["tile.dirt", "tile.trunk"],
        "light_reduction": 5,
        "light_emission": 0,
        "tags": ["NO_COLLIDE"],
        "item_id_str": "item.INVALID",
        "item_count_range": (1, 1),
        "place_sound": "sound.grass",
        "hit_sound": "sound.grass",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/leaves.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 12,
        "id_str": "tile.copper",
        "name": "Copper Ore",
        "strength": 3.0,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": ["tile.dirt", "tile.stone", "tile.snow"],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": [],
        "item_id_str": "item.copper_ore",
        "item_count_range": (1, 1),
        "place_sound": "sound.tink",
        "hit_sound": "sound.tink",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/copper_ore.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 13,
        "id_str": "tile.silver",
        "name": "Silver",
        "strength": 0,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": [],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": [],
        "item_id_str": "item.silver",
        "item_count_range": (1, 1),
        "place_sound": "sound.tink",
        "hit_sound": "sound.tink",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/silver.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 14,
        "id_str": "tile.spike",
        "name": "Spike",
        "strength": 1.0,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": ["DAMAGING", "TRANSPARENT"],
        "item_id_str": "item.spike",
        "item_count_range": (1, 1),
        "tile_damage": 50,
        "tile_damage_name": "spike",
        "place_sound": "sound.tink",
        "hit_sound": "sound.tink",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/spike.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 15,
        "id_str": "tile.torch",
        "name": "Torch",
        "strength": 1.0,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 0,
        "light_emission": 200,
        "tags": ["NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.torch",
        "item_count_range": (1, 1),
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/lamp.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 16,
        "id_str": "tile.platform_wood",
        "name": "Wood Platform",
        "strength": 1.0,
        "strength_type": "PICKAXE",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": ["PLATFORM", "TRANSPARENT"],
        "item_id_str": "item.wood_platform",
        "item_count_range": (1, 1),
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/platform_wood.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 17,
        "id_str": "tile.chest_wood",
        "name": "Chest",
        "strength": 2.0,
        "strength_type": "HAMMER",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": ["CHEST", "MULTITILE", "NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.wood_chest",
        "item_count_range": (1, 1),
        "multitile_dimensions": (2, 2),
        "multitile_required_solids": [(0, 2), (1, 2)],
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/chest_wood.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 18,
        "id_str": "tile.crafting_table_wood",
        "name": "Wood Crafting Table",
        "strength": 1.0,
        "strength_type": "HAMMER",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": ["WORKBENCH", "MULTITILE", "NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.workbench",
        "item_count_range": (1, 1),
        "multitile_dimensions": (2, 1),
        "multitile_required_solids": [(0, 1), (1, 1)],
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/crafting_table.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 19,
        "id_str": "tile.door_wood_open_left",
        "name": "Wood Door Open Left",
        "strength": 1.0,
        "strength_type": "HAMMER",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 10,
        "light_emission": 0,
        "tags": ["CYCLABLE", "MULTITILE", "NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.wood_door",
        "item_count_range": (1, 1),
        "cycle_facing_left_tile_id_str": "tile.door_wood_closed",
        "cycle_facing_left_tile_offset": [1, 0],
        "cycle_facing_left_sound": "sound.door_closed",
        "cycle_facing_right_tile_id_str": "tile.door_wood_closed",
        "cycle_facing_right_tile_offset": [1, 0],
        "cycle_facing_right_sound": "sound.door_closed",
        "multitile_dimensions": (2, 3),
        "multitile_required_solids": [(1, 3), (1, -1)],
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/door_wood_open_left.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 20,
        "id_str": "tile.door_wood_closed",
        "name": "Closed Wood Door",
        "strength": 1.0,
        "strength_type": "HAMMER",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 35,
        "light_emission": 0,
        "tags": ["CYCLABLE", "MULTITILE", "TRANSPARENT"],
        "item_id_str": "item.wood_door",
        "item_count_range": (1, 1),
        "cycle_facing_left_tile_id_str": "tile.door_wood_open_left",
        "cycle_facing_left_tile_offset": [-1, 0],
        "cycle_facing_left_sound": "sound.door_opened",
        "cycle_facing_right_tile_id_str": "tile.door_wood_open_right",
        "cycle_facing_right_tile_offset": [0, 0],
        "cycle_facing_right_sound": "sound.door_opened",
        "multitile_dimensions": (1, 3),
        "multitile_required_solids": [(0, 3), (0, -1)],
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/door_wood_closed.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 21,
        "id_str": "tile.door_wood_open_right",
        "name": "Wood Door Open Right",
        "strength": 1.0,
        "strength_type": "HAMMER",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 10,
        "light_emission": 0,
        "tags": ["CYCLABLE", "MULTITILE", "NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.wood_door",
        "item_count_range": (1, 1),
        "cycle_facing_left_tile_id_str": "tile.door_wood_closed",
        "cycle_facing_left_tile_offset": [0, 0],
        "cycle_facing_left_sound": "sound.door_closed",
        "cycle_facing_right_tile_id_str": "tile.door_wood_closed",
        "cycle_facing_right_tile_offset": [0, 0],
        "cycle_facing_right_sound": "sound.door_closed",
        "multitile_dimensions": (2, 3),
        "multitile_required_solids": [(0, 3), (0, -1)],
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/door_wood_open_right.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 22,
        "id_str": "tile.pot_tall_gray",
        "name": "Tall Gray Pot",
        "strength": 0.5,
        "strength_type": "DAMAGE",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": ["BREAKABLE", "MULTITILE", "NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.INVALID",
        "item_count_range": (0, 0),
        "loot_group_id_str": "loot.pot",
        "multitile_dimensions": (1, 2),
        "multitile_required_solids": [(0, 2)],
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/pot_tall_gray.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 23,
        "id_str": "tile.pot_tall_brown",
        "name": "Tall Brown Pot",
        "strength": 0.5,
        "strength_type": "DAMAGE",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": ["BREAKABLE", "MULTITILE", "NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.INVALID",
        "item_count_range": (0, 0),
        "loot_group_id_str": "loot.pot",
        "multitile_dimensions": (1, 2),
        "multitile_required_solids": [(0, 2)],
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/pot_tall_brown.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 24,
        "id_str": "tile.pot_thick_brown",
        "name": "thick Brown Pot",
        "strength": 0.5,
        "strength_type": "DAMAGE",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 0,
        "light_emission": 0,
        "tags": ["BREAKABLE", "MULTITILE", "NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.INVALID",
        "item_count_range": (0, 0),
        "multitile_dimensions": (2, 2),
        "multitile_required_solids": [(0, 2), (1, 2)],
        "loot_group_id_str": "loot.pot",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/pot_thick_brown.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 25,
        "id_str": "tile.pot_thick_gray",
        "name": "thick Gray Pot",
        "strength": 0.5,
        "strength_type": "DAMAGE",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 0,
        "light_emission": 0,
        "tags": ["BREAKABLE", "MULTITILE", "NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.INVALID",
        "item_count_range": (0, 0),
        "multitile_dimensions": (2, 2),
        "multitile_required_solids": [(0, 2), (1, 2)],
        "loot_group_id_str": "loot.pot",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/pot_thick_brown.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 26,
        "id_str": "tile.pot_short_gray",
        "name": "Short Gray Pot",
        "strength": 0.5,
        "strength_type": "DAMAGE",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": ["BREAKABLE", "NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.INVALID",
        "item_count_range": (0, 0),
        "loot_group_id_str": "loot.pot",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/pot_short_gray.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 27,
        "id_str": "tile.pot_short_brown",
        "name": "Short Brown Pot",
        "strength": 0.5,
        "strength_type": "DAMAGE",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": ["BREAKABLE", "NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.INVALID",
        "item_count_range": (0, 0),
        "loot_group_id_str": "loot.pot",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/pot_short_brown.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 28,
        "id_str": "tile.tree_canopy_a",
        "name": "Tree Canopy A",
        "strength": 0,
        "strength_type": "DAMAGE",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 0,
        "light_emission": 0,
        "tags": ["MULTITILE", "NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.wood",
        "item_count_range": (4, 20),
        "multitile_dimensions": (5, 5),
        "multitile_required_solids": [(2, 5)],
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/tree_canopy_a.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 29,
        "id_str": "tile.painting_a",
        "name": "Painting A",
        "strength": 0.5,
        "strength_type": "HAMMER",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": ["MULTITILE", "NO_COLLIDE"],
        "item_id_str": "item.painting_a",
        "item_count_range": (0, 0),
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "multitile_dimensions": (3, 2),
        "multitile_required_solids": [],
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/painting_a.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 30,
        "id_str": "tile.painting_b",
        "name": "Painting B",
        "strength": 0.5,
        "strength_type": "HAMMER",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": ["MULTITILE", "NO_COLLIDE"],
        "item_id_str": "item.painting_b",
        "item_count_range": (0, 0),
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "multitile_dimensions": (2, 2),
        "multitile_required_solids": [],
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/painting_b.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 31,
        "id_str": "tile.painting_c",
        "name": "Painting C",
        "strength": 0.5,
        "strength_type": "HAMMER",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 25,
        "light_emission": 0,
        "tags": ["MULTITILE", "NO_COLLIDE"],
        "item_id_str": "item.painting_c",
        "item_count_range": (0, 0),
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "multitile_dimensions": (3, 2),
        "multitile_required_solids": [],
        "image": pygame.transform.scale(
            pygame.image.load(
                "assets/images/tiles/multitiles/painting_c.png"
            ).convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 32,
        "id_str": "tile.mushroom",
        "name": "Mushroom",
        "strength": 0,
        "strength_type": "Pickaxe, Axe, Sword",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "light_reduction": 0,
        "light_emission": 0,
        "tags": ["NO_COLLIDE", "TRANSPARENT"],
        "item_id_str": "item.mushroom",
        "item_count_range": (1, 1),
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/tiles/mushroom.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
]

WALL_DATA: list[WallData] = [
    {
        "id": 0,
        "id_str": "wall.INVALID",
        "name": "INVALID",
        "mask_type": TileMaskType.NONE,
        "mask_merge_ids": [],
        "item_id_str": "item.INVALID",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.Surface((0, 0)),
    },
    {
        "id": 1,
        "id_str": "wall.none",
        "name": "None",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": [],
        "item_id_str": "item.INVALID",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.Surface((0, 0)),
    },
    {
        "id": 2,
        "id_str": "wall.dirt",
        "name": "Dirt Wall",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": [
            "wall.dirt",
            "wall.ice",
            "wall.hardened_sand",
            "wall.sandstone",
            "wall.snow",
            "wall.stone",
            "wall.wood",
        ],
        "item_id_str": "item.dirt_wall",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/walls/dirt.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 3,
        "id_str": "wall.stone",
        "name": "Stone",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": ["wall.dirt", "wall.snow", "wall.wood"],
        "item_id_str": "item.stone_wall",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/walls/stone.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 4,
        "id_str": "wall.ice",
        "name": "Ice",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": ["wall.snow"],
        "item_id_str": "item.ice_wall",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/walls/ice.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 5,
        "id_str": "wall.snow",
        "name": "Snow",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": [
            "wall.dirt",
            "wall.ice",
            "wall.sandstone",
            "wall.snow",
            "wall.stone",
            "wall.wood",
        ],
        "item_id_str": "item.snow_wall",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/walls/snow.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 6,
        "id_str": "wall.sandstone",
        "name": "Sandstone",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": ["wall.dirt", "wall.hardened_sand", "wall.snow"],
        "item_id_str": "item.sandstone_wall",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/walls/sandstone.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 7,
        "id_str": "wall.hardened_sand",
        "name": "Sand",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": [
            "wall.dirt",
            "wall.sandstone",
            "wall.snow",
            "wall.stone",
            "wall.wood",
        ],
        "item_id_str": "item.hardened_sand_wall",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/walls/hardened_sand.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
    {
        "id": 8,
        "id_str": "wall.wood",
        "name": "Wood",
        "mask_type": TileMaskType.NOISY,
        "mask_merge_ids": [
            "wall.dirt",
            "wall.hardened_sand",
            "wall.snow",
            "wall.stone",
        ],
        "item_id_str": "item.wood_wall",
        "place_sound": "sound.dig",
        "hit_sound": "sound.dig",
        "image": pygame.transform.scale(
            pygame.image.load("assets/images/walls/wood.png").convert_alpha(),
            (BLOCK_SIZE, BLOCK_SIZE),
        ),
    },
]

WORLD_GEN_DATA: list[WorldGenData] = [
    {"id": 0, "id_str": "world_gen.INVALID"},
    {"id": 1, "id_str": "world_gen.default"},
]
