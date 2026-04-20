import datetime
import math
import random
import sys
from typing import Any, List

import pygame

import commons
import entity_manager
import game_constants
import game_data
import item
import menu_manager
import player
import prompt
import shared_methods
import sound_manager
import world
from background import BACKGROUND_DATA, Biome
from game_state import GameState
from state_manager import State
from main_utils import *

class MainMenuState(State):
    def update(self, dt: float) -> None:
        draw_menu_background()
        menu_manager.update_menu_buttons()
        menu_manager.draw_menu_buttons()
        if commons.game_sub_state == "MAIN":
            commons.screen.blit(
                menu_logo,
                (commons.WINDOW_WIDTH * 0.5 - menu_logo.get_width() * 0.5, 20),
            )
        
        elif commons.game_sub_state == "PLAYER_SELECTION":
            if pygame.mouse.get_pressed()[0] and not commons.WAIT_TO_USE:
                if pygame.Rect(load_menu_box_left1, 120, 336, 384).collidepoint(commons.MOUSE_POSITION):
                    for save_option_index in range(len(commons.PLAYER_SAVE_OPTIONS)):
                        if pygame.Rect(
                                load_menu_box_left2,
                                132 + save_option_index * 62 + GameState.save_select_y_offset,
                                315,
                                60,
                        ).collidepoint(commons.MOUSE_POSITION):
                            commons.WAIT_TO_USE = True
                            commons.PLAYER_DATA["name"] = commons.PLAYER_SAVE_OPTIONS[save_option_index][0]["name"]
                            commons.PLAYER_DATA["model_appearance"] = commons.PLAYER_SAVE_OPTIONS[save_option_index][0][
                                "model_appearance"
                            ]
                            commons.PLAYER_DATA["hotbar"] = commons.PLAYER_SAVE_OPTIONS[save_option_index][0]["hotbar"]
                            commons.PLAYER_DATA["inventory"] = commons.PLAYER_SAVE_OPTIONS[save_option_index][0][
                                "inventory"]
                            commons.PLAYER_DATA["hp"] = commons.PLAYER_SAVE_OPTIONS[save_option_index][0]["hp"]
                            commons.PLAYER_DATA["max_hp"] = commons.PLAYER_SAVE_OPTIONS[save_option_index][0]["max_hp"]
                            commons.PLAYER_DATA["playtime"] = commons.PLAYER_SAVE_OPTIONS[save_option_index][0][
                                "playtime"]
                            commons.PLAYER_DATA["creation_date"] = commons.PLAYER_SAVE_OPTIONS[save_option_index][0][
                                "creation_date"]
                            commons.PLAYER_DATA["last_played_date"] = commons.PLAYER_SAVE_OPTIONS[save_option_index][0][
                                "last_played_date"
                            ]
                            menu_manager.load_menu_world_data()
                            game_data.play_sound("sound.menu_open")
                            commons.game_sub_state = "WORLD_SELECTION"
                            menu_manager.update_active_menu_buttons()
                            GameState.save_select_y_offset = 0
        
            GameState.save_select_y_velocity *= game_constants.MENU_SCROLL_DAMPENING
            if len(commons.PLAYER_SAVE_OPTIONS) > game_constants.MENU_VISIBLE_ITEMS:
                GameState.save_select_y_offset += GameState.save_select_y_velocity
                if GameState.save_select_y_offset < -game_constants.MENU_ITEM_TOTAL_HEIGHT * len(
                        commons.PLAYER_SAVE_OPTIONS) + 350:
                    GameState.save_select_y_offset = -game_constants.MENU_ITEM_TOTAL_HEIGHT * len(
                        commons.PLAYER_SAVE_OPTIONS) + 350
                if GameState.save_select_y_offset > 0:
                    GameState.save_select_y_offset = 0
        
            commons.screen.blit(load_menu_surf, (load_menu_box_left1, 120))
            GameState.save_select_surface.fill((0, 0, 0, 0))
            for save_option_index in range(len(commons.PLAYER_SAVE_OPTIONS)):
                GameState.save_select_surface.blit(
                    commons.PLAYER_SAVE_OPTIONS[save_option_index][1],
                    (0, save_option_index * game_constants.MENU_ITEM_HEIGHT + GameState.save_select_y_offset),
                )
            commons.screen.blit(GameState.save_select_surface, (load_menu_box_left2, 132))
        
        elif commons.game_sub_state == "PLAYER_CREATION":
            commons.screen.blit(
                commons.PLAYER_FRAMES,
                (
                    commons.WINDOW_WIDTH * 0.5 - commons.PLAYER_FRAMES.get_width() * 0.5,
                    100,
                ),
            )
        
        elif commons.game_sub_state == "WORLD_SELECTION":
            should_break = False
            if pygame.mouse.get_pressed()[0] and not commons.WAIT_TO_USE:
                if pygame.Rect(load_menu_box_left1, 120, 336, 384).collidepoint(commons.MOUSE_POSITION):
                    for world_option_index in range(len(commons.WORLD_SAVE_OPTIONS)):
                        if pygame.Rect(
                                load_menu_box_left2,
                                132 + world_option_index * 60 + GameState.save_select_y_offset,
                                315,
                                60,
                        ).collidepoint(commons.MOUSE_POSITION):
                            game_data.play_sound("sound.menu_open")
        
                            world.load(commons.WORLD_SAVE_OPTIONS[world_option_index][0])
        
                            world.WORLD_SIZE_X, world.WORLD_SIZE_Y = len(world.world.tile_data), len(
                                world.world.tile_data[0]
                            )
        
                            world.biome_border_x_1 = world.WORLD_SIZE_X * 0.333333
                            world.biome_border_x_2 = world.WORLD_SIZE_X * 0.666666
        
                            world.border_left = int(commons.BLOCK_SIZE)
                            world.border_right = int(world.WORLD_SIZE_X * commons.BLOCK_SIZE - commons.BLOCK_SIZE)
                            world.border_up = int(commons.BLOCK_SIZE * 1.5)
                            world.border_down = int(world.WORLD_SIZE_Y * commons.BLOCK_SIZE - commons.BLOCK_SIZE * 1.5)
        
                            world.tile_mask_data = [
                                [-1 for _ in range(world.WORLD_SIZE_Y)] for _ in range(world.WORLD_SIZE_X)
                            ]
                            world.wall_tile_mask_data = [
                                [-1 for _ in range(world.WORLD_SIZE_Y)] for _ in range(world.WORLD_SIZE_X)
                            ]
                            background_id = 5
        
                            entity_manager.create_player()
        
                            commons.screen.fill((0, 0, 0))
        
                            loading_greeting_text = shared_methods.outline_text(
                                f"Greetings {entity_manager.client_player.name}, bear with us while",
                                pygame.Color(255, 255, 255),
                                commons.LARGE_FONT,
                            )
                            loading_world_text = shared_methods.outline_text(
                                f"we load up '{world.world.name}'",
                                pygame.Color(255, 255, 255),
                                commons.LARGE_FONT,
                            )
                            loading_tip_text = shared_methods.outline_text(
                                game_data.TIPS[random.randint(0, len(game_data.TIPS) - 1)],
                                pygame.Color(255, 255, 255),
                                commons.DEFAULT_FONT,
                            )
        
                            commons.screen.blit(
                                loading_greeting_text,
                                (
                                    commons.WINDOW_WIDTH * 0.5 - loading_greeting_text.get_width() * 0.5,
                                    commons.WINDOW_HEIGHT * 0.5 - 30,
                                ),
                            )
                            commons.screen.blit(
                                loading_world_text,
                                (
                                    commons.WINDOW_WIDTH * 0.5 - loading_world_text.get_width() * 0.5,
                                    commons.WINDOW_HEIGHT * 0.5,
                                ),
                            )
                            commons.screen.blit(
                                loading_tip_text,
                                (
                                    commons.WINDOW_WIDTH * 0.5 - loading_tip_text.get_width() * 0.5,
                                    commons.WINDOW_HEIGHT * 0.75,
                                ),
                            )
        
                            pygame.display.flip()
        
                            entity_manager.camera_position = (
                                world.world.spawn_position[0],
                                0,
                            )
                            entity_manager.client_player.position = tuple(world.world.spawn_position)
                            entity_manager.client_player.render_current_item_image()
                            entity_manager.client_player.render_hotbar()
                            entity_manager.client_player.render_inventory()
                            world.create_terrain_surface()
        
                            render_hand_text()
        
                            GameState.map_light = [[0 for _ in range(world.WORLD_SIZE_Y)] for _ in
                                                   range(world.WORLD_SIZE_X)]
                            for world_x in range(world.WORLD_SIZE_X - 1):
                                for world_y in range(world.WORLD_SIZE_Y - 1):
                                    if (
                                            world.world.tile_data[world_x][world_y][0] == -1
                                            and world.world.tile_data[world_x][world_y][1] == -1
                                            and world_y < game_constants.SURFACE_LIGHT_LEVEL_Y
                                    ):
                                        GameState.map_light[world_x][world_y] = global_lighting
                                    else:
                                        GameState.map_light[world_x][world_y] = 0
        
                            commons.game_state = "PLAYING"
                            should_break = True
                            sound_manager.play_music()
                            break
        
            if not should_break:
                GameState.save_select_y_velocity *= game_constants.MENU_SCROLL_DAMPENING
                if len(commons.WORLD_SAVE_OPTIONS) > game_constants.MENU_VISIBLE_ITEMS:
                    GameState.save_select_y_offset += GameState.save_select_y_velocity
                    if GameState.save_select_y_offset < -game_constants.MENU_ITEM_TOTAL_HEIGHT * len(
                            commons.WORLD_SAVE_OPTIONS) + 350:
                        GameState.save_select_y_offset = -game_constants.MENU_ITEM_TOTAL_HEIGHT * len(
                            commons.WORLD_SAVE_OPTIONS) + 350
                    if GameState.save_select_y_offset > 0:
                        GameState.save_select_y_offset = 0
        
                commons.screen.blit(load_menu_surf, (load_menu_box_left1, 120))
                GameState.save_select_surface.fill((0, 0, 0, 0))
                for save_option_index in range(len(commons.WORLD_SAVE_OPTIONS)):
                    GameState.save_select_surface.blit(
                        commons.WORLD_SAVE_OPTIONS[save_option_index][1],
                        (0, save_option_index * game_constants.MENU_ITEM_HEIGHT + GameState.save_select_y_offset),
                    )
                commons.screen.blit(GameState.save_select_surface, (load_menu_box_left2, 132))
        
        elif commons.game_sub_state == "CLOTHES":
            commons.screen.blit(
                commons.PLAYER_FRAMES,
                (
                    commons.WINDOW_WIDTH * 0.5 - commons.PLAYER_FRAMES.get_width() * 0.5,
                    100,
                ),
            )
        
        elif commons.game_sub_state == "WORLD_NAMING":
            text = shared_methods.outline_text(
                f"{commons.TEXT_INPUT}|", pygame.Color(255, 255, 255), commons.LARGE_FONT
            )
            commons.screen.blit(text, (commons.WINDOW_WIDTH * 0.5 - text.get_width() * 0.5, 175))
        
        elif commons.game_sub_state == "PLAYER_NAMING":
            text = shared_methods.outline_text(
                f"{commons.TEXT_INPUT}|", pygame.Color(255, 255, 255), commons.LARGE_FONT
            )
            commons.screen.blit(text, (commons.WINDOW_WIDTH * 0.5 - text.get_width() * 0.5, 175))
            commons.screen.blit(
                commons.PLAYER_FRAMES,
                (
                    commons.WINDOW_WIDTH * 0.5 - commons.PLAYER_FRAMES.get_width() * 0.5,
                    100,
                ),
            )
        
        elif commons.game_sub_state == "COLOR_PICKER":
        
            entity_manager.client_color_picker.update()
        
            if (
                    entity_manager.client_color_picker.selected_x is not None
                    and entity_manager.client_color_picker.selected_y is not None
            ):
                commons.PLAYER_MODEL_DATA[commons.PLAYER_MODEL_COLOR_INDEX][
                    0
                ] = entity_manager.client_color_picker.selected_red
                commons.PLAYER_MODEL_DATA[commons.PLAYER_MODEL_COLOR_INDEX][
                    1
                ] = entity_manager.client_color_picker.selected_green
                commons.PLAYER_MODEL_DATA[commons.PLAYER_MODEL_COLOR_INDEX][
                    2
                ] = entity_manager.client_color_picker.selected_blue
                commons.PLAYER_MODEL_DATA[commons.PLAYER_MODEL_COLOR_INDEX][
                    3
                ] = entity_manager.client_color_picker.selected_x
                commons.PLAYER_MODEL_DATA[commons.PLAYER_MODEL_COLOR_INDEX][
                    4
                ] = entity_manager.client_color_picker.selected_y
                menu_manager.player_model = player.Model(
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
                commons.PLAYER_FRAMES = menu_manager.player_model.create_sprite()
            commons.screen.blit(
                commons.PLAYER_FRAMES,
                (
                    commons.WINDOW_WIDTH * 0.5 - commons.PLAYER_FRAMES.get_width() * 0.5,
                    100,
                ),
            )
            entity_manager.client_color_picker.draw()
        

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                pass # Handled in main
            if commons.game_sub_state == "PLAYER_SELECTION" or commons.game_sub_state == "WORLD_SELECTION":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        GameState.save_select_y_velocity += game_constants.MENU_SCROLL_VELOCITY_MULTIPLIER
                    if event.button == 5:
                        GameState.save_select_y_velocity -= game_constants.MENU_SCROLL_VELOCITY_MULTIPLIER
            
            elif commons.game_sub_state == "PLAYER_NAMING" or commons.game_sub_state == "WORLD_NAMING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        commons.TEXT_INPUT = commons.TEXT_INPUT[:-1]
                    elif (
                            len(commons.TEXT_INPUT) <= game_constants.PLAYER_NAME_MAX_LENGTH and commons.game_sub_state == "PLAYER_NAMING") or (
                            len(commons.TEXT_INPUT) <= game_constants.WORLD_NAME_MAX_LENGTH and commons.game_sub_state == "WORLD_NAMING"
                    ):
                        commons.TEXT_INPUT += event.unicode
