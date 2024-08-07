import pygame
import commons

tile_masks = []
misc_gui = []
backgrounds = []
walls = []
projectiles = []
hair = []
special_tiles = []
torsos = []
slimes = []
large_backgrounds = []
menu_background = []


def load_tile_mask_surfaces():
	global tile_masks
	tile_mask_image = pygame.image.load("res/images/maskTileset.png").convert_alpha()
	tile_masks = []
	for j in range(5):
		for i in range(13):
			surf = pygame.Surface((8, 8), pygame.SRCALPHA)
			surf.blit(tile_mask_image, (-i * 9, -j * 9))
			surf = pygame.transform.scale(surf, (commons.BLOCK_SIZE, commons.BLOCK_SIZE))
			tile_masks.append(surf)


def load_misc_gui_surfaces():
	global misc_gui
	misc_gui = []
	misc_gui_image = pygame.image.load("res/images/miscGUI.png").convert()
	for j in range(1):
		for i in range(11):
			surf = pygame.Surface((48, 48))
			surf.set_colorkey((255, 0, 255))
			surf.blit(misc_gui_image, (-i * 48, -j * 48))
			misc_gui.append(surf)


def load_background_surfaces():
	global backgrounds
	background_image = pygame.image.load("res/images/backgrounds/forest_background.png").convert()
	backgrounds = []
	for i in range(9):
		surf = pygame.Surface((2048, 838))
		surf.blit(background_image, (-i, 0))
		surf = pygame.transform.scale(surf, (4096, 1676))
		backgrounds.append(surf)

def load_projectile_surfaces():
	global projectiles
	projectile_tileset_image = pygame.image.load("res/images/projectileTileset.png").convert()
	projectiles = []
	for j in range(10):
		for i in range(10):
			surf = pygame.Surface((16, 16))
			surf.blit(projectile_tileset_image, (-i * 16, -j * 16))
			surf.set_colorkey((255, 0, 255))
			projectiles.append(surf)


def load_hair_surfaces():
	global hair
	hair = []
	scale = 2
	hair_tileset_image = pygame.transform.scale(pygame.image.load("res/images/hairsTileset.png"), (int(22 * 10 * scale), int(24 * scale)))
	for i in range(10):
		surf = pygame.Surface((int(22 * scale), int(24 * scale)))
		surf.set_colorkey((255, 0, 255))
		surf.blit(hair_tileset_image, (-i * 22 * scale, 0))
		surf = pygame.transform.scale(surf, (int(20 * scale), int(24 * scale)))
		hair.append(surf)


def load_torso_surfaces():
	global torsos
	torsos = []
	scale = 2
	torso_tileset_image = pygame.transform.scale(pygame.image.load("res/images/torsoTileset.png"), (int(20 * 19 * scale), int(30 * 4 * scale)))
	for j in range(4):
		for i in range(19):
			surf = pygame.Surface((int(20 * scale), int(30 * scale)))
			surf.set_colorkey((255, 0, 255))
			surf.blit(torso_tileset_image, (-i * 20 * scale, -j * 30 * scale))
			torsos.append(surf)


def load_slime_surfaces():
	global slimes
	slimes = []
	scale = 2
	slime_tileset_image = pygame.transform.scale(pygame.image.load("res/images/slimeTileset.png"), (int(16 * 3 * scale), int(12 * 5 * scale)))
	for j in range(5):
		for i in range(3):
			surf = pygame.Surface((int(16 * scale), int(12 * scale)))
			surf.set_colorkey((255, 0, 255))
			surf.blit(slime_tileset_image, (-i * 16 * scale, -j * 12 * scale))
			surf.set_alpha(200)
			slimes.append(surf)


def compile_background_images():  # creates a larger surf compiled with background surfs
	global large_backgrounds
	large_backgrounds = []
	for k in range(9):
		large_background = pygame.Surface((commons.WINDOW_WIDTH + 2048, commons.WINDOW_HEIGHT + 838))
		for i in range(int(commons.WINDOW_WIDTH / 2048 + 1)):
			for j in range(int(commons.WINDOW_HEIGHT / 838 + 1)):
				large_background.blit(backgrounds[k], (i * 2048, j * 838))
		large_backgrounds.append(large_background)
		

load_tile_mask_surfaces()
load_misc_gui_surfaces()
load_background_surfaces()
load_projectile_surfaces()
load_hair_surfaces()
load_torso_surfaces()
load_slime_surfaces()
compile_background_images()
