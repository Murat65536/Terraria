import datetime
import math
import pickle
import random
from enum import Enum

import commons
import entity_manager
import game_data
import item
import pygame
import shared_methods
import tilesets
import world
from item import Item, ItemLocation, ItemSlotClickResult, ItemTag
from pygame.locals import Rect

"""=================================================================================================================
    player.get_death_message -> string

    Uses the player's name, the thing that killed them, and the worlds name to generate a random death message
-----------------------------------------------------------------------------------------------------------------"""


def get_death_message(name, source):
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


"""=================================================================================================================
    player.Model

    Stores information about the appearance of a player
-----------------------------------------------------------------------------------------------------------------"""


class Model:
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


class ItemStorage:
    def __init__(self, hotbar=None, inventory=None):
        self.hotbar: list[None] | list[Item] = hotbar
        self.inventory: list[None] | list[Item] = inventory
        self.chest: list[None] | list[Item] = [None for _ in range(20)]
        self.crafting_menu: list[None] | list[Item] = []


"""=================================================================================================================
    player.Player

    Performs physics and renders a player within the current world
-----------------------------------------------------------------------------------------------------------------"""


class Player:
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

        self.items: dict[ItemLocation, list[None] | list[Item]] = {
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

    """=================================================================================================================
        player.Player.update -> void

        Updates many variables within the player object
    -----------------------------------------------------------------------------------------------------------------"""

    def update(self):
        if self.alive:
            if self.invincible:
                if self.invincible_timer <= 0.0:
                    self.invincible = False
                else:
                    self.invincible_timer -= commons.DELTA_TIME

            if self.sprites.get_movement() == Movement.LEFT:
                if not self.stop_left:
                    if self.sprites.moving_down:
                        self.velocity = (-5, self.velocity[1])
                    else:
                        self.velocity = (-12, self.velocity[1])
            elif self.sprites.get_movement() == Movement.RIGHT:
                if not self.stop_right:
                    if self.sprites.moving_down:
                        self.velocity = (5, self.velocity[1])
                    else:
                        self.velocity = (12, self.velocity[1])

            drag_factor = 1.0 - commons.DELTA_TIME

            self.velocity = (
                self.velocity[0] * drag_factor,
                self.velocity[1] * drag_factor + commons.GRAVITY * commons.DELTA_TIME,
            )
            self.position: tuple[float, float] = (
                self.position[0] + self.velocity[0] * commons.DELTA_TIME * commons.BLOCK_SIZE,
                self.position[1] + self.velocity[1] * commons.DELTA_TIME * commons.BLOCK_SIZE,
            )

            self.rect.left = self.position[0] - commons.PLAYER_WIDTH * 0.5
            self.rect.top = self.position[1] - commons.PLAYER_HEIGHT * 0.5

            self.block_position = (
                int(self.position[1] // commons.BLOCK_SIZE),
                int(self.position[0] // commons.BLOCK_SIZE),
            )

            self.grounded = False

            self.stop_left = False
            self.stop_right = False

            fall_damaged = False

            if not self.can_use:
                if self.use_tick > self.use_delay:
                    self.arm_out = False
                    self.can_use = True
                    self.item_swing = False
                    self.item_extend = False
                    self.swinging_arm = False
                    self.holding_arm = False
                else:
                    self.use_tick += commons.DELTA_TIME
                    if self.use_delay > 0.0001:
                        self.use_delta = self.use_tick / self.use_delay

            if self.velocity[0] < 0:
                if self.position[0] < world.border_left:
                    self.position = (int(world.border_left), self.position[1])
            elif self.velocity[0] > 0:
                if self.position[0] > world.border_right:
                    self.position = (int(world.border_right), self.position[1])
            if self.velocity[1] < 0:
                if self.position[1] < world.border_up:
                    self.position = (self.position[0], int(world.border_up))
                    self.velocity = (self.velocity[0], 0)
            elif self.velocity[1] > 0:
                if self.position[1] > world.border_down:
                    self.position = (self.position[0], int(world.border_down))
                    self.velocity = (self.velocity[0], 0)
                    self.grounded = True

            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                use = False
                if self.inventory_open:
                    if (
                        not Rect(5, 5, 480, 244).collidepoint(commons.MOUSE_POSITION)
                        and not Rect(
                            commons.WINDOW_WIDTH - 50,
                            commons.WINDOW_HEIGHT - 20,
                            50,
                            20,
                        ).collidepoint(commons.MOUSE_POSITION)
                        and not Rect(5, 270, 48, 288).collidepoint(commons.MOUSE_POSITION)
                    ):
                        if self.chest_open:
                            if not Rect(245, 265, 240, 192).collidepoint(commons.MOUSE_POSITION):
                                use = True
                        else:
                            use = True
                else:
                    use = True
                if use and entity_manager.client_prompt is None and not commons.WAIT_TO_USE:
                    if pygame.mouse.get_pressed()[0]:
                        self.use_item()
                    elif pygame.mouse.get_pressed()[2]:
                        self.use_item(right_click=True)

            collide = False

            for j in range(-2, 3):
                for i in range(-2, 3):
                    if world.tile_in_map(self.block_position[1] + j, self.block_position[0] + i):
                        if self.block_position[1] + j >= 0:
                            tile_id = world.world.tile_data[self.block_position[1] + j][self.block_position[0] + i][0]
                            tile_data = game_data.get_tile_by_id(tile_id)
                            if commons.TileTag.NO_COLLIDE not in tile_data.tags:
                                block_rect = Rect(
                                    commons.BLOCK_SIZE * (self.block_position[1] + j),
                                    commons.BLOCK_SIZE * (self.block_position[0] + i),
                                    commons.BLOCK_SIZE,
                                    commons.BLOCK_SIZE,
                                )
                                is_platform = False
                                if commons.TileTag.PLATFORM in tile_data.tags:
                                    is_platform = True
                                    if block_rect.colliderect(
                                        int(self.rect.left - 1),
                                        int(self.rect.top + 2),
                                        1,
                                        int(self.rect.height - 4),
                                    ):
                                        self.stop_left = True  # is there a solid block left
                                    if block_rect.colliderect(
                                        int(self.rect.right + 1),
                                        int(self.rect.top + 2),
                                        1,
                                        int(self.rect.height - 4),
                                    ):
                                        self.stop_right = True  # is there a solid block right
                                if block_rect.colliderect(self.rect):
                                    if not self.invincible and commons.TileTag.DAMAGING in tile_data.tags:
                                        self.damage(
                                            tile_data.tile_damage,
                                            (tile_data.tile_damage_name, "World"),
                                        )

                                    delta_x = self.position[0] - block_rect.centerx
                                    delta_y = self.position[1] - block_rect.centery
                                    if abs(delta_x) > abs(delta_y):
                                        if delta_x > 0:
                                            if not is_platform:
                                                self.position = (
                                                    block_rect.right + commons.PLAYER_WIDTH * 0.5,
                                                    self.position[1],
                                                )  # Move player right
                                                self.velocity = (
                                                    0,
                                                    self.velocity[1],
                                                )  # Stop player horizontally
                                        else:
                                            if not is_platform:
                                                self.position = (
                                                    block_rect.left - commons.PLAYER_WIDTH * 0.5,
                                                    self.position[1],
                                                )  # Move player left
                                                self.velocity = (
                                                    0,
                                                    self.velocity[1],
                                                )  # Stop player horizontally
                                    else:
                                        if delta_y > 0:
                                            if self.velocity[1] < 0:
                                                if not is_platform:
                                                    if Rect(
                                                        self.rect.left + 3,
                                                        self.rect.top,
                                                        self.rect.width - 6,
                                                        self.rect.height,
                                                    ).colliderect(block_rect):
                                                        self.position = (
                                                            self.position[0],
                                                            block_rect.bottom + commons.PLAYER_HEIGHT * 0.5,
                                                        )  # Move player down
                                                        self.velocity = (
                                                            self.velocity[0],
                                                            0,
                                                        )  # Stop player vertically
                                        else:
                                            if self.velocity[1] > 0:
                                                if Rect(
                                                    self.rect.left + 3,
                                                    self.rect.top,
                                                    self.rect.width - 6,
                                                    self.rect.height,
                                                ).colliderect(block_rect):
                                                    if is_platform:
                                                        if self.sprites.moving_down:
                                                            collide = False
                                                        else:
                                                            if self.velocity[1] < 5:
                                                                if (
                                                                    self.position[1] + commons.BLOCK_SIZE
                                                                    < block_rect.top
                                                                ):
                                                                    collide = True
                                                            else:
                                                                collide = True
                                                    else:
                                                        collide = True
                                                    if collide:
                                                        if not fall_damaged:
                                                            if self.velocity[1] > 58:
                                                                damage = int(
                                                                    (self.velocity[1] - 57) ** 2
                                                                )  # Work out fall damage
                                                                self.damage(
                                                                    damage,
                                                                    (
                                                                        "falling",
                                                                        "World",
                                                                    ),
                                                                )  # Apply fall damage once
                                                                fall_damaged = True
                                                        self.last_block_on = int(tile_id)
                                                        self.moving_down_tick = -1
                                                        self.position = (
                                                            self.position[0],
                                                            block_rect.top - commons.PLAYER_HEIGHT * 0.5 + 1,
                                                        )  # Move player up
                                                        self.velocity = (
                                                            self.velocity[0] * 0.5,
                                                            0,
                                                        )  # Slow down player horizontally and stop player vertically
                                                        self.grounded = True

            if self.stop_moving_down:
                if self.moving_down_tick < 0:
                    self.sprites.moving_left = False
                    self.sprites.moving_right = False
                    self.stop_moving_down = False
                else:
                    self.moving_down_tick -= self.velocity[1]

            if self.inventory_open:
                self.crafting_menu_offset_velocity_y *= 1.0 - commons.DELTA_TIME * 10
                self.crafting_menu_offset_y += self.crafting_menu_offset_velocity_y * commons.DELTA_TIME
                if self.crafting_menu_offset_y < -len(self.items[ItemLocation.CRAFTING_MENU]) * 48 + 168:
                    self.crafting_menu_offset_y = -len(self.items[ItemLocation.CRAFTING_MENU]) * 48 + 168
                elif self.crafting_menu_offset_y > 120:
                    self.crafting_menu_offset_y = 120

        else:
            if self.respawn_time_remaining > 0:
                self.respawn_time_remaining -= commons.DELTA_TIME
            else:
                self.respawn()
            if self.death_message_alpha > 0:
                self.death_message_alpha -= commons.DELTA_TIME / self.respawn_time

        self.update_inventory_old_slots()

    """=================================================================================================================
        player.Player.damage -> void

        Kills the player, adds a death message, spawns particles, plays a sound
    -----------------------------------------------------------------------------------------------------------------"""

    def damage(
        self,
        value: int,
        source_name: tuple[str, str],
        knockback: int = 0,
        direction: int = 0,
        source_velocity: tuple[float, float] = (0, 0),
    ) -> None:
        if not commons.CREATIVE and self.alive and not self.invincible:
            self.invincible = True
            self.invincible_timer = 0.35

            value -= self.defense
            value += random.randint(-1, 1)
            if value < 1:
                value = 1
            self.hp -= value

            entity_manager.add_damage_number(self.position, value, color=(240, 20, 20))

            if self.hp < 0:
                self.hp = 0

            if self.hp > 0:
                game_data.play_sound("sound.player_hurt")

                if commons.PARTICLES:
                    if source_velocity != (0, 0):
                        velocity_angle = math.atan2(
                            self.velocity[1] + source_velocity[0],
                            self.velocity[0] + source_velocity[1],
                        )
                        velocity_magnitude = math.sqrt(
                            (self.velocity[0] + source_velocity[0]) ** 2 + (self.velocity[1] + source_velocity[1]) ** 2
                        )
                    else:
                        velocity_angle = math.atan2(self.velocity[1], self.velocity[0])
                        velocity_magnitude = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

                    for _ in range(int(10 * commons.PARTICLE_DENSITY)):  # blood
                        particle_pos = (
                            self.position[0] + random.random() * commons.PLAYER_WIDTH - commons.PLAYER_WIDTH * 0.5,
                            self.position[1] + random.random() * commons.PLAYER_HEIGHT - commons.PLAYER_HEIGHT * 0.5,
                        )
                        entity_manager.spawn_particle(
                            particle_pos,
                            pygame.Color(230, 0, 0),
                            life=1,
                            size=10,
                            angle=velocity_angle,
                            spread=math.pi * 0.2,
                            magnitude=random.random() * velocity_magnitude,
                            gravity=0.15,
                            outline=True,
                        )
            else:
                self.kill(source_name, source_velocity)

            if knockback != 0:
                remaining_knockback = max(0, knockback - self.knockback_resist)
                self.velocity = (
                    self.velocity[0] + direction * remaining_knockback,
                    remaining_knockback * -1.5,
                )

        hp_float = self.hp / self.max_hp
        self.hp_text = shared_methods.outline_text(
            str(self.hp),
            pygame.Color(int((1 - hp_float) * 255), int(hp_float * 255), 0),
            commons.DEFAULT_FONT,
            outline_color=pygame.Color(int((1 - hp_float) * 180), int(hp_float * 180), 0),
        )
        self.hp_x_position = commons.WINDOW_WIDTH - 10 - hp_float * 100 - self.hp_text.get_width() * 0.5

    """=================================================================================================================
        player.Player.kill -> void

        Kills the player, adds a death message, spawns particles, and plays a sound
    -----------------------------------------------------------------------------------------------------------------"""

    def kill(self, source, source_velocity=None):
        if self.alive:
            self.alive = False
            self.respawn_time_remaining = self.respawn_time
            self.death_message_alpha = 1
            self.velocity = (0, 0)

            entity_manager.add_message(get_death_message(self.name, source), pygame.Color(255, 0, 0))

            if commons.PARTICLES:
                if source_velocity is not None:
                    self.velocity = (
                        self.velocity[0] + source_velocity[0],
                        self.velocity[1] + source_velocity[1],
                    )

                velocity_angle = math.atan2(self.velocity[1], self.velocity[0])
                velocity_magnitude = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

                for i in range(int(35 * commons.PARTICLE_DENSITY)):  # more blood
                    entity_manager.spawn_particle(
                        (
                            self.position[0] + random.random() * commons.PLAYER_WIDTH - commons.PLAYER_WIDTH * 0.5,
                            self.position[1] + random.random() * commons.PLAYER_HEIGHT - commons.PLAYER_HEIGHT * 0.5,
                        ),
                        pygame.Color(230, 0, 0),
                        life=1,
                        angle=velocity_angle,
                        size=10,
                        spread=0.9,
                        magnitude=random.random() * velocity_magnitude * 0.8,
                        gravity=0.15,
                        outline=True,
                    )
            game_data.play_sound("sound.player_death")  # death sound

    """=================================================================================================================
        player.Player.respawn -> void

        Sets the player's position to the world's spawn point and resets some variables
    -----------------------------------------------------------------------------------------------------------------"""

    def respawn(self):
        self.position = world.world.spawn_position  # set position to world.world.spawn_point
        self.velocity = (0, 0)
        self.alive = True
        self.hp = int(self.max_hp)  # reset hp
        self.hp_text = shared_methods.outline_text(
            str(self.hp), pygame.Color(0, 255, 0), commons.DEFAULT_FONT, outline_color=pygame.Color(0, 180, 0)
        )
        self.hp_x_position = commons.WINDOW_WIDTH - 10 - 100 - self.hp_text.get_width() * 0.5
        self.invincible = True  # When you spawn, you are invincible for 3 seconds.
        self.invincible_timer = 3.0

    """=================================================================================================================
        player.Player.render_current_item_image    -> void

        Renders the item that the player is currently holding to the current_item_image surface
    -----------------------------------------------------------------------------------------------------------------"""

    def render_current_item_image(self):
        if not commons.is_holding_item:
            current_item = self.items[ItemLocation.HOTBAR][self.hotbar_index]
        else:
            current_item = item.item_holding
        if current_item is not None:
            self.current_item_image = current_item.get_image()

            # Item swing surface
            swing_surface = self.current_item_image
            if current_item.has_tag(ItemTag.WEAPON):
                world_override_image = current_item.get_world_override_image()
                if world_override_image is not None:
                    swing_surface = world_override_image

            item_scale = current_item.get_scale()
            inner_dimensions = (
                int(swing_surface.get_width() * item_scale),
                int(swing_surface.get_height() * item_scale),
            )
            scaled_surface = pygame.transform.scale(swing_surface, inner_dimensions)
            padded_dimensions = (
                int(inner_dimensions[0] * 1.414),
                int(inner_dimensions[1] * 1.414),
            )
            padded_surface = pygame.Surface(padded_dimensions, pygame.SRCALPHA)
            padded_surface.blit(
                scaled_surface,
                (
                    int(padded_dimensions[0] * 0.5 - inner_dimensions[0] * 0.5),
                    int(padded_dimensions[1] * 0.5 - inner_dimensions[1] * 0.5),
                ),
            )
            self.current_item_swing_image = padded_surface
            self.current_item_swing_offset = (
                math.sqrt((inner_dimensions[0] * 0.5) ** 2 + (inner_dimensions[1] * 0.5) ** 2) * 0.8
            )
            self.current_item_extend_image = padded_surface
            self.current_item_extend_offset = (
                math.sqrt((inner_dimensions[0] * 0.5) ** 2 + (inner_dimensions[1] * 0.5) ** 2) * 0.8
            )

    """=================================================================================================================
        player.Player.animate -> void

        Updates the player
    -----------------------------------------------------------------------------------------------------------------"""

    def animate(self):
        self.sprites.swinging = self.swinging_arm
        if self.holding_arm:
            self.sprites.hold()
        elif self.grounded:
            if self.sprites.get_movement() == Movement.LEFT or self.sprites.get_movement() == Movement.RIGHT:
                self.sprites.walk()
            else:
                self.sprites.idle()
        else:
            self.sprites.jump()

    """=================================================================================================================
        player.Player.use_item -> void

        Gets the item that the player is holding and calls the correct use function
    -----------------------------------------------------------------------------------------------------------------"""

    def use_item(self, right_click=False):
        current_item: Item | None = None

        if commons.is_holding_item:
            current_item = item.item_holding
        elif not self.inventory_open:
            current_item = self.items[ItemLocation.HOTBAR][self.hotbar_index]

        if current_item is None and not right_click:
            return

        screen_position_x = self.position[0] - entity_manager.camera_position[0] + commons.WINDOW_WIDTH * 0.5
        screen_position_y = self.position[1] - entity_manager.camera_position[1] + commons.WINDOW_HEIGHT * 0.5

        if not right_click:
            self.should_swing_arm = False
            self.should_hold_arm = False

            assert item is not None

            if current_item.has_tag(ItemTag.TILE):
                self.place_block(screen_position_x, screen_position_y, current_item, True)

            if current_item.has_tag(ItemTag.WALL):
                self.place_block(screen_position_x, screen_position_y, current_item, False)

            elif (
                current_item.has_tag(ItemTag.PICKAXE)
                or current_item.has_tag(ItemTag.HAMMER)
                or current_item.has_tag(ItemTag.AXE)
            ):
                self.use_tool(screen_position_x, screen_position_y, current_item)

            elif current_item.has_tag(ItemTag.LONGSWORD):
                self.use_longsword_weapon(current_item)

            elif current_item.has_tag(ItemTag.SHORTSWORD):
                self.use_shortsword_weapon(current_item)

            elif current_item.has_tag(ItemTag.RANGED):
                self.use_ranged_weapon(screen_position_x, screen_position_y, current_item)

            if self.should_swing_arm:
                if not self.swinging_arm:
                    self.swinging_arm = True

            if self.should_hold_arm:
                if not self.holding_arm:
                    self.holding_arm = True

        else:
            if (
                math.sqrt(
                    (screen_position_x - commons.MOUSE_POSITION[0]) ** 2
                    + (screen_position_y - commons.MOUSE_POSITION[1]) ** 2
                )
                < commons.BLOCK_SIZE * commons.PLAYER_REACH
                or commons.CREATIVE
            ):
                block_position = commons.HOVERED_TILE
                tile_dat = world.world.tile_data[block_position[0]][block_position[1]]
                json_tile_data = game_data.get_tile_by_id(tile_dat[0])
                if (
                    commons.TileTag.CHEST in json_tile_data.tags
                    or commons.TileTag.CYCLABLE in json_tile_data.tags
                ):
                    if commons.TileTag.MULTI_TILE in json_tile_data.tags:
                        origin = (
                            block_position[0] - tile_dat[2][0],
                            block_position[1] - tile_dat[2][1],
                        )
                    else:
                        origin = block_position
                    world.use_special_tile(origin[0], origin[1])

                if commons.TileTag.WORKBENCH in json_tile_data.tags:
                    if commons.TileTag.MULTI_TILE in json_tile_data.tags:
                        origin = (
                            block_position[0] - tile_dat[2][0],
                            block_position[1] - tile_dat[2][1],
                        )
                    else:
                        origin = block_position
                    world.use_special_tile(origin[0], origin[1])

    """=================================================================================================================
        player.Player.place_block -> void

        Uses a screen position and a block item    to place a block in the    world
    -----------------------------------------------------------------------------------------------------------------"""

    def place_block(self, screen_position_x, screen_position_y, block_item, is_tile):
        if (
            math.sqrt(
                (screen_position_x - commons.MOUSE_POSITION[0]) ** 2
                + (screen_position_y - commons.MOUSE_POSITION[1]) ** 2
            )
            < commons.BLOCK_SIZE * commons.PLAYER_REACH
            or commons.CREATIVE
        ):
            block_position = commons.HOVERED_TILE
            if world.tile_in_map(block_position[0], block_position[1]):
                block_rect = Rect(
                    commons.BLOCK_SIZE * block_position[0],
                    commons.BLOCK_SIZE * block_position[1] + 1,
                    commons.BLOCK_SIZE,
                    commons.BLOCK_SIZE,
                )
                if not block_rect.colliderect(self.rect):
                    block_placed = False
                    if is_tile:
                        tile_to_place = game_data.get_tile_by_id_str(block_item.get_tile_id_str())

                        if commons.TileTag.MULTI_TILE in tile_to_place.tags:
                            can_place = True

                            tile_dimensions = tile_to_place.multitile_dimensions

                            for x in range(tile_dimensions[0]):
                                for y in range(tile_dimensions[1]):
                                    if (
                                        not world.world.tile_data[block_position[0] + x][block_position[1] + y][0]
                                        == game_data.air_tile_id
                                    ):
                                        can_place = False

                            required_solids = tile_to_place.multitile_required_solids

                            for i in range(len(required_solids)):
                                tile_id = world.world.tile_data[block_position[0] + required_solids[i][0]][
                                    block_position[1] + required_solids[i][1]
                                ][0]
                                tile_data = game_data.get_tile_by_id(tile_id)
                                if commons.TileTag.NO_COLLIDE in tile_data.tags:
                                    can_place = False

                            if can_place:
                                world.place_multitile(
                                    block_position[0],
                                    block_position[1],
                                    tile_dimensions,
                                    tile_to_place.id,
                                    True,
                                )

                                if commons.TileTag.CHEST in tile_to_place.tags:
                                    world.world.chest_data.append([block_position, [None for _ in range(20)]])

                                block_placed = True

                                game_data.play_tile_place_sfx(tile_to_place.id)

                        else:
                            if world.world.tile_data[block_position[0]][block_position[1]][0] == game_data.air_tile_id:
                                if world.get_neighbor_count(block_position[0], block_position[1]) > 0:
                                    world.world.tile_data[block_position[0]][block_position[1]][0] = tile_to_place.id

                                    if world.tile_in_map(block_position[0], block_position[1] + 1):
                                        if (
                                            game_data.get_tile_by_id(
                                                world.world.tile_data[block_position[0]][block_position[1]][0]
                                            ).id_str
                                            == "tile.grass"
                                        ):
                                            world.world.tile_data[block_position[0]][block_position[1]][0] = (
                                                game_data.get_tile_id_by_id_str("tile.dirt")
                                            )

                                    world.update_terrain_surface(block_position[0], block_position[1])

                                    game_data.play_tile_place_sfx(tile_to_place.id)
                                    block_placed = True
                    else:
                        if world.world.tile_data[block_position[0]][block_position[1]][1] == game_data.air_wall_id:
                            if world.get_neighbor_count(block_position[0], block_position[1], tile=1) > 0:
                                wall_to_place = game_data.get_wall_by_id_str(block_item.get_wall_id_str())

                                world.world.tile_data[block_position[0]][block_position[1]][1] = int(
                                    wall_to_place.id
                                )
                                world.update_terrain_surface(block_position[0], block_position[1])

                                game_data.play_wall_place_sfx(wall_to_place.id)

                                block_placed = True

                    if block_placed:
                        self.should_swing_arm = True
                        self.should_hold_arm = True
                        self.item_swing = True
                        self.use_delay = 0.2
                        self.use_tick = 0
                        self.use_delta = 0.0
                        self.can_use = False
                        if not commons.CREATIVE:
                            if not commons.is_holding_item:
                                self.items[ItemLocation.HOTBAR][self.hotbar_index].amount -= 1
                                dat = [ItemLocation.HOTBAR, self.hotbar_index]
                                if dat not in self.old_inventory_positions:
                                    self.old_inventory_positions.append(dat)
                                if self.items[ItemLocation.HOTBAR][self.hotbar_index].amount <= 0:
                                    self.items[ItemLocation.HOTBAR][self.hotbar_index] = None
                            else:
                                commons.WAIT_TO_USE = True
                                assert item.item_holding is not None
                                item.item_holding.amount -= 1
                                if item.item_holding.amount <= 0:
                                    item.item_holding = None
                                    commons.is_holding_item = False

    """=================================================================================================================
        player.Player.use_pickaxe -> void

        Uses a screen position and a pickaxe item to mine a    block in the world
    -----------------------------------------------------------------------------------------------------------------"""

    def use_tool(self, screen_position_x, screen_position_y, tool_item):
        if self.can_use or commons.CREATIVE:
            self.enemies_hit = []
            self.can_use = False
            self.use_tick = 0
            self.use_delta = 0.0
            self.use_delay = tool_item.get_attack_speed() * 0.01
            self.should_swing_arm = True
            self.item_swing = True

            game_data.play_sound("sound.swing")

            if (
                math.sqrt(
                    (screen_position_x - commons.MOUSE_POSITION[0]) ** 2
                    + (screen_position_y - commons.MOUSE_POSITION[1]) ** 2
                )
                < commons.BLOCK_SIZE * commons.PLAYER_REACH
                or commons.CREATIVE
            ):
                block_position = commons.HOVERED_TILE
                if world.tile_in_map(block_position[0], block_position[1]):
                    if tool_item.has_tag(ItemTag.PICKAXE):
                        tile_id = world.world.tile_data[block_position[0]][block_position[1]][0]
                        tile_dat = game_data.get_tile_by_id(tile_id)
                        if commons.TileTag.MULTI_TILE in tile_dat.tags:
                            multitile_origin = world.get_multitile_origin(block_position[0], block_position[1])
                            world.remove_multitile(multitile_origin, True)
                            game_data.play_tile_hit_sfx(tile_id)
                        else:
                            if tile_id != game_data.air_tile_id:
                                item_id = game_data.get_item_id_by_id_str(tile_dat.item_id_str)
                                # Remove Grass from    dirt
                                if tile_id == game_data.grass_tile_id:
                                    world.world.tile_data[block_position[0]][block_position[1]][0] = (
                                        game_data.get_tile_id_by_id_str("tile.dirt")
                                    )
                                else:
                                    world.world.tile_data[block_position[0]][block_position[1]][
                                        0
                                    ] = game_data.air_tile_id

                                    entity_manager.spawn_physics_item(
                                        Item(item_id),
                                        (
                                            (block_position[0] + 0.5) * commons.BLOCK_SIZE,
                                            (block_position[1] + 0.5) * commons.BLOCK_SIZE,
                                        ),
                                        pickup_delay=10,
                                    )
                                world.update_terrain_surface(block_position[0], block_position[1])
                                game_data.play_tile_hit_sfx(tile_id)
                                if commons.PARTICLES:
                                    for i in range(int(random.randint(2, 3) * commons.PARTICLE_DENSITY)):
                                        entity_manager.spawn_particle(
                                            (
                                                block_position[0] * commons.BLOCK_SIZE + commons.BLOCK_SIZE * 0.5,
                                                block_position[1] * commons.BLOCK_SIZE + commons.BLOCK_SIZE * 0.5,
                                            ),
                                            pygame.transform.average_color(tile_dat["image"]),
                                            size=13,
                                            life=1,
                                            angle=-math.pi * 0.5,
                                            spread=math.pi,
                                            gravity=0.05,
                                        )

                    elif tool_item.has_tag(ItemTag.HAMMER):
                        wall_id = world.world.tile_data[block_position[0]][block_position[1]][1]
                        if wall_id != game_data.air_wall_id:
                            if (
                                world.get_neighbor_count(
                                    block_position[0],
                                    block_position[1],
                                    tile=1,
                                    check_centre_tile=False,
                                    check_centre_wall=False,
                                )
                                < 4
                            ):
                                wall_dat = game_data.get_wall_by_id(wall_id)

                                item_id = game_data.get_item_id_by_id_str(wall_dat.item_id_str)
                                entity_manager.spawn_physics_item(
                                    Item(item_id),
                                    (
                                        (block_position[0] + 0.5) * commons.BLOCK_SIZE,
                                        (block_position[1] + 0.5) * commons.BLOCK_SIZE,
                                    ),
                                    pickup_delay=10,
                                )

                                world.world.tile_data[block_position[0]][block_position[1]][1] = game_data.air_wall_id

                                world.update_terrain_surface(block_position[0], block_position[1])

                                game_data.play_wall_hit_sfx(wall_id)

    """=================================================================================================================
        player.Player.use_longsword_weapon -> void

        Swings the given longsword weapon item
    -----------------------------------------------------------------------------------------------------------------"""

    def use_longsword_weapon(self, longsword_weapon_item) -> None:
        if self.can_use:
            self.enemies_hit = []
            self.can_use = False
            self.use_tick = 0
            self.use_delta = 0.0
            self.use_delay = longsword_weapon_item.get_attack_speed() * 0.01

            game_data.play_sound("sound.swing")

            self.should_swing_arm = True
            self.item_swing = True

    def use_shortsword_weapon(self, shortsword_weapon_item) -> None:
        if self.can_use:
            self.enemies_hit = []
            self.can_use = False
            self.use_tick = 0
            self.use_delta = 0.0
            self.use_delay = shortsword_weapon_item.get_attack_speed() * 0.01

            game_data.play_sound("sound.swing")

            self.should_hold_arm = True
            self.item_extend = True

    """=================================================================================================================
        player.Player.use_ranged_weapon    -> void

        Shoots the given ranged    weapon item
    -----------------------------------------------------------------------------------------------------------------"""

    def use_ranged_weapon(self, screen_position_x, screen_position_y, ranged_weapon_item) -> None:
        if self.can_use:
            ammo_to_use_id = -1
            ammo_to_use_dat = None
            for item_id in ranged_weapon_item.json_item["ranged_ammo_type"]:
                item_ammo_slots = self.find_existing_item_stacks(game_data.get_item_id_by_id_str(item_id))
                if len(item_ammo_slots) > 0:
                    ammo_to_use_dat = item_ammo_slots[0]
                    ammo_to_use_id = game_data.get_item_id_by_id_str(item_id)
                    break

            if ammo_to_use_id != -1:
                assert ammo_to_use_dat is not None

                self.remove_item((ammo_to_use_dat[0], ammo_to_use_dat[1]), remove_count=1)

                game_data.play_sound(ranged_weapon_item.json_item["use_sound"])

                if commons.MOUSE_POSITION[0] < screen_position_x:
                    self.direction = 0
                else:
                    self.direction = 1

                self.can_use = False

                self.arm_out = True
                self.arm_out_angle = math.atan2(
                    screen_position_y - commons.MOUSE_POSITION[1],
                    abs(screen_position_x - commons.MOUSE_POSITION[0]),
                )

                self.use_tick = 0
                self.use_delay = ranged_weapon_item.get_attack_speed() * 0.01

                angle = math.atan2(
                    commons.MOUSE_POSITION[1] - screen_position_y,
                    commons.MOUSE_POSITION[0] - screen_position_x,
                )

                source = self.name

                entity_manager.spawn_projectile(self.position, angle, ranged_weapon_item, ammo_to_use_id, source)

    """=================================================================================================================
        player.Player.give_item    -> varying return info

        Gives the player one or several    potentially    prefixed items.

        Performs an optional search    on the player's    available item spaces to merge the item    with pre-existing stacks or
        just place it in an empty slot
    -----------------------------------------------------------------------------------------------------------------"""

    def give_item(self, current_item, amount=1, position=None):
        # No position specified
        if position is None:
            is_coin = current_item.has_tag(ItemTag.COIN)
            # Find all suitable    slots
            existing_slots = self.find_existing_item_stacks(current_item.item_id)
            # Slots that already have the item
            while len(existing_slots) > 0 and amount > 0:
                # Work out how many to add to the stack
                fill_count = existing_slots[0][2]
                amount -= fill_count
                if amount < 0:
                    fill_count += amount

                # Increase the amount of the chosen slot
                self.items[existing_slots[0][0]][existing_slots[0][1]].amount += fill_count

                # Automatically craft new coins
                if is_coin:
                    if (
                        self.items[existing_slots[0][0]][existing_slots[0][1]].amount
                        == self.items[existing_slots[0][0]][existing_slots[0][1]].get_max_stack()
                    ):
                        if amount > 0:
                            self.items[existing_slots[0][0]][existing_slots[0][1]].amount = amount
                        else:
                            self.items[existing_slots[0][0]][existing_slots[0][1]] = None
                        self.give_item(Item(current_item.item_id + 1))
                        amount = 0

                # Flag the position for a surface update
                dat = [existing_slots[0][0], existing_slots[0][1]]
                if dat not in self.old_inventory_positions:
                    self.old_inventory_positions.append(dat)
                # Remove the used data
                existing_slots.pop(0)

            # Free slots
            free_slots = self.find_free_spaces(current_item.json_item.max_stack)

            while len(free_slots) > 0 and amount > 0:  # No stacks left to fill so fill empty slots
                # Work out how many to add to the stack
                fill_count = free_slots[0][2]
                amount -= fill_count
                if amount < 0:
                    fill_count += amount

                # Add that number to the free slot
                self.items[free_slots[0][0]][free_slots[0][1]] = current_item.copy(new_amount=fill_count)

                # Flag the position for a surface update
                dat = [free_slots[0][0], free_slots[0][1]]
                if dat not in self.old_inventory_positions:
                    self.old_inventory_positions.append(dat)
                # Remove the used data
                free_slots.remove(free_slots[0])

            if amount <= 0:
                return [ItemSlotClickResult.GAVE_ALL]
            else:
                if current_item.item_id not in self.un_pickupable_items:
                    self.un_pickupable_items.append(current_item.item_id)
                return [ItemSlotClickResult.GAVE_SOME, amount]

        # Position specified
        else:
            # Slot is free, add
            if self.items[position[0]][position[1]] is None:
                self.items[position[0]][position[1]] = current_item.copy(new_amount=amount)
                return [ItemSlotClickResult.GAVE_ALL]

            # Slot has an item with the same ID
            if self.items[position[0]][position[1]].item_id == current_item.item_id:
                max_stack = self.items[position[0]][position[1]].get_max_stack()
                # Item is already at max stack, swap
                if self.items[position[0]][position[1]].amount == max_stack:
                    return [
                        ItemSlotClickResult.SWAPPED,
                        self.items[position[0]][position[1]],
                        position[0],
                    ]

                else:
                    self.items[position[0]][position[1]].amount += amount
                    # Entire stack cannot be given
                    if self.items[position[0]][position[1]].amount > max_stack:
                        amount = self.items[position[0]][position[1]].amount - max_stack
                        self.items[position[0]][position[1]].amount = max_stack
                        return [ItemSlotClickResult.GAVE_SOME, amount]

                    # Entire stack was given
                    else:
                        return [ItemSlotClickResult.GAVE_ALL]

            # Slot has an item with a different ID, swap
            elif self.items[position[0]][position[1]].item_id != current_item.item_id:
                return [
                    ItemSlotClickResult.SWAPPED,
                    self.items[position[0]][position[1]],
                    position[0],
                ]
            return None

    """=================================================================================================================
        player.Player.remove_item -> item

        Removes all the items from a slot in one of the player's available item slots
    -----------------------------------------------------------------------------------------------------------------"""

    def remove_item(self, position, remove_count=None):
        current_item = self.items[position[0]][position[1]]
        if current_item is not None:
            if remove_count is None:
                self.items[position[0]][position[1]] = None
            else:
                self.items[position[0]][position[1]].amount -= remove_count
                if self.items[position[0]][position[1]].amount <= 0:
                    self.items[position[0]][position[1]] = None

            if position not in self.old_inventory_positions:
                self.old_inventory_positions.append(position)

            if remove_count is None:
                return current_item.copy()
            else:
                return current_item.copy(new_amount=remove_count)
        return None

    """=================================================================================================================
        player.Player.find_existing_item_stacks -> existing space list

        Finds any occurrences of an item in the player's inventory or hotbar
    -----------------------------------------------------------------------------------------------------------------"""

    def find_existing_item_stacks(self, item_id, search_hotbar=True, search_inventory=True):
        # [which array,    position in array, amount]
        existing_spaces = []
        item_data = game_data.get_item_by_id(item_id)

        if search_hotbar:
            for hotbar_index in range(len(self.items[ItemLocation.HOTBAR])):
                current_item = self.items[ItemLocation.HOTBAR][hotbar_index]
                if current_item is not None:
                    if current_item.item_id == item_id:
                        available = item_data.max_stack - self.items[ItemLocation.HOTBAR][hotbar_index].amount
                        existing_spaces.append([ItemLocation.HOTBAR, hotbar_index, available])

        if search_inventory:
            for inventory_index in range(len(self.items[ItemLocation.INVENTORY])):
                current_item = self.items[ItemLocation.INVENTORY][inventory_index]
                if current_item is not None:
                    if current_item.item_id == item_id:
                        available = item_data.max_stack - self.items[ItemLocation.INVENTORY][inventory_index].amount
                        if available > 0:
                            existing_spaces.append([ItemLocation.INVENTORY, inventory_index, available])

        return existing_spaces

    """=================================================================================================================
        player.Player.find_free_spaces -> free space list

        Finds any free spaces in the player's inventory    or hotbar
    -----------------------------------------------------------------------------------------------------------------"""

    def find_free_spaces(self, max_stack=9999, search_hotbar=True, search_inventory=True):
        free_spaces = []

        if search_hotbar:
            for hotbar_index in range(len(self.items[ItemLocation.HOTBAR])):
                if self.items[ItemLocation.HOTBAR][hotbar_index] is None:
                    free_spaces.append([ItemLocation.HOTBAR, hotbar_index, max_stack])

        if search_inventory:
            for inventory_index in range(len(self.items[ItemLocation.INVENTORY])):
                if self.items[ItemLocation.INVENTORY][inventory_index] is None:
                    free_spaces.append([ItemLocation.INVENTORY, inventory_index, max_stack])

        return free_spaces

    """=================================================================================================================
        player.Player.render_hotbar    -> void

        Fully renders the player's hotbar to the hotbar_image surface, including all the items in the hotbar
    -----------------------------------------------------------------------------------------------------------------"""

    def render_hotbar(self):
        self.hotbar_image.fill((255, 0, 255))
        for hotbar_index in range(len(self.items[ItemLocation.HOTBAR])):
            self.hotbar_image.blit(tilesets.misc_gui[0], (48 * hotbar_index, 0))
            current_item = self.items[ItemLocation.HOTBAR][hotbar_index]
            if current_item is not None:
                self.hotbar_image.blit(
                    current_item.get_resized_image(),
                    (
                        current_item.get_resized_offset_x() + 48 * hotbar_index,
                        current_item.get_resized_offset_y(),
                    ),
                )
                if current_item.amount > 1:
                    self.hotbar_image.blit(
                        shared_methods.outline_text(
                            str(current_item.amount), pygame.Color(255, 255, 255), commons.SMALL_FONT
                        ),
                        (24 + 48 * hotbar_index, 30),
                    )

    """=================================================================================================================
        player.Player.render_inventory -> void

        Fully renders the player's inventory to the    inventory_image    surface, including all the items in the    inventory
    -----------------------------------------------------------------------------------------------------------------"""

    def render_inventory(self):
        self.inventory_image.fill((255, 0, 255))
        pygame.draw.rect(self.inventory_image, (150, 150, 150), Rect(5, 5, 472, 184), 0)
        for inventory_index in range(len(self.items[ItemLocation.INVENTORY])):
            slot_x = inventory_index % 10
            slot_y = inventory_index // 10
            self.inventory_image.blit(tilesets.misc_gui[0], (48 * slot_x, 48 * slot_y))
            current_item = self.items[ItemLocation.INVENTORY][inventory_index]
            if current_item is not None:
                self.inventory_image.blit(
                    current_item.get_resized_image(),
                    (
                        current_item.get_resized_offset_x() + 48 * slot_x,
                        current_item.get_resized_offset_y() + 48 * slot_y,
                    ),
                )
                if self.items[ItemLocation.INVENTORY][inventory_index].amount > 1:
                    self.inventory_image.blit(
                        shared_methods.outline_text(
                            str(self.items[ItemLocation.INVENTORY][inventory_index].amount),
                            pygame.Color(255, 255, 255),
                            commons.SMALL_FONT,
                        ),
                        (24 + 48 * slot_x, 30 + 48 * slot_y),
                    )

    """=================================================================================================================
        player.Player.render_chest -> void

        Fully renders the chest the player has open to the chest_image surface, including all the items in the open chest
    -----------------------------------------------------------------------------------------------------------------"""

    def render_chest(self):
        self.chest_image.fill((255, 0, 255))
        pygame.draw.rect(self.chest_image, (150, 150, 150), Rect(5, 5, 232, 184), 0)
        for chest_index in range(len(self.items[ItemLocation.CHEST])):
            slot_x = chest_index % 5
            slot_y = chest_index // 5
            self.chest_image.blit(tilesets.misc_gui[0], (48 * slot_x, 48 * slot_y))
            current_item = self.items[ItemLocation.CHEST][chest_index]
            if current_item is not None:
                self.chest_image.blit(
                    current_item.get_resized_image(),
                    (
                        current_item.get_resized_offset_x() + 48 * slot_x,
                        current_item.get_resized_offset_y() + 48 * slot_y,
                    ),
                )
                if self.items[ItemLocation.CHEST][chest_index].amount > 1:
                    self.chest_image.blit(
                        shared_methods.outline_text(
                            str(self.items[ItemLocation.CHEST][chest_index].amount),
                            pygame.Color(255, 255, 255),
                            commons.SMALL_FONT,
                        ),
                        (24 + 48 * slot_x, 30 + 48 * slot_y),
                    )

    """=================================================================================================================
        player.Player.update_inventory_old_slots -> void

        Uses a list of outdated positions in the hotbar, inventory or an open chest to update the respective area's surfaces
    -----------------------------------------------------------------------------------------------------------------"""

    def update_inventory_old_slots(self):
        for data in self.old_inventory_positions:
            if data[0] == ItemLocation.HOTBAR:
                current_item = self.items[ItemLocation.HOTBAR][data[1]]
                self.hotbar_image.blit(tilesets.misc_gui[0], (data[1] * 48, 0))
                if current_item is not None:
                    self.hotbar_image.blit(
                        current_item.get_resized_image(),
                        (
                            current_item.get_resized_offset_x() + 48 * data[1],
                            current_item.get_resized_offset_y(),
                        ),
                    )
                    if current_item.amount > 1:
                        self.hotbar_image.blit(
                            shared_methods.outline_text(
                                str(current_item.amount), pygame.Color(255, 255, 255), commons.SMALL_FONT
                            ),
                            (24 + 48 * data[1], 30),
                        )
            elif data[0] == ItemLocation.INVENTORY:
                current_item = self.items[ItemLocation.INVENTORY][data[1]]
                slot_x = data[1] % 10
                slot_y = data[1] // 10
                self.inventory_image.blit(tilesets.misc_gui[0], (slot_x * 48, slot_y * 48))
                if current_item is not None:
                    self.inventory_image.blit(
                        current_item.get_resized_image(),
                        (
                            current_item.get_resized_offset_x() + slot_x * 48,
                            current_item.get_resized_offset_y() + slot_y * 48,
                        ),
                    )
                    if current_item.amount > 1:
                        self.inventory_image.blit(
                            shared_methods.outline_text(
                                str(current_item.amount), pygame.Color(255, 255, 255), commons.SMALL_FONT
                            ),
                            (24 + 48 * slot_x, 30 + 48 * slot_y),
                        )

            elif data[0] == ItemLocation.CHEST:
                current_item = self.items[ItemLocation.CHEST][data[1]]
                slot_x = data[1] % 5
                slot_y = data[1] // 5
                self.chest_image.blit(tilesets.misc_gui[0], (slot_x * 48, slot_y * 48))
                if current_item is not None:
                    self.chest_image.blit(
                        current_item.get_resized_image(),
                        (
                            current_item.get_resized_offset_x() + slot_x * 48,
                            current_item.get_resized_offset_y() + slot_y * 48,
                        ),
                    )
                    if current_item.amount > 1:
                        self.chest_image.blit(
                            shared_methods.outline_text(
                                str(current_item.amount), pygame.Color(255, 255, 255), commons.SMALL_FONT
                            ),
                            (24 + 48 * slot_x, 30 + 48 * slot_y),
                        )
        self.old_inventory_positions = []

    """=================================================================================================================
        player.Player.update_craftable_items -> void

        Creates a list of items that can be crafted with the current materials List structure [item_id, amount]
    -----------------------------------------------------------------------------------------------------------------"""

    def update_craftable_items(self):
        self.items[ItemLocation.CRAFTING_MENU] = [[i + 1, 1] for i in range(len(game_data.json_item_data) - 1)]

    """=================================================================================================================
        player.Player.render_craftable_items_surf -> void

        Uses the craftable_items list to create a surface that displays all the items the player can craft
    -----------------------------------------------------------------------------------------------------------------"""

    def render_craftable_items_surf(self):
        self.craftable_items_surf = pygame.Surface((48, len(self.items[ItemLocation.CRAFTING_MENU]) * 48))
        self.craftable_items_surf.fill((255, 0, 255))
        for i in range(len(self.items[ItemLocation.CRAFTING_MENU])):
            self.craftable_items_surf.blit(tilesets.misc_gui[0], (0, i * 48))
            item_data = game_data.json_item_data[self.items[ItemLocation.CRAFTING_MENU][i][0]]
            image = item_data.surface
            if max(image.get_width(), image.get_height()) > 32:
                image = pygame.transform.scale(
                    image,
                    (
                        image.get_width() * 32 / max(image.get_width(), image.get_height()),
                        image.get_height() * 32 / max(image.get_width(), image.get_height()),
                    ),
                )
            self.craftable_items_surf.blit(
                image,
                (
                    int(24 - image.get_width() * 0.5),
                    int(24 - image.get_height() * 0.5) + i * 48,
                ),
            )

    """=================================================================================================================
        player.Player.draw -> void

        Uses various player variables to draw the player in the world
    -----------------------------------------------------------------------------------------------------------------"""

    def draw(self):  # Draw player to screen
        if self.alive:
            screen_position_x = self.position[0] - entity_manager.camera_position[0] + commons.WINDOW_WIDTH * 0.5
            screen_position_y = self.position[1] - entity_manager.camera_position[1] + commons.WINDOW_HEIGHT * 0.5
            commons.screen.blit(
                self.sprites.create_sprite(),
                (
                    screen_position_x - self.sprites.SURFACE_WIDTH * 0.5,
                    screen_position_y - self.sprites.SURFACE_HEIGHT * 0.5,
                ),
            )

            if self.arm_out:
                if not commons.is_holding_item:
                    current_item = self.items[ItemLocation.HOTBAR][self.hotbar_index]
                else:
                    current_item = item.item_holding

                if current_item.get_world_override_image() is not None:
                    rotated_item_surf = shared_methods.rotate_surface(
                        current_item.get_world_override_image(),
                        self.arm_out_angle * 180 / math.pi,
                    )
                else:
                    rotated_item_surf = shared_methods.rotate_surface(
                        current_item.get_image(), self.arm_out_angle * 180 / math.pi
                    )
                if self.direction == 1:
                    offset_x = commons.PLAYER_WIDTH * 0.5
                else:
                    offset_x = 0
                    rotated_item_surf = pygame.transform.flip(rotated_item_surf, True, False)
                commons.screen.blit(
                    rotated_item_surf,
                    (
                        screen_position_x - rotated_item_surf.get_width() * 0.5 + offset_x,
                        screen_position_y - rotated_item_surf.get_height() * 0.5,
                    ),
                )

            elif self.item_swing:
                if not commons.is_holding_item:
                    current_item = self.items[ItemLocation.HOTBAR][self.hotbar_index]
                else:
                    current_item = item.item_holding

                if current_item is not None and current_item.has_tag(ItemTag.WEAPON):
                    assert self.current_item_swing_image is not None
                    if self.direction == 1:
                        hit_rect = Rect(
                            self.position[0],
                            self.position[1] - self.current_item_swing_image.get_height() * 0.5,
                            self.current_item_swing_image.get_width(),
                            self.current_item_swing_image.get_height(),
                        )
                    else:
                        hit_rect = Rect(
                            self.position[0] - self.current_item_swing_image.get_width(),
                            self.position[1] - self.current_item_swing_image.get_height() * 0.5,
                            self.current_item_swing_image.get_width(),
                            self.current_item_swing_image.get_height(),
                        )

                    if commons.HITBOXES:
                        hit_rect_screen_x = hit_rect.x - entity_manager.camera_position[0] + commons.WINDOW_WIDTH * 0.5
                        hit_rect_screen_y = hit_rect.y - entity_manager.camera_position[1] + commons.WINDOW_HEIGHT * 0.5
                        pygame.draw.rect(
                            commons.screen,
                            (255, 0, 0),
                            Rect(
                                hit_rect_screen_x,
                                hit_rect_screen_y,
                                hit_rect.w,
                                hit_rect.h,
                            ),
                            1,
                        )

                    # Probably should be in update
                    for enemy in entity_manager.enemies:
                        if enemy.rect.colliderect(hit_rect):
                            if enemy.game_id not in self.enemies_hit:
                                if self.direction == 0:
                                    direction = -1
                                else:
                                    direction = 1
                                damage = current_item.get_attack_damage()
                                crit = random.random() <= current_item.get_crit_chance()

                                to_enemy = shared_methods.normalize_vec_2(
                                    (
                                        enemy.position[0] - self.position[0],
                                        enemy.position[1] - self.position[1],
                                    )
                                )

                                enemy.damage(
                                    damage,
                                    ["longsword", "Player"],
                                    current_item.get_knockback(),
                                    direction=direction,
                                    crit=crit,
                                    source_velocity=(
                                        to_enemy[0] * 30,
                                        to_enemy[1] * 30,
                                    ),
                                )
                                self.enemies_hit.append(int(enemy.game_id))

                eased_use_delta = shared_methods.ease_out_zero_to_one(self.use_delta, 1)
                less_eased_delta = shared_methods.lerp_float(self.use_delta, eased_use_delta, 0.7)

                if self.direction == 1:
                    self.swing_angle = -less_eased_delta * 175 + 85
                else:
                    self.swing_angle = less_eased_delta * 175 + 5

                rotated_surface = shared_methods.rotate_surface(self.current_item_swing_image, self.swing_angle)

                if current_item is not None:
                    if current_item.has_tag(ItemTag.SHORTSWORD):
                        total_offset = (
                            commons.PLAYER_ARM_LENGTH + self.current_item_extend_offset * current_item.get_hold_offset()
                        )
                    else:
                        total_offset = (
                            commons.PLAYER_ARM_LENGTH + self.current_item_swing_offset * current_item.get_hold_offset()
                        )
                else:
                    total_offset = commons.PLAYER_ARM_LENGTH

                # Looking right
                if self.direction == 1:
                    hand_angle_global_degrees = shared_methods.lerp_float(-130, 45, less_eased_delta)
                    hand_angle_global_radians = hand_angle_global_degrees * (math.pi / 180)
                    offset_x = (
                        math.cos(hand_angle_global_radians) * total_offset - rotated_surface.get_width() * 0.5 - 5
                    )
                    offset_y = (
                        math.sin(hand_angle_global_radians) * total_offset - rotated_surface.get_height() * 0.5 + 2
                    )
                    self.sprites.arm_radians = hand_angle_global_radians
                # Looking left
                else:
                    hand_angle_global_degrees = shared_methods.lerp_float(130, -45, less_eased_delta)
                    hand_angle_global_radians = hand_angle_global_degrees * (math.pi / 180)
                    offset_x = (
                        -math.cos(hand_angle_global_radians) * total_offset - rotated_surface.get_width() * 0.5 + 5
                    )
                    offset_y = (
                        -math.sin(hand_angle_global_radians) * total_offset - rotated_surface.get_height() * 0.5 + 2
                    )
                    self.sprites.arm_radians = hand_angle_global_radians

                commons.screen.blit(
                    rotated_surface,
                    (screen_position_x + offset_x, screen_position_y + offset_y),
                )

            elif self.item_extend:
                if not commons.is_holding_item:
                    current_item = self.items[ItemLocation.HOTBAR][self.hotbar_index]
                else:
                    current_item = item.item_holding

                if current_item is not None and current_item.has_tag(ItemTag.WEAPON):
                    assert self.current_item_extend_image is not None
                    if self.direction == 1:
                        hit_rect = Rect(
                            self.position[0],
                            self.position[1] - self.current_item_extend_image.get_height() * 0.5,
                            self.current_item_extend_image.get_width(),
                            self.current_item_extend_image.get_height(),
                        )
                    else:
                        hit_rect = Rect(
                            self.position[0] - self.current_item_extend_image.get_width(),
                            self.position[1] - self.current_item_extend_image.get_height() * 0.5,
                            self.current_item_extend_image.get_width(),
                            self.current_item_extend_image.get_height(),
                        )

                    if commons.HITBOXES:
                        hit_rect_screen_x = hit_rect.x - entity_manager.camera_position[0] + commons.WINDOW_WIDTH * 0.5
                        hit_rect_screen_y = hit_rect.y - entity_manager.camera_position[1] + commons.WINDOW_HEIGHT * 0.5
                        pygame.draw.rect(
                            commons.screen,
                            (255, 0, 0),
                            Rect(
                                hit_rect_screen_x,
                                hit_rect_screen_y,
                                hit_rect.w,
                                hit_rect.h,
                            ),
                            1,
                        )

                    # Probably should be in update
                    for enemy in entity_manager.enemies:
                        if enemy.rect.colliderect(hit_rect):
                            if enemy.game_id not in self.enemies_hit:
                                if self.direction == 0:
                                    direction = -1
                                else:
                                    direction = 1
                                damage = current_item.get_attack_damage()
                                if random.random() <= current_item.get_crit_chance():
                                    crit = True
                                else:
                                    crit = False

                                to_enemy = shared_methods.normalize_vec_2(
                                    (
                                        enemy.position[0] - self.position[0],
                                        enemy.position[1] - self.position[1],
                                    )
                                )

                                enemy.damage(
                                    damage,
                                    ["shortsword", "Player"],
                                    current_item.get_knockback(),
                                    direction=direction,
                                    crit=crit,
                                    source_velocity=(
                                        to_enemy[0] * 30,
                                        to_enemy[1] * 30,
                                    ),
                                )
                                self.enemies_hit.append(int(enemy.game_id))

                eased_use_delta = shared_methods.ease_out_zero_to_one(self.use_delta, 1)
                less_eased_delta = shared_methods.lerp_float(self.use_delta, eased_use_delta, 0.7)

                if self.direction == 1:
                    self.swing_angle = -less_eased_delta * 175 + 85
                else:
                    self.swing_angle = less_eased_delta * 175 + 5

                rotated_surface = shared_methods.rotate_surface(self.current_item_swing_image, self.swing_angle)

                if current_item is not None:
                    if current_item.has_tag(ItemTag.SHORTSWORD):
                        total_offset = (
                            commons.PLAYER_ARM_LENGTH + self.current_item_extend_offset * current_item.get_hold_offset()
                        )
                    else:
                        total_offset = (
                            commons.PLAYER_ARM_LENGTH + self.current_item_swing_offset * current_item.get_hold_offset()
                        )
                else:
                    total_offset = commons.PLAYER_ARM_LENGTH

                # Looking right
                if self.direction == 1:
                    hand_angle_global_degrees = shared_methods.lerp_float(-130, 45, less_eased_delta)
                    hand_angle_global_radians = hand_angle_global_degrees * (math.pi / 180)
                    offset_x = (
                        math.cos(hand_angle_global_radians) * total_offset - rotated_surface.get_width() * 0.5 - 5
                    )
                    offset_y = (
                        math.sin(hand_angle_global_radians) * total_offset - rotated_surface.get_height() * 0.5 + 2
                    )
                # Looking left
                else:
                    hand_angle_global_degrees = shared_methods.lerp_float(130, -45, less_eased_delta)
                    hand_angle_global_radians = hand_angle_global_degrees * (math.pi / 180)
                    offset_x = (
                        -math.cos(hand_angle_global_radians) * total_offset - rotated_surface.get_width() * 0.5 + 5
                    )
                    offset_y = (
                        -math.sin(hand_angle_global_radians) * total_offset - rotated_surface.get_height() * 0.5 + 2
                    )

                commons.screen.blit(
                    rotated_surface,
                    (screen_position_x + offset_x, screen_position_y + offset_y),
                )

            if commons.HITBOXES:  # Show hitbox
                pygame.draw.rect(
                    commons.screen,
                    (255, 0, 0),
                    Rect(
                        screen_position_x - commons.PLAYER_WIDTH * 0.5,
                        screen_position_y - commons.PLAYER_HEIGHT * 0.5,
                        commons.PLAYER_WIDTH,
                        commons.PLAYER_HEIGHT,
                    ),
                    1,
                )

    """=================================================================================================================
        player.Player.draw_hp -> void

        Draws the player's health in the top right
    -----------------------------------------------------------------------------------------------------------------"""

    def draw_hp(self):
        if self.hp > 0:
            rect = Rect(commons.WINDOW_WIDTH - 10 - self.hp * 2, 25, self.hp * 2, 20)
            hp_float = self.hp / self.max_hp
            col: tuple[int, int, int] = (
                int((1 - hp_float) * 255),
                int(hp_float * 255),
                0,
            )
            pygame.draw.rect(commons.screen, col, rect, 0)
            pygame.draw.rect(commons.screen, (int(col[0] * 0.8), int(col[1] * 0.8), 0), rect, 3)
            commons.screen.blit(self.hp_text, (self.hp_x_position, 45))

    """=================================================================================================================
        player.Player.open_chest -> void

        Plays the chest opening sound, opens the inventory and updates the items that the player can craft
    -----------------------------------------------------------------------------------------------------------------"""

    def open_chest(self, items):
        if not self.chest_open:
            game_data.play_sound("sound.menu_open")
            self.chest_open = True
        self.inventory_open = True
        self.items[ItemLocation.CHEST] = items
        self.crafting_menu_offset_y = 120
        self.update_craftable_items()
        self.render_craftable_items_surf()
        self.render_chest()

    """=================================================================================================================
        player.Player.save -> void

        Packs the important player data    into an array and serialises it using the pickle module
    -----------------------------------------------------------------------------------------------------------------"""

    def save(self):
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

    """=================================================================================================================
        player.Player.jump -> void

        Plays a sound, spawns particles and sets the player's y velocity
    -----------------------------------------------------------------------------------------------------------------"""

    def jump(self):
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
