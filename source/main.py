import _thread
import datetime
import math
import random
import sys
from typing import Any, List

import pygame
import pygame.locals

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

pygame.mixer.pre_init(48000, -16, 2, 1024)
pygame.init()
pygame.mixer.init()


from main_utils import *
from state_manager import StateManager
from states.playing_state import PlayingState
from states.main_menu_state import MainMenuState

state_manager_instance = StateManager()
state_manager_instance.add_state('PLAYING', PlayingState())
state_manager_instance.add_state('MAIN_MENU', MainMenuState())

while True:
    commons.MOUSE_POSITION = pygame.mouse.get_pos()
    commons.HOVERED_TILE = (
        int(
            (entity_manager.camera_position[0] + commons.MOUSE_POSITION[0] - commons.WINDOW_WIDTH * 0.5)
            // commons.BLOCK_SIZE
        ),
        int(
            (entity_manager.camera_position[1] + commons.MOUSE_POSITION[1] - commons.WINDOW_HEIGHT * 0.5)
            // commons.BLOCK_SIZE
        ),
    )

    commons.DELTA_TIME = (pygame.time.get_ticks() - old_time_milliseconds) * 0.001
    old_time_milliseconds = pygame.time.get_ticks()

    # If framerate is less than 30, simulate at a slower speed
    if commons.DELTA_TIME > 0.033333:
        commons.DELTA_TIME = 0.033333

    if pygame.key.get_mods() & (pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT):
        commons.SHIFT_ACTIVE = True
    else:
        commons.SHIFT_ACTIVE = False

    state_manager_instance.current_state_name = commons.game_state
    state_manager_instance.current_state = state_manager_instance.states.get(commons.game_state)
    events = pygame.event.get()
    state_manager_instance.handle_events(events)
    state_manager_instance.update(commons.DELTA_TIME)
    state_manager_instance.draw(commons.screen)
    # Draw a prompt if there is one
    if entity_manager.client_prompt is not None:
        entity_manager.client_prompt.update()
        entity_manager.client_prompt.draw()
        if entity_manager.client_prompt.close:
            entity_manager.client_prompt = None

    # Update fps text
    if commons.DRAW_UI:
        if GameState.fps_tick <= 0:
            GameState.fps_tick += game_constants.FPS_UPDATE_FREQUENCY
            if commons.DELTA_TIME > 0:
                fps_text = shared_methods.outline_text(
                    str(int(1.0 / commons.DELTA_TIME)),
                    pygame.Color(255, 255, 255),
                    commons.DEFAULT_FONT,
                )
        else:
            GameState.fps_tick -= commons.DELTA_TIME
        commons.screen.blit(fps_text, (commons.WINDOW_WIDTH - fps_text.get_width(), 0))

    # Reset some variables when the mouse button is lifted
    if not pygame.mouse.get_pressed()[0]:
        if commons.WAIT_TO_USE and not pygame.mouse.get_pressed()[2]:
            commons.WAIT_TO_USE = False
        if commons.is_holding_item:
            GameState.can_drop_holding = True
        elif not commons.is_holding_item:
            GameState.can_pickup_item = True

    if not pygame.mouse.get_pressed()[2]:
        GameState.item_drop_rate = game_constants.DEFAULT_ITEM_DROP_RATE
        GameState.item_drop_tick = 0

    for event in events:
        if event.type == pygame.QUIT:
            if commons.game_state == "PLAYING":
                entity_manager.get_client_player().inventory_open = False
                entity_manager.get_client_player().chest_open = False
                entity_manager.client_prompt = prompt.Prompt(
                    "Exit",
                    game_data.EXIT_MESSAGES[random.randint(0, len(game_data.EXIT_MESSAGES) - 1)],
                    button_1_name="Yep",
                    size=(6, 2),
                )
            else:
                print("Exiting because of pygame.QUIT!")
                pygame.quit()
                sys.exit()
            commons.WAIT_TO_USE = True

    pygame.display.flip()
    clock.tick(commons.TARGET_FPS)
