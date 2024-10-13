# entity_manager.py

import pygame
import math
import random
from pygame.locals import Rect
from typing import TypedDict

import commons
import game_data
import world

import shared_methods

from player import Player
from enemy import Enemy
from particle import Particle
from projectile import Projectile
from physics_item import PhysicsItem
from color_picker import ColorPicker
from item import Item

class Messages(TypedDict):
	text: pygame.Surface
	lifespan: float

enemies: list[Enemy] = []
particles: list[Particle] = []
projectiles: list[Projectile] = []
physics_items: list[PhysicsItem] = []
messages: list[Messages] = []
damage_numbers = []
recent_pickups = []

client_player = None
client_prompt = None
client_color_picker = ColorPicker((int(commons.WINDOW_WIDTH * 0.5 - 155),  190),  300,  300)

camera_position = (0, 0)
old_camera_position = (0, 0)
camera_position_difference = (0, 0)


"""================================================================================================================= 
	entity_manager.create_player -> void

	Sets the client player to a new player instance created with the data in PLAYER_DATA
-----------------------------------------------------------------------------------------------------------------"""


def create_player():
	global client_player
	name = commons.PLAYER_DATA["name"]
	model = commons.PLAYER_DATA["model"]

	# Load hotbar
	hotbar: list[Item | None] = [None for _ in range(10)]
	for loaded_hotbar_index in range(len(commons.PLAYER_DATA["hotbar"])):
		loaded_item_data = commons.PLAYER_DATA["hotbar"][loaded_hotbar_index]
		item = Item(game_data.get_item_id_by_id_str(loaded_item_data[1]), loaded_item_data[2])
		item.assign_prefix(loaded_item_data[3])
		hotbar[loaded_item_data[0]] = item

	# Load inventory
	inventory: list[Item | None] = [None for _ in range(40)]
	for loaded_inventory_index in range(len(commons.PLAYER_DATA["inventory"])):
		loaded_item_data = commons.PLAYER_DATA["inventory"][loaded_inventory_index]
		item = Item(game_data.get_item_id_by_id_str(loaded_item_data[1]), loaded_item_data[2])
		item.assign_prefix(loaded_item_data[3])
		inventory[loaded_item_data[0]] = item

	hp = commons.PLAYER_DATA["hp"]
	max_hp = commons.PLAYER_DATA["max_hp"]
	playtime = commons.PLAYER_DATA["playtime"]
	creation_date = commons.PLAYER_DATA["creation_date"]
	last_played_date = commons.PLAYER_DATA["last_played_date"]
	client_player = Player((0, 0), model, name=name, hotbar=hotbar, inventory=inventory, hp=hp, max_hp=max_hp, playtime=playtime, creation_date=creation_date, last_played_date=last_played_date)


"""================================================================================================================= 
	entity_manager.check_enemy_spawn -> void

	Checks if an enemy needs to spawn around the player
-----------------------------------------------------------------------------------------------------------------"""


def check_enemy_spawn():
	if not commons.PASSIVE:
		if commons.ENEMY_SPAWN_TICK <= 0:
			commons.ENEMY_SPAWN_TICK += 1.0
			assert client_player is not None
			val = int(14 - ((client_player.position[1] // commons.BLOCK_SIZE) // 30))
			if val < 1:
				val = 1
			if len(enemies) < commons.MAX_ENEMY_SPAWNS + (7 - val * 0.5) and random.randint(1, val) == 1:  # Reduce enemy spawns
				spawn_enemy()
		else:
			commons.ENEMY_SPAWN_TICK -= commons.DELTA_TIME


"""================================================================================================================= 
	entity_manager.draw_enemy_hover_text -> void

	Checks if an enemy is being hovered over by the mouse, if it is, draw it's name and it's health
-----------------------------------------------------------------------------------------------------------------"""


def draw_enemy_hover_text():
	transformed_MOUSE_POSITION = (commons.MOUSE_POSITION[0] + camera_position[0] - commons.WINDOW_WIDTH * 0.5,
							 commons.MOUSE_POSITION[1] + camera_position[1] - commons.WINDOW_HEIGHT * 0.5)
	for enemy in enemies:
		if enemy.rect.collidepoint(transformed_MOUSE_POSITION):
			text1 = commons.MEDIUM_FONT.render(enemy.name + ": " + str(math.ceil(enemy.health)) + "/" + str(enemy.max_health), True, (255, 255, 255))
			text2 = commons.MEDIUM_FONT.render(enemy.name + ": " + str(math.ceil(enemy.health)) + "/" + str(enemy.max_health), True, (0, 0, 0))

			commons.screen.blit(text2, (commons.MOUSE_POSITION[0] - text2.get_width() * 0.5, commons.MOUSE_POSITION[1] - 38))
			commons.screen.blit(text2, (commons.MOUSE_POSITION[0] - text2.get_width() * 0.5, commons.MOUSE_POSITION[1] - 42))
			commons.screen.blit(text2, (commons.MOUSE_POSITION[0] - text2.get_width() * 0.5 - 2, commons.MOUSE_POSITION[1] - 40))
			commons.screen.blit(text2, (commons.MOUSE_POSITION[0] - text2.get_width() * 0.5 + 2, commons.MOUSE_POSITION[1] - 40))

			commons.screen.blit(text1, (commons.MOUSE_POSITION[0] - text1.get_width() * 0.5, commons.MOUSE_POSITION[1] - 40))
			break


"""================================================================================================================= 
	entity_manager.kill_all_entities -> void

	Kills all entities, used before quitting a world
-----------------------------------------------------------------------------------------------------------------"""


def kill_all_entities():
	enemies.clear()
	particles.clear()
	projectiles.clear()
	physics_items.clear()
	messages.clear()
	damage_numbers.clear()
	recent_pickups.clear()


"""================================================================================================================= 
	Entity Update Functions

	Calls update on every entity in their respective list
-----------------------------------------------------------------------------------------------------------------"""


def update_enemies():
	for enemy in enemies:
		enemy.update()


def update_particles():
	for particle in particles:
		particle.update()


def update_physics_items():
	for physicsItem in physics_items:
		physicsItem.update()


def update_projectiles():
	for projectile in projectiles:
		projectile.update()


def update_messages():
	global messages
	for message in messages:
		message["lifespan"] -= commons.DELTA_TIME
		if message["lifespan"] <= 0:
			messages.remove(message)


def update_damage_numbers():
	for damageNumber in damage_numbers:
		damageNumber[1] = (damageNumber[1][0] * 0.95, damageNumber[1][1] * 0.95)
		damageNumber[0] = (damageNumber[0][0] + damageNumber[1][0] - camera_position_difference[0], damageNumber[0][1] + damageNumber[1][1] - camera_position_difference[1])
		damageNumber[3] -= commons.DELTA_TIME
		if damageNumber[3] <= 0:
			damage_numbers.remove(damageNumber)


def update_recent_pickups():
	global recent_pickups
	to_remove = []
	for i in range(len(recent_pickups)):
		recent_pickups[i][5] -= commons.DELTA_TIME
		if recent_pickups[i][5] < 0.5:
			recent_pickups[i][2].set_alpha(recent_pickups[i][5] * 510)
			if recent_pickups[i][5] <= 0:
				to_remove.append(recent_pickups[i])
		for j in range(0, i):
			if i != j:
				# Check if it is colliding with previous messages, if so, move up
				if Rect(recent_pickups[i][3][0], recent_pickups[i][3][1], recent_pickups[i][2].get_width(), recent_pickups[i][2].get_height()).colliderect(Rect(recent_pickups[j][3][0], recent_pickups[j][3][1], recent_pickups[j][2].get_width(), recent_pickups[j][2].get_height())):
					recent_pickups[i][4] = (recent_pickups[i][4][0], recent_pickups[i][4][1] - 1 * commons.DELTA_TIME)
					recent_pickups[i][3] = (recent_pickups[i][3][0], recent_pickups[i][3][1] - 50 * commons.DELTA_TIME)
		drag_factor = 1.0 - commons.DELTA_TIME * 10
		recent_pickups[i][4] = (recent_pickups[i][4][0] * drag_factor, recent_pickups[i][4][1] * drag_factor)
		recent_pickups[i][3] = (recent_pickups[i][3][0] + recent_pickups[i][4][0] * commons.DELTA_TIME * commons.BLOCK_SIZE, recent_pickups[i][3][1] + recent_pickups[i][4][1] * commons.DELTA_TIME * commons.BLOCK_SIZE)
	for item in to_remove:
		recent_pickups.remove(item)


"""================================================================================================================= 
	Entity Draw Functions

	Calls draw on every entity in their respective list
-----------------------------------------------------------------------------------------------------------------"""


def draw_enemies():
	for enemy in enemies:
		enemy.draw()


def draw_particles():
	for particle in particles:
		particle.draw()


def draw_physics_items():
	for physicsItem in physics_items:
		physicsItem.draw()


def draw_projectiles():
	for projectile in projectiles:
		projectile.draw()


def draw_messages():
	for i in range(len(messages)):
		if messages[i]["lifespan"] < 1.0:
			messages[i]["text"].set_alpha(int(messages[i]["lifespan"] * 255))
		commons.screen.blit(messages[i]["text"], (10, commons.WINDOW_HEIGHT - 25 - i * 20))


def draw_damage_numbers():
	for damage_number in damage_numbers:
		if damage_number[3] < 0.5:
			damage_number[2].set_alpha(damage_number[3] * 510)
		surf = damage_number[2].copy()
		# surf = pygame.transform.scale2x(surf)
		surf = shared_methods.rotate_surface(surf, -damage_number[1][0] * 35)
		commons.screen.blit(surf, (damage_number[0][0] - surf.get_width() * 0.5, damage_number[0][1] - surf.get_height() * 0.5))


def draw_recent_pickups():
	for recent_pickup in recent_pickups:
		commons.screen.blit(recent_pickup[2], (recent_pickup[3][0] - recent_pickup[2].get_width() * 0.5 - camera_position[0] + commons.WINDOW_WIDTH * 0.5, recent_pickup[3][1] - camera_position[1] + commons.WINDOW_HEIGHT * 0.5))


"""================================================================================================================= 
	Entity Spawn Functions

	Construct an instance of an entity and append it to their respective list
-----------------------------------------------------------------------------------------------------------------"""


def spawn_enemy(position=None, enemy_id=None):
	if client_player is None:
		return
	if enemy_id is None:
		if client_player.position[1] < 200 * commons.BLOCK_SIZE:
			enemy_id = random.randint(1, 2)
		elif client_player.position[1] < 300 * commons.BLOCK_SIZE:
			enemy_id = random.randint(2, 3)
		elif client_player.position[1] >= 300 * commons.BLOCK_SIZE:
			enemy_id = random.randint(4, 5)
	if position is None:
		player_block_pos = (int(camera_position[0]) // commons.BLOCK_SIZE, int(camera_position[1]) // commons.BLOCK_SIZE)
		for i in range(500):
			if random.random() < 0.5:
				x = random.randint(player_block_pos[0] - commons.MAX_ENEMY_SPAWN_TILES_X, player_block_pos[0] - commons.MIN_ENEMY_SPAWN_TILES_X)
				if random.random() < 0.5:
					y = random.randint(player_block_pos[1] - commons.MAX_ENEMY_SPAWN_TILES_Y, player_block_pos[1] - commons.MIN_ENEMY_SPAWN_TILES_Y)
				else:
					y = random.randint(player_block_pos[1] + commons.MIN_ENEMY_SPAWN_TILES_Y, player_block_pos[1] + commons.MAX_ENEMY_SPAWN_TILES_Y)
			else:
				x = random.randint(player_block_pos[0] + commons.MIN_ENEMY_SPAWN_TILES_X, player_block_pos[0] + commons.MAX_ENEMY_SPAWN_TILES_X)
				if random.random() < 0.5:
					y = random.randint(player_block_pos[1] - commons.MAX_ENEMY_SPAWN_TILES_Y, player_block_pos[1] - commons.MIN_ENEMY_SPAWN_TILES_Y)
				else:
					y = random.randint(player_block_pos[1] + commons.MIN_ENEMY_SPAWN_TILES_Y, player_block_pos[1] + commons.MAX_ENEMY_SPAWN_TILES_Y)
			if world.tile_in_map(x, y, width=2):
				if world.world.tile_data[x][y][0] == game_data.air_tile_id:
					if world.world.tile_data[x - 1][y][0] == game_data.air_tile_id:
						if world.world.tile_data[x][y - 1][0] == game_data.air_tile_id:
							if world.world.tile_data[x + 1][y][0] == game_data.air_tile_id:
								if world.world.tile_data[x][y + 1][0] == game_data.air_tile_id:
									enemies.append(Enemy((x * commons.BLOCK_SIZE, y * commons.BLOCK_SIZE), enemy_id))
									return
	else:
		enemies.append(Enemy(position, enemy_id))


def spawn_particle(position: tuple[float, float], color: tuple[int, int, int], life: float=2.0, magnitude: float=1.0, size: int=5, angle: float=0, spread: float=math.pi / 4, gravity: float=0.25, velocity: float=0, outline: bool=True):
	particles.append(Particle(position, color, life, magnitude, size, angle, spread, gravity, velocity, outline))


def spawn_physics_item(item: Item, position: tuple[float, float], velocity: tuple[float, float]=(0, 0), pickup_delay: int=100):
	physics_items.append(PhysicsItem(item, position, velocity, pickup_delay))


def spawn_projectile(position, angle, weapon_item, ammo_item_id, source):
	ammo_item_data = game_data.get_item_by_id(ammo_item_id)

	total_damage = weapon_item.get_attack_damage() + ammo_item_data["ammo_damage"]
	knockback = weapon_item.get_knockback() * ammo_item_data["ammo_knockback_modifier"]
	ammo_gravity_modifier = ammo_item_data["ammo_gravity_modifier"]
	ammo_drag = ammo_item_data["ammo_drag"]
	ricochet_amount = ammo_item_data["ricochet_amount"]
	image = ammo_item_data["ammo_image"]
	
	speed = weapon_item.get_ranged_projectile_speed()

	for _ in range(weapon_item.get_ranged_num_projectiles()):
		inaccuracy = 1.0 - weapon_item.get_ranged_accuracy()
		angle += random.random() * inaccuracy - inaccuracy * 0.5
		velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

		is_crit = False
		if random.random() <= weapon_item.get_crit_chance():
			is_crit = True

		# Hack until we have projectile data loaded from the tool
		projectiles.append(Projectile(position, velocity, 0, source, total_damage, knockback, is_crit, ricochet_amount, "arrow", image, gravity=ammo_gravity_modifier, drag=ammo_drag))


def add_message(text: str, color: tuple[int, int, int], life: float=5.0, outline_color: tuple[int, int, int]=(0, 0, 0)):
	global messages
	text1 = commons.DEFAULT_FONT.render(text, False, color)
	text2 = commons.DEFAULT_FONT.render(text, False, outline_color)
	surf = pygame.Surface((text1.get_width() + 2, text1.get_height() + 2), pygame.SRCALPHA)
	if commons.FANCY_TEXT:
		surf.blit(text2, (-1, 1))
		surf.blit(text2, (3, 1))
		surf.blit(text2, (1, -1))
		surf.blit(text2, (1, 3))

	surf.blit(text1, (1, 1))
	messages.insert(0, {"text": surf, "lifespan": life})


def add_damage_number(pos: tuple[float, float], val: float, crit: bool=False, color: tuple[int, int, int]=(0, 0, 0)):
	global damage_numbers

	if color == (0, 0, 0):
		if crit:
			color = (246, 97, 28)
		else:
			color = (207, 127, 63)

	t1 = commons.MEDIUM_FONT.render(str(int(val)), False, color)
	t2 = commons.MEDIUM_FONT.render(str(int(val)), False, (int(color[0] * 0.8), int(color[1] * 0.8), int(color[2] * 0.8)))

	width = t1.get_width() + 2
	height = t1.get_height() + 2

	if width > height:
		size = width
	else:
		size = height

	surf = pygame.Surface((size, size), pygame.SRCALPHA)

	midX = size * 0.5 - width * 0.5
	midY = size * 0.5 - height * 0.5

	if commons.FANCY_TEXT:
		surf.blit(t2, (midX - 2, midY))
		surf.blit(t2, (midX + 2, midY))
		surf.blit(t2, (midX, midY - 2))
		surf.blit(t2, (midX, midY + 2))

	surf.blit(t1, (midX, midY))

	damage_numbers.append([(pos[0] - camera_position[0] + commons.WINDOW_WIDTH * 0.5,
							pos[1] - camera_position[1] + commons.WINDOW_HEIGHT * 0.5),
						   (random.random() * 4 - 2, -1 - random.random() * 4), surf, 1.5])


def add_recent_pickup(item_id, amount, tier, pos, unique=False, item=None):
	global recent_pickups
	if not unique:
		for recent_pickup in recent_pickups:
			if recent_pickup[0] == item_id:
				amount += recent_pickup[1]
				recent_pickups.remove(recent_pickup)
	if amount > 1:
		string = game_data.json_item_data[item_id]["name"] + "(" + str(amount) + ")"
	else:
		if item is not None:
			string = item.get_name()
		else:
			string = game_data.json_item_data[item_id]["name"]
	size = commons.DEFAULT_FONT.size(string)
	size = (size[0] + 2, size[1] + 2)
	surf = pygame.Surface(size, pygame.SRCALPHA)
	surf.blit(shared_methods.outline_text(string, shared_methods.get_tier_color(tier), commons.DEFAULT_FONT), (1, 1))
	vel = (random.random() * 2 - 1, -50.0)
	recent_pickups.append([item_id, amount, surf, pos, vel, 3.0])
