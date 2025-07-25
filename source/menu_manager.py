import datetime
import os
import pickle
import random
import sys
import webbrowser
from enum import Enum

import commons
import entity_manager
import game_data
import player
import prompt
import pygame
import shared_methods
import tilesets
import world
from pygame.locals import Rect


class Type(Enum):
    TEXT = 1
    BUTTON = 2


class TitleScreenButtons(Enum):
    SINGLE_PLAYER = 1
    CREDITS = 2
    CHANGES = 3
    SETTINGS = 4
    EXIT = 5


class PlayerSelectionButtons(Enum):
    NEW_PLAYER = 1
    BACK = 2


class PlayerCreationButtons(Enum):
    HAIR_TYPE = 1
    HAIR_COLOR = 2
    EYE_COLOR = 3
    SKIN_COLOR = 4
    CLOTHES = 5
    CREATE = 6
    RANDOMIZE = 7
    BACK = 8


class ColorPickerButtons(Enum):
    BACK = 1


class ClothesButtons(Enum):
    SHIRT_COLOR = 1
    UNDERSHIRT_COLOR = 2
    TROUSER_COLOR = 3
    SHOE_COLOR = 4
    BACK = 5


class PlayerNamingButtons(Enum):
    SET_NAME = 1
    BACK = 2


class WorldSelectionButtons(Enum):
    NEW_WORLD = 1
    BACK = 2


class WorldCreationButtons(Enum):
    TINY = 1
    SMALL = 2
    MEDIUM = 3
    LARGE = 4
    BACK = 5


class WorldNamingButtons(Enum):
    SET_NAME = 1
    BACK = 2


class CreditsButton(Enum):
    BACK = 1


class ChangesButtons(Enum):
    GITHUB = 1
    TRELLO = 2
    BACK = 3


class SettingsButtons(Enum):
    BACK = 1


"""=================================================================================================================
    menu_manager.MenuObject

    Stores information about a single button, the visibility of a given button is set by the active_menu_buttons
    table
-----------------------------------------------------------------------------------------------------------------"""


class MenuObject:
    def __init__(
        self,
        text: str,
        position: tuple[float, float],
        font: pygame.font.Font,
        type: Type,
        color: pygame.Color = pygame.Color(153, 153, 153),
        outline_color: pygame.Color = pygame.Color(0, 0, 0),
        function=None,
    ):
        self.text = text
        self.position = position
        self.type = type
        self.color = color
        self.function = function
        self.font_size = font.size(text)[1]
        self.hover_multiplier = 1.25
        self.text_surface = shared_methods.outline_text(text, self.color, font, outline_color)
        if self.type == Type.BUTTON:
            self.alt_text_surface = shared_methods.outline_text(
                text,
                pygame.Color(255, 255, 0),
                pygame.font.Font(commons.FONT_FILE_PATH, int(self.font_size * self.hover_multiplier)),
            )
        self.rect = Rect(
            self.position[0] - self.text_surface.get_width() * 0.5,
            self.position[1] - self.text_surface.get_height() * 0.5,
            self.text_surface.get_width(),
            self.text_surface.get_height(),
        )
        self.hovered = False
        self.clicked = False
        self.active = False

    """=================================================================================================================
        menu_manager.MenuObject.update -> void

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
        menu_manager.MenuObject.draw -> void

        Draws the button's text surface or alt_text_surface depending on the hover state of the button
    -----------------------------------------------------------------------------------------------------------------"""

    def draw(self):
        if not self.hovered:
            commons.screen.blit(self.text_surface, (self.rect.left, self.rect.top))
        else:
            commons.screen.blit(
                self.alt_text_surface,
                (
                    self.rect.left - (self.alt_text_surface.get_width() * 0.5 - self.text_surface.get_width() * 0.5),
                    self.rect.top - (self.alt_text_surface.get_height() * 0.5 - self.text_surface.get_height() * 0.5),
                ),
            )


commons.PLAYER_MODEL_DATA = [
    [0],
    [0],
    [255, 125, 90, 0, 0],
    [215, 90, 55, 0, 0],
    [105, 90, 75, 0, 0],
    [175, 165, 140, 0, 0],
    [160, 180, 215, 0, 0],
    [255, 230, 175, 0, 0],
    [160, 105, 60, 0, 0],
]

player_model = player.Model(
    {
        "sex": commons.PLAYER_MODEL_DATA[0][0],
        "hair_id": commons.PLAYER_MODEL_DATA[1][0],
        "skin_color": pygame.Color(
            commons.PLAYER_MODEL_DATA[2][0],
            commons.PLAYER_MODEL_DATA[2][1],
            commons.PLAYER_MODEL_DATA[2][2],
        ),
        "hair_color": pygame.Color(
            commons.PLAYER_MODEL_DATA[3][0],
            commons.PLAYER_MODEL_DATA[3][1],
            commons.PLAYER_MODEL_DATA[3][2],
        ),
        "eye_color": pygame.Color(
            commons.PLAYER_MODEL_DATA[4][0],
            commons.PLAYER_MODEL_DATA[4][1],
            commons.PLAYER_MODEL_DATA[4][2],
        ),
        "shirt_color": pygame.Color(
            commons.PLAYER_MODEL_DATA[5][0],
            commons.PLAYER_MODEL_DATA[5][1],
            commons.PLAYER_MODEL_DATA[5][2],
        ),
        "undershirt_color": pygame.Color(
            commons.PLAYER_MODEL_DATA[6][0],
            commons.PLAYER_MODEL_DATA[6][1],
            commons.PLAYER_MODEL_DATA[6][2],
        ),
        "trouser_color": pygame.Color(
            commons.PLAYER_MODEL_DATA[7][0],
            commons.PLAYER_MODEL_DATA[7][1],
            commons.PLAYER_MODEL_DATA[7][2],
        ),
        "shoe_color": pygame.Color(
            commons.PLAYER_MODEL_DATA[8][0],
            commons.PLAYER_MODEL_DATA[8][1],
            commons.PLAYER_MODEL_DATA[8][2],
        ),
    }
)


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
    global player_model
    player_model.walk()
    commons.PLAYER_FRAMES = player_model.create_sprite()

    for menu in active_menu_buttons:
        for text in active_menu_buttons[menu]:
            if text.active:
                text.update()

                if text.clicked:
                    text.clicked = False

                    match text.function:
                        case TitleScreenButtons.SINGLE_PLAYER:
                            commons.game_sub_state = "PLAYER_SELECTION"
                            load_menu_player_data()
                        case TitleScreenButtons.CREDITS:
                            commons.game_sub_state = "CREDITS"
                        case TitleScreenButtons.CHANGES:
                            commons.game_sub_state = "CHANGES"
                        case TitleScreenButtons.SETTINGS:
                            commons.game_sub_state = "SETTINGS"
                        case TitleScreenButtons.EXIT:
                            pygame.quit()
                            sys.exit()
                        case PlayerSelectionButtons.NEW_PLAYER:
                            commons.game_sub_state = "PLAYER_CREATION"
                            commons.PLAYER_MODEL_DATA = [
                                [0],
                                [0],
                                [255, 125, 90, 0, 0],
                                [215, 90, 55, 0, 0],
                                [105, 90, 75, 0, 0],
                                [175, 165, 140, 0, 0],
                                [160, 180, 215, 0, 0],
                                [255, 230, 175, 0, 0],
                                [160, 105, 60, 0, 0],
                            ]
                            player_model = player.Model(
                                {
                                    "sex": commons.PLAYER_MODEL_DATA[0][0],
                                    "hair_id": commons.PLAYER_MODEL_DATA[1][0],
                                    "skin_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[2][0],
                                        commons.PLAYER_MODEL_DATA[2][1],
                                        commons.PLAYER_MODEL_DATA[2][2],
                                    ),
                                    "hair_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[3][0],
                                        commons.PLAYER_MODEL_DATA[3][1],
                                        commons.PLAYER_MODEL_DATA[3][2],
                                    ),
                                    "eye_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[4][0],
                                        commons.PLAYER_MODEL_DATA[4][1],
                                        commons.PLAYER_MODEL_DATA[4][2],
                                    ),
                                    "shirt_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[5][0],
                                        commons.PLAYER_MODEL_DATA[5][1],
                                        commons.PLAYER_MODEL_DATA[5][2],
                                    ),
                                    "undershirt_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[6][0],
                                        commons.PLAYER_MODEL_DATA[6][1],
                                        commons.PLAYER_MODEL_DATA[6][2],
                                    ),
                                    "trouser_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[7][0],
                                        commons.PLAYER_MODEL_DATA[7][1],
                                        commons.PLAYER_MODEL_DATA[7][2],
                                    ),
                                    "shoe_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[8][0],
                                        commons.PLAYER_MODEL_DATA[8][1],
                                        commons.PLAYER_MODEL_DATA[8][2],
                                    ),
                                }
                            )
                            commons.PLAYER_FRAMES = player_model.create_sprite()
                        case PlayerSelectionButtons.BACK:
                            commons.game_sub_state = "MAIN"
                        case PlayerCreationButtons.HAIR_TYPE:
                            if player_model.hair_id < 163:
                                player_model.hair_id += 1
                            else:
                                player_model.hair_id = 0
                            commons.PLAYER_MODEL_DATA[1][0] = player_model.hair_id
                            commons.PLAYER_FRAMES = player_model.create_sprite()
                        case PlayerCreationButtons.HAIR_COLOR:
                            commons.game_sub_state = "COLOR_PICKER"
                            commons.PLAYER_MODEL_COLOR_INDEX = 3
                        case PlayerCreationButtons.EYE_COLOR:
                            commons.game_sub_state = "COLOR_PICKER"
                            commons.PLAYER_MODEL_COLOR_INDEX = 4
                        case PlayerCreationButtons.SKIN_COLOR:
                            commons.game_sub_state = "COLOR_PICKER"
                            commons.PLAYER_MODEL_COLOR_INDEX = 2
                        case PlayerCreationButtons.CLOTHES:
                            commons.game_sub_state = "CLOTHES"
                        case PlayerCreationButtons.CREATE:
                            commons.game_sub_state = "PLAYER_NAMING"
                            commons.TEXT_INPUT = ""
                        case PlayerCreationButtons.RANDOMIZE:
                            commons.PLAYER_MODEL_DATA = [
                                [0],
                                [
                                    random.randint(0, len(tilesets.hair) - 1),
                                ],
                                [
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    0,
                                    0,
                                ],
                                [
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    0,
                                    0,
                                ],
                                [
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    0,
                                    0,
                                ],
                                [
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    0,
                                    0,
                                ],
                                [
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    0,
                                    0,
                                ],
                                [
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    0,
                                    0,
                                ],
                                [
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    0,
                                    0,
                                ],
                                [
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    0,
                                    0,
                                ],
                            ]
                            player_model = player.Model(
                                {
                                    "sex": commons.PLAYER_MODEL_DATA[0][0],
                                    "hair_id": commons.PLAYER_MODEL_DATA[1][0],
                                    "skin_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[2][0],
                                        commons.PLAYER_MODEL_DATA[2][1],
                                        commons.PLAYER_MODEL_DATA[2][2],
                                    ),
                                    "hair_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[3][0],
                                        commons.PLAYER_MODEL_DATA[3][1],
                                        commons.PLAYER_MODEL_DATA[3][2],
                                    ),
                                    "eye_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[4][0],
                                        commons.PLAYER_MODEL_DATA[4][1],
                                        commons.PLAYER_MODEL_DATA[4][2],
                                    ),
                                    "shirt_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[5][0],
                                        commons.PLAYER_MODEL_DATA[5][1],
                                        commons.PLAYER_MODEL_DATA[5][2],
                                    ),
                                    "undershirt_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[6][0],
                                        commons.PLAYER_MODEL_DATA[6][1],
                                        commons.PLAYER_MODEL_DATA[6][2],
                                    ),
                                    "trouser_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[7][0],
                                        commons.PLAYER_MODEL_DATA[7][1],
                                        commons.PLAYER_MODEL_DATA[7][2],
                                    ),
                                    "shoe_color": pygame.Color(
                                        commons.PLAYER_MODEL_DATA[8][0],
                                        commons.PLAYER_MODEL_DATA[8][1],
                                        commons.PLAYER_MODEL_DATA[8][2],
                                    ),
                                }
                            )
                            commons.PLAYER_FRAMES = player_model.create_sprite()
                        case PlayerCreationButtons.BACK:
                            commons.game_sub_state = "PLAYER_SELECTION"
                        case ColorPickerButtons.BACK:
                            commons.game_sub_state = "PLAYER_CREATION"
                        case ClothesButtons.SHIRT_COLOR:
                            commons.game_sub_state = "COLOR_PICKER"
                            commons.PLAYER_MODEL_COLOR_INDEX = 5
                        case ClothesButtons.UNDERSHIRT_COLOR:
                            commons.game_sub_state = "COLOR_PICKER"
                            commons.PLAYER_MODEL_COLOR_INDEX = 6
                        case ClothesButtons.TROUSER_COLOR:
                            commons.game_sub_state = "COLOR_PICKER"
                            commons.PLAYER_MODEL_COLOR_INDEX = 7
                        case ClothesButtons.SHOE_COLOR:
                            commons.game_sub_state = "COLOR_PICKER"
                            commons.PLAYER_MODEL_COLOR_INDEX = 8
                        case ClothesButtons.BACK:
                            commons.game_sub_state = "PLAYER_CREATION"
                        case PlayerNamingButtons.SET_NAME:
                            date = datetime.datetime.now()
                            commons.PLAYER_DATA["name"] = commons.TEXT_INPUT
                            commons.PLAYER_DATA["model_appearance"] = player_model.get_appearance()
                            commons.PLAYER_DATA["hotbar"] = []
                            commons.PLAYER_DATA["inventory"] = []
                            commons.PLAYER_DATA["hp"] = 100
                            commons.PLAYER_DATA["max_hp"] = 100
                            commons.PLAYER_DATA["playtime"] = 0
                            commons.PLAYER_DATA["creation_date"] = date
                            commons.PLAYER_DATA["last_played_date"] = date
                            pickle.dump(
                                commons.PLAYER_DATA,
                                open(f"assets/players/{commons.TEXT_INPUT}.player", "wb"),
                            )  # Save player array
                            commons.game_sub_state = "PLAYER_SELECTION"
                            load_menu_player_data()
                        case PlayerNamingButtons.BACK:
                            commons.game_sub_state = "PLAYER_CREATION"
                        case WorldSelectionButtons.NEW_WORLD:
                            commons.game_sub_state = "WORLD_CREATION"
                        case WorldSelectionButtons.BACK:
                            commons.game_sub_state = "PLAYER_SELECTION"
                        case WorldCreationButtons.TINY:
                            commons.game_sub_state = "WORLD_NAMING"
                            commons.TEXT_INPUT = ""
                            world.WORLD_SIZE_X = 100
                            world.WORLD_SIZE_Y = 350
                        case WorldCreationButtons.SMALL:
                            commons.game_sub_state = "WORLD_NAMING"
                            commons.TEXT_INPUT = ""
                            world.WORLD_SIZE_X = 200
                            world.WORLD_SIZE_Y = 400
                        case WorldCreationButtons.MEDIUM:
                            commons.game_sub_state = "WORLD_NAMING"
                            commons.TEXT_INPUT = ""
                            world.WORLD_SIZE_X = 400
                            world.WORLD_SIZE_Y = 450
                        case WorldCreationButtons.LARGE:
                            commons.game_sub_state = "WORLD_NAMING"
                            commons.TEXT_INPUT = ""
                            world.WORLD_SIZE_X = 700
                            world.WORLD_SIZE_Y = 550
                        case WorldCreationButtons.BACK:
                            commons.game_sub_state = "WORLD_SELECTION"
                        case WorldNamingButtons.SET_NAME:
                            world.WORLD_NAME = commons.TEXT_INPUT
                            world.generate_terrain("DEFAULT", blit_progress=True)
                            world.save()
                            commons.game_sub_state = "WORLD_SELECTION"
                            load_menu_player_data()
                        case WorldNamingButtons.BACK:
                            commons.game_sub_state = "WORLD_CREATION"
                        case CreditsButton.BACK:
                            commons.game_sub_state = "MAIN"
                        case ChangesButtons.GITHUB:
                            entity_manager.client_prompt = prompt.Prompt(
                                "browser opened",
                                "GitHub page opened in a new tab.",
                                size=(5, 2),
                            )
                            webbrowser.open("https://github.com/Murat65536/Terraria")
                        case ChangesButtons.TRELLO:
                            entity_manager.client_prompt = prompt.Prompt(
                                "browser opened",
                                "Trello board opened in a new tab.",
                                size=(5, 2),
                            )
                            webbrowser.open("https://trello.com/b/tI74vC1t/terraria-trello-board")
                        case ChangesButtons.BACK:
                            commons.game_sub_state = "MAIN"
                        case SettingsButtons.BACK:
                            commons.game_sub_state = "MAIN"

                    if commons.game_sub_state == "COLOR_PICKER":
                        if (
                            commons.PLAYER_MODEL_DATA[commons.PLAYER_MODEL_COLOR_INDEX][0] is not None
                            or commons.PLAYER_MODEL_DATA[commons.PLAYER_MODEL_COLOR_INDEX][1] is not None
                            or commons.PLAYER_MODEL_DATA[commons.PLAYER_MODEL_COLOR_INDEX][2] is not None
                        ):
                            entity_manager.client_color_picker.selected_red = commons.PLAYER_MODEL_DATA[
                                commons.PLAYER_MODEL_COLOR_INDEX
                            ][0]
                            entity_manager.client_color_picker.selected_green = commons.PLAYER_MODEL_DATA[
                                commons.PLAYER_MODEL_COLOR_INDEX
                            ][1]
                            entity_manager.client_color_picker.selected_blue = commons.PLAYER_MODEL_DATA[
                                commons.PLAYER_MODEL_COLOR_INDEX
                            ][2]
                            entity_manager.client_color_picker.selected_x = commons.PLAYER_MODEL_DATA[
                                commons.PLAYER_MODEL_COLOR_INDEX
                            ][3]
                            entity_manager.client_color_picker.selected_y = commons.PLAYER_MODEL_DATA[
                                commons.PLAYER_MODEL_COLOR_INDEX
                            ][4]

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
        player_data_surf.blit(
            shared_methods.outline_text(dat["name"], pygame.Color(255, 255, 255), commons.DEFAULT_FONT),
            (5, 3),
        )  # Name
        player_data_surf.blit(
            shared_methods.outline_text("Created: ", pygame.Color(255, 255, 255), commons.DEFAULT_FONT),
            (5, 20),
        )  # Creation date
        player_data_surf.blit(
            shared_methods.outline_text("Playtime: ", pygame.Color(255, 255, 255), commons.DEFAULT_FONT),
            (5, 40),
        )  # Playtime
        player_data_surf.blit(
            shared_methods.outline_text(
                str(dat["creation_date"])[:19], pygame.Color(230, 230, 0), commons.DEFAULT_FONT
            ),
            (80, 20),
        )  # Creation date
        player_data_surf.blit(
            shared_methods.outline_text(
                str(dat["hp"]) + "HP",
                pygame.Color(230, 10, 10),
                commons.DEFAULT_FONT,
                outline_color=pygame.Color(128, 5, 5),
            ),
            (155, 3),
        )  # hp
        player_data_surf.blit(
            shared_methods.outline_text(
                "100MNA",
                pygame.Color(80, 102, 244),
                commons.DEFAULT_FONT,
                outline_color=pygame.Color(30, 41, 122),
            ),
            (205, 3),
        )  # mana
        player_data_surf.blit(
            shared_methods.outline_text(
                str(int((dat["playtime"] / 60) // 60))
                + ":"
                + str(int(dat["playtime"] // 60 % 60)).zfill(2)
                + ":"
                + str(int(dat["playtime"] % 60)).zfill(2),
                pygame.Color(230, 230, 0),
                commons.DEFAULT_FONT,
            ),
            (90, 40),
        )  # playtime
        sprites = player.Model(dat["model_appearance"]).create_sprite()
        player_data_surf.blit(sprites, (270, 0))
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
        if os.path.splitext(possible_loads[i])[1] == ".dat":  # if it's a dat file
            world.load(possible_loads[i][:-4], load_all=False)

            world_data_surf = pygame.Surface((315, 60))
            world_data_surf.fill((50, 50, 50))
            pygame.draw.rect(world_data_surf, pygame.Color(60, 60, 60), Rect(0, 0, 315, 60), 4)

            world_data_surf.blit(
                shared_methods.outline_text(world.world.name, pygame.Color(255, 255, 255), commons.DEFAULT_FONT),
                (5, 3),
            )  # name
            world_data_surf.blit(
                shared_methods.outline_text("Created: ", pygame.Color(255, 255, 255), commons.DEFAULT_FONT),
                (5, 20),
            )  # Creation date
            world_data_surf.blit(
                shared_methods.outline_text("Playtime: ", pygame.Color(255, 255, 255), commons.DEFAULT_FONT),
                (5, 40),
            )  # Playtime
            world_data_surf.blit(
                shared_methods.outline_text(
                    world.world.get_creation_date_string(),
                    pygame.Color(230, 230, 0),
                    commons.DEFAULT_FONT,
                ),
                (80, 20),
            )  # Creation date
            world_data_surf.blit(
                shared_methods.outline_text(
                    str(int((world.world.playtime / 60) // 60))
                    + ":"
                    + str(int(world.world.playtime // 60 % 60)).zfill(2)
                    + ":"
                    + str(int(world.world.playtime % 60)).zfill(2),
                    pygame.Color(230, 230, 0),
                    commons.DEFAULT_FONT,
                ),
                (90, 40),
            )  # playtime

            world_data_surf.blit(tilesets.misc_gui[10], (260, 7))

            commons.WORLD_SAVE_OPTIONS.append((world.world.name, world_data_surf))


active_menu_buttons: dict[str, list[MenuObject]] = {
    "MAIN": [
        MenuObject(
            "Single Player",
            (commons.WINDOW_WIDTH * 0.5, 250),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=TitleScreenButtons.SINGLE_PLAYER,
        ),
        MenuObject(
            "Credits",
            (commons.WINDOW_WIDTH * 0.5, 305),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=TitleScreenButtons.CREDITS,
        ),
        MenuObject(
            "Changes",
            (commons.WINDOW_WIDTH * 0.5, 360),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=TitleScreenButtons.CHANGES,
        ),
        MenuObject(
            "Settings",
            (commons.WINDOW_WIDTH * 0.5, 415),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=TitleScreenButtons.SETTINGS,
        ),
        MenuObject(
            "Exit",
            (commons.WINDOW_WIDTH * 0.5, 470),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=TitleScreenButtons.EXIT,
        ),
    ],
    "PLAYER_SELECTION": [
        MenuObject(
            "Select Player",
            (commons.WINDOW_WIDTH * 0.5, 90),
            commons.LARGE_FONT,
            Type.TEXT,
        ),
        MenuObject(
            "New Player",
            (commons.WINDOW_WIDTH * 0.5, 550),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=PlayerSelectionButtons.NEW_PLAYER,
        ),
        MenuObject(
            "Back",
            (commons.WINDOW_WIDTH * 0.5, 600),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=PlayerSelectionButtons.BACK,
        ),
    ],
    "PLAYER_CREATION": [
        MenuObject(
            "Hair Type",
            (commons.WINDOW_WIDTH * 0.5, 200),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=PlayerCreationButtons.HAIR_TYPE,
        ),
        MenuObject(
            "Hair Color",
            (commons.WINDOW_WIDTH * 0.5, 260),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=PlayerCreationButtons.HAIR_COLOR,
        ),
        MenuObject(
            "Eye Color",
            (commons.WINDOW_WIDTH * 0.5, 320),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=PlayerCreationButtons.EYE_COLOR,
        ),
        MenuObject(
            "Skin Color",
            (commons.WINDOW_WIDTH * 0.5, 380),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=PlayerCreationButtons.SKIN_COLOR,
        ),
        MenuObject(
            "Clothes",
            (commons.WINDOW_WIDTH * 0.5, 440),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=PlayerCreationButtons.CLOTHES,
        ),
        MenuObject(
            "Create",
            (commons.WINDOW_WIDTH * 0.5, 500),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=PlayerCreationButtons.CREATE,
        ),
        MenuObject(
            "Randomize",
            (commons.WINDOW_WIDTH * 0.5, 600),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=PlayerCreationButtons.RANDOMIZE,
        ),
        MenuObject(
            "Back",
            (commons.WINDOW_WIDTH * 0.5, 660),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=PlayerCreationButtons.BACK,
        ),
    ],
    "COLOR_PICKER": [
        MenuObject(
            "Back",
            (commons.WINDOW_WIDTH * 0.5, 570),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=ColorPickerButtons.BACK,
        )
    ],
    "CLOTHES": [
        MenuObject(
            "Shirt Color",
            (commons.WINDOW_WIDTH * 0.5, 240),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=ClothesButtons.SHIRT_COLOR,
        ),
        MenuObject(
            "Undershirt Color",
            (commons.WINDOW_WIDTH * 0.5, 300),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=ClothesButtons.UNDERSHIRT_COLOR,
        ),
        MenuObject(
            "Trouser Color",
            (commons.WINDOW_WIDTH * 0.5, 360),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=ClothesButtons.TROUSER_COLOR,
        ),
        MenuObject(
            "Shoe Color",
            (commons.WINDOW_WIDTH * 0.5, 420),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=ClothesButtons.SHOE_COLOR,
        ),
        MenuObject(
            "Back",
            (commons.WINDOW_WIDTH * 0.5, 540),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=ClothesButtons.BACK,
        ),
    ],
    "PLAYER_NAMING": [
        MenuObject(
            "Set Player Name",
            (commons.WINDOW_WIDTH * 0.5, 450),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=PlayerNamingButtons.SET_NAME,
        ),
        MenuObject(
            "Back",
            (commons.WINDOW_WIDTH * 0.5, 570),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=PlayerNamingButtons.BACK,
        ),
    ],
    "WORLD_SELECTION": [
        MenuObject(
            "Select World",
            (commons.WINDOW_WIDTH * 0.5, 90),
            commons.LARGE_FONT,
            Type.TEXT,
        ),
        MenuObject(
            "New World",
            (commons.WINDOW_WIDTH * 0.5, 530),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=WorldSelectionButtons.NEW_WORLD,
        ),
        MenuObject(
            "Back",
            (commons.WINDOW_WIDTH * 0.5, 570),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=WorldSelectionButtons.BACK,
        ),
    ],
    "WORLD_CREATION": [
        MenuObject(
            "World Size",
            (commons.WINDOW_WIDTH * 0.5, 120),
            commons.EXTRA_LARGE_FONT,
            Type.TEXT,
        ),
        MenuObject(
            "Tiny (100x350)",
            (commons.WINDOW_WIDTH * 0.5, 240),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=WorldCreationButtons.TINY,
        ),
        MenuObject(
            "Small (200x400)",
            (commons.WINDOW_WIDTH * 0.5, 280),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=WorldCreationButtons.SMALL,
        ),
        MenuObject(
            "Medium (400x450)",
            (commons.WINDOW_WIDTH * 0.5, 320),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=WorldCreationButtons.MEDIUM,
        ),
        MenuObject(
            "Large (700x550)",
            (commons.WINDOW_WIDTH * 0.5, 360),
            commons.LARGE_FONT,
            Type.BUTTON,
            pygame.Color(200, 0, 0),
            pygame.Color(100, 0, 0),
            function=WorldCreationButtons.LARGE,
        ),
        MenuObject(
            "Back",
            (commons.WINDOW_WIDTH * 0.5, 570),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=WorldCreationButtons.BACK,
        ),
    ],
    "WORLD_NAMING": [
        MenuObject(
            "Set World Name",
            (commons.WINDOW_WIDTH * 0.5, 450),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=WorldNamingButtons.SET_NAME,
        ),
        MenuObject(
            "Back",
            (commons.WINDOW_WIDTH * 0.5, 570),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=WorldNamingButtons.BACK,
        ),
    ],
    "CREDITS": [
        MenuObject(
            "Credits",
            (commons.WINDOW_WIDTH * 0.5, 120),
            commons.EXTRA_LARGE_FONT,
            Type.TEXT,
        ),
        MenuObject(
            "Images: Re-Logic",
            (commons.WINDOW_WIDTH * 0.5, 270),
            commons.LARGE_FONT,
            Type.TEXT,
        ),
        MenuObject(
            "Sounds: Re-Logic",
            (commons.WINDOW_WIDTH * 0.5, 310),
            commons.LARGE_FONT,
            Type.TEXT,
        ),
        MenuObject(
            "Back",
            (commons.WINDOW_WIDTH * 0.5, 570),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=CreditsButton.BACK,
        ),
    ],
    "CHANGES": [
        MenuObject(
            "Changes",
            (commons.WINDOW_WIDTH * 0.5, 120),
            commons.EXTRA_LARGE_FONT,
            Type.TEXT,
        ),
        MenuObject(
            "GitHub Repo",
            (commons.WINDOW_WIDTH * 0.5, 320),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=ChangesButtons.GITHUB,
        ),
        MenuObject(
            "Trello Board",
            (commons.WINDOW_WIDTH * 0.5, 400),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=ChangesButtons.TRELLO,
        ),
        MenuObject(
            "Back",
            (commons.WINDOW_WIDTH * 0.5, 570),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=ChangesButtons.BACK,
        ),
    ],
    "SETTINGS": [
        MenuObject(
            "Settings",
            (commons.WINDOW_WIDTH * 0.5, 120),
            commons.EXTRA_LARGE_FONT,
            Type.TEXT,
        ),
        MenuObject(
            "Coming soon",
            (commons.WINDOW_WIDTH * 0.5, 300),
            commons.LARGE_FONT,
            Type.TEXT,
        ),
        MenuObject(
            "Back",
            (commons.WINDOW_WIDTH * 0.5, 570),
            commons.LARGE_FONT,
            Type.BUTTON,
            function=SettingsButtons.BACK,
        ),
    ],
}

update_active_menu_buttons()
