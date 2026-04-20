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

def move_parallax(offset: tuple[float, float]) -> None:
    """
    Moves the background by a set amount, looping back when necessary
    """
    GameState.parallax_position = (
        GameState.parallax_position[0] + offset[0],
        GameState.parallax_position[1] + offset[1]
    )
    if GameState.parallax_position[0] > 0:
        GameState.parallax_position = (
            -game_constants.PARALLAX_BACKGROUND_WIDTH + GameState.parallax_position[0],
            GameState.parallax_position[1]
        )
    elif GameState.parallax_position[0] < -game_constants.PARALLAX_BACKGROUND_RESET_THRESHOLD:
        GameState.parallax_position = (
            GameState.parallax_position[0] + game_constants.PARALLAX_BACKGROUND_WIDTH,
            GameState.parallax_position[1]
        )


def fade_background(new_background_id: int) -> None:
    """
    Fade the background to a different background type
    """
    GameState.fade_background_id = new_background_id
    GameState.fade_back = True
    GameState.fade_float = 0.0


def draw_death_message() -> None:
    """
    Renders and draws a large death message to the screen
    """
    assert isinstance(entity_manager.get_client_player(), entity_manager.Player)
    death_text = shared_methods.outline_text("You were slain...", pygame.Color(255, 127, 127), commons.LARGE_FONT)
    respawn_text = shared_methods.outline_text(
        str(int(entity_manager.get_client_player().respawn_time_remaining) + 1),
        pygame.Color(255, 127, 127),
        commons.LARGE_FONT,
    )
    alpha = int((1 - entity_manager.get_client_player().death_message_alpha) * 255)
    death_text.set_alpha(alpha)
    respawn_text.set_alpha(alpha)
    commons.screen.blit(
        death_text, (commons.WINDOW_WIDTH * 0.5 - death_text.get_width() * 0.5, commons.WINDOW_HEIGHT * 0.5)
    )
    commons.screen.blit(
        respawn_text,
        (
            commons.WINDOW_WIDTH * 0.5 - respawn_text.get_width() * 0.5,
            commons.WINDOW_HEIGHT * 0.5 + death_text.get_height(),
        ),
    )


def render_hand_text() -> None:
    """
    Renders the full name of the item that the player has equipped in their hotbar to a surface
    """
    assert isinstance(entity_manager.get_client_player(), entity_manager.Player)
    equipped = entity_manager.get_client_player().items[item.ItemLocation.HOTBAR][entity_manager.get_client_player().hotbar_index]
    if equipped is not None:
        color = shared_methods.get_tier_color(equipped.get_tier())
        GameState.hand_text = shared_methods.outline_text(equipped.get_name(), color, commons.DEFAULT_FONT)
    else:
        GameState.hand_text = shared_methods.outline_text("", pygame.Color(255, 255, 255), commons.DEFAULT_FONT)


def run_splash_screen() -> None:
    """
    Run when booting the game to display some text and the default character running across the screen
    """
    age = 0
    black_surf = pygame.Surface((commons.WINDOW_WIDTH, commons.WINDOW_HEIGHT))

    commons.OLD_TIME_MILLISECONDS = pygame.time.get_ticks()

    splash_screen_running = True
    splash_screen_num = random.randint(1, 9)
    while splash_screen_running:
        commons.DELTA_TIME = (pygame.time.get_ticks() - commons.OLD_TIME_MILLISECONDS) * 0.001
        commons.OLD_TIME_MILLISECONDS = pygame.time.get_ticks()
        splashscreen = pygame.image.load(f"assets/images/backgrounds/splash_screens/splash_{splash_screen_num}.png")
        splashscreen = pygame.transform.scale(splashscreen, (commons.WINDOW_WIDTH, commons.WINDOW_HEIGHT))
        commons.screen.blit(splashscreen, (0, 0))
        entity_manager.draw_particles()

        if age < 0.5:
            black_surf.set_alpha(255)

        elif 0.5 < age < 1.5:
            alpha = int((1.5 - age) * 255)
            black_surf.set_alpha(alpha)

        elif 4.5 < age < 5.5:
            entity_manager.update_particles()
            alpha = int((age - 4.5) * 255)
            black_surf.set_alpha(alpha)

        elif age > 6.0:
            splash_screen_running = False
        commons.screen.blit(black_surf, (0, 0))

        age += commons.DELTA_TIME

        for splash_screen_event in pygame.event.get():
            if splash_screen_event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if splash_screen_event.type == pygame.KEYDOWN:
                splash_screen_running = False
        pygame.display.flip()

        clock.tick(commons.TARGET_FPS)


def _render_weapon_stats(equipped, stats):
    """Helper function to render weapon-specific stats"""
    if equipped.has_tag(item.ItemTag.WEAPON):
        stats.append(
            shared_methods.outline_text(
                f"{str(round(equipped.get_attack_damage(), 1)).rstrip('0').rstrip('.')} true melee damage",
                pygame.Color(255, 255, 255),
                commons.DEFAULT_FONT,
            )
        )
        stats.append(
            shared_methods.outline_text(
                f"{str(round(equipped.get_crit_chance() * 100, 1)).rstrip('0').rstrip('.')} % critical strike chance",
                pygame.Color(255, 255, 255),
                commons.DEFAULT_FONT,
            )
        )
        stats.append(
            shared_methods.outline_text(
                get_speed_text(equipped.get_attack_speed()),
                pygame.Color(255, 255, 255),
                commons.DEFAULT_FONT,
            )
        )
        stats.append(
            shared_methods.outline_text(
                get_knockback_text(equipped.get_knockback()),
                pygame.Color(255, 255, 255),
                commons.DEFAULT_FONT,
            )
        )


def _render_ammo_stats(equipped, stats):
    """Helper function to render ammunition-specific stats"""
    if equipped.has_tag(item.ItemTag.AMMO):
        stats.append(
            shared_methods.outline_text("Ammunition", pygame.Color(255, 255, 255), commons.DEFAULT_FONT)
        )
        stats.append(
            shared_methods.outline_text(
                f"{equipped.get_ammo_damage()} damage",
                pygame.Color(255, 255, 255),
                commons.DEFAULT_FONT,
            )
        )
        stats.append(
            shared_methods.outline_text(
                f"{round(equipped.get_ammo_knockback_modifier() * 100, 1)} % knockback",
                pygame.Color(255, 255, 255),
                commons.DEFAULT_FONT,
            )
        )
        stats.append(
            shared_methods.outline_text(
                f"{round(equipped.get_ammo_gravity_modifier() * 100, 1)} % gravity",
                pygame.Color(255, 255, 255),
                commons.DEFAULT_FONT,
            )
        )
        stats.append(
            shared_methods.outline_text(
                f"{round(equipped.get_ammo_drag() * 100, 1)} % drag",
                pygame.Color(255, 255, 255),
                commons.DEFAULT_FONT,
            )
        )


def _render_tile_stats(equipped, stats):
    """Helper function to render tile-specific stats"""
    if equipped.has_tag(item.ItemTag.TILE):
        stats.append(
            shared_methods.outline_text("Can be placed", pygame.Color(255, 255, 255), commons.DEFAULT_FONT)
        )


def _render_material_stats(equipped, stats):
    """Helper function to render material-specific stats"""
    if equipped.has_tag(item.ItemTag.MATERIAL):
        stats.append(shared_methods.outline_text("Material", pygame.Color(255, 255, 255), commons.DEFAULT_FONT))


def _render_prefix_stats(equipped, stats):
    """Helper function to render item prefix stats"""
    if not equipped.has_prefix or equipped.prefix_data is None:
        return

    # Damage modifier
    if equipped.prefix_data[1]["damage"] != 0:
        color = GameState.good_color if equipped.prefix_data[1]["damage"] > 0 else GameState.bad_color
        stats.append(
            shared_methods.outline_text(
                f"{add_plus(str(int(equipped.prefix_data[1]['damage'] * 100)))} % damage",
                color,
                commons.DEFAULT_FONT,
                outline_color=shared_methods.darken_color(color),
            )
        )

    # Speed/crit chance modifiers based on prefix group
    if equipped.prefix_data[0] != item.ItemPrefixGroup.UNIVERSAL:
        if equipped.prefix_data[1]["speed"] != 0:
            color = GameState.good_color if equipped.prefix_data[1]["speed"] > 0 else GameState.bad_color
            stats.append(
                shared_methods.outline_text(
                    f"{add_plus(str(int(equipped.prefix_data[1]['speed'] * 100)))} % speed",
                    color,
                    commons.DEFAULT_FONT,
                    outline_color=shared_methods.darken_color(color),
                )
            )
    else:
        # Universal prefix group has different stat handling
        if equipped.prefix_data[1]["speed"] != 0:
            color = GameState.good_color if equipped.prefix_data[1]["speed"] > 0 else GameState.bad_color
            stats.append(
                shared_methods.outline_text(
                    f"{add_plus(str(int(equipped.prefix_data[1]['speed'] * 100)))} % critical strike chance",
                    color,
                    commons.DEFAULT_FONT,
                    outline_color=shared_methods.darken_color(color),
                )
            )

    # Continue with other prefix-specific stats...
    _render_remaining_prefix_stats(equipped, stats)


def _render_remaining_prefix_stats(equipped, stats):
    """Helper function to render remaining prefix stats to avoid code duplication"""
    # Critical chance and knockback stats for different prefix groups
    if equipped.prefix_data[0] != item.ItemPrefixGroup.UNIVERSAL:
        if equipped.prefix_data[1]["crit_chance"] != 0:
            color = GameState.good_color if equipped.prefix_data[1]["crit_chance"] > 0 else GameState.bad_color
            stats.append(
                shared_methods.outline_text(
                    f"{add_plus(str(int(equipped.prefix_data[1]['crit_chance'] * 100)))} % critical strike chance",
                    color,
                    commons.DEFAULT_FONT,
                    outline_color=shared_methods.darken_color(color),
                )
            )

    # Handle specific prefix group modifiers
    prefix_group_handlers = {
        item.ItemPrefixGroup.COMMON: _handle_common_prefix,
        item.ItemPrefixGroup.LONGSWORD: _handle_longsword_prefix,
        item.ItemPrefixGroup.SHORTSWORD: _handle_shortsword_prefix,
        item.ItemPrefixGroup.RANGED: _handle_ranged_prefix,
        item.ItemPrefixGroup.MAGICAL: _handle_magical_prefix,
    }

    handler = prefix_group_handlers.get(equipped.prefix_data[0])
    if handler:
        handler(equipped, stats)


def _handle_common_prefix(equipped, stats):
    """Handle common prefix group stats"""
    if equipped.prefix_data[1]["knockback"] != 0:
        color = GameState.good_color if equipped.prefix_data[1]["knockback"] > 0 else GameState.bad_color
        stats.append(
            shared_methods.outline_text(
                f"{add_plus(str(int(equipped.prefix_data[1]['knockback'] * 100)))} % knockback",
                color,
                commons.DEFAULT_FONT,
                outline_color=shared_methods.darken_color(color),
            )
        )


def _handle_longsword_prefix(equipped, stats):
    """Handle longsword prefix group stats"""
    if equipped.prefix_data[1]["size"] != 0:
        color = GameState.good_color if equipped.prefix_data[1]["size"] > 0 else GameState.bad_color
        # Note: The original code didn't append this stat, keeping that behavior


def _handle_shortsword_prefix(equipped, stats):
    """Handle shortsword prefix group stats"""
    if equipped.prefix_data[1]["size"] != 0:
        color = GameState.good_color if equipped.prefix_data[1]["size"] > 0 else GameState.bad_color
        stats.append(
            shared_methods.outline_text(
                f"{add_plus(str(int(equipped.prefix_data[1]['size'] * 100)))} % size",
                color,
                commons.DEFAULT_FONT,
                outline_color=shared_methods.darken_color(color),
            )
        )


def _handle_ranged_prefix(equipped, stats):
    """Handle ranged prefix group stats"""
    if equipped.prefix_data[1]["velocity"] != 0:
        color = GameState.good_color if equipped.prefix_data[1]["velocity"] > 0 else GameState.bad_color
        stats.append(
            shared_methods.outline_text(
                f"{add_plus(str(int(equipped.prefix_data[1]['velocity'] * 100)))} % projectile velocity",
                color,
                commons.DEFAULT_FONT,
                outline_color=shared_methods.darken_color(color),
            )
        )


def _handle_magical_prefix(equipped, stats):
    """Handle magical prefix group stats"""
    if equipped.prefix_data[1]["mana_cost"] != 0:
        color = GameState.good_color if equipped.prefix_data[1]["mana_cost"] < 0 else GameState.bad_color
        stats.append(
            shared_methods.outline_text(
                f"{add_plus(str(int(equipped.prefix_data[1]['mana_cost'] * 100)))} % mana cost",
                color,
                commons.DEFAULT_FONT,
                outline_color=shared_methods.darken_color(color),
            )
        )


def render_stats_text(pos: List[Any]) -> bool:
    """
    Gets an item using the parsed position and renders it's information to a surface
    """
    assert isinstance(entity_manager.get_client_player(), entity_manager.Player)

    if pos[0] == item.ItemLocation.CRAFTING_MENU:
        equipped = item.Item(
            entity_manager.get_client_player().items[pos[0]][pos[1]][0],
            entity_manager.get_client_player().items[pos[0]][pos[1]][1],
        )
    else:
        equipped = entity_manager.get_client_player().items[pos[0]][pos[1]]

    if equipped is not None:
        if equipped != GameState.last_hovered_item:
            GameState.last_hovered_item = equipped
            GameState.stats_text = pygame.Surface((
                game_constants.UI_STATS_SURFACE_WIDTH,
                game_constants.UI_STATS_SURFACE_HEIGHT
            ), pygame.SRCALPHA)

            stats = [
                shared_methods.outline_text(
                    equipped.get_name(),
                    shared_methods.get_tier_color(equipped.get_tier()),
                    commons.DEFAULT_FONT,
                )
            ]

            _render_weapon_stats(equipped, stats)
            _render_ammo_stats(equipped, stats)
            _render_tile_stats(equipped, stats)
            _render_material_stats(equipped, stats)
            _render_prefix_stats(equipped, stats)

            for stat_index in range(len(stats)):
                GameState.stats_text.blit(stats[stat_index], (0, stat_index * game_constants.UI_STAT_LINE_HEIGHT))
        return True
    return False


def update_light() -> None:
    """
    Run by the lighting thread to update the light surface and it's position in the world
    """
    GameState.thread_active = True

    target_position = (
        entity_manager.camera_position[0]
        + (entity_manager.camera_position_difference[0] / commons.DELTA_TIME) * GameState.last_thread_time,
        entity_manager.camera_position[1]
        + (entity_manager.camera_position_difference[1] / commons.DELTA_TIME) * GameState.last_thread_time,
    )

    GameState.light_min_x = int(target_position[0] // commons.BLOCK_SIZE - GameState.LIGHT_RENDER_DISTANCE_X)
    GameState.light_max_x = int(target_position[0] // commons.BLOCK_SIZE + GameState.LIGHT_RENDER_DISTANCE_X)
    GameState.light_min_y = int(target_position[1] // commons.BLOCK_SIZE - GameState.LIGHT_RENDER_DISTANCE_Y)
    GameState.light_max_y = int(target_position[1] // commons.BLOCK_SIZE + GameState.LIGHT_RENDER_DISTANCE_Y)

    min_change_x = 0
    min_change_y = 0

    if GameState.light_min_x < 0:
        min_change_x = -GameState.light_min_x
        GameState.light_min_x = 0
    if GameState.light_min_y < 0:
        min_change_y = -GameState.light_min_y
        GameState.light_min_y = 0

    if GameState.light_min_x >= world.WORLD_SIZE_X or GameState.light_min_y >= world.WORLD_SIZE_Y or GameState.light_max_x < 0 or GameState.light_max_y < 0:
        GameState.thread_active = False
        return

    temp_pos = (
        (target_position[
             0] // commons.BLOCK_SIZE - GameState.LIGHT_RENDER_DISTANCE_X + min_change_x) * commons.BLOCK_SIZE,
        (target_position[
             1] // commons.BLOCK_SIZE - GameState.LIGHT_RENDER_DISTANCE_Y + min_change_y) * commons.BLOCK_SIZE,
    )

    if GameState.light_max_x > world.WORLD_SIZE_X:
        GameState.light_max_x = world.WORLD_SIZE_X
    if GameState.light_max_y > world.WORLD_SIZE_Y:
        GameState.light_max_y = world.WORLD_SIZE_Y

    # timeBefore = pygame.time.get_ticks()

    for x_index in range(GameState.light_min_x, GameState.light_max_x):
        for y_index in range(GameState.light_min_y, GameState.light_max_y):
            GameState.map_light[x_index][y_index] = max(0, GameState.map_light[x_index][y_index] - 16)

    # mapLight = [[0 for i in range(world.WORLD_SIZE_Y)] for j in range(world.WORLD_SIZE_X)]

    for x_index in range(GameState.light_min_x, GameState.light_max_x):
        for y_index in range(GameState.light_min_y, GameState.light_max_y):
            if y_index < 110:
                if (
                        world.world.tile_data[x_index][y_index][1] == game_data.air_wall_id
                        and world.world.tile_data[x_index][y_index][0] == game_data.air_tile_id
                ):
                    fill_light(x_index, y_index, commons.CURRENT_SKY_LIGHTING)
            tile_emission = game_data.tile_id_light_emission_lookup[world.world.tile_data[x_index][y_index][0]]
            if tile_emission > 0:
                fill_light(x_index, y_index, tile_emission)

    # print("Fill Light MS: ", pygame.time.get_ticks() - timeBefore)

    range_x = GameState.light_max_x - GameState.light_min_x
    range_y = GameState.light_max_y - GameState.light_min_y

    # timeBefore = pygame.time.get_ticks()

    GameState.light_surface = pygame.Surface((range_x, range_y), pygame.SRCALPHA)

    for x_index in range(range_x):
        for y_index in range(range_y):
            tile_dat = world.world.tile_data[GameState.light_min_x + x_index][GameState.light_min_y + y_index]
            if tile_dat[0] == game_data.air_tile_id and tile_dat[1] == game_data.air_wall_id:
                GameState.light_surface.set_at((x_index, y_index), (0, 0, 0, 255 - commons.CURRENT_SKY_LIGHTING))
            else:
                GameState.light_surface.set_at(
                    (x_index, y_index),
                    (
                        0,
                        0,
                        0,
                        255 - GameState.map_light[x_index + GameState.light_min_x][y_index + GameState.light_min_y],
                    ),
                )

    GameState.light_surface = pygame.transform.scale(GameState.light_surface,
                                                     (range_x * commons.BLOCK_SIZE, range_y * commons.BLOCK_SIZE))

    GameState.newest_light_surface_position = temp_pos
    GameState.newest_light_surface = GameState.light_surface
    GameState.thread_active = False

    # print("Scale Copy MS: ", pygame.time.get_ticks() - timeBefore)


def fill_light(x_pos: int, y_pos: int, light_value: int) -> None:
    """Recursively calls itself to populate data in the map_light array"""
    if GameState.light_min_x <= x_pos < GameState.light_max_x and GameState.light_min_y <= y_pos < GameState.light_max_y:
        light_reduction = game_data.tile_id_light_reduction_lookup[world.world.tile_data[x_pos][y_pos][0]]
        new_light_value = max(0, light_value - light_reduction)
        if new_light_value > GameState.map_light[x_pos][y_pos]:
            GameState.map_light[x_pos][y_pos] = int(new_light_value)
            fill_light(x_pos - 1, y_pos, new_light_value)
            fill_light(x_pos + 1, y_pos, new_light_value)
            fill_light(x_pos, y_pos - 1, new_light_value)
            fill_light(x_pos, y_pos + 1, new_light_value)
        else:
            return
    else:
        return


def get_speed_text(speed: float) -> str:
    """
    Gets a string relating to the speed value given
    """
    if speed <= 8:
        return "Insanely fast speed"
    elif speed <= 20:
        return "Very fast speed"
    elif speed < 25:
        return "Fast speed"
    elif speed < 30:
        return "Average speed"
    elif speed < 35:
        return "Slow speed"
    elif speed < 45:
        return "Very slow speed"
    elif speed < 55:
        return "Extremely slow speed"
    else:
        return "Snail speed"


def get_knockback_text(knockback: float) -> str:
    """
    Gets a string relating to the knockback value given
    """
    if knockback == 0:
        return "No knockback"
    elif knockback < 1.5:
        return "Extremely weak knockback"
    elif knockback < 3:
        return "Very weak knockback"
    elif knockback < 4:
        return "Weak knockback"
    elif knockback < 6:
        return "Average knockback"
    elif knockback < 7:
        return "Strong knockback"
    elif knockback < 9:
        return "Very strong knockback"
    elif knockback < 11:
        return "Extremely strong knockback"
    else:
        return "Insane knockback"


def get_bounces_text(bounces: int) -> str:
    """Cleans up ammunition's bounce text"""
    if bounces == 0:
        return "No bounces"
    elif bounces == 1:
        return "1 bounce"
    else:
        return f"{bounces} bounces"


def add_plus(string: str) -> str:
    """
    Adds a plus to a string if it doesn't start with a minus
    """
    if string[0] != "-":
        string = f"+{string}"
    return string


def draw_inventory_hover_text() -> None:
    """
    Checks if the player is hovering over an item in the UI and displays the item's info if they are
    """
    assert isinstance(entity_manager.get_client_player(), entity_manager.Player)
    pos = None

    # Inventory
    if pygame.Rect(5, 20, 480, 244).collidepoint(commons.MOUSE_POSITION):
        for hotbar_index in range(10):
            if pygame.Rect(5 + 48 * hotbar_index, 20, 48, 48).collidepoint(commons.MOUSE_POSITION):
                pos = [item.ItemLocation.HOTBAR, hotbar_index]
                break

        for inventory_index in range(40):
            slot_x = inventory_index % 10
            slot_y = inventory_index // 10
            if pygame.Rect(5 + 48 * slot_x, 67 + 48 * slot_y, 48, 48).collidepoint(commons.MOUSE_POSITION):
                pos = [item.ItemLocation.INVENTORY, inventory_index]
                break

    # Chest
    elif entity_manager.get_client_player().chest_open and pygame.Rect(245, 265, 384, 192).collidepoint(
            commons.MOUSE_POSITION
    ):
        for chest_index in range(20):
            slot_x = chest_index % 10
            slot_y = chest_index // 10
            if pygame.Rect(245 + 48 * slot_x, 265 + slot_y * 48, 48, 48).collidepoint(commons.MOUSE_POSITION):
                pos = [item.ItemLocation.CHEST, chest_index]
                break

    # Crafting menu
    elif pygame.Rect(5, 270, 48, 288).collidepoint(commons.MOUSE_POSITION):
        array_index = (commons.MOUSE_POSITION[1] - 270 - int(entity_manager.get_client_player().crafting_menu_offset_y)) // 48
        if 0 <= array_index < len(entity_manager.get_client_player().items[item.ItemLocation.CRAFTING_MENU]):
            if pygame.mouse.get_pressed()[0]:
                if not commons.is_holding_item:
                    item.item_holding = item.Item(
                        entity_manager.get_client_player().items[item.ItemLocation.CRAFTING_MENU][array_index][0],
                        amount=entity_manager.get_client_player().items[item.ItemLocation.CRAFTING_MENU][array_index][1],
                        auto_assign_prefix=True,
                    )
                    commons.is_holding_item = True
                    GameState.can_pickup_item = False
                    GameState.can_drop_holding = False
                    game_data.play_sound(item.item_holding.get_pickup_sound_id_str())
                elif GameState.can_drop_holding and item.item_holding is not None:
                    if (
                            item.item_holding.item_id
                            == entity_manager.get_client_player().items[item.ItemLocation.CRAFTING_MENU][array_index][0]
                    ):
                        if item.item_holding.amount < item.item_holding.get_max_stack():
                            item.item_holding.amount += entity_manager.get_client_player().items[
                                item.ItemLocation.CRAFTING_MENU
                            ][array_index][1]
                            game_data.play_sound("sound.grab")

            if render_stats_text([item.ItemLocation.CRAFTING_MENU, array_index]) and not commons.is_holding_item:
                commons.screen.blit(
                    GameState.stats_text,
                    (commons.MOUSE_POSITION[0] + 10, commons.MOUSE_POSITION[1] + 10),
                )

    if pos is not None:
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0] or mouse_buttons[2]:
            # Dropping holding item
            if GameState.can_drop_holding and item.item_holding is not None:
                if mouse_buttons[0]:
                    amount = item.item_holding.amount
                else:
                    amount = 1

                item_add_data = None

                if mouse_buttons[0] or GameState.item_drop_tick <= 0:
                    item_add_data = entity_manager.get_client_player().give_item(item.item_holding, amount, position=pos)

                if item_add_data is not None:
                    GameState.can_drop_holding = False

                    # Items are being dropped
                    if item_add_data[0] == item.ItemSlotClickResult.GAVE_ALL:
                        game_data.play_sound(item.item_holding.get_drop_sound_id_str())
                        if mouse_buttons[0]:
                            item.item_holding = None
                            commons.is_holding_item = False
                        else:
                            item.item_holding.amount -= 1

                    # Dropping some items
                    elif item_add_data[0] == item.ItemSlotClickResult.GAVE_SOME:
                        game_data.play_sound(item.item_holding.get_drop_sound_id_str())
                        item.item_holding.amount = int(item_add_data[1])

                    # Items are being swapped
                    elif item_add_data[0] == item.ItemSlotClickResult.SWAPPED:
                        game_data.play_sound(item.item_holding.get_drop_sound_id_str())
                        entity_manager.get_client_player().items[item_add_data[2]][pos[1]] = item.item_holding
                        item.item_holding = item_add_data[1]

                    if pos not in entity_manager.get_client_player().old_inventory_positions:
                        entity_manager.get_client_player().old_inventory_positions.append(pos)

                if GameState.item_drop_tick <= 0:
                    GameState.item_drop_rate -= 1
                    if GameState.item_drop_rate <= 0:
                        GameState.item_drop_rate = 0
                    GameState.item_drop_tick = int(GameState.item_drop_rate)
                    if item.item_holding is not None and item.item_holding.amount <= 0:
                        item.item_holding = None
                        commons.is_holding_item = False
                else:
                    GameState.item_drop_tick -= commons.DELTA_TIME

            # Picking up item
            elif GameState.can_pickup_item and not mouse_buttons[2]:
                GameState.can_pickup_item = False
                item.item_holding = entity_manager.get_client_player().remove_item(pos)
                if item.item_holding is not None:
                    game_data.play_sound(item.item_holding.get_pickup_sound_id_str())
                    commons.is_holding_item = True
                entity_manager.get_client_player().render_current_item_image()

        if render_stats_text(pos) and not commons.is_holding_item:
            commons.screen.blit(
                GameState.stats_text,
                (commons.MOUSE_POSITION[0] + 10, commons.MOUSE_POSITION[1] + 10),
            )

    elif pygame.mouse.get_pressed()[2] and commons.is_holding_item:
        if entity_manager.get_client_player().direction == 1:
            velocity = (32, random.random() * 2)
        else:
            velocity = (-32, random.random() * 2)

        entity_manager.spawn_physics_item(
            item.item_holding,
            entity_manager.get_client_player().position,
            velocity=velocity,
        )

        commons.is_holding_item = False
        GameState.can_drop_holding = False
        item.item_holding = None


def draw_item_holding() -> None:
    """Draws the exit button in the bottom left, also spawns the exit confirmation prompt"""
    if commons.is_holding_item and item.item_holding is not None:
        commons.screen.blit(
            item.item_holding.get_image(),
            (commons.MOUSE_POSITION[0] + 10, commons.MOUSE_POSITION[1] + 10),
        )
        if item.item_holding.amount > 1:
            commons.screen.blit(
                shared_methods.outline_text(
                    str(item.item_holding.amount),
                    pygame.Color(255, 255, 255),
                    commons.SMALL_FONT,
                ),
                (commons.MOUSE_POSITION[0] + 34, commons.MOUSE_POSITION[1] + 40),
            )


def draw_exit_button() -> None:
    """
    Draws the exit button in the bottom left, also spawns the exit confirmation prompt
    """
    global exit_button_hover
    top = commons.WINDOW_HEIGHT - 20
    left = commons.WINDOW_WIDTH - 100
    if pygame.Rect(left, top, 50, 20).collidepoint(commons.MOUSE_POSITION):
        if not exit_button_hover:
            exit_button_hover = True
            game_data.play_sound("sound.menu_select")
        color = pygame.Color(230, 230, 0)
        if pygame.mouse.get_pressed()[0]:
            entity_manager.get_client_player().inventory_open = False
            entity_manager.get_client_player().chest_open = False
            entity_manager.client_prompt = prompt.Prompt(
                "Exit",
                game_data.EXIT_MESSAGES[random.randint(0, len(game_data.EXIT_MESSAGES) - 1)],
                button_1_name="Yep",
                size=(6, 2),
            )
            commons.WAIT_TO_USE = True
    else:
        color = pygame.Color(255, 255, 255)
        exit_button_hover = False
    exit_text = shared_methods.outline_text("Save and Quit", color, commons.DEFAULT_FONT)
    commons.screen.blit(exit_text, (left, top))


def draw_interactive_block_hover() -> None:
    """
    Draws the item image of an interactive block being hovered by the mouse
    """
    if world.tile_in_map(commons.HOVERED_TILE[0], commons.HOVERED_TILE[1]):
        tile_id = world.world.tile_data[commons.HOVERED_TILE[0]][commons.HOVERED_TILE[1]][0]
        tile_data = game_data.get_tile_by_id(tile_id)
        if tile_data is not None:
            if commons.TileTag.CHEST in tile_data.tags or commons.TileTag.CYCLABLE in tile_data.tags:
                item_data = game_data.get_item_by_id_str(tile_data.item_id_str)
                if item_data is not None:
                    commons.screen.blit(item_data.surface, commons.MOUSE_POSITION)


def draw_menu_background() -> None:
    """
    Draws the menu background
    """
    BACKGROUND_DATA.update_biome(Biome.TREE)
    BACKGROUND_DATA.render()
    BACKGROUND_DATA.shift(commons.DELTA_TIME * 10, 0.2)
    BACKGROUND_DATA.update(commons.DELTA_TIME)


# Initialize game state
GameState.LIGHT_RENDER_DISTANCE_X = int((commons.WINDOW_WIDTH * 0.5) / commons.BLOCK_SIZE) + 9
GameState.LIGHT_RENDER_DISTANCE_Y = int((commons.WINDOW_HEIGHT * 0.5) / commons.BLOCK_SIZE) + 9

# MAX SURF WIDTH IS 16,383

pygame.display.set_caption("Terraria")

song_end_event = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(song_end_event)

ICON = pygame.image.load("assets/images/favicon/favicon.png")
pygame.display.set_icon(ICON)

clock = pygame.time.Clock()

if commons.SPLASHSCREEN:
    run_splash_screen()

fps_text = shared_methods.outline_text(str(0), pygame.Color(255, 255, 255), commons.DEFAULT_FONT)

fade_surf = pygame.Surface((0, 0))
global_lighting = 255

load_menu_surf = shared_methods.create_menu_surface(7, 8, "")
load_menu_box_left1 = commons.WINDOW_WIDTH * 0.5 - 336 * 0.5
load_menu_box_left2 = commons.WINDOW_WIDTH * 0.5 - 315 * 0.5

menu_logo = pygame.image.load("assets/images/logo/logo.png")

old_time_milliseconds = pygame.time.get_ticks()

