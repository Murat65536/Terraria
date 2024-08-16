# game_data.py

import pygame
from enum import Enum
import commons
import random
from typing import Any
import json


class ItemTag(Enum):
	TILE = 0
	WALL = 1
	MATERIAL = 2
	WEAPON = 3
	TOOL = 4
	LONGSWORD = 5
	RANGED = 6
	MAGICAL = 7
	AMMO = 8
	PICKAXE = 9
	AXE = 10
	HAMMER = 11
	GRAPPLE = 12 # TODO The code for the grappling hook is incomplete.
	COIN = 13
	SHORTSWORD = 14


class ItemPrefixGroup(Enum):
	UNIVERSAL = 0
	COMMON = 1
	LONGSWORD = 2
	RANGED = 3
	MAGICAL = 4
	SHORTSWORD = 5


class TileTag(Enum):
	TRANSPARENT = 0
	NO_DRAW = 1
	NO_COLLIDE = 2
	MULTITILE = 3
	CYCLABLE = 4
	CHEST = 5
	BREAKABLE = 6
	WORKBENCH = 7
	PLATFORM = 8
	DAMAGING = 9


class TileStrengthType(Enum):
	PICKAXE = 0
	HAMMER = 1
	AXE = 2
	DAMAGE = 3


class TileMaskType(Enum):
	NONE = 0
	NOISY = 1


def make_item_tag_list(item_tags_str):
	str_list = item_tags_str.split(",")
	enum_list = []
	for string in str_list:
		for tag in ItemTag:
			if tag.name == string:
				enum_list.append(tag)
				break
	return enum_list

def make_item_prefix_list(item_prefixes_str):
	str_list = item_prefixes_str.split(",")
	enum_list = []
	for string in str_list:
		for prefix in ItemPrefixGroup:
			if prefix.name == string:
				enum_list.append(prefix)
				break
	return enum_list


def make_tile_tag_list(tile_tags_str):
	str_list = tile_tags_str.split(",")
	enum_list = []
	for string in str_list:
		for tag in TileTag:
			if tag.name == string:
				enum_list.append(tag)
				break
	return enum_list


def int_tuple_str_to_int_tuple(string):
	split_string = string.split(",")
	return int(split_string[0]), int(split_string[1])


def float_tuple_str_to_float_tuple(string):
	split_string = string.split(",")
	return float(split_string[0]), float(split_string[1])


def int_tuple_list_str_to_int_tuple_list(string):
	tuple_strs = string.split(";")
	return_list = []
	for tuple_str in tuple_strs:
		if tuple_str != "":
			return_list.append(int_tuple_str_to_int_tuple(tuple_str))
	return return_list


def float_tuple_list_str_to_float_tuple_list(string):
	tuple_strs = string.split(";")
	return_list = []
	for tuple_str in tuple_strs:
		return_list.append(float_tuple_str_to_float_tuple(tuple_str))
	return return_list


def get_tile_strength_type_from_str(strength_type_string):
	if strength_type_string == "Pickaxe":
		return TileStrengthType.PICKAXE
	elif strength_type_string == "Axe":
		return TileStrengthType.AXE
	elif strength_type_string == "Hammer":
		return TileStrengthType.HAMMER
	elif strength_type_string == "Damage":
		return TileStrengthType.DAMAGE


def get_tile_mask_type_from_str(mask_type_string):
	if mask_type_string == "None":
		return TileMaskType.NONE
	elif mask_type_string == "Noisy":
		return TileMaskType.NOISY


def find_next_char_in_string(string, char, start_index):
	for char_index in range(start_index, len(string)):
		if string[char_index] == char:
			return char_index
	return -1


# Biome Tile Information
# [[surface tile,base tile, alt tile],[wall tile, alt wall tile]]
biome_tile_vals = [[["tile.grass", "tile.dirt", "tile.stone"], ["wall.dirt", "wall.stone"]],
				   [["tile.snow", "tile.snow", "tile.ice"], ["wall.snow", "wall.ice"]],
				   [["tile.sand", "tile.sand", "tile.sandstone"], ["wall.hardened_sand", "wall.sandstone"]]
				  ]

platform_blocks = [257]

json_item_data = []
item_id_str_hash_table = {}
ammo_type_item_lists = {}
json_tile_data = []
tile_id_str_hash_table = {}
tile_id_light_reduction_lookup = []
tile_id_light_emission_lookup = []
json_wall_data = []
wall_id_str_hash_table = {}
json_sound_data = []
sound_id_str_hash_table = {}
json_structure_data = []
structure_id_str_hash_table = {}
json_loot_data = []
loot_id_str_hash_table = {}
json_entity_data = []
entity_id_str_hash_table = {}

sound_volume_multiplier = commons.CONFIG_SOUND_VOLUME
music_volume_multiplier = 1.0


#				 Projectile Information
#
#				 ||	 Name	 |   Type  | Damage |Knockback|Bounces|Hitbox Size|  Trail  |  Gravity |Drag Mod|Sound ID |
projectile_data = [[  "Wooden Arrow",  "Arrow",	 5,		0,	  0,		 13,  "arrow",	   0.5,	   1,	   16],
					[   "Musket Ball", "Bullet",	 7,		2,	  0,		 10, "bullet",	  0.05,	 0.1,	   17],
					[   "Copper Coin", "Bullet",	 1,		2,	  0,		 10, "bullet",	  0.40,	   3,	   17],
					[   "Silver Coin", "Bullet",	 3,		2,	  0,		 10, "bullet",	  0.20,	   2,	   17],
					[	 "Gold Coin", "Bullet",	15,		2,	  0,		 10, "bullet",	  0.10,	   1,	   17],
					[ "Platinum Coin", "Bullet",	50,		2,	  0,		 10, "bullet",	  0.05,	 0.1,	   17],
				]


# Item Prefix Information
prefix_data = {
	ItemPrefixGroup.UNIVERSAL:
		[  # ||   Name   |Damage|Speed|Crit Chance|Knockback|Tier||
			[	  "Keen",	 0,	0,	 0,		0,   1],
			[  "Superior",   0.1,	0,  0.03,	  0.1,   2],
			[  "Forceful",	 0,	0,	 0,	 0.15,   1],
			[	"Broken",  -0.3,	0,	 0,	 -0.2,  -2],
			[   "Damaged", -0.15,	0,	 0,		0,  -1],
			[	"Shoddy",  -0.1,	0,	 0,	-0.15,  -2],
			[   "Hurtful",   0.1,	0,	 0,		0,   1],
			[	"Strong",	 0,	0,	 0,	 0.15,   1],
			["Unpleasant",  0.05,	0,	 0,	 0.15,   2],
			[	  "Weak",	 0,	0,	 0,	 -0.2,  -1],
			[  "Ruthless",  0.18,	0,	 0,	 -0.1,   1],
			[	 "Godly",  0.15,	0,  0.05,	 0.15,   2],
			[   "Demonic",  0.15,	0,  0.05,		0,   2],
			[   "Zealous",	 0,	0,  0.05,		0,   1],
		],

	ItemPrefixGroup.COMMON:
		[  # ||   Name  |Damage| Speed|Crit Chance|Knockback|Tier||
			[	"Quick",	 0,   0.1,		  0,		0,   1],
			[   "Deadly",   0.1,   0.1,		  0,		0,   2],
			[	"Agile",	 0,   0.1,	   0.03,		0,   1],
			[   "Nimble",	 0,  0.05,		  0,		0,   1],
			["Murderous", -0.07,  0.06,	   0.03,		0,   2],
			[	 "Slow",	 0, -0.15,		  0,		0,  -1],
			[ "Sluggish",	 0,  -0.2,		  0,		0,  -2],
			[	 "Lazy",	 0, -0.08,		  0,		0,  -1],
			[ "Annoying",  -0.2, -0.15,		  0,		0,  -2],
			[	"Nasty",  0.05,   0.1,	   0.02,	 -0.1,   1],
		],

	ItemPrefixGroup.LONGSWORD:
		[  # ||   Name  |Damage| Speed|Crit Chance| Size |Knockback|Tier||
			[	"Large",	 0,	 0,		  0,  0.12,		0,   1],
			[  "Massive",	 0,	 0,		  0,  0.18,		0,   1],
			["Dangerous",  0.05,	 0,	   0.02,  0.05,		0,   1],
			[   "Savage",   0.1,	 0,		  0,   0.1,	  0.1,   2],
			[	"Sharp",  0.15,	 0,		  0,	 0,		0,   1],
			[   "Pointy",   0.1,	 0,		  0,	 0,		0,   1],
			[	 "Tiny",	 0,	 0,		  0, -0.18,		0,  -1],
			[ "Terrible", -0.15,	 0,		  0, -0.13,	-0.15,  -2],
			[	"Small",	 0,	 0,		  0,  -0.1,		0,  -1],
			[	 "Dull", -0.15,	 0,		  0,	 0,		0,  -1],
			[  "Unhappy",	 0,  -0.1,		  0,  -0.1,	 -0.1,  -2],
			[	"Bulky",  0.05, -0.15,		  0,   0.1,	  0.1,   1],
			[ "Shameful",  -0.1,	 0,		  0,   0.1,	 -0.2,  -2],
			[	"Heavy",	 0,  -0.1,		  0,	 0,	 0.15,   0],
			[	"Light",	 0,  0.15,		  0,	 0,	 -0.1,   0],
			["Legendary",  0.15,   0.1,	   0.05,   0.1,	 0.15,   2],
		],

			ItemPrefixGroup.SHORTSWORD:
		[  # ||   Name  |Damage| Speed|Crit Chance| Size |Knockback|Tier||
			[	"Large",	 0,	 0,		  0,  0.12,		0,   1],
			[  "Massive",	 0,	 0,		  0,  0.18,		0,   1],
			["Dangerous",  0.05,	 0,	   0.02,  0.05,		0,   1],
			[   "Savage",   0.1,	 0,		  0,   0.1,	  0.1,   2],
			[	"Sharp",  0.15,	 0,		  0,	 0,		0,   1],
			[   "Pointy",   0.1,	 0,		  0,	 0,		0,   1],
			[	 "Tiny",	 0,	 0,		  0, -0.18,		0,  -1],
			[ "Terrible", -0.15,	 0,		  0, -0.13,	-0.15,  -2],
			[	"Small",	 0,	 0,		  0,  -0.1,		0,  -1],
			[	 "Dull", -0.15,	 0,		  0,	 0,		0,  -1],
			[  "Unhappy",	 0,  -0.1,		  0,  -0.1,	 -0.1,  -2],
			[	"Bulky",  0.05, -0.15,		  0,   0.1,	  0.1,   1],
			[ "Shameful",  -0.1,	 0,		  0,   0.1,	 -0.2,  -2],
			[	"Heavy",	 0,  -0.1,		  0,	 0,	 0.15,   0],
			[	"Light",	 0,  0.15,		  0,	 0,	 -0.1,   0],
			["Legendary",  0.15,   0.1,	   0.05,   0.1,	 0.15,   2],
		],

	ItemPrefixGroup.RANGED:
		[  # ||	Name	| Damage  |Speed|Crit Chance|Velocity|Knockback|Tier||
			[	 "Sighted",	  0.1,	0,	   0.03,	   0,		0,   1],
			[	   "Rapid",		0, 0.15,		  0,	 0.1,		0,   2],
			[	   "Hasty",		0,  0.1,		  0,	0.15,		0,   2],
			["Intimidating",		0,	0,		  0,	0.05,	 0.15,   2],
			[	  "Deadly",	  0.1, 0.05,	   0.02,	0.05,	 0.05,   2],
			[	 "Staunch",	  0.1,	0,		  0,	   0,	 0.15,   2],
			[	   "Awful",	-0.15,	0,		  0,	-0.1,	 -0.1,  -2],
			[   "Lethargic",		0, 0.15,		  0,	-0.1,		0,  -2],
			[	 "Awkward",		0, -0.1,		  0,	   0,	 -0.2,  -2],
			[	"Powerful",	 0.15, -0.1,	   0.01,	   0,		0,   1],
			[   "Frenzying",	-0.15, 0.15,		  0,	   0,		0,   0],
			[	  "Unreal",	 0.15,  0.1,	   0.05,	 0.1,	 0.15,   2],
		],

	ItemPrefixGroup.MAGICAL:
		[  # ||  Name   |Damage|Speed|Crit Chance|Mana Cost|Knockback|Tier||
			[   "Mystic",   0.1,	0,		  0,	-0.15,		0,   2],
			[	"Adept",	 0,	0,		  0,	-0.15,		0,   1],
			["Masterful",  0.15,	0,		  0,	 -0.2,	 0.05,   2],
			[	"Inept",	 0,	0,		  0,	  0.1,		0,  -1],
			[ "Ignorant",  -0.1,	0,		  0,	  0.2,		0,  -2],
			[ "Deranged",  -0.1,	0,		  0,		0,	 -0.1,  -1],
			[  "Intense",   0.1,	0,		  0,	 0.15,		0,  -1],
			[	"Taboo",	 0,  0.1,		  0,	  0.1,	  0.1,   1],
			["Celestial",   0.1, -0.1,		  0,	 -0.1,	  0.1,   1],
			[  "Furious",  0.15,	0,		  0,	  0.2,	 0.15,   1],
			[	"Manic",  -0.1,  0.1,		  0,	 -0.1,		0,   1],
			[ "Mythical",  0.15,  0.1,	   0.05,	 -0.1,	 0.15,   2]
		]
}

# (((result,((component1,amnt),(component2,amnt),etc..))#recipe)#bench type)
crafting_data = [((4, ((10, 1))),
				 (17, ((4, 10), (2, 10)))),  # inventory/no bench
				 (),
				 (),
				 (),
				]


# Randomly chosen when the player dies

# <p> inserts the players name 
# <e> inserts the name of the enemy that killed the player
# <w> inserts the world name

death_lines = {
	"spike":
		[
			"<p> got impaled by a spike.",
			"A spike impaled the face of <p>.",
			"The spikes of <w> eradicated <p>.",
			"<p> didn't look where they were going.",
			"<p> found out that spikes are sharp.",
		],
	"falling":
		[
			"<p> fell to their death.",
			"<p> didn't bounce.",
			"<p> invented gravity.",
			"<p> discovered the meaning of defenestration.",
			"<p> was freeeee, free-fallin'.",
			"<p> tried to ice skate uphill.",
			"<p> thought they could fly.",
			"<p> left a crater.",
			"<p> forgot their happy thought.",
		],
	"enemy":
		[
			"<p> was slain by <e>.",
			"<p> was eviscerated by <e>.",
			"<p> was murdered by <e>.",
			"<p>'s face was torn off by <e>.",
			"<p>'s entrails were ripped out by <e>.",
			"<p> was destroyed by <e>.",
			"<p>'s skull was crushed by <e>.",
			"<p> got massacred by <e>.",
			"<p> got impaled by <e>.",
			"<p> was torn in half by <e>.",
			"<p> was decapitated by <e>.",
			"<p> let their arms get torn off by <e>.",
			"<p> watched their innards become outards by <e>.",
			"<p> was brutally dissected by <e>.",
			"<p>'s extremities were detached by <e>.",
			"<p>'s body was mangled by <e>.",
			"<p>'s vital organs were ruptured by <e>.",
			"<p> was turned into a pile of flesh by <e>.",
			"<p> was removed from <w> by <e>.",
			"<p> got snapped in half by <e>.",
			"<p> was cut down the middle by <e>.",
			"<p> was chopped up by <e>.",
			"<p>'s plead for death was answered by <e>.",
			"<p>'s meat was ripped off the bone by <e>.",
			"<p>'s flailing about was finally stopped by <e>.",
			"<p> had their head removed by <e>.",
			"<p>'s bowels were unplugged by <e>.",
			"<p>'s journey was ended by <e>.",
			"<p> was sent to Ocram's House by <e>.",
			"<p> was macerated by <e>.",
			"<p> was exsanguinated by <e>.",
			"<p> was sent to the bone zone by <e>.",
			"<p> was spontaneously lobotomized by <e>.",
			"<p> was pressed into a succulent pulp by <e>.",
			"<p> was ground into sad meat by <e>.",
			"<p>'s bones were shattered by <e>.",
			"<p> was turned into monster food by <e>.",
			"<p> had their home remodeled by <e>.",
			"<p> was voluntold to donate blood by <e>.",
			"<p> had their cap peeled back by <e>.",
			"<p>'s top knot was carved off by <e>.",
			"<p>'s parts were misplaced by <e>.",
			"<p> was blended into a zesty sauce by <e>.",
			"<p>'s spine was ripped out by <e>.",
			"<p>'s living streak was ended by <e>.",
			"<p> received a forced amputation by <e>.",
			"<p>'s neck was snapped by <e>.",
			"<p> was shredded to bits by <e>.",
			"<p> succumbed to a fatal injury by <e>.",
			"<p> was informed of their expiration date by <e>.",
			"<p>'s incompetence was put on display by <e>.",
			"<p>'s soul was extractinated by <e>.",
			"<p> underwent a merciful euthanasia by <e>.",
			"<p> was eaten from the bottom up by <e>.",
			"<p> was deboned by <e>.",
			"<p> had both kidneys stolen by <e>.",
			"<p>'s depravity was ended by <e>.",
			"<p>'s disc was herniated by <e>.",
			"<p>'s body was donated to science by <e>.",
			"<p> had their brain turned to jam by <e>.",
			"<p> was turned into long pig by <e>.",
			"<p> was sent to the farm by <e>.",
			"<p>'s clogs were popped by <e>.",
			"<p>'s ticker was stopped by <e>.",
			"<p> was whacked in the head by <e>.",
			"<p> got rubbed out by <e>.",
			"<p> was degloved by <e>.",
			"<p> was flayed by <e>.",
			"<p> was ganked by <e>.",
			"<p> got spanked by <e>.",
			"<p> got got by <e>.",
			"<p> got murked by <e>.",
			"<p> was put in a glass coffin by <e>.",
			"<p> was put on the wrong side of the grass by <e>.",
			"<p> will quickly be forgotten by <e>.",
			"<p> was smote by <e>.",
		]
}


# Messages displayed when a world is loading

helpful_tips = [
	"Advanced players may wish to remap their buttons; you can do this from the Controls Menu in Settings.",
	"The Housing section of the Equipment Menu allows you to decide what rooms you want your NPCs to live in.",
	"You can check if a room is valid housing from the Housing section of the Inventory Menu.",
	"If you get lost or need to find another player, open the World Map.",
	"Not sure what to do next? Take a look at the Achievement Guide for a clue!",
	"With the Block Swap mechanic enabled, you can replace one block with another directly, rather than having to mine it first.",
	"Press the + and - keys to zoom in & out! Focus on what matters!",
	"Have something on the Map to show a friend? Double click on the Map to ping a location for everyone to see!",
	"You can continuously use some items by holding down the Use / Attack button.",
	"Press Smart Cursor to switch between Cursor Modes.",
	"If your Inventory is full, you can press trash and Use / Attack to send items to the Trash.",
	"When speaking to a vendor, you can sell items in your Inventory by pressing trash and Use / Attack.",
	"You can remove Torches with Interact or with a pickaxe.",
	"In your Inventory, you can press Interact to equip items such as armor or accessories directly to a usable slot.",
	"Hold Auto Select to use Auto Select, a versatile feature that adapts to your environment. It will allow you to automatically hold your Torches in dark caves, Glowsticks when underwater, or even select the right tool for breaking something.",
	"Press Alt and Use / Attack to Favorite an item. Favorited items can no longer be sold, thrown away, or dropped. No more accidentally losing your favorite items!",
	"Other players can loot your chests! If you don't trust them, use a Safe or Piggy Bank; those items have storage that is exclusive to each player.",
	"Info accessories don't need to be equipped to provide you and nearby friends with useful information; you can just leave them in your Inventory.",
	"Rope can really help you get around while exploring caves. You can even craft it into a Rope Coil which can be thrown and automatically unfolds!",
	"You can change your spawn point by placing and using a bed.",
	"If you find a Magic Mirror, you can use it to teleport back to your spawn point.",
	"Water will break your fall.",
	"Torches and Glowsticks can be a light for you in dark places when all other lights go out. Torches won't work underwater, but Glowsticks will.",
	"Don't fall into lava without drinking an Obsidian Skin Potion first!",
	"You won't take falling damage if you have a Lucky Horseshoe. Look for them in chests found on Floating Islands.",
	"Walking on Hellstone and Meteorite can burn you! Protect yourself by equipping an Obsidian Skull or similar accessory.",
	"Life Crystals are hidden around the World. Use them to increase your health.",
	"Torches require Wood and Gel to craft. Gel can be obtained by defeating slimes.",
	"Some ores require better pickaxes to mine.",
	"Bows and guns require the proper ammo in your Ammo Slots.",
	"When exploring, it helps to keep some Platforms on hand. They can be crafted from numerous materials such as Wood, Glass, or even Bones.",
	"Wear a Mining Helmet if you don't want to use Torches.",
	"You can wear Buckets on your head!",
	"Demon Altars and Crimson Altars can't be destroyed with a normal hammer. You have to pwn them.",
	"Killing Bunnies is cruel. Period.",
	"Falling Stars sometimes appear at night. Collect 5 of them to craft a Mana Crystal you can use to increase your Mana.",
	"A pet can be your best friend.",
	"Time heals all wounds.",
	"You can plant Acorns to grow new trees.",
	"Rocket science gave us Rocket Boots.",
	"The Cloud in a Bottle and Shiny Red Balloon accessories both improve your ability to jump. Combine them to make a Cloud in a Balloon.",
	"If you store your Coins in a Chest or Piggy Bank, you will be less likely to lose them.",
	"To craft potions, place a Bottle on a Table to make an Alchemy Station. Double, double, toil and trouble!",
	"Wearing a full set of armor crafted from the same material gives you an extra bonus.",
	"Build a Furnace to craft metal bars out of ore.",
	"You can harvest Cobwebs and turn them into Silk. You can use Silk to craft beds, sofas, and more!",
	"You can buy Wires from the Mechanic and use them to create traps, pumping systems, or other elaborate devices.",
	"If you're sick of getting knocked around, try equipping a Cobalt Shield. You can find one in the Dungeon.",
	"Grappling Hooks are invaluable tools for exploration. Try crafting them with Hooks or gems.",
	"The best wizards around use Mana Flowers.",
	"Use " + '"' + "suspicious looking items" + '"'  + "at your own risk!",
	"Seeds can be used to grow a variety of useful ingredients for crafting potions.",
	"If you need to remove background walls, craft a hammer!",
	"Got some extra walls or platforms? You can turn them back into their original materials!",
	"Fishing is a fantastic source of crafting ingredients, accessories, and loot crates!",
	"Nothing improves your mobility like Wings. Who wouldn't want to fly?",
	"Riding Minecarts is one of the best ways of getting around. You can build your own tracks, or find them Underground.",
	"Life Crystals not enough for you? Eventually, Life Fruit will grow in the Jungle, and can give you an extra boost to your health.",
	"Change your clothes in game at a Dresser or talk to the Stylist for a new hairdo.",
	"Mounts grant the player increased mobility and a variety of useful abilities. Each one is unique!",
	"Looking for a challenge? Try Expert mode!",
	"If an enemy steals your money after you die in Expert Mode, hunt it down! If you defeat it, you can get your money back.",
	"Keep an eye out for Goodie Bags around Halloween. If you open them, you can find all sorts of spooky items.  Trick or Treat!",
	"Clouds are nice and soft, and you won't get hurt falling on them no matter how far you fall.",
	"Did you know you can order your Summons to attack a specific target? While holding a Summoning Weapon, Right Click an enemy!",
	"The Void Bag is a magical artifact that will store items for you when your inventory is full.",
	"Explosives are dangerous!\n...and effective...",
	"Sometimes you can find NPCs hidden around the World.",
	"The Old Man at the Dungeon is a Clothier. If only someone could lift his curse...",
	"Merchants love money. If you save up enough, one might move in!",
	"Keep an explosive in your inventory or a storage container to attract a Demolitionist to your house.",
	"Make sure you have valid housing with empty rooms, and you may attract new inhabitants to your World.",
	"Slay a boss to attract a Dryad to your house. She can tell you the state of Corruption, Crimson, and Hallow in your World.",
	"Santa Claus is real. He comes to town after the Frost Legion is defeated (and 'tis the season).",
	"A room in a house can have Wood Platforms as a floor or ceiling, but NPCs need at least one solid block to stand on.",
	"The Goblin Tinkerer found in Underground Caverns will sell you many useful items, including a Tinkerer's Workshop.",
	"The Arms Dealer knows more about guns than anyone. If you find one, he might move in.",
	"The Mechanic got lost in the Dungeon. You'll have to help her out if you want her to move in.",
	"Once you use a Life Crystal, a Nurse might move in! Speak to her for healing at any time . . . for a price, of course.",
	"If you ever want to get stylish, try dyes! The Dye Trader can help you turn some materials into new dye colors.",
	"The Tavernkeep is a guest from a faraway land called Etheria.",
	"If you need a new haircut, go check out a nearby Spider Biome. Stylists always end up lost in them!",
	"Regular Wood and Stone not vibrant enough for you? A Painter will move in and sell paints if enough townsfolk move in.",
	"You could get a Witch Doctor to come to your World if you defeat the Queen Bee.",
	"The Party Girl won't move in unless your World is full of other townsfolk. Afterall, what's a party without lots of guests?",
	"The Wizard sells some useful magic artifacts, but he has a tendency to wander off Underground.",
	"The Tax Collector spends his days wandering the Underworld as a Tortured Soul. If only there were a way to purify him . . .",
	"Pirates are so unpredictable. First they invade your world, and then they move into your houses!",
	"If you ever defeat any giant robots, a Steampunker might move in to your World.",
	"If you like rockets, the Cyborg may have some for sale.",
	"The Traveling Merchant never stays in one place for long, but he always brings different wares when he visits!",
	"Not all Skeletons are evil. Some are even known to sell unique items to those that can find them.",
	"Find a cool new Material?  Want to know what you can make?  Check with your friendly neighborhood Guide!",
	"Have some NPCs perished?  Don't worry, they'll be back in the morning.",
	"Mushroom Biomes can be grown above ground as well as below. Friendly Truffles will sometimes make themselves at home in Surface Mushroom Biomes.",
	"There are Floating Islands in the sky.",
	"Watch out for Meteorites!",
	"If you dig deep enough, you'll end up in The Underworld!",
	"You can use Hallowed Seeds, Holy Water, or Pearlstone to make Hallow spread.",
	"The Hallow is the only place where Corruption and Crimson cannot spread.",
	"The Corruption is full of chasms. Mind the gaps.",
	"If your house doesn't have background walls, monsters will be able to spawn inside.",
	"You can destroy Shadow Orbs and Crimson Hearts with a hammer or explosives, but prepare yourself for the forces they unleash.",
	"When dealing with a Goblin Army, crowd control is key.",
	"Sand is overpowered.",
	"When a Sandstorm hits, deserts can be very dangerous. New enemies, reduced visibility, and it can even be hard to move!",
	"It's worth it to explore your Oceans. You can find treasure, dyes, and even sleeping fishermen.",
	"Enemies aren't the only danger when exploring Underground. Watch out for traps too!",
	"During a Blood Moon, Zombies can open doors.",
	"Bosses are easier to defeat with friends.",
	"Defeat the boss in The Underworld to change the World forever. Find a Guide Voodoo Doll and hurl it into the infernal lava to summon him.",
	"Don't shake a Snow Globe unless you want to summon the Frost Legion.",
	"Be careful around Martian Probes. If they scan you, they'll summon a Martian Invasion!",
	"During a Solar Eclipse, be on the lookout for tons of strange and creepy monsters.",
	"Sometimes, enemies may even invade from other dimensions . . .",
	"A Pumpkin Medallion can be used to summon the Pumpkin Moon. Spooky!",
	"Feeling up for the chill of winter? Use a Naughty Present to summon the Frost Moon!"
]

# Messages displayed when the user presses the quit button in a world

exit_messages = [
	"Are you sure you want to exit?",
	"Leaving so soon?",
	"You'll come back someday right?",
	"So this is goodbye?",
	"Don't be gone long, k?",
	"If you quit, I'll look for you, I will find you...",
	"Running won't help, they'll still get you...",
	"You're just gonna leave your slime friends?",
	"When you quit, you're killing slimes...",
	"You're just gonna play for two seconds then leave?",
]

active_menu_buttons = [
	["MAIN", 0, 2, 3, 4, 5, 6],
	["SETTINGS", 0, 1, 7, 8],
	["CREDITS", 0, 1, 9, 10, 11, 12, 13],
	["PLAYERSELECTION", 0, 1, 14, 15],
	["PLAYERCREATION", 0, 1, 16, 17, 18, 19, 20, 21, 22],
	["COLORPICKER", 0, 1],
	["CLOTHES", 0, 1, 23, 24, 25, 26],
	["PLAYERNAMING", 0, 1, 27],
	["WORLDSELECTION", 0, 1, 28, 29],
	["WORLDCREATION", 0, 1, 30, 31, 32, 33, 34],
	["WORLDNAMING", 0, 1, 35],
	["CHANGES", 0, 1, 36, 37, 38, 39, 40],
]

structure_tiles = [
	[  # Mine shaft hut
		[-3, -7],
		[
			[[ -2, -2], [  4,  4], [  4,  4], [  4,  4], [  4,  4], [  4,  4], [ -2, -2]], 
			[[  4,  4], [  4,  4], [  4,  4], [  4,  4], [  4,  4], [  4,  4], [  4,  4]],
			[[  4,  4], [  4,  4], [ -1,  4], [ -1,  4], [ -1,  4], [  4,  4], [  4,  4]],
			[[ -2, -2], [  1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [  1,  1], [ -2, -2]], 
			[[ -2, -2], [261,  1], [ -1,  1], [ -1, -1], [ -1,  1], [261,  1], [ -2, -2]], 
			[[ -2, -2], [271,  1], [ -1,  1], [ -1,  1], [ -1,  1], [271,  1], [ -2, -2]], 
			[[ -2, -2], [281,  1], [ -1,  1], [ -1,  1], [ -1,  1], [281,  1], [ -2, -2]], 
			[[ -2, -2], [  1,  1], [257,  4], [257,  4], [257,  4], [  1,  1], [ -2, -2]]
		]
	],
	[  # Mine shaft vertical
		[-2, -7],
		[
			[[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]], 
			[[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]],
			[[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]],
			[[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]], 
			[[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]], 
			[[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]], 
			[[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]], 
			[[  1,  1], [257,  4], [257,  4], [257,  4], [  1,  1]]
		]
	],
	[  # Mine shaft vertical door left
	   [-2, -7],
	   [
		   [[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]], 
		   [[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]],
		   [[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]],
		   [[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]], 
		   [[261,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]], 
		   [[271,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]], 
		   [[281,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]], 
		   [[  1,  1], [257,  4], [257,  4], [257,  4], [  1,  1]]
	   ]
	],
	[  # Mine shaft vertical door right
	   [-2, -7],
	   [
		   [[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]], 
		   [[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]],
		   [[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]],
		   [[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [  1,  1]], 
		   [[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [261,  1]], 
		   [[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [271,  1]], 
		   [[  1,  1], [ -1,  4], [ -1,  4], [ -1,  4], [281,  1]], 
		   [[  1,  1], [257,  4], [257,  4], [257,  4], [  1,  1]]
	   ]
	],
	[  # Mine shaft vertical bottom
	   [-2, -7],
	   [
		   [[  1,  1], [ -1,  4], [ -1, -2], [ -1,  4], [  1,  1]], 
		   [[  1,  1], [ -1, -2], [ -1,  4], [ -1, -2], [  1,  1]],
		   [[  1,  1], [ -1,  4], [ -2,  4], [ -1,  4], [ -1,  1]],
		   [[  1,  1], [ -2, -2], [ -1, -2], [ -1, -2], [  1,  1]], 
		   [[  1,  1], [ -2,  4], [ -1, -2], [ -2,  4], [ -2, -2]], 
		   [[ -2, -2], [ -2, -2], [ -2, -2], [ -2, -2], [  1,  1]], 
		   [[  1,  1], [ -2, -2], [ -2, -2], [ -2, -2], [ -2, -2]], 
		   [[ -2, -2], [ -2, -2], [ -2, -2], [ -2, -2], [ -2, -2]]
	   ]
	],
	[  # Mine shaft chest room left
	   [-12, -3],
	   [
		   [[  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [ -2, -2], [ -2, -2], [ -2, -2]],
		   [[  1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1]], 
		   [[  1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [261,  1], [ -1,  1], [ -1,  1], [ -1,  1]], 
		   [[  1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -3,  1], [ -2,  1], [ -1,  1], [ -1,  1], [ -1,  1], [271,  1], [ -1,  1], [ -1,  1], [ -1,  1]], 
		   [[  1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -2,  1], [ -2,  1], [ -1,  1], [ -1,  1], [ -1,  1], [281,  1], [ -1,  1], [ -1,  1], [ -1,  1]], 
		   [[  1,  1], [258,  1], [258,  1], [258,  1], [258,  1], [258,  1], [258,  1], [258,  1], [258,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1]], 
		   [[  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [ -2, -2], [ -2, -2], [ -2, -2]],
	   ]
	],
	[  # Mine shaft chest room right
	   [0, -3],
	   [
		   [[ -2, -2], [ -2, -2], [ -2, -2], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1]],
		   [[  1,  1], [  1,  1], [  1,  1], [  1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [  1,  1]], 
		   [[ -1,  1], [ -1,  1], [ -1,  1], [261,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -1,  1], [  1,  1]], 
		   [[ -1,  1], [ -1,  1], [ -1,  1], [271,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -3,  1], [ -2,  1], [ -1,  1], [ -1,  1], [ -1,  1], [  1,  1]], 
		   [[ -1,  1], [ -1,  1], [ -1,  1], [281,  1], [ -1,  1], [ -1,  1], [ -1,  1], [ -2,  1], [ -2,  1], [ -1,  1], [ -1,  1], [ -1,  1], [  1,  1]], 
		   [[  1,  1], [  1,  1], [  1,  1], [  1,  1], [258,  1], [258,  1], [258,  1], [258,  1], [258,  1], [258,  1], [258,  1], [258,  1], [  1,  1]], 
		   [[ -2, -2], [ -2, -2], [ -2, -2], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1], [  1,  1]], 
	   ]
	],
]

# Special items for loot chests
#			 | Item ID | Chance | Block Depth | Random Count Range |
special_loot = [
				[	   19,	 0.5,			0,		   [1, 1]],
				[	   17,	 0.5,			0,		   [1, 1]],
			  ]

# Misc items for loot chests
#		   | Item ID | Chance | Block Depth | Random Count Range |
misc_loot = [
			[	   18,   0.333,			0,			[10, 100]],
			[	   20,   0.333,			0,			[10, 100]],
			[	   30,   0.333,			0,			  [5, 30]],
		   ]


def find_prefix_data_by_name(prefix_name):
	for prefix_dat in prefix_data[ItemPrefixGroup.UNIVERSAL]:
		if prefix_dat[0] == prefix_name:
			return [ItemPrefixGroup.UNIVERSAL, prefix_dat]
	for prefix_dat in prefix_data[ItemPrefixGroup.COMMON]:
		if prefix_dat[0] == prefix_name:
			return [ItemPrefixGroup.COMMON, prefix_dat]
	for prefix_dat in prefix_data[ItemPrefixGroup.LONGSWORD]:
		if prefix_dat[0] == prefix_name:
			return [ItemPrefixGroup.LONGSWORD, prefix_dat]
	for prefix_dat in prefix_data[ItemPrefixGroup.RANGED]:
		if prefix_dat[0] == prefix_name:
			return [ItemPrefixGroup.RANGED, prefix_dat]
	for prefix_dat in prefix_data[ItemPrefixGroup.MAGICAL]:
		if prefix_dat[0] == prefix_name:
			return [ItemPrefixGroup.MAGICAL, prefix_dat]
	for prefix_dat in prefix_data[ItemPrefixGroup.SHORTSWORD]:
		if prefix_dat[0] == prefix_name:
			return [ItemPrefixGroup.SHORTSWORD, prefix_dat]
	return None


def parse_item_data():
	global json_item_data
	json_read_file = open("assets/game_data/item_data.json", "r")
	json_item_data = json.loads(json_read_file.read())["items"]["item"]
	json_read_file.close()

	json_item_data = sorted(json_item_data, key=lambda x: int(x["id"]))

	for item_data in json_item_data:
		item_data["id"] = int(item_data["id"])
		item_data["tags"] = make_item_tag_list(item_data["tags"])
		item_data["tier"] = int(item_data["tier"])
		item_data["max_stack"] = int(item_data["max_stack"])
		item_data["buy_price"] = int(item_data["buy_price"])
		item_data["sell_price"] = int(item_data["sell_price"])
		item_data["hold_offset"] = float(item_data["hold_offset"])
		try:
			loaded_surf = pygame.image.load(item_data["image_path"]).convert_alpha()
			if max(loaded_surf.get_width(), loaded_surf.get_height()) > 32:
				loaded_surf = pygame.transform.scale(loaded_surf, (loaded_surf.get_width() * (32 / max(loaded_surf.get_width(), loaded_surf.get_height())), loaded_surf.get_height() * (32 / max(loaded_surf.get_width(), loaded_surf.get_height()))))
			item_data["image"] = loaded_surf
			item_data["item_slot_offset_x"] = int(24 - item_data["image"].get_width() * 0.5)
			item_data["item_slot_offset_y"] = int(24 - item_data["image"].get_height() * 0.5)
		except FileNotFoundError:
			item_data["image"] = None
		except pygame.error:
			item_data["image"] = None

		if ItemTag.WEAPON in item_data["tags"]:
			item_data["attack_speed"] = float(item_data["attack_speed"])
			item_data["attack_damage"] = float(item_data["attack_damage"])
			item_data["knockback"] = float(item_data["knockback"])
			item_data["crit_chance"] = float(item_data["crit_chance"])
			try:
				loaded_surf = pygame.image.load(item_data["world_override_image_path"]).convert_alpha()
				item_data["world_override_image"] = pygame.Surface((max(loaded_surf.get_width(), loaded_surf.get_height()), max(loaded_surf.get_width(), loaded_surf.get_height())))
			except FileNotFoundError:
				item_data["world_override_image"] = None
			except pygame.error:
				item_data["world_override_image"] = None

			item_data["prefixes"] = make_item_prefix_list(item_data["prefixes"])

		if ItemTag.RANGED in item_data["tags"]:
			item_data["ranged_projectile_speed"] = float(item_data["ranged_projectile_speed"])
			item_data["ranged_accuracy"] = float(item_data["ranged_accuracy"])
			item_data["ranged_num_projectiles"] = int(item_data["ranged_num_projectiles"])

		if ItemTag.MAGICAL in item_data["tags"]:
			item_data["mana_cost"] = int(item_data["mana_cost"])

		if ItemTag.AMMO in item_data["tags"]:
			item_data["ammo_damage"] = float(item_data["ammo_damage"])
			item_data["ammo_drag"] = float(item_data["ammo_drag"])
			item_data["ammo_gravity_mod"] = float(item_data["ammo_gravity_mod"])
			item_data["ammo_knockback_mod"] = float(item_data["ammo_knockback_mod"])
			try:
				ammo_type_item_lists[item_data["ammo_type"]].append(int(item_data["id"]))
			except KeyError:
				ammo_type_item_lists[item_data["ammo_type"]] = [int(item_data["id"])]

		if ItemTag.PICKAXE in item_data["tags"]:
			item_data["pickaxe_power"] = float(item_data["pickaxe_power"])

		if ItemTag.AXE in item_data["tags"]:
			item_data["axe_power"] = float(item_data["axe_power"])
		if ItemTag.HAMMER in item_data["tags"]:
			item_data["hammer_power"] = float(item_data["hammer_power"])

		if ItemTag.GRAPPLE in item_data["tags"]:
			item_data["grapple_speed"] = float(item_data["grapple_speed"])
			item_data["grapple_chain_length"] = float(item_data["grapple_chain_length"])
			item_data["grapple_max_chains"] = int(item_data["grapple_max_chains"])
			try:
				loaded_surf = pygame.image.load(item_data["grapple_chain_image_path"]).convert_alpha()
				item_data["grapple_chain_image"] = pygame.Surface((loaded_surf.get_width(), loaded_surf.get_height()))
			except FileNotFoundError:
				item_data["grapple_chain_image"] = None
			except pygame.error:
				item_data["grapple_chain_image"] = None

			try:
				loaded_surf = pygame.image.load(item_data["grapple_claw_image_path"]).convert_alpha()
				item_data["grapple_claw_image"] = pygame.Surface((loaded_surf.get_width(), loaded_surf.get_height()))
				item_data["grapple_claw_image"].set_colorkey((255, 0, 255))
			except FileNotFoundError:
				item_data["grapple_claw_image"] = None
			except pygame.error:
				item_data["grapple_claw_image"] = None


def get_item_by_id(item_id) -> Any:
	if item_id < len(json_item_data):
		return json_item_data[item_id]


def get_item_id_by_id_str(item_id_str):
	return item_id_str_hash_table[item_id_str]


def get_item_by_id_str(item_id_str):
	return get_item_by_id(get_item_id_by_id_str(item_id_str))


def create_item_id_str_hash_table():
	global item_id_str_hash_table
	for item_index in range(len(json_item_data)):
		item_id_str_hash_table[json_item_data[item_index]["id_str"]] = item_index


def get_ammo_item_ids_for_ammo_type(ammo_type):
	ammo_item_ids = []
	for item_data in json_item_data:
		if ItemTag.AMMO in item_data["tags"]:
			if item_data["ammo_type"] == ammo_type:
				ammo_item_ids.append(int(item_data["id"]))


def parse_tile_data():
	global json_tile_data
	json_read_file = open("assets/game_data/tile_data.json", "r")
	json_tile_data = json.loads(json_read_file.read())["tiles"]["tile"]
	json_read_file.close()

	json_tile_data = sorted(json_tile_data, key=lambda x: int(x["id"]))

	for tile_data in json_tile_data:
		tile_data["id"] = int(tile_data["id"])
		tile_data["strength"] = float(tile_data["strength"])
		tile_data["strength_type"] = get_tile_strength_type_from_str(tile_data["strength_type"])
		tile_data["mask_type"] = get_tile_mask_type_from_str(tile_data["mask_type"])
		tile_data["mask_merge_id_strs"] = tile_data["mask_merge_id_strs"].split(",")
		tile_data["light_reduction"] = int(tile_data["light_reduction"])
		tile_data["light_emission"] = int(tile_data["light_emission"])

		if tile_data["average_color"] == "auto":
			tile_data["average_color"] = (255, 0, 255)
			override_average_color = True
		else:
			val_array = tile_data["average_color"].split(",")
			tile_data["average_color"] = (int(val_array[0]), int(val_array[1]), int(val_array[2]))
			override_average_color = False

		tile_data["tags"] = make_tile_tag_list(tile_data["tags"])
		try:
			tile_data["image"] = pygame.image.load(tile_data["image_path"]).convert_alpha()  # , (commons.BLOCK_SIZE, commons.BLOCK_SIZE)
			if override_average_color:
				tile_data["average_color"] = pygame.transform.average_color(tile_data["image"])
		except FileNotFoundError:
			tile_data["image"] = None
		except pygame.error:
			tile_data["image"] = None

		tile_data["item_count_range"] = int_tuple_str_to_int_tuple(tile_data["item_count_range"])

		if TileTag.MULTITILE in tile_data["tags"]:
			tile_data["multitile_dimensions"] = int_tuple_str_to_int_tuple(tile_data["multitile_dimensions"])
			tile_data["multitile_required_solids"] = int_tuple_list_str_to_int_tuple_list(tile_data["multitile_required_solids"])
			tile_data["multitile_image"] = pygame.image.load(tile_data["multitile_image_path"]).convert_alpha()  # , (commons.BLOCK_SIZE * tile_data["multitile_dimensions"][0], commons.BLOCK_SIZE * tile_data["multitile_dimensions"][1])
			if override_average_color:
				tile_data["average_color"] = pygame.transform.average_color(tile_data["multitile_image"])

		if TileTag.CYCLABLE in tile_data["tags"]:
			tile_data["cycle_facing_left_tile_offset"] = int_tuple_str_to_int_tuple(tile_data["cycle_facing_left_tile_offset"])
			tile_data["cycle_facing_right_tile_offset"] = int_tuple_str_to_int_tuple(tile_data["cycle_facing_right_tile_offset"])

		if TileTag.DAMAGING in tile_data["tags"]:
			tile_data["tile_damage"] = int(tile_data["tile_damage"])


def create_tile_id_str_hash_table():
	global tile_id_str_hash_table
	for tile_index in range(len(json_tile_data)):
		tile_id_str_hash_table[json_tile_data[tile_index]["id_str"]] = tile_index


def create_tile_light_reduction_lookup():
	global tile_id_light_reduction_lookup
	tile_id_light_reduction_lookup.clear()
	for tile_index in range(len(json_tile_data)):
		tile_id_light_reduction_lookup.append(json_tile_data[tile_index]["light_reduction"])


def create_tile_light_emission_lookup():
	global tile_id_light_emission_lookup
	tile_id_light_emission_lookup.clear()
	for tile_index in range(len(json_tile_data)):
		tile_id_light_emission_lookup.append(json_tile_data[tile_index]["light_emission"])


def get_tile_by_id(tile_id):
	if tile_id < len(json_tile_data):
		return json_tile_data[tile_id]


def get_tile_id_by_id_str(tile_id_str):
	return tile_id_str_hash_table[tile_id_str]


def get_tile_by_id_str(tile_id_str):
	return get_tile_by_id(get_tile_id_by_id_str(tile_id_str))


def get_current_tile_id_str_lookup():
	tile_id_str_lookup = []
	for tile in json_tile_data:
		tile_id_str_lookup.append(tile["id_str"])
	return tile_id_str_lookup


def parse_wall_data():
	global json_wall_data
	json_read_file = open("assets/game_data/wall_data.json", "r")
	json_wall_data = json.loads(json_read_file.read())["walls"]["wall"]
	json_read_file.close()

	json_wall_data = sorted(json_wall_data, key=lambda x: int(x["id"]))

	for wall_data in json_wall_data:
		wall_data["id"] = int(wall_data["id"])
		wall_data["mask_type"] = get_tile_mask_type_from_str(wall_data["mask_type"])
		wall_data["mask_merge_id_strs"] = wall_data["mask_merge_id_strs"].split(",")

		if wall_data["average_color"] == "auto":
			wall_data["average_color"] = (255, 0, 255)
			override_average_color = True
		else:
			val_array = wall_data["average_color"].split(",")
			wall_data["average_color"] = (int(val_array[0]), int(val_array[1]), int(val_array[2]))
			override_average_color = False

		try:
			wall_data["image"] = pygame.transform.scale(pygame.image.load(wall_data["image_path"]).convert_alpha(), (commons.BLOCK_SIZE, commons.BLOCK_SIZE))
			wall_data["image"].set_colorkey((255, 0, 255))
			if override_average_color:
				wall_data["average_color"] = pygame.transform.average_color(wall_data["image"])

		except FileNotFoundError:
			wall_data["image"] = None
		except pygame.error:
			wall_data["image"] = None


def create_wall_id_str_hash_table():
	global wall_id_str_hash_table
	for wall_index in range(len(json_wall_data)):
		wall_id_str_hash_table[json_wall_data[wall_index]["id_str"]] = wall_index


def get_wall_by_id(wall_id):
	if wall_id < len(json_wall_data):
		return json_wall_data[wall_id]


def get_wall_id_by_id_str(wall_id_str):
	return wall_id_str_hash_table[wall_id_str]


def get_wall_by_id_str(wall_id_str):
	return get_wall_by_id(get_wall_id_by_id_str(wall_id_str))


def get_current_wall_id_str_lookup():
	wall_id_str_lookup = []
	for wall in json_wall_data:
		wall_id_str_lookup.append(wall["id_str"])
	return wall_id_str_lookup


def parse_sound_data():
	global json_sound_data
	json_read_file = open("assets/game_data/sound_data.json", "r")
	json_sound_data = json.loads(json_read_file.read())["sounds"]["sound"]
	json_read_file.close()

	json_sound_data = sorted(json_sound_data, key=lambda x: int(x["id"]))

	for sound_data in json_sound_data:
		sound_data["id"] = int(sound_data["id"])
		sound_data["volume"] = float(sound_data["volume"])
		sound_data["variation_paths"] = sound_data["variation_paths"].split(",")
		sound_data["variations"] = []
		for sound_variation in sound_data["variation_paths"]:
			try:
				sound = pygame.mixer.Sound(sound_variation)
				sound.set_volume(sound_data["volume"])
				sound_data["variations"].append(sound)
			except FileNotFoundError:
				pass
			except pygame.error:
				pass


def create_sound_id_str_hash_table():
	global sound_id_str_hash_table
	for sound_index in range(len(json_sound_data)):
		sound_id_str_hash_table[json_sound_data[sound_index]["id_str"]] = sound_index


def get_sound_by_id(sound_id):
	if sound_id < len(json_sound_data):
		return json_sound_data[sound_id]


def get_sound_id_by_id_str(sound_id_str):
	return sound_id_str_hash_table[sound_id_str]


def get_sound_by_id_str(sound_id_str):
	return get_sound_by_id(get_sound_id_by_id_str(sound_id_str))


def change_music_volume(amount):
	global music_volume_multiplier
	volume_before = music_volume_multiplier
	music_volume_multiplier += amount
	music_volume_multiplier = max(min(music_volume_multiplier, 1), 0)
	if music_volume_multiplier != volume_before:
		pygame.mixer.music.set_volume(music_volume_multiplier)
		# entity_manager.add_message("Music volume set to " + str(round(music_volume_multiplier, 2)),  (255, 223, 10), life=2, outline_color=(80, 70, 3))


def change_sound_volume(amount):
	global sound_volume_multiplier
	
	if sound_volume_multiplier + amount >= 0 and sound_volume_multiplier + amount <= 2:
		sound_volume_multiplier += amount


def play_sound(sound_id_str):
	global sound_volume_multiplier

	if commons.SOUND:
		sound_data = get_sound_by_id_str(sound_id_str)
		if (sound_data != None):
			sound_index = random.randint(0, len(sound_data["variations"]) - 1)
			sound = sound_data["variations"][sound_index]
			sound.set_volume(sound_data["volume"] * sound_volume_multiplier)
			sound.play()


def play_tile_hit_sfx(tile_id):
	if commons.SOUND:
		tile_data = get_tile_by_id(tile_id)
		if (tile_data != None):
			play_sound(tile_data["hit_sound"])


def play_tile_place_sfx(tile_id):
	if commons.SOUND:
		tile_data = get_tile_by_id(tile_id)
		if (tile_data != None):
			play_sound(tile_data["place_sound"])


def play_wall_hit_sfx(wall_id):
	if commons.SOUND:
		wall_data = get_wall_by_id(wall_id)
		if(wall_data != None):
			play_sound(wall_data["hit_sound"])


def play_wall_place_sfx(wall_id):
	if commons.SOUND:
		wall_data = get_wall_by_id(wall_id)
		if (wall_data != None):
			play_sound(wall_data["place_sound"])


class StructureConnectionOrientation(Enum):
	UP = 0
	RIGHT = 1
	DOWN = 2
	LEFT = 3


def parse_structure_data():
	global json_structure_data
	json_read_file = open("assets/game_data/structure_data.json", "r")
	json_structure_data = json.loads(json_read_file.read())["structures"]["structure"]
	json_read_file.close()

	json_structure_data = sorted(json_structure_data, key=lambda x: int(x["id"]))

	for structure_data in json_structure_data:
		structure_data["id"] = int(structure_data["id"])
		structure_data["spawn_weight"] = int(structure_data["spawn_weight"])
		structure_data["width"] = int(structure_data["width"])
		structure_data["height"] = int(structure_data["height"])

		structure_data["connections"] = []
		structure_data["chest_loot"] = []

		tile_data = []
		columns = structure_data["tile_data"].split("|")
		for column in columns:
			tile_data.append([])
			char_index = 0
			x_pos = len(tile_data) - 1
			while char_index < len(column):
				tile_data[-1].append([None, None, None])
				if column[char_index] != "-":
					y_pos = len(tile_data[-1]) - 1
					end_index = find_next_char_in_string(column, "]", char_index)
					if end_index != -1:
						tile_data_string = column[char_index + 1:end_index]
						char_index = end_index
						data_strs = tile_data_string.split(";")
						for data_str in data_strs:
							data_str_split = data_str.split(":")
							data_str_id = int(data_str_split[0])
							if data_str_id == 0:
								tile_data[-1][-1][0] = data_str_split[1]
							elif data_str_id == 2:
								structure_data["chest_loot"].append([(x_pos, y_pos), data_str_split[1]])
							elif data_str_id == 3:
								tile_data[-1][-1][1] = data_str_split[1]
							elif data_str_id == 1:
								split_str = data_str_split[1].split(",")
								tile_data[-1][-1][2] = int(split_str[0]), int(split_str[1])
							elif data_str_id == 4:
								connection_data = data_str_split[1].split(",")
								structure_data["connections"].append([(x_pos, y_pos), connection_data[0],  get_structure_connection_orientation_from_str(connection_data[1])])
				char_index += 1

		structure_data["tile_data"] = tile_data


def create_structure_id_str_hash_table():
	global structure_id_str_hash_table
	for structure_index in range(len(json_structure_data)):
		structure_id_str_hash_table[json_structure_data[structure_index]["id_str"]] = structure_index


def get_structure_by_id(structure_id):
	if structure_id < len(json_structure_data):
		return json_structure_data[structure_id]


def get_structure_id_by_id_str(structure_id_str):
	return structure_id_str_hash_table[structure_id_str]


def get_structure_by_id_str(structure_id_str):
	return get_structure_by_id(get_structure_id_by_id_str(structure_id_str))


def find_structures_for_connection(connection_type, connection_orientation):
	out_connections = []
	opposite_connection_orientation = get_opposite_structure_connection_orientation(connection_orientation)
	for structure in json_structure_data:
		for connection in structure["connections"]:
			if connection[1] == connection_type and connection[2] == opposite_connection_orientation:
				out_connections.append([structure["id_str"], connection[0]])

	return out_connections


def get_opposite_structure_connection_orientation(structure_connection_orientation):
	if structure_connection_orientation == StructureConnectionOrientation.DOWN:
		return StructureConnectionOrientation.UP
	elif structure_connection_orientation == StructureConnectionOrientation.LEFT:
		return StructureConnectionOrientation.RIGHT
	elif structure_connection_orientation == StructureConnectionOrientation.UP:
		return StructureConnectionOrientation.DOWN
	elif structure_connection_orientation == StructureConnectionOrientation.RIGHT:
		return StructureConnectionOrientation.LEFT


def get_structure_connection_orientation_from_str(structure_connection_orientation_str):
	if structure_connection_orientation_str == "Up":
		return StructureConnectionOrientation.UP
	elif structure_connection_orientation_str == "Right":
		return StructureConnectionOrientation.RIGHT
	elif structure_connection_orientation_str == "Down":
		return StructureConnectionOrientation.DOWN
	elif structure_connection_orientation_str == "Left":
		return StructureConnectionOrientation.LEFT


def parse_loot_data():
	global json_loot_data
	json_read_file = open("assets/game_data/loot_data.json", "r")
	json_loot_data = json.loads(json_read_file.read())["loot"]
	json_read_file.close()

	json_loot_data = sorted(json_loot_data, key=lambda x: int(x["id"]))

	for loot_data in json_loot_data:
		loot_data["id"] = int(loot_data["id"])
		loot_data["item_spawn_count_range"] = int_tuple_str_to_int_tuple(loot_data["item_spawn_count_range"])
		possible_item_strs = loot_data["item_list_data"]
		item_list_data = []
		for possible_item_properties_str in possible_item_strs:

			possible_item_id_str = possible_item_properties_str["item_id_str"]
			possible_item_spawn_weight = possible_item_properties_str["item_spawn_weight"]
			possible_item_spawn_depth_range = tuple(possible_item_properties_str["item_spawn_depth_range"])
			possible_item_stack_count_range = tuple(possible_item_properties_str["item_stack_count_range"])
			possible_item_slot_priority = possible_item_properties_str["item_slot_priority"]
			once_per_instance = possible_item_properties_str["once_per_instance"]

			item_list_data.append([possible_item_id_str, possible_item_spawn_weight, possible_item_spawn_depth_range, possible_item_stack_count_range, possible_item_slot_priority, once_per_instance])
		print(item_list_data)

		loot_data["item_list_data"] = item_list_data

		loot_data["coin_spawn_range"] = int_tuple_str_to_int_tuple(loot_data["coin_spawn_range"])


def create_loot_id_str_hash_table():
	global loot_id_str_hash_table
	for loot_index in range(len(json_loot_data)):
		loot_id_str_hash_table[json_loot_data[loot_index]["id_str"]] = loot_index


def get_loot_by_id(loot_id):
	if loot_id < len(json_loot_data):
		return json_loot_data[loot_id]


def get_loot_id_by_id_str(loot_id_str):
	return loot_id_str_hash_table[loot_id_str]


def get_loot_by_id_str(loot_id_str):
	return get_loot_by_id(get_loot_id_by_id_str(loot_id_str))


def parse_entity_data():
    global json_entity_data
    json_read_file = open("assets/game_data/entity_data.json")
    json_entity_data = json.loads(json_read_file.read())["entities"]["entity"]
    json_read_file.close()
    
    json_entity_data = sorted(json_entity_data, key=lambda x: x["id"])

def create_entity_id_str_hash_table():
    global entity_id_str_hash_table
    for entity_index in range(len(json_entity_data)):
        entity_id_str_hash_table[json_entity_data[entity_index]["id_str"]] = entity_index

parse_item_data()
create_item_id_str_hash_table()

parse_tile_data()
create_tile_id_str_hash_table()
create_tile_light_reduction_lookup()
create_tile_light_emission_lookup()

parse_wall_data()
create_wall_id_str_hash_table()

parse_sound_data()
create_sound_id_str_hash_table()

parse_structure_data()
create_structure_id_str_hash_table()

parse_loot_data()
create_loot_id_str_hash_table()

parse_entity_data()
create_entity_id_str_hash_table()

air_tile_id = get_tile_id_by_id_str("tile.none")
grass_tile_id = get_tile_id_by_id_str("tile.grass")

air_wall_id = get_wall_id_by_id_str("wall.none")
