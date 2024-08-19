import pygame
import random
import os
import sys
import pickle
import webbrowser
import datetime
from pygame.locals import Rect
from enum import Enum
import player

import commons
import game_data
import prompt
import world

import entity_manager
import surface_manager
import shared_methods


class Type(Enum):
	TEXT = 1,
	BUTTON = 2

class MenuButtons(Enum):
	SINGLE_PLAYER = 1,
	CREDITS = 2,
	CHANGES = 3,
	SETTINGS = 4,
	EXIT = 5

class PlayerSelectionButtons(Enum):
	NEW_PLAYER = 1,
	BACK = 2

class PlayerCreationButtons(Enum):
	HAIR_TYPE = 1,
	HAIR_COLOR = 2,
	EYE_COLOR = 3,
	SKIN_COLOR = 4,
	CLOTHES = 5,
	CREATE = 6,
	RANDOMIZE = 7,
	BACK = 8

class ColorPickerButtons(Enum):
	BACK = 1

class ClothesButtons(Enum):
	SHIRT_COLOR = 1,
	UNDERSHIRT_COLOR = 2,
	TROUSER_COLOR = 3,
	SHOE_COLOR = 4,
	BACK = 5

class PlayerNamingButtons(Enum):
	SET_NAME = 1,
	BACK = 2

class WorldSelectionButtons(Enum):
	NEW_WORLD = 1,
	BACK = 2

class WorldCreationButtons(Enum):
	TINY = 1,
	SMALL = 2,
	MEDIUM = 3,
	LARGE = 4,
	BACK = 5

class WorldNamingButtons(Enum):
	SET_NAME = 1,
	BACK = 2

class CreditsButton(Enum):
	BACK = 1

class ChangesButtons(Enum):
	GITHUB = 1,
	TRELLO = 2,
	BACK = 3

class SettingsButtons(Enum):
	BACK = 1



"""================================================================================================================= 
	menu_manager.MenuButton

	Stores information about a single button, the visibility of a given button is set by the active_menu_buttons
	table
-----------------------------------------------------------------------------------------------------------------"""
class MenuButton:
	def __init__(self, text: str, position: tuple[float, float], font, click_sound_id, type: Type, color=(153, 153, 153), outline_color=(0, 0, 0), function=None):
		self.text = text
		self.position = position
		self.type = type
		self.color = color
		self.function = function
		self.text_surface = shared_methods.outline_text(text, self.color, font, outline_color)
		if self.type == Type.BUTTON:
			self.alt_text_surface = shared_methods.outline_text(text, (255, 255, 0), font)
		self.rect = Rect(self.position[0] - self.text_surface.get_width() * 0.5, self.position[1] - self.text_surface.get_height() * 0.5, self.text_surface.get_width(), self.text_surface.get_height())
		self.hovered = False
		self.clicked = False
		self.click_sound_id = click_sound_id
		self.active = False

	"""================================================================================================================= 
		menu_manager.MenuButton.update -> void

		Checks to see if the mouse is interacting with the button instance, performing all the related logic
	-----------------------------------------------------------------------------------------------------------------"""
	def update(self):
		if self.type == Type.BUTTON:
			if self.rect.collidepoint(commons.MOUSE_POSITION):
				if not self.hovered:
					game_data.play_sound("sound.menu_select")
					self.hovered = True
				if pygame.mouse.get_pressed()[0] and not commons.WAIT_TO_USE:
					commons.WAIT_TO_USE = True
					self.clicked = True
					if self.text == "Back":
						game_data.play_sound("sound.menu_close")
					else:
						game_data.play_sound("sound.menu_open")
			else:
				self.hovered = False
				self.clicked = False

	"""================================================================================================================= 
		menu_manager.MenuButton.draw -> void

		Draws the button's text surface or alt_text_surface depending on the hover state of the button
	-----------------------------------------------------------------------------------------------------------------"""
	def draw(self):
		if not self.hovered:
			if self.text == "Terraria":
				commons.screen.blit(self.text_surface, (self.rect.left, self.rect.top + 3))
			commons.screen.blit(self.text_surface, (self.rect.left, self.rect.top))
		else:
			commons.screen.blit(self.alt_text_surface, (self.rect.left, self.rect.top))




"""================================================================================================================= 
	menu_manager.update_active_menu_buttons -> void

	Sets the active state of all buttons to false and then re-adds buttons based on the current game sub state 
	and data in the 'active_menu_buttons' table
-----------------------------------------------------------------------------------------------------------------"""
def update_active_menu_buttons():
	for menu in active_menu_buttons:
		for text in active_menu_buttons[menu]:
			text.active = False
	
	for menu in active_menu_buttons:
		if commons.game_sub_state == menu:
			for text in active_menu_buttons[menu]:
				text.active = True
			break



"""================================================================================================================= 
	menu_manager.update_menu_buttons -> void

	Calls update on all active button instances, handles unique button press logic
-----------------------------------------------------------------------------------------------------------------"""
def update_menu_buttons():
	for menu in active_menu_buttons:
		for text in active_menu_buttons[menu]:
			if text.active:
				text.update()

				if text.clicked:
					text.clicked = False

					temp_game_sub_state = commons.game_sub_state
					# TODO Continue adding more enums and linking the buttons to them instead of the text. Also make the menu buttons able to be in any order.
					# Note: Since detection is occurring with the function parameter instead of the text parameter, the back button will need to be placed for every menu. This may allow for the game_sub_state_stack to be removed, significantly decreasing the complexity.
					if text.function == MenuButtons.SINGLE_PLAYER:
						commons.game_sub_state = "PLAYER_SELECTION"
						load_menu_player_data()

					elif text.function == MenuButtons.CREDITS:
						commons.game_sub_state = "CREDITS"

					elif text.function == MenuButtons.CHANGES:
						commons.game_sub_state = "CHANGES"

					elif text.function == MenuButtons.SETTINGS:
						commons.game_sub_state = "SETTINGS"

					elif text.function == MenuButtons.EXIT:
						pygame.quit()
						sys.exit()
					
					elif text.function == PlayerSelectionButtons.NEW_PLAYER:
						commons.game_sub_state = "PLAYER_CREATION"
						commons.PLAYER_MODEL_DATA = [0, 0,
													[(127, 72, 36), None, None],
													[(0, 0, 0), None, None],
													[(0, 0, 0), None, None],
													[(95, 125, 127), None, None],
													[(48, 76, 127), None, None],
													[(129, 113, 45), None, None],
													[(80, 100, 45), None, None]]
						commons.PLAYER_MODEL = player.Model(commons.PLAYER_MODEL_DATA[0], commons.PLAYER_MODEL_DATA[1],
															commons.PLAYER_MODEL_DATA[2][0],
															commons.PLAYER_MODEL_DATA[3][0],
															commons.PLAYER_MODEL_DATA[4][0],
															commons.PLAYER_MODEL_DATA[5][0],
															commons.PLAYER_MODEL_DATA[6][0],
															commons.PLAYER_MODEL_DATA[7][0],
															commons.PLAYER_MODEL_DATA[8][0])
						commons.PLAYER_FRAMES = player.render_sprites(commons.PLAYER_MODEL, directions=1, arm_frame_count=1, torso_frame_count=1)

					elif text.function == PlayerSelectionButtons.BACK:
						commons.game_sub_state = commons.game_sub_state_stack.pop()
					
					elif text.function == PlayerCreationButtons.HAIR_TYPE:
						assert commons.PLAYER_MODEL is not None
						if commons.PLAYER_MODEL.hair_id < 163:
							commons.PLAYER_MODEL.hair_id += 1
						else:
							commons.PLAYER_MODEL.hair_id = 0
						commons.PLAYER_MODEL_DATA[1] = commons.PLAYER_MODEL.hair_id
						commons.PLAYER_FRAMES = player.render_sprites(commons.PLAYER_MODEL, directions=1, arm_frame_count=1, torso_frame_count=1)

					elif text.function == PlayerCreationButtons.HAIR_COLOR:
						commons.game_sub_state = "COLOR_PICKER"
						commons.PLAYER_MODEL_COLOR_INDEX = 3

					elif text.function == PlayerCreationButtons.EYE_COLOR:
						commons.game_sub_state = "COLOR_PICKER"
						commons.PLAYER_MODEL_COLOR_INDEX = 4

					elif text.function == PlayerCreationButtons.SKIN_COLOR:
						commons.game_sub_state = "COLOR_PICKER"
						commons.PLAYER_MODEL_COLOR_INDEX = 2

					elif text.function == PlayerCreationButtons.CLOTHES:
						commons.game_sub_state = "CLOTHES"


					elif text.function == PlayerCreationButtons.CREATE:
						commons.game_sub_state = "PLAYER_NAMING"
						commons.TEXT_INPUT = ""

					elif text.function == PlayerCreationButtons.RANDOMIZE:
						commons.PLAYER_MODEL_DATA = [0, random.randint(0, 8),
							[(random.randint(0, 128), random.randint(0, 128), random.randint(0, 128)), None, None],
							[(random.randint(0, 128), random.randint(0, 128), random.randint(0, 128)), None, None],
							[(random.randint(0, 128), random.randint(0, 128), random.randint(0, 128)), None, None],
							[(random.randint(0, 128), random.randint(0, 128), random.randint(0, 128)), None, None],
							[(random.randint(0, 128), random.randint(0, 128), random.randint(0, 128)), None, None],
							[(random.randint(0, 128), random.randint(0, 128), random.randint(0, 128)), None, None],
							[(random.randint(0, 128), random.randint(0, 128), random.randint(0, 128)), None, None],
							[(random.randint(0, 128), random.randint(0, 128), random.randint(0, 128)), None, None]
						]
						player.update_player_model_using_model_data()
						commons.PLAYER_FRAMES = player.render_sprites(commons.PLAYER_MODEL, directions=1, arm_frame_count=1, torso_frame_count=1)

					elif text.function == PlayerCreationButtons.BACK:
						commons.game_sub_state = commons.game_sub_state_stack.pop()
					
					elif text.function == ColorPickerButtons.BACK:
						commons.game_sub_state = commons.game_sub_state_stack.pop()

					elif text.function == ClothesButtons.SHIRT_COLOR:
						commons.game_sub_state = "COLOR_PICKER"
						commons.PLAYER_MODEL_COLOR_INDEX = 5

					elif text.function == ClothesButtons.UNDERSHIRT_COLOR:
						commons.game_sub_state = "COLOR_PICKER"
						commons.PLAYER_MODEL_COLOR_INDEX = 6

					elif text.function == ClothesButtons.TROUSER_COLOR:
						commons.game_sub_state = "COLOR_PICKER"
						commons.PLAYER_MODEL_COLOR_INDEX = 7

					elif text.function == ClothesButtons.SHOE_COLOR:
						commons.game_sub_state = "COLOR_PICKER"
						commons.PLAYER_MODEL_COLOR_INDEX = 8

					elif text.function == ClothesButtons.BACK:
						commons.game_sub_state = commons.game_sub_state_stack.pop()

					elif text.function == PlayerNamingButtons.SET_NAME:
						date = datetime.datetime.now()
						commons.player_data = [commons.TEXT_INPUT, commons.PLAYER_MODEL, None, None, 100, 100, 0, date, date]  # Create player array
						pickle.dump(commons.player_data, open("assets/players/" + commons.TEXT_INPUT + ".player", "wb"))  # Save player array
						commons.game_sub_state = "PLAYER_SELECTION"
						load_menu_player_data()

					elif text.function == PlayerNamingButtons.BACK:
						commons.game_sub_state = commons.game_sub_state_stack.pop()

					elif text.function == WorldSelectionButtons.NEW_WORLD:
						commons.game_sub_state = "WORLD_CREATION"

					elif text.function == WorldSelectionButtons.BACK:
						commons.game_sub_state = commons.game_sub_state_stack.pop()

					elif text.function == WorldCreationButtons.TINY:
						commons.game_sub_state = "WORLD_NAMING"
						commons.TEXT_INPUT = ""
						world.WORLD_SIZE_X = 100
						world.WORLD_SIZE_Y = 350

					elif text.function == WorldCreationButtons.SMALL:
						commons.game_sub_state = "WORLD_NAMING"
						commons.TEXT_INPUT = ""
						world.WORLD_SIZE_X = 200
						world.WORLD_SIZE_Y = 400

					elif text.function == WorldCreationButtons.MEDIUM:
						commons.game_sub_state = "WORLD_NAMING"
						commons.TEXT_INPUT = ""
						world.WORLD_SIZE_X = 400
						world.WORLD_SIZE_Y = 450

					elif text.function == WorldCreationButtons.LARGE:
						commons.game_sub_state = "WORLD_NAMING"
						commons.TEXT_INPUT = ""
						world.WORLD_SIZE_X = 700
						world.WORLD_SIZE_Y = 550

					elif text.function == WorldCreationButtons.BACK:
						commons.game_sub_state = commons.game_sub_state_stack.pop()

					elif text.function == WorldNamingButtons.SET_NAME:
						world.SET_NAME = commons.TEXT_INPUT
						world.generate_terrain("DEFAULT", blit_progress=True)
						world.save()
						commons.game_sub_state = "WORLD_SELECTION"
						load_menu_player_data()

					elif text.function == WorldNamingButtons.BACK:
						commons.game_sub_state = commons.game_sub_state_stack.pop()

					elif text.function == CreditsButton.BACK:
						commons.game_sub_state = commons.game_sub_state_stack.pop()

					elif text.function == ChangesButtons.GITHUB:
						entity_manager.client_prompt = prompt.Prompt("browser opened", "GitHub page opened in a new tab.", size=(5, 2))
						webbrowser.open("https://github.com/Murat65536/Terraria")

					elif text.function == ChangesButtons.TRELLO:
						entity_manager.client_prompt = prompt.Prompt("browser opened", "Trello board opened in a new tab.", size=(5, 2))
						webbrowser.open("https://trello.com/b/tI74vC1t/terraria-trello-board")
					
					elif text.function == ChangesButtons.BACK:
						commons.game_sub_state = commons.game_sub_state_stack.pop()
					
					elif text.function == SettingsButtons.BACK:
						commons.game_sub_state = commons.game_sub_state_stack.pop()

					if commons.game_sub_state == "COLOR_PICKER":
						if commons.PLAYER_MODEL_DATA[commons.PLAYER_MODEL_COLOR_INDEX][1] is not None:
							entity_manager.client_color_picker.selected_color = tuple(commons.PLAYER_MODEL_DATA[commons.PLAYER_MODEL_COLOR_INDEX][0])
						entity_manager.client_color_picker.selected_x = commons.PLAYER_MODEL_DATA[commons.PLAYER_MODEL_COLOR_INDEX][1]
						entity_manager.client_color_picker.selected_y = commons.PLAYER_MODEL_DATA[commons.PLAYER_MODEL_COLOR_INDEX][2]

					# Update last game sub state variable is the sub state changed
					if temp_game_sub_state != commons.game_sub_state:
						if text.text != "Back":
							commons.game_sub_state_stack.append(temp_game_sub_state)

						if text.function == PlayerNamingButtons.SET_NAME:
							commons.game_sub_state_stack = commons.game_sub_state_stack[:1]

						if text.function == WorldNamingButtons.SET_NAME:
							commons.game_sub_state_stack = commons.game_sub_state_stack[:2]

					update_active_menu_buttons()


"""================================================================================================================= 
	menu_manager.draw_menu_buttons -> void

	Calls draw on all active button instances
-----------------------------------------------------------------------------------------------------------------"""
def draw_menu_buttons():
	for menu in active_menu_buttons:
		for text in active_menu_buttons[menu]:
			if text.active:
				text.draw()


"""================================================================================================================= 
	menu_manager.load_menu_player_data -> void

	Loads all player save metadata and creates a surface for each one
-----------------------------------------------------------------------------------------------------------------"""
def load_menu_player_data():
	path = "assets/players"
	if not os.path.exists(path):
		os.makedirs(path)
	possible_loads = os.listdir(path)  # Get filenames
	commons.PLAYER_SAVE_OPTIONS = []

	for i in range(len(possible_loads)):
		dat = pickle.load(open("assets/players/" + possible_loads[i], "rb"))
		possible_loads[i] = possible_loads[i][:-7]
		player_data_surf = pygame.Surface((315, 60))
		player_data_surf.fill((50, 50, 50))
		pygame.draw.rect(player_data_surf, (60, 60, 60), Rect(0, 0, 315, 60), 4)
		player_data_surf.blit(shared_methods.outline_text(dat[0], (255, 255, 255), commons.DEFAULT_FONT), (5, 3))  # Name
		player_data_surf.blit(shared_methods.outline_text("Created: ", (255, 255, 255), commons.DEFAULT_FONT), (5, 20))  # Creation date
		player_data_surf.blit(shared_methods.outline_text("Playtime: ", (255, 255, 255), commons.DEFAULT_FONT), (5, 40))  # Playtime
		player_data_surf.blit(shared_methods.outline_text(str(dat[7])[:19], (230, 230, 0), commons.DEFAULT_FONT), (80, 20))  # Creation date
		player_data_surf.blit(shared_methods.outline_text(str(dat[5]) + "HP", (230, 10, 10), commons.DEFAULT_FONT, outline_color=(128, 5, 5)), (155, 3))  # hp
		player_data_surf.blit(shared_methods.outline_text("100MNA", (80, 102, 244), commons.DEFAULT_FONT, outline_color=(30, 41, 122)), (205, 3))  # mana
		player_data_surf.blit(shared_methods.outline_text(str(int((dat[6] / 60) // 60)) + ":" + str(int(dat[6] // 60 % 60)).zfill(2) + ":" + str(int(dat[6] % 60)).zfill(2), (230, 230, 0), commons.DEFAULT_FONT), (90, 40))  # playtime
		sprites = player.render_sprites(dat[1], directions=1, arm_frame_count=1, torso_frame_count=1)
		player_data_surf.blit(sprites[0][0], (270, 0))
		player_data_surf.blit(sprites[1][0], (270, 0))
		commons.PLAYER_SAVE_OPTIONS.append([dat, player_data_surf])


"""================================================================================================================= 
	menu_manager.load_menu_world_data -> void

	Loads all world save metadata and creates a surface for each one
-----------------------------------------------------------------------------------------------------------------"""
def load_menu_world_data():
	path = "assets/worlds"
	if not os.path.exists(path):
		os.makedirs(path)
	possible_loads = os.listdir(path)  # Get filenames
	commons.WORLD_SAVE_OPTIONS = []
	for i in range(len(possible_loads)):
		if possible_loads[i][-3:] == "dat":  # if it's a dat file
			world.load(possible_loads[i][:-4], load_all=False)

			world_data_surf = pygame.Surface((315, 60))
			world_data_surf.fill((50, 50, 50))
			pygame.draw.rect(world_data_surf, (60, 60, 60), Rect(0, 0, 315, 60), 4)

			world_data_surf.blit(shared_methods.outline_text(world.world.name, (255, 255, 255), commons.DEFAULT_FONT), (5, 3))  # name
			world_data_surf.blit(shared_methods.outline_text("Created: ", (255, 255, 255), commons.DEFAULT_FONT), (5, 20))  # Creation date
			world_data_surf.blit(shared_methods.outline_text("Playtime: ", (255, 255, 255), commons.DEFAULT_FONT), (5, 40))  # Playtime
			world_data_surf.blit(shared_methods.outline_text(world.world.get_creation_date_string(), (230, 230, 0), commons.DEFAULT_FONT), (80, 20))  # Creation date
			world_data_surf.blit(shared_methods.outline_text(str(int((world.world.play_time / 60) // 60)) + ":" + str(int(world.world.play_time // 60 % 60)).zfill(2) + ":" + str(int(world.world.play_time % 60)).zfill(2), (230, 230, 0), commons.DEFAULT_FONT), (90, 40))  # playtime

			world_data_surf.blit(surface_manager.misc_gui[10], (260, 7))

			commons.WORLD_SAVE_OPTIONS.append([world.world.name, world_data_surf])

active_menu_buttons = {
	"MAIN": [
		MenuButton("Single Player", (commons.WINDOW_WIDTH * 0.5, 250), commons.LARGE_FONT, 24, Type.BUTTON, function=MenuButtons.SINGLE_PLAYER),
		MenuButton("Credits", (commons.WINDOW_WIDTH * 0.5, 305), commons.LARGE_FONT, 24, Type.BUTTON, function=MenuButtons.CREDITS),
		MenuButton("Changes", (commons.WINDOW_WIDTH * 0.5, 360), commons.LARGE_FONT, 24, Type.BUTTON, function=MenuButtons.CHANGES),
		MenuButton("Settings", (commons.WINDOW_WIDTH * 0.5, 415), commons.LARGE_FONT, 24, Type.BUTTON, function=MenuButtons.SETTINGS),
		MenuButton("Exit", (commons.WINDOW_WIDTH * 0.5, 470), commons.LARGE_FONT, 25, Type.BUTTON, function=MenuButtons.EXIT)
	],
	"PLAYER_SELECTION": [
		MenuButton("Select Player", (commons.WINDOW_WIDTH * 0.5, 90), commons.LARGE_FONT, 24, Type.TEXT),
		MenuButton("New Player", (commons.WINDOW_WIDTH * 0.5, 530), commons.LARGE_FONT, 24, Type.BUTTON, function=PlayerSelectionButtons.NEW_PLAYER),
		MenuButton("Back", (commons.WINDOW_WIDTH * 0.5, 570), commons.LARGE_FONT, 25, Type.BUTTON, function=PlayerSelectionButtons.BACK)
	],
	"PLAYER_CREATION": [
		MenuButton("Hair Type", (commons.WINDOW_WIDTH * 0.5, 200), commons.LARGE_FONT, 26, Type.BUTTON, function=PlayerCreationButtons.HAIR_TYPE),
		MenuButton("Hair Color", (commons.WINDOW_WIDTH * 0.5, 240), commons.LARGE_FONT, 24, Type.BUTTON, function=PlayerCreationButtons.HAIR_COLOR),
		MenuButton("Eye Color", (commons.WINDOW_WIDTH * 0.5, 280), commons.LARGE_FONT, 24, Type.BUTTON, function=PlayerCreationButtons.EYE_COLOR),
		MenuButton("Skin Color", (commons.WINDOW_WIDTH * 0.5, 320), commons.LARGE_FONT, 24, Type.BUTTON, function=PlayerCreationButtons.SKIN_COLOR),
		MenuButton("Clothes", (commons.WINDOW_WIDTH * 0.5, 360), commons.LARGE_FONT, 24, Type.BUTTON, function=PlayerCreationButtons.CLOTHES),
		MenuButton("Create", (commons.WINDOW_WIDTH * 0.5, 450), commons.LARGE_FONT, 24, Type.BUTTON, function=PlayerCreationButtons.CREATE),
		MenuButton("Randomize", (commons.WINDOW_WIDTH * 0.5, 490), commons.LARGE_FONT, 26, Type.BUTTON, function=PlayerCreationButtons.RANDOMIZE),
		MenuButton("Back", (commons.WINDOW_WIDTH * 0.5, 570), commons.LARGE_FONT, 25, Type.BUTTON, function=PlayerCreationButtons.BACK)
	],
	"COLOR_PICKER": [
		MenuButton("Back", (commons.WINDOW_WIDTH * 0.5, 570), commons.LARGE_FONT, 25, Type.BUTTON, function=ColorPickerButtons.BACK)
	],
	"CLOTHES": [
		MenuButton("Shirt Color", (commons.WINDOW_WIDTH * 0.5, 240), commons.LARGE_FONT, 24, Type.BUTTON, function=ClothesButtons.SHIRT_COLOR),
		MenuButton("Undershirt Color", (commons.WINDOW_WIDTH * 0.5, 280), commons.LARGE_FONT, 24, Type.BUTTON, function=ClothesButtons.UNDERSHIRT_COLOR),
		MenuButton("Trouser Color", (commons.WINDOW_WIDTH * 0.5, 320), commons.LARGE_FONT, 24, Type.BUTTON, function=ClothesButtons.TROUSER_COLOR),
		MenuButton("Shoe Color", (commons.WINDOW_WIDTH * 0.5, 360), commons.LARGE_FONT, 24, Type.BUTTON, function=ClothesButtons.SHOE_COLOR),
		MenuButton("Back", (commons.WINDOW_WIDTH * 0.5, 570), commons.LARGE_FONT, 25, Type.BUTTON, function=ClothesButtons.BACK)
	],
	"PLAYER_NAMING": [
		MenuButton("Set Player Name", (commons.WINDOW_WIDTH * 0.5, 450), commons.LARGE_FONT, 24, Type.BUTTON, function=PlayerNamingButtons.SET_NAME),
		MenuButton("Back", (commons.WINDOW_WIDTH * 0.5, 570), commons.LARGE_FONT, 25, Type.BUTTON, function=PlayerNamingButtons.BACK)
	],
	"WORLD_SELECTION": [
		MenuButton("Select World", (commons.WINDOW_WIDTH * 0.5, 90), commons.LARGE_FONT, 24, Type.TEXT),
		MenuButton("New World", (commons.WINDOW_WIDTH * 0.5, 530), commons.LARGE_FONT, 24, Type.BUTTON, function=WorldSelectionButtons.NEW_WORLD),
		MenuButton("Back", (commons.WINDOW_WIDTH * 0.5, 570), commons.LARGE_FONT, 25, Type.BUTTON, function=WorldSelectionButtons.BACK)
	],
	"WORLD_CREATION": [
		MenuButton("World Size", (commons.WINDOW_WIDTH * 0.5, 120), commons.EXTRA_LARGE_FONT, 24, Type.TEXT),
		MenuButton("Tiny (100x350)", (commons.WINDOW_WIDTH * 0.5, 240), commons.LARGE_FONT, 24, Type.BUTTON, function=WorldCreationButtons.TINY),
		MenuButton("Small (200x400)", (commons.WINDOW_WIDTH * 0.5, 280), commons.LARGE_FONT, 24, Type.BUTTON, function=WorldCreationButtons.SMALL),
		MenuButton("Medium (400x450)", (commons.WINDOW_WIDTH * 0.5, 320), commons.LARGE_FONT, 24, Type.BUTTON, function=WorldCreationButtons.MEDIUM),
		MenuButton("Large (700x550)", (commons.WINDOW_WIDTH * 0.5, 360), commons.LARGE_FONT, 24, Type.BUTTON, (200, 0, 0), (100, 0, 0), function=WorldCreationButtons.LARGE),
		MenuButton("Back", (commons.WINDOW_WIDTH * 0.5, 570), commons.LARGE_FONT, 25, Type.BUTTON, function=WorldCreationButtons.BACK)
	],
	"WORLD_NAMING": [
		MenuButton("Set World Name", (commons.WINDOW_WIDTH * 0.5, 450), commons.LARGE_FONT, 24, Type.BUTTON, function=WorldNamingButtons.SET_NAME),
		MenuButton("Back", (commons.WINDOW_WIDTH * 0.5, 570), commons.LARGE_FONT, 25, Type.BUTTON, function=WorldNamingButtons.BACK)
	],
	"CREDITS": [
		MenuButton("Credits", (commons.WINDOW_WIDTH * 0.5, 120), commons.EXTRA_LARGE_FONT, 25, Type.TEXT),
		MenuButton("Images: Re-Logic", (commons.WINDOW_WIDTH * 0.5, 270), commons.LARGE_FONT, 25, Type.TEXT),
		MenuButton("Sounds: Re-Logic", (commons.WINDOW_WIDTH * 0.5, 310), commons.LARGE_FONT, 25, Type.TEXT),
		MenuButton("Back", (commons.WINDOW_WIDTH * 0.5, 570), commons.LARGE_FONT, 25, Type.BUTTON, function=CreditsButton.BACK)
	],
	"CHANGES": [
		MenuButton("Changes", (commons.WINDOW_WIDTH * 0.5, 120), commons.EXTRA_LARGE_FONT, 25, Type.TEXT),
		MenuButton("GitHub Repo", (commons.WINDOW_WIDTH * 0.5, 320), commons.LARGE_FONT, 24, Type.BUTTON, function=ChangesButtons.GITHUB),
		MenuButton("Trello Board", (commons.WINDOW_WIDTH * 0.5, 400), commons.LARGE_FONT, 24, Type.BUTTON, function=ChangesButtons.TRELLO),
		MenuButton("Back", (commons.WINDOW_WIDTH * 0.5, 570), commons.LARGE_FONT, 25, Type.BUTTON, function=ChangesButtons.BACK)
	],
	"SETTINGS": [
		MenuButton("Settings", (commons.WINDOW_WIDTH * 0.5, 120), commons.EXTRA_LARGE_FONT, 25, Type.TEXT),
		MenuButton("Coming soon", (commons.WINDOW_WIDTH * 0.5, 300), commons.LARGE_FONT, 25, Type.TEXT),
		MenuButton("Back", (commons.WINDOW_WIDTH * 0.5, 570), commons.LARGE_FONT, 25, Type.BUTTON, function=SettingsButtons.BACK)
	]
}

update_active_menu_buttons()