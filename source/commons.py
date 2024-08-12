import pygame
pygame.init()

BLOCK_SIZE = 16
TARGET_FPS = 60
MOUSE_POSITION = (0, 0)
TILE_POSITION_MOUSE_HOVERING = (0, 0)
SHIFT_ACTIVE = False

GAME_STATE = "MAINMENU"
GAME_SUB_STATE = "MAIN"
GAME_SUB_STATE_STACK = []

# Config loading
config = open("config.txt", "r")
configDataStr = config.readlines()
configData = []
for item in configDataStr:
	item = item.split("=")
	configData.append(item[1][:-1])
WINDOW_WIDTH = int(configData[0].split(",")[0])
WINDOW_HEIGHT = int(configData[0].split(",")[1])
GRAVITY = 9.8 * BLOCK_SIZE * 0.666 * float(configData[1])  # 3 tiles = 1 metre
RUN_FULLSCREEN = bool(int(configData[2]))
PARTICLES = bool(int(configData[3]))
PARTICLE_DENSITY = float(configData[4])
MUSIC = bool(int(configData[5]))
CONFIG_MUSIC_VOLUME = float(configData[6])
SOUND = bool(int(configData[7]))
CONFIG_SOUND_VOLUME = float(configData[8])
CREATIVE = bool(int(configData[9]))
BACKGROUND = bool(int(configData[10]))
PARALLAX_AMOUNT = float(configData[11])
PASSIVE = bool(int(configData[12]))
MAX_ENEMY_SPAWNS = int(configData[13])
FANCY_TEXT = bool(int(configData[14]))
HITBOXES = bool(int(configData[15]))
SPLASHSCREEN = bool(int(configData[16]))
AUTO_SAVE_FREQUENCY = float(configData[17])
EXPERIMENTAL_LIGHTING = bool(int(configData[18]))
SMOOTH_CAM = bool(int(configData[19]))
DRAW_UI = bool(int(configData[20]))

if RUN_FULLSCREEN:
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
else:
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

font_file_path = r"res/fonts/AndyBold.ttf"
SMALL_FONT = pygame.font.Font(font_file_path, 10)
DEFAULT_FONT = pygame.font.Font(font_file_path, 16)
MEDIUM_FONT = pygame.font.Font(font_file_path, 22)
LARGE_FONT = pygame.font.Font(font_file_path, 40)
EXTRA_LARGE_FONT = pygame.font.Font(font_file_path, 50)

WAIT_TO_USE = False

ENEMY_SPAWN_TICK = 0

MIN_ENEMY_SPAWN_TILES_X = int((WINDOW_WIDTH // BLOCK_SIZE) * 0.5)
MAX_ENEMY_SPAWN_TILES_X = int(MIN_ENEMY_SPAWN_TILES_X * 2)
MIN_ENEMY_SPAWN_TILES_Y = int((WINDOW_HEIGHT // BLOCK_SIZE) * 0.5)
MAX_ENEMY_SPAWN_TILES_Y = int(MIN_ENEMY_SPAWN_TILES_Y * 2)

PLAYER_DATA = []

PLAYER_WIDTH = 26
PLAYER_HEIGHT = 48
PLAYER_ARM_LENGTH = 20

PLAYER_MODEL_DATA = []
PLAYER_MODEL = None
PLAYER_FRAMES = []
PLAYER_REACH = 8
PLAYER_MODEL_COLOR_INDEX = 0
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