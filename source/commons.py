from datetime import datetime
from enum import Enum
from typing import TextIO, TypedDict

import pygame


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
    GRAPPLE = 12  # TODO The code for the grappling hook
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
    MULTI_TILE = 3
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


class PlayerAppearance(TypedDict):
    sex: int
    hair_id: int
    skin_color: pygame.Color
    hair_color: pygame.Color
    eye_color: pygame.Color
    shirt_color: pygame.Color
    undershirt_color: pygame.Color
    trouser_color: pygame.Color
    shoe_color: pygame.Color


class PlayerData(TypedDict):
    name: str
    model_appearance: PlayerAppearance
    hotbar: list[tuple[int, str, int, str]]
    inventory: list[tuple[int, str, int, str]]
    hp: int
    max_hp: int
    playtime: int
    creation_date: datetime
    last_played_date: datetime


pygame.init()

BLOCK_SIZE: int = 16
TARGET_FPS: int = 60
MOUSE_POSITION: tuple[int, int] = (0, 0)
HOVERED_TILE: tuple[int, int] = (0, 0)
SHIFT_ACTIVE: bool = False

game_state: str = "MAIN_MENU"
game_sub_state: str = "MAIN"

# Config loading
CONFIG: TextIO = open("config.txt", "r")
CONFIG_DATA: list[str] = CONFIG.readlines()
configData: list[str] = []
for item in CONFIG_DATA:
    item = item.split("=")
    configData.append(item[1][:-1])
WINDOW_WIDTH: int = int(configData[0].split(",")[0])
WINDOW_HEIGHT: int = int(configData[0].split(",")[1])
GRAVITY: float = 9.8 * BLOCK_SIZE * 0.666 * float(configData[1])  # 3 tiles = 1 meter
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

MIN_ENEMY_SPAWN_TILES_X: int = int(WINDOW_WIDTH // BLOCK_SIZE * 0.5)
MAX_ENEMY_SPAWN_TILES_X: int = MIN_ENEMY_SPAWN_TILES_X * 2
MIN_ENEMY_SPAWN_TILES_Y: int = int(WINDOW_HEIGHT // BLOCK_SIZE * 0.5)
MAX_ENEMY_SPAWN_TILES_Y: int = MIN_ENEMY_SPAWN_TILES_Y * 2

PLAYER_DATA: PlayerData = {
    "name": "",
    "model_appearance": {
        "sex": 0,
        "hair_id": 0,
        "skin_color": pygame.Color(0, 0, 0),
        "hair_color": pygame.Color(0, 0, 0),
        "eye_color": pygame.Color(0, 0, 0),
        "shirt_color": pygame.Color(0, 0, 0),
        "undershirt_color": pygame.Color(0, 0, 0),
        "trouser_color": pygame.Color(0, 0, 0),
        "shoe_color": pygame.Color(0, 0, 0),
    },
    "hotbar": [],
    "inventory": [],
    "hp": 0,
    "max_hp": 0,
    "playtime": 0,
    "creation_date": datetime(1, 1, 1),
    "last_played_date": datetime(1, 1, 1),
}
PLAYER_SAVE_OPTIONS: list[list[PlayerData]] = []

PLAYER_WIDTH: int = 30
PLAYER_HEIGHT: int = 50
PLAYER_ARM_LENGTH: int = 20

PLAYER_MODEL_DATA: list[list[int]] = []
PLAYER_FRAMES: pygame.Surface = pygame.Surface((0, 0))
PLAYER_REACH: int = 8
PLAYER_MODEL_COLOR_INDEX: int = 0
TEXT_INPUT: str = ""

is_holding_item: bool = False

OLD_TIME_MILLISECONDS: int = pygame.time.get_ticks()
DELTA_TIME: int = 0

CURRENT_SKY_LIGHTING: int = 255

WORLD_SAVE_OPTIONS: list[tuple[str, pygame.Surface]] = []
