import datetime
import math
import random
import sys
import _thread
from typing import Any, List

import pygame

import commons
import entity_manager
import game_constants
import game_data
import item
import menu_manager
import prompt
import shared_methods
import sound_manager
import world
from background import BACKGROUND_DATA, Biome
from game_state import GameState
from state_manager import State
from main_utils import *

class PlayingState(State):
    def update(self, dt: float) -> None:
        assert isinstance(entity_manager.get_client_player(), entity_manager.Player)
        # TODO Check if the new day and night cycle is 24 minutes and in the future, make the days 15 and the nights 9 minutes.
        base_zero_to_one_float = (
                math.sin(
                    datetime.timedelta(seconds=entity_manager.get_client_player().playtime)
                    / datetime.timedelta(hours=1)
                    / 0.4
                    * 6
                )
                * 0.5
                + 0.5
        )
        smoothed_zero_to_one_float = shared_methods.smooth_zero_to_one(base_zero_to_one_float, 0)
        smoothed_zero_to_one_float = smoothed_zero_to_one_float * 0.75 + 0.25
        commons.CURRENT_SKY_LIGHTING = int(
            smoothed_zero_to_one_float * global_lighting
        )  # Global lighting is 17. 15 minutes of day and 9 minutes of night. 17*15=255.
        
        world_time_hours = str(int((world.world.playtime / 60) // 60))
        world_time_minutes = str(int(world.world.playtime // 60 % 60))
        world_time_seconds = str(int(world.world.playtime % 60))
        if len(world_time_hours) == 1:
            world_time_hours = f"0{world_time_hours}"
        if len(world_time_minutes) == 1:
            world_time_minutes = f"0{world_time_minutes}"
        if len(world_time_seconds) == 1:
            world_time_seconds = f"0{world_time_seconds}"
        # print(f"{world_time_hours} : {world_time_minutes} : {world_time_seconds}")
        world.world.playtime += commons.DELTA_TIME
        entity_manager.get_client_player().playtime += int(commons.DELTA_TIME)
        
        previous_camera_position = entity_manager.old_camera_position
        
        entity_manager.old_camera_position = (
            entity_manager.camera_position[0],
            entity_manager.camera_position[1],
        )
        
        entity_manager.update_enemies()
        entity_manager.update_projectiles()
        entity_manager.update_particles()
        entity_manager.update_messages()
        entity_manager.update_physics_items()
        entity_manager.check_enemy_spawn()
        
        entity_manager.get_client_player().update()
        entity_manager.get_client_player().animate()
        
        entity_manager.update_damage_numbers()
        entity_manager.update_recent_pickups()
        
        world.check_grow_grass()
        
        temp_cam_pos_x = entity_manager.camera_position[0]
        temp_cam_pos_y = entity_manager.camera_position[1]
        
        if commons.SMOOTH_CAM:
            need_to_move_x = (entity_manager.get_client_player().position[0] - temp_cam_pos_x) * commons.DELTA_TIME * 4
            need_to_move_y = (entity_manager.get_client_player().position[1] - temp_cam_pos_y) * commons.DELTA_TIME * 4
        
            need_to_move_magnitude = math.sqrt(need_to_move_x ** 2 + need_to_move_y ** 2)
            need_to_move_angle = math.atan2(need_to_move_y, need_to_move_x)
        
            cam_diff_magnitude = math.sqrt(
                entity_manager.camera_position_difference[0] ** 2 + entity_manager.camera_position_difference[1] ** 2
            )
        
            if cam_diff_magnitude < 1:
                cam_diff_magnitude = 1
        
            can_move_magnitude = cam_diff_magnitude * (1 + commons.DELTA_TIME * 8)
        
            # Make sure it does not exceed a max camera speed
            can_move_magnitude = min(can_move_magnitude, 200 * commons.BLOCK_SIZE * commons.DELTA_TIME)
        
            if need_to_move_magnitude > can_move_magnitude:
                temp_cam_pos_x = temp_cam_pos_x + math.cos(need_to_move_angle) * can_move_magnitude
                temp_cam_pos_y = temp_cam_pos_y + math.sin(need_to_move_angle) * can_move_magnitude
            else:
                temp_cam_pos_x = temp_cam_pos_x + math.cos(need_to_move_angle) * need_to_move_magnitude
                temp_cam_pos_y = temp_cam_pos_y + math.sin(need_to_move_angle) * need_to_move_magnitude
        
        else:
            temp_cam_pos_x = entity_manager.get_client_player().position[0]
            temp_cam_pos_y = entity_manager.get_client_player().position[1]
        
        if temp_cam_pos_x > world.border_right + commons.BLOCK_SIZE - commons.WINDOW_WIDTH * 0.5:
            temp_cam_pos_x = world.border_right + commons.BLOCK_SIZE - commons.WINDOW_WIDTH * 0.5
        elif temp_cam_pos_x < commons.WINDOW_WIDTH * 0.5:
            temp_cam_pos_x = commons.WINDOW_WIDTH * 0.5
        if temp_cam_pos_y > world.border_down + commons.BLOCK_SIZE * 1.5 - commons.WINDOW_HEIGHT * 0.5:
            temp_cam_pos_y = world.border_down + commons.BLOCK_SIZE * 1.5 - commons.WINDOW_HEIGHT * 0.5
        elif temp_cam_pos_y < commons.WINDOW_HEIGHT * 0.5:
            temp_cam_pos_y = commons.WINDOW_HEIGHT * 0.5
        
        entity_manager.camera_position = (temp_cam_pos_x, temp_cam_pos_y)
        
        entity_manager.camera_position_difference = (
            entity_manager.camera_position[0] - entity_manager.old_camera_position[0],
            entity_manager.camera_position[1] - entity_manager.old_camera_position[1],
        )
        
        move_parallax(
            (
                -entity_manager.camera_position_difference[0] * commons.PARALLAX_AMOUNT,
                -entity_manager.camera_position_difference[1] * commons.PARALLAX_AMOUNT,
            )
        )  # move parallax based on vel
        
        if entity_manager.client_prompt is not None:
            entity_manager.client_prompt.update()
            if entity_manager.client_prompt.close:
                entity_manager.client_prompt = None
                commons.WAIT_TO_USE = True
        
        if commons.BACKGROUND:
            BACKGROUND_DATA.update_biome(Biome.TREE)
            BACKGROUND_DATA.render(GameState.parallax_position[0], GameState.parallax_position[1], 0.1)
            BACKGROUND_DATA.shift(commons.DELTA_TIME * 10, 0.001)
            BACKGROUND_DATA.update(commons.DELTA_TIME)
        else:
            commons.screen.fill((0, 0, 0))
        
        terrain_position = (
            commons.WINDOW_WIDTH * 0.5 - entity_manager.camera_position[0],
            commons.WINDOW_HEIGHT * 0.5 - entity_manager.camera_position[1],
        )
        commons.screen.blit(world.terrain_surface, terrain_position)
        entity_manager.draw_projectiles()
        entity_manager.get_client_player().draw()
        entity_manager.draw_particles()
        entity_manager.draw_enemies()
        entity_manager.draw_physics_items()
        
        if commons.EXPERIMENTAL_LIGHTING:
            if not GameState.thread_active:
                GameState.last_thread_time = (pygame.time.get_ticks() - GameState.last_thread_start) * 0.001
                _thread.start_new_thread(update_light, ())
                GameState.last_thread_start = pygame.time.get_ticks()
        
            GameState.newest_light_surface.unlock()
            commons.screen.blit(
                GameState.newest_light_surface,
                (
                    GameState.newest_light_surface_position[0] - entity_manager.camera_position[
                        0] + commons.WINDOW_WIDTH * 0.5,
                    GameState.newest_light_surface_position[1] - entity_manager.camera_position[
                        1] + commons.WINDOW_HEIGHT * 0.5,
                ),
            )
        
        if commons.DRAW_UI:
            entity_manager.get_client_player().draw_hp()
            commons.screen.blit(entity_manager.get_client_player().hotbar_image, (5, 20))
            entity_manager.draw_messages()
        
        entity_manager.draw_damage_numbers()
        entity_manager.draw_enemy_hover_text()
        entity_manager.draw_recent_pickups()
        draw_interactive_block_hover()
        
        if entity_manager.client_prompt is not None:
            entity_manager.client_prompt.draw()
        
        if not entity_manager.get_client_player().alive:
            draw_death_message()
        
        if commons.DRAW_UI:
            if entity_manager.get_client_player().inventory_open:
                commons.screen.blit(entity_manager.get_client_player().inventory_image, (5, 70))
                entity_manager.get_client_player().blit_craft_surf.fill((255, 0, 255))
                entity_manager.get_client_player().blit_craft_surf.blit(
                    entity_manager.get_client_player().craftable_items_surf,
                    (0, entity_manager.get_client_player().crafting_menu_offset_y),
                )
                commons.screen.blit(entity_manager.get_client_player().blit_craft_surf, (5, 270))
        
            if entity_manager.get_client_player().chest_open:
                commons.screen.blit(entity_manager.get_client_player().chest_image, (245, 265))
        
            pygame.draw.rect(
                commons.screen,
                (230, 230, 10),
                pygame.Rect(5 + entity_manager.get_client_player().hotbar_index * 48, 20, 48, 48),
                3,
            )
        
            if entity_manager.get_client_player().inventory_open:
                draw_inventory_hover_text()
                draw_exit_button()
        
            if GameState.hand_text is not None:
                commons.screen.blit(GameState.hand_text, (242 - GameState.hand_text.get_width() * 0.5, 0))
            draw_item_holding()
        
        if commons.BACKGROUND:
            move_parallax((GameState.background_scroll_velocity, 0))
        
        if GameState.auto_save_tick <= 0:
            GameState.auto_save_tick += commons.AUTO_SAVE_FREQUENCY
            entity_manager.get_client_player().save()
            world.save()
        else:
            GameState.auto_save_tick -= commons.DELTA_TIME
        

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                pass # Handled in main
            # print(round(entity_manager.get_client_player().position[0] / commons.BLOCK_SIZE, 0) * commons.BLOCK_SIZE, round(entity_manager.get_client_player().position[1] / commons.BLOCK_SIZE, 0) * commons.BLOCK_SIZE)
            if event.type == pygame.KEYDOWN:
                # Toggle Inventory
                if event.key == pygame.K_ESCAPE:
                    if entity_manager.get_client_player().inventory_open:
                        game_data.play_sound("sound.menu_close")
                        entity_manager.get_client_player().render_current_item_image()
                        entity_manager.get_client_player().inventory_open = False
                        entity_manager.get_client_player().chest_open = False
                    else:
                        game_data.play_sound("sound.menu_open")
                        entity_manager.get_client_player().inventory_open = True
                        entity_manager.get_client_player().crafting_menu_offset_y = 120
                        entity_manager.get_client_player().update_craftable_items()
                        entity_manager.get_client_player().render_craftable_items_surf()
                        entity_manager.client_prompt = None
            
                if event.key == pygame.K_a:
                    entity_manager.get_client_player().sprites.moving_left = True
                    entity_manager.get_client_player().direction = 0
            
                if event.key == pygame.K_d:
                    entity_manager.get_client_player().sprites.moving_right = True
                    entity_manager.get_client_player().direction = 1
            
                # Player Walk
                if event.key == pygame.K_s:
                    entity_manager.get_client_player().sprites.moving_down = True
                    entity_manager.get_client_player().animation_speed = 0.05
            
                # Player Jump
                if event.key == pygame.K_SPACE:
                    entity_manager.get_client_player().jump()
            
                # Kill All Enemies Cheat
                if event.key == pygame.K_x:
                    if commons.SHIFT_ACTIVE:
                        while len(entity_manager.enemies) > 0:
                            entity_manager.enemies[0].kill((0, -50))
                        entity_manager.add_message(
                            "All enemies killed",
                            pygame.Color(255, 223, 10),
                            outline_color=pygame.Color(80, 70, 3),
                        )
            
                # Spawn Enemy Cheat
                if event.key == pygame.K_f:
                    if commons.SHIFT_ACTIVE:
                        entity_manager.spawn_enemy(
                            random.randint(1, 5),
                            (
                                entity_manager.camera_position[0]
                                - commons.WINDOW_WIDTH * 0.5
                                + commons.MOUSE_POSITION[0],
                                entity_manager.camera_position[1]
                                - commons.WINDOW_HEIGHT * 0.5
                                + commons.MOUSE_POSITION[1],
                            ),
                        )
                        entity_manager.add_message(
                            "Spawned enemy", pygame.Color(255, 223, 10), outline_color=pygame.Color(80, 70, 3)
                        )
            
                # Respawn Cheats
                if event.key == pygame.K_r:
                    if commons.SHIFT_ACTIVE:
                        world.world.spawn_position = (
                            entity_manager.get_client_player().position[0],
                            entity_manager.get_client_player().position[1],
                        )
                        entity_manager.add_message(
                            f"Spawn point moved to {str(world.world.spawn_position)}",
                            pygame.Color(255, 223, 10),
                            outline_color=pygame.Color(80, 70, 3),
                        )
                    else:
                        if commons.PARTICLES:
                            for particle_index in range(
                                    int(game_constants.PARTICLE_COUNT_RESPAWN * commons.PARTICLE_DENSITY)):
                                entity_manager.spawn_particle(
                                    entity_manager.get_client_player().position,
                                    pygame.Color(230, 230, 255),
                                    magnitude=game_constants.PARTICLE_MAGNITUDE_BASE + random.random() * game_constants.PARTICLE_MAGNITUDE_RANGE,
                                    size=game_constants.PARTICLE_SIZE,
                                    gravity=0,
                                )
            
                        game_data.play_sound("sound.mirror")
            
                        entity_manager.get_client_player().respawn()
                        entity_manager.add_message(
                            "Player respawned",
                            pygame.Color(255, 223, 10),
                            outline_color=pygame.Color(80, 70, 3),
                        )
            
                        if commons.PARTICLES:
                            for particle_index in range(
                                    int(game_constants.PARTICLE_COUNT_RESPAWN_ARRIVE * commons.PARTICLE_DENSITY)):
                                entity_manager.spawn_particle(
                                    entity_manager.get_client_player().position,
                                    pygame.Color(230, 230, 255),
                                    magnitude=game_constants.PARTICLE_MAGNITUDE_BASE + random.random() * game_constants.PARTICLE_MAGNITUDE_RANGE,
                                    size=game_constants.PARTICLE_SIZE,
                                    gravity=0,
                                )
            
                # World Snapshot
                if event.key == pygame.K_t:
                    if commons.SHIFT_ACTIVE:
                        tile_scale = 2
                        size_string = f"{str(world.WORLD_SIZE_X * tile_scale)}x{str(world.WORLD_SIZE_Y * tile_scale)}"
                        date_string = (
                            str(datetime.datetime.now()).replace("-", ".").replace(" ", " - ").replace(":", ".")[:-7]
                        )
                        path = f"assets/images/world_snapshots/{date_string} - {size_string}.png"
                        world_surf = pygame.Surface(
                            (
                                tile_scale * world.WORLD_SIZE_X,
                                tile_scale * world.WORLD_SIZE_Y,
                            )
                        )
                        for tile_x in range(len(world.world.tile_data)):
                            for tile_y in range(len(world.world.tile_data[tile_x])):
                                tile_id = world.world.tile_data[tile_x][tile_y][0]
                                wall_id = world.world.tile_data[tile_x][tile_y][1]
            
                                if tile_id != game_data.air_tile_id:
                                    tile_data = game_data.get_tile_by_id(tile_id)
                                    if type(tile_data.image) is pygame.Surface:
                                        try:
                                            pygame.draw.rect(
                                                world_surf,
                                                pygame.transform.average_color(tile_data.image),
                                                pygame.Rect(
                                                    tile_x * tile_scale,
                                                    tile_y * tile_scale,
                                                    tile_scale,
                                                    tile_scale,
                                                ),
                                                0,
                                            )
                                        except FileNotFoundError:
                                            pass
                                        continue
            
                                if wall_id != game_data.air_wall_id:
                                    wall_data = game_data.get_wall_by_id(wall_id)
                                    if type(wall_data.surface) is pygame.Surface:
                                        try:
                                            pygame.draw.rect(
                                                world_surf,
                                                pygame.transform.average_color(wall_data.surface),
                                                pygame.Rect(
                                                    tile_x * tile_scale,
                                                    tile_y * tile_scale,
                                                    tile_scale,
                                                    tile_scale,
                                                ),
                                                0,
                                            )
                                        except FileNotFoundError:
                                            pass
                                        continue
            
                                sky_darken_factor = 1.0 - 0.7 * min(1.0, max(0.0, (tile_y - 55) / 110))
                                color = shared_methods.darken_color(pygame.Color(135, 206, 234), int(sky_darken_factor))
                                pygame.draw.rect(
                                    world_surf,
                                    color,
                                    pygame.Rect(
                                        tile_x * tile_scale,
                                        tile_y * tile_scale,
                                        tile_scale,
                                        tile_scale,
                                    ),
                                    0,
                                )
            
                        pygame.image.save(world_surf, path)
                        entity_manager.add_message(
                            f"World Snapshot Saved to: '{path}'",
                            pygame.Color(255, 223, 10),
                            outline_color=pygame.Color(80, 70, 3),
                        )
            
                # Gravity Reverse Cheat
                if event.key == pygame.K_g:
                    if commons.SHIFT_ACTIVE:
                        commons.GRAVITY = -commons.GRAVITY
                        entity_manager.add_message(
                            "Gravity reversed",
                            pygame.Color(255, 223, 10),
                            outline_color=pygame.Color(80, 70, 3),
                        )
            
                # Random Item Prefix Cheat
                if event.key == pygame.K_c:
                    if commons.SHIFT_ACTIVE:
                        if (
                                entity_manager.get_client_player().items[item.ItemLocation.HOTBAR][
                                    entity_manager.get_client_player().hotbar_index
                                ]
                                is not None
                        ):
                            current_hotbar_item = entity_manager.get_client_player().items[item.ItemLocation.HOTBAR][
                                entity_manager.get_client_player().hotbar_index
                            ]
                            assert current_hotbar_item is not None
                            entity_manager.get_client_player().items[item.ItemLocation.HOTBAR][
                                entity_manager.get_client_player().hotbar_index
                            ] = item.Item(
                                current_hotbar_item.item_id,
                                auto_assign_prefix=True,
                            )
                            entity_manager.add_message(
                                "Item prefix randomized",
                                pygame.Color(
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                ),
                                life=2.5,
                            )
                            entity_manager.get_client_player().render_current_item_image()
                            render_hand_text()
            
                # Test Prompt Cheat
                if event.key == pygame.K_v:
                    if commons.SHIFT_ACTIVE:
                        entity_manager.client_prompt = prompt.Prompt("test", "Test")
                        entity_manager.add_message(
                            "Random prompt deployed",
                            pygame.Color(255, 223, 10),
                            outline_color=pygame.Color(80, 70, 3),
                        )
            
                # Get Tile and Wall IDS
                if event.key == pygame.K_p:
                    if commons.SHIFT_ACTIVE:
                        if world.tile_in_map(commons.HOVERED_TILE[0], commons.HOVERED_TILE[1]):
                            wallID = world.world.tile_data[commons.HOVERED_TILE[0]][commons.HOVERED_TILE[1]][1]
                            entity_manager.add_message(
                                "Wall at ("
                                + str(commons.HOVERED_TILE[0])
                                + ", "
                                + str(commons.HOVERED_TILE[1])
                                + ") has ID: "
                                + str(wallID),
                                pygame.Color(255, 223, 10),
                                outline_color=pygame.Color(80, 70, 3),
                            )
                    else:
                        if world.tile_in_map(commons.HOVERED_TILE[0], commons.HOVERED_TILE[1]):
                            tileID = world.world.tile_data[commons.HOVERED_TILE[0]][commons.HOVERED_TILE[1]][0]
                            entity_manager.add_message(
                                "Tile at ("
                                + str(commons.HOVERED_TILE[0])
                                + ", "
                                + str(commons.HOVERED_TILE[1])
                                + ") has ID: "
                                + str(tileID),
                                pygame.Color(255, 223, 10),
                                outline_color=pygame.Color(80, 70, 3),
                            )
            
                # Toggle UI
                if event.key == pygame.K_u:
                    commons.DRAW_UI = not commons.DRAW_UI
                    entity_manager.add_message(
                        "UI " + shared_methods.get_on_off(commons.DRAW_UI),
                        pygame.Color(255, 223, 10),
                        outline_color=pygame.Color(80, 70, 3),
                    )
            
                # Toggle SMOOTH_CAM
                if event.key == pygame.K_j:
                    commons.SMOOTH_CAM = not commons.SMOOTH_CAM
                    entity_manager.add_message(
                        "Smooth camera " + shared_methods.get_on_off(commons.SMOOTH_CAM),
                        pygame.Color(255, 223, 10),
                        outline_color=pygame.Color(80, 70, 3),
                    )
            
                # Toggle HITBOXES
                if event.key == pygame.K_h:
                    commons.HITBOXES = not commons.HITBOXES
                    entity_manager.add_message(
                        "Hitboxes " + shared_methods.get_on_off(commons.HITBOXES),
                        pygame.Color(255, 223, 10),
                        outline_color=pygame.Color(80, 70, 3),
                    )
            
                # Hotbar Item Selection
                if event.key == pygame.K_1:
                    entity_manager.get_client_player().hotbar_index = 0
                if event.key == pygame.K_2:
                    entity_manager.get_client_player().hotbar_index = 1
                if event.key == pygame.K_3:
                    entity_manager.get_client_player().hotbar_index = 2
                if event.key == pygame.K_4:
                    entity_manager.get_client_player().hotbar_index = 3
                if event.key == pygame.K_5:
                    entity_manager.get_client_player().hotbar_index = 4
                if event.key == pygame.K_6:
                    entity_manager.get_client_player().hotbar_index = 5
                if event.key == pygame.K_7:
                    entity_manager.get_client_player().hotbar_index = 6
                if event.key == pygame.K_8:
                    entity_manager.get_client_player().hotbar_index = 7
                if event.key == pygame.K_9:
                    entity_manager.get_client_player().hotbar_index = 8
                if event.key == pygame.K_0:
                    entity_manager.get_client_player().hotbar_index = 9
            
                if (
                        event.key == pygame.K_1
                        or event.key == pygame.K_2
                        or event.key == pygame.K_3
                        or event.key == pygame.K_4
                        or event.key == pygame.K_5
                        or event.key == pygame.K_6
                        or event.key == pygame.K_7
                        or event.key == pygame.K_8
                        or event.key == pygame.K_9
                        or event.key == pygame.K_0
                ):
                    entity_manager.get_client_player().render_current_item_image()
                    entity_manager.get_client_player().item_swing = False
                    render_hand_text()
            
                    game_data.play_sound("sound.menu_select")
            
                # Toggle Lighting
                if event.key == pygame.K_l:
                    commons.EXPERIMENTAL_LIGHTING = not commons.EXPERIMENTAL_LIGHTING
                    entity_manager.add_message(
                        "Experimental lighting " + shared_methods.get_on_off(commons.EXPERIMENTAL_LIGHTING),
                        pygame.Color(255, 223, 10),
                        outline_color=pygame.Color(80, 70, 3),
                    )
            
                # Toggle Background
                if event.key == pygame.K_b:
                    if commons.SHIFT_ACTIVE:
                        commons.BACKGROUND = not commons.BACKGROUND
                        entity_manager.add_message(
                            "Background " + shared_methods.get_on_off(commons.BACKGROUND),
                            pygame.Color(255, 223, 10),
                            outline_color=pygame.Color(80, 70, 3),
                        )
            
                # Music Volume Up
                # if event.key == K_UP and commons.SHIFT_ACTIVE:
                #     sound_manager.change_music_volume(0.05)
            
                # Music Volume Down
                # if event.key == K_DOWN and commons.SHIFT_ACTIVE:
                #     sound_manager.change_music_volume(-0.05)
            
                # Sound Volume Up
                if event.key == pygame.K_RIGHT and commons.SHIFT_ACTIVE:
                    game_data.change_sound_volume(0.05)
            
                # Sound Volume Down
                if event.key == pygame.K_LEFT and commons.SHIFT_ACTIVE:
                    game_data.change_sound_volume(-0.05)
            
            # Key up Events
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    entity_manager.get_client_player().sprites.moving_left = False
                if event.key == pygame.K_d:
                    entity_manager.get_client_player().sprites.moving_right = False
                if event.key == pygame.K_s:
                    entity_manager.get_client_player().sprites.moving_down = False
                    entity_manager.get_client_player().moving_down_tick = 5
                    entity_manager.get_client_player().stop_moving_down = True
                    entity_manager.get_client_player().animation_speed = 0.025
            
            # Hotbar Item and Crafting Scrolling
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if entity_manager.get_client_player().inventory_open:
                        entity_manager.get_client_player().crafting_menu_offset_velocity_y += 200
                    else:
                        if entity_manager.get_client_player().hotbar_index > 0:
                            entity_manager.get_client_player().hotbar_index -= 1
                            entity_manager.get_client_player().render_current_item_image()
                            entity_manager.get_client_player().item_swing = False
                            render_hand_text()
                        else:
                            entity_manager.get_client_player().hotbar_index = 9
                        game_data.play_sound("sound.menu_select")
            
                if event.button == 5:
                    if entity_manager.get_client_player().inventory_open:
                        entity_manager.get_client_player().crafting_menu_offset_velocity_y -= 200
                    else:
                        if entity_manager.get_client_player().hotbar_index < 9:
                            entity_manager.get_client_player().hotbar_index += 1
                            entity_manager.get_client_player().render_current_item_image()
                            entity_manager.get_client_player().item_swing = False
                            render_hand_text()
                        else:
                            entity_manager.get_client_player().hotbar_index = 0
                        game_data.play_sound("sound.menu_select")
            
