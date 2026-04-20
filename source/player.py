import datetime
import math
import pickle
import random
from enum import Enum

import pygame
from pygame.locals import Rect

import commons
import entity_manager
import game_data
import item
import shared_methods
import tilesets
import world
from item import Item, ItemLocation, ItemSlotClickResult, ItemTag


def get_death_message(name, source):
    """
    Uses the player's name, the thing that killed them, and the worlds name to generate a random death message
    """
    string = game_data.DEATH_LINES[source[0]][random.randint(0, len(game_data.DEATH_LINES[source[0]]) - 1)]
    string = string.replace("<p>", name)
    string = string.replace("<w>", world.world.name)
    string = string.replace("<e>", source[1])
    return string


class Movement(Enum):
    LEFT = 0
    RIGHT = 1
    IDLE = 3


class MovementFrames:
    def __init__(
            self,
            total_frames: int,
            walk_range: tuple[int, int] | None = None,
            swing_range: tuple[int, int] | None = None,
            jump_frame: int | None = None,
            hold_frame: int | None = None,
            idle_frame: int | None = None,
    ) -> None:
        self.total_frames = total_frames
        self.current_frame = 0
        self.walk_range = walk_range
        self.swing_range = swing_range
        self.jump_frame = jump_frame
        self.hold_frame = hold_frame
        self.idle_frame = idle_frame
        self.animation_speed = 0.5 / (self.walk_range[1] - self.walk_range[0]) if self.walk_range is not None else 1
        self.animation_tick = 0

    def walk(self, swinging: bool, swing_frame: int) -> None:
        if swinging and self.swing_range is not None:
            self.swing(swing_frame)
        else:
            if self.animation_tick <= 0:
                self.animation_tick += self.animation_speed
                if self.walk_range is not None:
                    self.current_frame = (
                        self.current_frame + 1
                        if self.walk_range[0] <= self.current_frame < self.walk_range[1]
                        else self.walk_range[0]
                    )
            else:
                self.animation_tick -= commons.DELTA_TIME

    def swing(self, frame: int) -> None:
        if self.swing_range is not None:
            self.current_frame = min(self.swing_range[0] + frame, self.swing_range[1])

    def jump(self, swinging: bool, swing_frame: int) -> None:
        if swinging and self.swing_range is not None:
            self.swing(swing_frame)
        elif self.jump_frame is not None:
            if self.animation_tick <= 0:
                self.animation_tick += self.animation_speed
                self.current_frame = self.jump_frame
            else:
                self.animation_tick -= commons.DELTA_TIME

    def hold(self, swinging: bool, swing_frame: int) -> None:
        if swinging and self.swing_range is not None:
            self.swing(swing_frame)
        else:
            if self.animation_tick <= 0:
                self.animation_tick += self.animation_speed
                if self.hold_frame is not None:
                    self.current_frame = self.hold_frame
            else:
                self.animation_tick -= commons.DELTA_TIME

    def idle(self, swinging: bool, swing_frame: int) -> None:
        if swinging and self.swing_range is not None:
            self.swing(swing_frame)
        else:
            if self.animation_tick <= 0:
                self.animation_tick += self.animation_speed
                if self.idle_frame is not None:
                    self.current_frame = self.idle_frame
            else:
                self.animation_tick -= commons.DELTA_TIME


class Model:
    """
    Stores information about the appearance of a player
    """

    def __init__(self, model_appearance: commons.PlayerAppearance) -> None:
        self.swinging: bool = False
        self.flip: bool = False
        self.moving_left: bool = False
        self.moving_right: bool = False
        self.moving_down: bool = False
        self.arm_radians: float = 0
        self.swing_radians: tuple[float, ...] = (
            math.radians(-130),
            math.radians(-85),
            math.radians(-40),
            math.radians(5),
            math.radians(50),
        )

        self.hair_frames: MovementFrames = MovementFrames(14)
        self.head_frames: MovementFrames = MovementFrames(20)
        self.eye_frames: MovementFrames = MovementFrames(20)
        self.pupil_frames: MovementFrames = MovementFrames(20)
        self.undershirt_frames: MovementFrames = MovementFrames(1)
        self.shirt_frames: MovementFrames = MovementFrames(1)
        self.trouser_frames: MovementFrames = MovementFrames(20, walk_range=(6, 19), jump_frame=5, idle_frame=0)
        self.shoe_frames: MovementFrames = MovementFrames(20, walk_range=(6, 19), jump_frame=5, idle_frame=0)
        self.arm_frames: MovementFrames = MovementFrames(
            28, walk_range=(8, 11), swing_range=(1, 4), jump_frame=7, hold_frame=3, idle_frame=0
        )
        self.sleeve_frames: MovementFrames = MovementFrames(
            28, walk_range=(8, 11), swing_range=(1, 4), jump_frame=7, hold_frame=3, idle_frame=0
        )

        self.sex = model_appearance["sex"]
        self.hair_id = model_appearance["hair_id"]
        self.skin_col = model_appearance["skin_color"]
        self.hair_col = model_appearance["hair_color"]
        self.eye_col = model_appearance["eye_color"]
        self.shirt_col = model_appearance["shirt_color"]
        self.undershirt_col = model_appearance["undershirt_color"]
        self.trouser_col = model_appearance["trouser_color"]
        self.shoe_col = model_appearance["shoe_color"]

        self.SURFACE_WIDTH = 40
        self.SURFACE_HEIGHT = 56

    def create_sprite(self) -> pygame.Surface:
        mirror_arm_frame = 14
        offset = (0, 0)
        player_surface: pygame.Surface = pygame.Surface((self.SURFACE_WIDTH, self.SURFACE_HEIGHT), pygame.SRCALPHA)
        player_surface.blit(
            shared_methods.transparent_color_surface(
                tilesets.undershirts[self.undershirt_frames.current_frame], self.undershirt_col
            ),
            offset,
        )
        player_surface.blit(
            shared_methods.transparent_color_surface(tilesets.shirts[self.shirt_frames.current_frame], self.shirt_col),
            offset,
        )
        player_surface.blit(
            shared_methods.transparent_color_surface(
                tilesets.trousers[self.trouser_frames.current_frame], self.trouser_col
            ),
            offset,
        )
        player_surface.blit(
            shared_methods.transparent_color_surface(tilesets.shoes[self.shoe_frames.current_frame], self.shoe_col),
            offset,
        )
        player_surface.blit(
            shared_methods.transparent_color_surface(tilesets.head[self.head_frames.current_frame], self.skin_col),
            offset,
        )
        player_surface.blit(
            shared_methods.transparent_color_surface(
                tilesets.hair[self.hair_id][self.hair_frames.current_frame], self.hair_col
            ),
            offset,
        )
        player_surface.blit(
            shared_methods.transparent_color_surface(
                tilesets.eyes[self.eye_frames.current_frame], pygame.Color(255, 255, 255)
            ),
            offset,
        )
        player_surface.blit(
            shared_methods.transparent_color_surface(tilesets.pupils[self.pupil_frames.current_frame], self.eye_col),
            offset,
        )
        player_surface.blit(
            shared_methods.transparent_color_surface(tilesets.arms[self.arm_frames.current_frame], self.skin_col),
            offset,
        )
        player_surface.blit(
            shared_methods.transparent_color_surface(
                tilesets.arms[self.arm_frames.current_frame + mirror_arm_frame], self.skin_col
            ),
            offset,
        )
        player_surface.blit(
            shared_methods.transparent_color_surface(
                tilesets.sleeves[self.sleeve_frames.current_frame], self.undershirt_col
            ),
            offset,
        )
        player_surface.blit(
            shared_methods.transparent_color_surface(
                tilesets.sleeves[self.sleeve_frames.current_frame + mirror_arm_frame], self.undershirt_col
            ),
            offset,
        )
        player_surface = pygame.transform.flip(player_surface, self.flip, False)
        return player_surface

    def get_appearance(self) -> commons.PlayerAppearance:
        return {
            "sex": self.sex,
            "hair_id": self.hair_id,
            "skin_color": self.skin_col,
            "hair_color": self.hair_col,
            "eye_color": self.eye_col,
            "shirt_color": self.shirt_col,
            "undershirt_color": self.undershirt_col,
            "trouser_color": self.trouser_col,
            "shoe_color": self.shoe_col,
        }

    def get_movement(self) -> Movement:
        if self.moving_left ^ self.moving_right:
            if self.moving_left:
                return Movement.LEFT
            else:
                return Movement.RIGHT
        return Movement.IDLE

    def get_flip(self) -> bool:
        return self.get_movement() == Movement.LEFT or (not self.get_movement() == Movement.RIGHT and self.flip)

    def get_swing_frame(self) -> int:
        if not self.flip:
            return min(
                range(len(self.swing_radians)), key=lambda index: abs(self.swing_radians[index] - self.arm_radians)
            )
        else:
            return min(
                range(len(self.swing_radians)), key=lambda index: abs(-self.swing_radians[index] - self.arm_radians)
            )

    def walk(self) -> None:
        self.flip = self.get_flip()
        swing_frame: int = self.get_swing_frame()
        self.hair_frames.walk(self.swinging, swing_frame)
        self.head_frames.walk(self.swinging, swing_frame)
        self.eye_frames.walk(self.swinging, swing_frame)
        self.pupil_frames.walk(self.swinging, swing_frame)
        self.undershirt_frames.walk(self.swinging, swing_frame)
        self.shirt_frames.walk(self.swinging, swing_frame)
        self.trouser_frames.walk(self.swinging, swing_frame)
        self.shoe_frames.walk(self.swinging, swing_frame)
        self.arm_frames.walk(self.swinging, swing_frame)
        self.sleeve_frames.walk(self.swinging, swing_frame)

    def jump(self) -> None:
        self.flip = self.get_flip()
        swing_frame: int = self.get_swing_frame()
        self.hair_frames.jump(self.swinging, swing_frame)
        self.head_frames.jump(self.swinging, swing_frame)
        self.eye_frames.jump(self.swinging, swing_frame)
        self.pupil_frames.jump(self.swinging, swing_frame)
        self.undershirt_frames.jump(self.swinging, swing_frame)
        self.shirt_frames.jump(self.swinging, swing_frame)
        self.trouser_frames.jump(self.swinging, swing_frame)
        self.shoe_frames.jump(self.swinging, swing_frame)
        self.arm_frames.jump(self.swinging, swing_frame)
        self.sleeve_frames.jump(self.swinging, swing_frame)

    def hold(self) -> None:
        self.flip = self.get_flip()
        swing_frame: int = self.get_swing_frame()
        self.hair_frames.hold(self.swinging, swing_frame)
        self.head_frames.hold(self.swinging, swing_frame)
        self.eye_frames.hold(self.swinging, swing_frame)
        self.pupil_frames.hold(self.swinging, swing_frame)
        self.undershirt_frames.hold(self.swinging, swing_frame)
        self.shirt_frames.hold(self.swinging, swing_frame)
        self.trouser_frames.hold(self.swinging, swing_frame)
        self.shoe_frames.hold(self.swinging, swing_frame)
        self.arm_frames.hold(self.swinging, swing_frame)
        self.sleeve_frames.hold(self.swinging, swing_frame)

    def idle(self) -> None:
        self.flip = self.get_flip()
        swing_frame: int = self.get_swing_frame()
        self.hair_frames.idle(self.swinging, swing_frame)
        self.head_frames.idle(self.swinging, swing_frame)
        self.eye_frames.idle(self.swinging, swing_frame)
        self.pupil_frames.idle(self.swinging, swing_frame)
        self.undershirt_frames.idle(self.swinging, swing_frame)
        self.shirt_frames.idle(self.swinging, swing_frame)
        self.trouser_frames.idle(self.swinging, swing_frame)
        self.shoe_frames.idle(self.swinging, swing_frame)
        self.arm_frames.idle(self.swinging, swing_frame)
        self.sleeve_frames.idle(self.swinging, swing_frame)





class Player:
    """
    Performs physics and renders a player within the current world
    """

    def __init__(
            self,
            position: tuple[float, float],
            model,
            name="unassigned",
            hp=0,
            max_hp=100,
            hotbar=None,
            inventory=None,
            playtime=0,
            creation_date=None,
            last_played_date=None,
    ):
        self.grounded = False
        self.position: tuple[float, float] = position
        self.block_position = (0, 0)
        self.model = model
        self.name = name
        self.hp = hp if hp > 0 else max_hp
        self.max_hp = max_hp

        self.items: dict[ItemLocation, list[Item | None]] = {
            ItemLocation.HOTBAR: hotbar,
            ItemLocation.INVENTORY: inventory,
            ItemLocation.CHEST: [None for _ in range(20)],
            ItemLocation.CRAFTING_MENU: [],
        }

        self.hotbar_index = 0

        # Save stats
        self.playtime = playtime

        date = datetime.datetime.now()

        if creation_date is None:
            self.creation_date = date
        else:
            self.creation_date = creation_date

        if last_played_date is None:
            self.last_played_date = date
        else:
            self.last_played_date = last_played_date

        self.sprites = Model(self.model)

        self.rect = Rect(
            self.position[0] - commons.PLAYER_WIDTH * 0.5,
            self.position[1] - commons.PLAYER_HEIGHT * 0.5,
            commons.PLAYER_WIDTH,
            commons.PLAYER_HEIGHT,
        )
        self.velocity = (0, 0)

        self.alive = True
        self.respawn_time = 3
        self.respawn_time_remaining = self.respawn_time
        self.death_message_alpha = 0

        self.invincible_timer = 2.0
        self.invincible = True

        hp_text_color = pygame.Color(
            int(255 * (1 - self.hp / self.max_hp)),
            int(255 * (self.hp / self.max_hp)),
            0,
        )
        self.hp_text = shared_methods.outline_text(
            str(self.hp),
            hp_text_color,
            commons.DEFAULT_FONT,
            outline_color=pygame.Color(
                hp_text_color[0] // 2,
                hp_text_color[1] // 2,
                hp_text_color[2] // 2,
            ),
        )
        self.hp_x_position = commons.WINDOW_WIDTH - 10 - self.hp - self.hp_text.get_width() * 0.5

        self.moving_down_tick = 0
        self.stop_moving_down = False

        self.stop_left = False
        self.stop_right = False

        self.direction = 1

        self.swinging_arm = False
        self.should_swing_arm = False

        self.holding_arm = False
        self.should_hold_arm = False

        self.last_block_on = 0

        self.knockback_resist = 0
        self.defense = 0

        self.use_tick = 0
        self.use_delay = 0
        self.use_delta = 0
        self.can_use = False
        self.arm_out = False
        self.arm_out_angle = 0
        self.swing_angle = 0
        self.item_swing = False
        self.item_extend = False
        self.current_item_image = None
        self.current_item_swing_image = None
        self.current_item_swing_offset = 0
        self.current_item_extend_image = None
        self.current_item_extend_offset = 0
        self.enemies_hit = []

        self.un_pickupable_items = []

        self.hotbar_image = pygame.Surface((480, 48))
        self.hotbar_image.set_colorkey((255, 0, 255))

        self.inventory_image = pygame.Surface((480, 192))
        self.inventory_image.set_colorkey((255, 0, 255))

        self.chest_image = pygame.Surface((240, 192))
        self.chest_image.set_colorkey((255, 0, 255))

        self.blit_craft_surf = pygame.Surface((48, 288))
        self.blit_craft_surf.set_colorkey((255, 0, 255))

        self.craftable_items_surf = pygame.Surface((48, 0))

        self.crafting_menu_offset_y = 120
        self.crafting_menu_offset_velocity_y = 0

        self.inventory_open = False
        self.chest_open = False

        self.old_inventory_positions = []
        from player_components import PlayerPhysics, PlayerInventory, PlayerCombat, PlayerInteraction, PlayerRenderer
        self.physics = PlayerPhysics()
        self.inventory = PlayerInventory()
        self.combat = PlayerCombat()
        self.interaction = PlayerInteraction()
        self.renderer = PlayerRenderer()

    def update(self):
            return self.physics.update(self)

    def damage(self, value: int, source_name: tuple[str, str], knockback: int = 0, direction: int = 0, source_velocity: tuple[float, float] = (0, 0)) -> None:
            return self.combat.damage(self, value, source_name, knockback, direction, source_velocity)

    def kill(self, source, source_velocity=None):
            return self.combat.kill(self, source, source_velocity)

    def respawn(self):
            return self.combat.respawn(self)

    def render_current_item_image(self):
            return self.renderer.render_current_item_image(self)

    def animate(self):
            return self.renderer.animate(self)

    def use_item(self, right_click=False):
            return self.interaction.use_item(self, right_click)

    def place_block(self, screen_position_x, screen_position_y, block_item, is_tile):
            return self.interaction.place_block(self, screen_position_x, screen_position_y, block_item, is_tile)

    def use_tool(self, screen_position_x, screen_position_y, tool_item):
            return self.interaction.use_tool(self, screen_position_x, screen_position_y, tool_item)

    def use_longsword_weapon(self, longsword_weapon_item) -> None:
            return self.interaction.use_longsword_weapon(self, longsword_weapon_item)

    def use_shortsword_weapon(self, shortsword_weapon_item) -> None:
            return self.interaction.use_shortsword_weapon(self, shortsword_weapon_item)

    def use_ranged_weapon(self, screen_position_x, screen_position_y, ranged_weapon_item) -> None:
            return self.interaction.use_ranged_weapon(self, screen_position_x, screen_position_y, ranged_weapon_item)

    def give_item(self, current_item, amount=1, position=None):
            return self.inventory.give_item(self, current_item, amount, position)

    def remove_item(self, position, remove_count=None):
            return self.inventory.remove_item(self, position, remove_count)

    def find_existing_item_stacks(self, item_id, search_hotbar=True, search_inventory=True):
            return self.inventory.find_existing_item_stacks(self, item_id, search_hotbar, search_inventory)

    def find_free_spaces(self, max_stack=9999, search_hotbar=True, search_inventory=True):
            return self.inventory.find_free_spaces(self, max_stack, search_hotbar, search_inventory)

    def render_hotbar(self):
            return self.renderer.render_hotbar(self)

    def render_inventory(self):
            return self.renderer.render_inventory(self)

    def render_chest(self):
            return self.renderer.render_chest(self)

    def update_inventory_old_slots(self):
            return self.inventory.update_inventory_old_slots(self)

    def update_craftable_items(self):
            return self.inventory.update_craftable_items(self)

    def render_craftable_items_surf(self):
            return self.renderer.render_craftable_items_surf(self)

    def draw(self):
            return self.renderer.draw(self)

    def draw_hp(self):
            return self.renderer.draw_hp(self)

    def open_chest(self, items):
            return self.inventory.open_chest(self, items)

    def save(self):
        """
        Packs the important player data into an array and serializes it using the pickle module
        """
        # Convert the items    in the hotbar to a less    data heavy format
        formatted_hotbar = []
        for item_index in range(len(self.items[ItemLocation.HOTBAR])):
            current_item = self.items[ItemLocation.HOTBAR][item_index]
            if current_item is not None:
                if current_item.prefix_data is None:
                    formatted_hotbar.append([item_index, current_item.get_id_str(), current_item.amount, None])
                else:
                    formatted_hotbar.append(
                        [
                            item_index,
                            current_item.get_id_str(),
                            current_item.amount,
                            current_item.get_prefix_name(),
                        ]
                    )

        # Convert the items    in the inventory to a less data    heavy format
        formatted_inventory = []
        for item_index in range(len(self.items[ItemLocation.INVENTORY])):
            current_item: None | Item = self.items[ItemLocation.INVENTORY][item_index]
            if current_item is not None:
                if current_item.prefix_data is None:
                    formatted_inventory.append((item_index, current_item.get_id_str(), current_item.amount, ""))
                else:
                    formatted_inventory.append(
                        (
                            item_index,
                            current_item.get_id_str(),
                            current_item.amount,
                            current_item.get_prefix_name(),
                        )
                    )

        # Save the data to disk and display a message
        commons.PLAYER_DATA["name"] = self.name
        commons.PLAYER_DATA["model_appearance"] = self.model
        commons.PLAYER_DATA["hotbar"] = formatted_hotbar
        commons.PLAYER_DATA["inventory"] = formatted_inventory
        commons.PLAYER_DATA["hp"] = self.hp
        commons.PLAYER_DATA["max_hp"] = self.max_hp
        commons.PLAYER_DATA["playtime"] = self.playtime
        commons.PLAYER_DATA["creation_date"] = self.creation_date
        commons.PLAYER_DATA["last_played_date"] = self.last_played_date
        pickle.dump(commons.PLAYER_DATA, open(f"assets/players/{self.name}.player", "wb"))  # Save player array
        entity_manager.add_message("Saved Player: " + self.name + "!", pygame.Color(255, 255, 255))

    def jump(self):
        """
        Plays a sound, spawns particles, and sets the player's y velocity
        """
        if self.alive and self.grounded:
            game_data.play_sound("sound.jump")
            if commons.PARTICLES:
                color = pygame.transform.average_color(game_data.get_tile_by_id(self.last_block_on).image)
                for _ in range(int(random.randint(5, 8) * commons.PARTICLE_DENSITY)):
                    entity_manager.spawn_particle(
                        (self.position[0], self.position[1] + commons.BLOCK_SIZE * 1.5),
                        color,
                        size=10,
                        life=1,
                        angle=-math.pi * 0.5,
                        spread=math.pi * 0.33,
                        gravity=0.2,
                        magnitude=1.5 + random.random() * 10,
                    )
            self.velocity = (self.velocity[0], -50)
            self.grounded = False

    def get_date_created_string(self):
        return str(self.creation_date)[:19]

    def get_last_date_played_string(self):
        return str(self.last_played_date)[:19]
