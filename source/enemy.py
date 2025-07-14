import math
from random import randint, random

import commons
import entity_manager
import game_data
import item
import pygame
import shared_methods
import tilesets
import world
from data.tile import DamagingTileData, DoorTileData, LootMultitileData, LootTileData, MultitileData, TileData
from pygame.locals import Rect

from source.data.entity import ENTITY_DATA

"""=================================================================================================================
    enemy.Enemy

    Stores all information about an enemy instance
-----------------------------------------------------------------------------------------------------------------"""


class Enemy:
    def __init__(self, position, enemy_id) -> None:
        self.position: tuple[float, float] = position
        self.block_pos: tuple[int, int] = (0, 0)
        self.velocity: tuple[float, float] = (0, 0)
        self.enemy_id: int = enemy_id
        self.name: str = ENTITY_DATA[self.enemy_id].name
        self.type: str = ENTITY_DATA[self.enemy_id].species
        self.health: float = ENTITY_DATA[self.enemy_id].health
        self.max_health: float = self.health
        self.defense: int = ENTITY_DATA[self.enemy_id].defense
        self.knockback_resistance: float = ENTITY_DATA[self.enemy_id].knockback_resistance
        self.attack_damage: int = ENTITY_DATA[self.enemy_id].attack_damage
        self.color: pygame.Color = ENTITY_DATA[self.enemy_id].color
        self.rect: pygame.Rect = Rect(
            self.position[0] - commons.BLOCK_SIZE,
            self.position[1] - commons.BLOCK_SIZE / 1.5,
            commons.BLOCK_SIZE * 2,
            commons.BLOCK_SIZE * 1.5,
        )
        self.grounded: bool = False
        self.stop_left: bool = False
        self.stop_right: bool = False
        self.moving_left: bool = False
        self.moving_right: bool = False
        self.damage_tick: float = 0
        self.jump_tick: float = 1
        self.despawn_tick: int = 5
        self.animation_frame: int = 0
        self.game_id: int = randint(1000, 9999)
        self.world_invincible_timer: float = 0
        self.world_invincible: bool = False
        self.alive: bool = True

    """=================================================================================================================
        enemy.Enemy.update -> void

        Updates the enemy instance, performing physics, AI and animation
    -----------------------------------------------------------------------------------------------------------------"""

    def update(self) -> None:
        assert isinstance(entity_manager.client_player, entity_manager.Player)
        if self.alive:
            if self.world_invincible:
                if self.world_invincible_timer <= 0:
                    self.world_invincible = False
                else:
                    self.world_invincible_timer -= commons.DELTA_TIME

            self.stop_left = False
            self.stop_right = False

            if self.despawn_tick <= 0:
                self.despawn_tick += 5
                if self.despawn_radius():
                    return
            else:
                self.despawn_tick -= commons.DELTA_TIME

            if self.moving_left:  # Moves enemy left
                if not self.stop_left:
                    self.velocity = (-12.5, self.velocity[1])
            if self.moving_right:  # Moves enemy right
                if not self.stop_right:
                    self.velocity = (12.5, self.velocity[1])
            if not self.grounded:
                self.velocity = (
                    self.velocity[0],
                    self.velocity[1] + commons.GRAVITY * commons.DELTA_TIME,
                )
            self.run_ai()

            drag_factor = 1 - commons.DELTA_TIME * 4

            self.velocity = (
                self.velocity[0] * drag_factor,
                self.velocity[1] * drag_factor,
            )
            self.position = (
                self.position[0] + self.velocity[0] * commons.DELTA_TIME * commons.BLOCK_SIZE,
                self.position[1] + self.velocity[1] * commons.DELTA_TIME * commons.BLOCK_SIZE,
            )
            self.rect.left = int(self.position[0] - self.rect.width * 0.5)  # updating rect
            self.rect.top = int(self.position[1] - self.rect.height * 0.5)
            self.block_pos = int(self.position[1] // commons.BLOCK_SIZE), int(self.position[0] // commons.BLOCK_SIZE)
            self.grounded = False

            if self.velocity[0] < 0:
                if self.position[0] < world.border_left:
                    self.position = (int(world.border_left), self.position[1])
            elif self.velocity[0] > 0:
                if self.position[0] > world.border_right:
                    self.position = (int(world.border_right), self.position[1])
            if self.velocity[1] > 0:
                if self.position[1] > world.border_down:
                    self.position = (self.position[0], int(world.border_down))
                    self.velocity = (self.velocity[0], 0)
                    self.grounded = True

            if self.damage_tick <= 0:
                if entity_manager.client_player.rect.colliderect(self.rect):
                    if entity_manager.client_player.position[0] < self.position[0]:
                        direction = -1
                    else:
                        direction = 1

                    entity_manager.client_player.damage(
                        self.attack_damage,
                        ("enemy", self.name),
                        knockback=10,
                        direction=direction,
                        source_velocity=self.velocity,
                    )  # (normalizedPositionDifference[0] * 10, normalizedPositionDifference[1] * 10)
                    self.damage_tick += 0.5
            else:
                self.damage_tick -= commons.DELTA_TIME

            for j in range(-2, 3):
                for i in range(-2, 3):
                    if world.tile_in_map(self.block_pos[1] + j, self.block_pos[0] + i):
                        tile_id: int = world.world.tile_data[self.block_pos[1] + j][self.block_pos[0] + i][0]
                        tile_data: (
                            TileData
                            | DamagingTileData
                            | MultitileData
                            | DoorTileData
                            | LootTileData
                            | LootMultitileData
                        ) = game_data.get_tile_by_id(tile_id)
                        if commons.TileTag.NO_COLLIDE not in tile_data["tags"]:
                            block_rect = Rect(
                                commons.BLOCK_SIZE * (self.block_pos[1] + j),
                                commons.BLOCK_SIZE * (self.block_pos[0] + i),
                                commons.BLOCK_SIZE,
                                commons.BLOCK_SIZE,
                            )
                            if commons.TileTag.PLATFORM in tile_data["tags"]:
                                platform = True
                            else:
                                platform = False
                            if block_rect.colliderect(
                                int(self.rect.left - 1),
                                int(self.rect.top + 2),
                                1,
                                int(self.rect.height - 4),
                            ):
                                self.stop_left = True  # Is there a solid block left
                            if block_rect.colliderect(
                                int(self.rect.right + 1),
                                int(self.rect.top + 2),
                                1,
                                int(self.rect.height - 4),
                            ):
                                self.stop_right = True  # Is there a solid block right
                            if block_rect.colliderect(self.rect):
                                if not self.world_invincible and commons.TileTag.DAMAGING in tile_data["tags"]:
                                    # self.damage(tile_data["tile_damage"], [tile_data["tile_damage_name"], "World"])
                                    pass

                                delta_x = self.position[0] - block_rect.centerx
                                delta_y = self.position[1] - block_rect.centery
                                if abs(delta_x) > abs(delta_y):
                                    if not platform:
                                        if delta_x > 0:
                                            self.position = (
                                                block_rect.right + self.rect.width * 0.5,
                                                self.position[1],
                                            )  # Move enemy right
                                            self.velocity = (
                                                0,
                                                self.velocity[1],
                                            )  # Stop enemy horizontally
                                        else:
                                            self.position = (
                                                block_rect.left - self.rect.width * 0.5,
                                                self.position[1],
                                            )  # Move enemy left
                                            self.velocity = (
                                                0,
                                                self.velocity[1],
                                            )  # Stop enemy horizontally
                                else:
                                    if delta_y > 0:
                                        if self.velocity[1] < 0:
                                            if not platform:
                                                if Rect(
                                                    self.rect.left + 3,
                                                    self.rect.top,
                                                    self.rect.width - 6,
                                                    self.rect.height,
                                                ).colliderect(block_rect):
                                                    self.position = (
                                                        self.position[0],
                                                        block_rect.bottom + self.rect.height * 0.5,
                                                    )  # Move enemy down
                                                    self.velocity = (
                                                        self.velocity[0],
                                                        0,
                                                    )  # Stop enemy vertically
                                    else:
                                        if self.velocity[1] > 0:
                                            if Rect(
                                                self.rect.left + 3,
                                                self.rect.top,
                                                self.rect.width - 6,
                                                self.rect.height,
                                            ).colliderect(block_rect):
                                                self.position = (
                                                    self.position[0],
                                                    block_rect.top - self.rect.height * 0.5 + 1,
                                                )  # Move enemy up
                                                self.velocity = (
                                                    self.velocity[0] * 0.5,
                                                    0,
                                                )  # Slow down enemy horizontally and stop player vertically
                                                self.grounded = True
                                                self.moving_right = False
                                                self.moving_left = False
            self.animate()

    """=================================================================================================================
        enemy.Enemy.damage -> void

        Damages the enemy instance spawning particles and playing a sound

        Will call 'kill' on the enemy if it's health drops below 0
    -----------------------------------------------------------------------------------------------------------------"""

    def damage(
        self,
        value: float,
        source: list[str],
        knockback: float = 0,
        direction: int = 0,
        crit: bool = False,
        source_velocity: tuple[float, float] = (0, 0),
    ):
        if self.alive:
            if source[1] == "World" and self.world_invincible:
                return
            else:
                self.world_invincible_timer = 0.35
                self.world_invincible = True

            self.moving_right = False
            self.moving_left = False

            value -= self.defense
            value *= 1 + random() * 0.1 - 0.05
            if value < 1:
                value = 1

            if crit:
                value *= 2.0

            self.health -= value

            if self.health < 0:
                self.health = 0

            entity_manager.add_damage_number(self.position, value, crit=crit)

            if self.health > 0:  # Check if the enemy has died from damage
                game_data.play_sound("sound.slime_hurt")
                if commons.PARTICLES:
                    if source_velocity != (0, 0):
                        velocity_angle = math.atan2(source_velocity[1], source_velocity[0])
                        velocity_magnitude = math.sqrt(source_velocity[0] ** 2 + source_velocity[1] ** 2)
                    else:
                        velocity_angle = math.atan2(self.velocity[1], self.velocity[0])
                        velocity_magnitude = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

                    for _ in range(int(5 * commons.PARTICLE_DENSITY)):  # Blood particles
                        particle_pos = (
                            self.position[0] + random() * self.rect.width - self.rect.width * 0.5,
                            self.position[1] + random() * self.rect.height - self.rect.height * 0.5,
                        )
                        entity_manager.spawn_particle(
                            particle_pos,
                            self.color,
                            life=0.5,
                            size=10,
                            angle=velocity_angle,
                            spread=math.pi * 0.2,
                            magnitude=random() * velocity_magnitude * 0.5,
                            outline=True,
                        )
            else:
                self.kill(source_velocity)

            if knockback != 0:
                remaining_knockback: float = max(0.0, knockback - self.knockback_resistance)
                self.velocity = (
                    self.velocity[0] + direction * remaining_knockback * 3.0,
                    remaining_knockback * -5.0,
                )

    """=================================================================================================================
        enemy.Enemy.kill -> void

        Sets the enemies alive variable to false, will be removed from the entity list by the manager

        Plays a sound and spawns particles and loot
    -----------------------------------------------------------------------------------------------------------------"""

    def kill(self, source_velocity: tuple[float, float] | None):
        if self.alive:
            self.alive = False

            coin_range: tuple[int, int] = ENTITY_DATA[self.enemy_id].coin_drop_range
            coin_drop_range: list[item.Item] = item.get_coins_from_int(randint(coin_range[0], coin_range[1]))
            item_drops = ENTITY_DATA[self.enemy_id].item_drops

            for coin_item in coin_drop_range:
                entity_manager.spawn_physics_item(coin_item, self.position, pickup_delay=10)
            for item_drop in item_drops:
                entity_manager.spawn_physics_item(
                    item.Item(
                        game_data.get_item_id_by_id_str(item_drop.name),
                        randint(item_drop.drop_range[0], item_drop.drop_range[1]),
                    ),
                    self.position,
                    pickup_delay=10,
                )

            if commons.PARTICLES:
                if source_velocity is not None:
                    self.velocity = (
                        self.velocity[0] + source_velocity[0],
                        self.velocity[1] + source_velocity[1],
                    )

                velocity_angle = math.atan2(self.velocity[1], self.velocity[0])
                velocity_magnitude = math.sqrt(self.velocity[0] ** 2 + self.velocity[1] ** 2)

                for _ in range(int(25 * commons.PARTICLE_DENSITY)):  # Blood particles
                    particle_pos = (
                        self.position[0] + random() * self.rect.width - self.rect.width * 0.5,
                        self.position[1] + random() * self.rect.height - self.rect.height * 0.5,
                    )
                    entity_manager.spawn_particle(
                        particle_pos,
                        self.color,
                        life=0.5,
                        size=10,
                        angle=velocity_angle,
                        spread=math.pi * 0.2,
                        magnitude=random() * velocity_magnitude * 0.4,
                        outline=True,
                    )

            game_data.play_sound("sound.slime_death")  # Death sound

            entity_manager.enemies.remove(self)

    """=================================================================================================================
        enemy.Enemy.animate -> void

        Updates the animation frame of the enemy instance
    -----------------------------------------------------------------------------------------------------------------"""

    def animate(self):
        if not self.grounded:
            if self.velocity[1] > 2:
                self.animation_frame = 2
            elif self.velocity[1] < -2:
                self.animation_frame = 1
            else:
                self.animation_frame = 0
        else:
            self.animation_frame = 0

    """=================================================================================================================
        enemy.Enemy.despawn_radius -> bool

        Checks if the enemy has gone too far beyond the player's view, if so, return true
    -----------------------------------------------------------------------------------------------------------------"""

    def despawn_radius(self):
        assert isinstance(entity_manager.client_player, entity_manager.Player)
        if (
            self.position[0]
            < entity_manager.client_player.position[0] - commons.MAX_ENEMY_SPAWN_TILES_X * 1.5 * commons.BLOCK_SIZE
        ):
            entity_manager.enemies.remove(self)
            return True
        elif (
            self.position[0]
            > entity_manager.client_player.position[0] + commons.MAX_ENEMY_SPAWN_TILES_X * 1.5 * commons.BLOCK_SIZE
        ):
            entity_manager.enemies.remove(self)
            return True
        elif (
            self.position[1]
            < entity_manager.client_player.position[1] - commons.MAX_ENEMY_SPAWN_TILES_Y * 1.5 * commons.BLOCK_SIZE
        ):
            entity_manager.enemies.remove(self)
            return True
        elif (
            self.position[1]
            > entity_manager.client_player.position[1] + commons.MAX_ENEMY_SPAWN_TILES_Y * 1.5 * commons.BLOCK_SIZE
        ):
            entity_manager.enemies.remove(self)
            return True
        return False

    """=================================================================================================================
        enemy.Enemy.draw -> void

        Draws the enemy instance at the current animation frame
    -----------------------------------------------------------------------------------------------------------------"""

    def draw(self):
        left = self.rect.left - entity_manager.camera_position[0] + commons.WINDOW_WIDTH * 0.5
        top = self.rect.top - entity_manager.camera_position[1] + commons.WINDOW_HEIGHT * 0.5
        commons.screen.blit(
            tilesets.slimes[(self.enemy_id - 1) * 3 + self.animation_frame],
            (left, top),
        )
        if self.health < self.max_health:
            health_float = self.health / self.max_health
            col: pygame.Color = pygame.Color(
                int(255 * (1 - health_float)),
                int(255 * health_float),
                0,
            )
            pygame.draw.rect(
                commons.screen,
                shared_methods.darken_color(col),
                Rect(left, top + 30, self.rect.width, 10),
                0,
            )
            pygame.draw.rect(
                commons.screen,
                col,
                Rect(left + 2, top + 32, (self.rect.width - 4) * health_float, 6),
                0,
            )
        shared_methods.draw_hitbox(
            entity_manager.camera_position[0],
            entity_manager.camera_position[1],
            self.rect.left,
            self.rect.top,
            self.rect.width,
            self.rect.height,
        )

    """=================================================================================================================
        enemy.Enemy.run_ai -> void

        Runs AI specific to this type of enemy
    -----------------------------------------------------------------------------------------------------------------"""

    def run_ai(self):
        assert isinstance(entity_manager.client_player, entity_manager.Player)
        if self.type == "Slime":
            if self.grounded:
                if self.jump_tick <= 0:
                    self.jump_tick += 0.5 + random()
                    if entity_manager.client_player.position[0] < self.position[0]:
                        if entity_manager.client_player.alive:
                            self.velocity = (-10, -45 + random())
                            self.moving_left = True
                        else:
                            self.velocity = (10, -45 + random())
                            self.moving_right = True
                    else:
                        if entity_manager.client_player.alive:
                            self.velocity = (10, -45 + random())
                            self.moving_right = True
                        else:
                            self.velocity = (-10, -45 + random())
                            self.moving_left = True
                else:
                    self.jump_tick -= commons.DELTA_TIME
