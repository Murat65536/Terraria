import pygame
from typing import TextIO, Union
from datetime import datetime
pygame.init()

BLOCK_SIZE: int = 16
TARGET_FPS: int = 60
MOUSE_POSITION: tuple[int, int] = (0, 0)
TILE_POSITION_MOUSE_HOVERING: tuple[int, int] = (0, 0)
SHIFT_ACTIVE: bool = False

game_state: str = "MAIN_MENU"
game_sub_state: str = "MAIN"

# Config loading
config: TextIO = open("config.txt", "r")
configDataStr: list[str] = config.readlines()
configData: list[str] = []
for item in configDataStr:
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

font_file_path: str = r"assets/fonts/AndyBold.ttf"
SMALL_FONT: pygame.font.Font = pygame.font.Font(font_file_path, 10)
DEFAULT_FONT: pygame.font.Font = pygame.font.Font(font_file_path, 16)
MEDIUM_FONT: pygame.font.Font = pygame.font.Font(font_file_path, 22)
LARGE_FONT: pygame.font.Font = pygame.font.Font(font_file_path, 40)
EXTRA_LARGE_FONT: pygame.font.Font = pygame.font.Font(font_file_path, 50)

WAIT_TO_USE: bool = False

ENEMY_SPAWN_TICK: int = 0

MIN_ENEMY_SPAWN_TILES_X: int = int((WINDOW_WIDTH // BLOCK_SIZE) * 0.5)
MAX_ENEMY_SPAWN_TILES_X: int = int(MIN_ENEMY_SPAWN_TILES_X * 2)
MIN_ENEMY_SPAWN_TILES_Y: int = int((WINDOW_HEIGHT // BLOCK_SIZE) * 0.5)
MAX_ENEMY_SPAWN_TILES_Y: int = int(MIN_ENEMY_SPAWN_TILES_Y * 2)

# TODO Convert to tuple for better typing
player_data: list[Union[str, object, list[list[int | str]], list[list[int | str]], int, int, int, datetime, datetime]] = []

PLAYER_WIDTH: int = 26
PLAYER_HEIGHT: int = 48
PLAYER_ARM_LENGTH: int = 20

PLAYER_MODEL_DATA: list[list[int]] = []
PLAYER_MODEL = None
PLAYER_FRAMES = []
PLAYER_REACH = 8
PLAYER_MODEL_COLOR_INDEX: int = 0
TEXT_INPUT = ""

DEFAULT_PLAYER_MODEL = None

IS_HOLDING_ITEM = False
ITEM_HOLDING = None

PLAYER_SAVE_OPTIONS = []

OLD_TIME_MILLISECONDS = pygame.time.get_ticks()
DELTA_TIME = 0

CURRENT_SKY_LIGHTING = 255
CURRENT_TIME_STATE = None

WORLD_SAVE_OPTIONS = []