# game_data.py

import pygame
from enum import Enum
import commons
import random
from typing import Any, TypedDict, NotRequired

class PrefixData(TypedDict):
	name: str
	damage: float
	speed: float
	crit_chance: float
	size: NotRequired[float]
	velocity: NotRequired[float]
	mana_cost: NotRequired[float]
	knockback: float
	tier: int

def make_item_tag_list(item_tags_str: list[str]):
	enum_list: list[commons.ItemTag] = []
	for string in item_tags_str:
		for tag in commons.ItemTag:
			if tag.name == string:
				enum_list.append(tag)
				break
	return enum_list

def make_item_prefix_list(item_prefixes_str: list[str]):
	enum_list: list[commons.ItemPrefixGroup] = []
	for string in item_prefixes_str:
		for prefix in commons.ItemPrefixGroup:
			if prefix.name == string:
				enum_list.append(prefix)
				break
	return enum_list


def make_tile_tag_list(tile_tags_str: list[str]):
	enum_list: list[commons.TileTag] = []
	for string in tile_tags_str:
		for tag in commons.TileTag:
			if tag.name == string:
				enum_list.append(tag)
				break
	return enum_list


def get_tile_strength_type_from_str(strength_type_string: str):
	for types in commons.TileStrengthType:
		if types.name == strength_type_string:
			return types


def get_tile_mask_type_from_str(mask_type_string: str):
	for masks in commons.TileMaskType:
		if masks.name == mask_type_string:
			return masks


def find_next_char_in_string(string: str, char: str, start_index: int):
	for char_index in range(start_index, len(string)):
		if string[char_index] == char:
			return char_index
	return -1


# Biome Tile Information
# [[surface tile,base tile, alt tile],[wall tile, alt wall tile]]
biome_tile_vals: list[list[list[str]]] = [
	[["tile.grass", "tile.dirt", "tile.stone"], ["wall.dirt", "wall.stone"]],
	[["tile.snow", "tile.snow", "tile.ice"], ["wall.snow", "wall.ice"]],
	[["tile.sand", "tile.sand", "tile.sandstone"], ["wall.hardened_sand", "wall.sandstone"]]
]

platform_blocks: list[int] = [257]

json_item_data: list[commons.PlacableTileItemData | commons.ImplacableTileItemData | commons.MaterialItemData | commons.WallItemData | commons.PickaxeItemData | commons.HammerItemData | commons.AxeItemData | commons.SwordItemData | commons.RangedItemData | commons.AmmunitionItemData | commons.GrapplingHookItemData | commons.MagicalWeaponItemData] = []
item_id_str_hash_table: dict[str, int] = {}

ammo_type_item_lists: dict[str, list[int]] = {}

json_tile_data: list[commons.TileData] = []
tile_id_str_hash_table: dict[str, int] = {}
tile_id_light_reduction_lookup: list[int] = []
tile_id_light_emission_lookup: list[int] = []

json_wall_data: list[commons.WallData] = []
wall_id_str_hash_table: dict[str, int] = {}

json_sound_data: list[commons.SoundData] = []
sound_id_str_hash_table: dict[str, int] = {}

json_structure_data: list[commons.StructureData] = []
structure_id_str_hash_table: dict[str, int] = {}

json_loot_data: list[commons.LootData] = []
loot_id_str_hash_table: dict[str, int] = {}

json_entity_data: list[commons.EntityData] = []
entity_id_str_hash_table: dict[str, int] = {}

sound_volume_multiplier: float = commons.CONFIG_SOUND_VOLUME
music_volume_multiplier: float = commons.CONFIG_MUSIC_VOLUME


# Item Prefix Information
prefix_data: dict[commons.ItemPrefixGroup, list[PrefixData]] = {
	commons.ItemPrefixGroup.UNIVERSAL: [
			{"name": "Keen", "damage": 0, "speed": 0, "crit_chance": 0, "knockback": 0, "tier": 1},
			{"name": "Superior", "damage": 0.1, "speed": 0, "crit_chance": 0.03, "knockback": 0.1, "tier": 2},
			{"name": "Forceful", "damage": 0, "speed": 0, "crit_chance": 0, "knockback": 0.15, "tier": 1},
			{"name": "Broken", "damage": -0.3, "speed": 0, "crit_chance": 0, "knockback": -0.2, "tier": -2},
			{"name": "Damaged", "damage": -0.15, "speed": 0, "crit_chance": 0, "knockback": 0, "tier": -1},
			{"name": "Shoddy", "damage": -0.1, "speed": 0, "crit_chance": 0, "knockback": -0.15, "tier": -2},
			{"name": "Hurtful", "damage": 0.1, "speed": 0, "crit_chance": 0, "knockback": 0, "tier": 1},
			{"name": "Strong", "damage": 0, "speed": 0, "crit_chance": 0, "knockback": 0.15, "tier": 1},
			{"name": "Unpleasant", "damage": 0.05, "speed": 0, "crit_chance": 0, "knockback": 0.15, "tier": 2},
			{"name": "Weak", "damage": 0, "speed": 0, "crit_chance": 0, "knockback": -0.2, "tier": -1},
			{"name": "Ruthless", "damage": 0.18, "speed": 0, "crit_chance": 0, "knockback": -0.1, "tier": 1},
			{"name": "Godly", "damage": 0.15, "speed": 0, "crit_chance": 0.05, "knockback": 0.15, "tier": 2},
			{"name": "Demonic", "damage": 0.15, "speed": 0, "crit_chance": 0.05, "knockback": 0, "tier": 2},
			{"name": "Zealous","damage": 0,"speed": 0, "crit_chance": 0.05, "knockback": 0, "tier": 1}
		],
	commons.ItemPrefixGroup.COMMON: [
			{"name": "Quick", "damage": 0, "speed": 0.1, "crit_chance": 0, "knockback": 0, "tier": 1},
			{"name": "Deadly","damage": 0.1, "speed": 0.1, "crit_chance": 0, "knockback": 0, "tier": 2},
			{"name": "Agile", "damage": 0, "speed": 0.1, "crit_chance": 0.03, "knockback": 0, "tier": 1},
			{"name": "Nimble", "damage": 0, "speed": 0.05, "crit_chance": 0, "knockback": 0, "tier": 1},
			{"name": "Murderous", "damage": -0.07, "speed": 0.06, "crit_chance": 0.03, "knockback": 0, "tier": 2},
			{"name": "Slow", "damage": 0, "speed": -0.15, "crit_chance": 0, "knockback": 0, "tier": -1},
			{"name": "Sluggish", "damage": 0,  "speed": -0.2, "crit_chance": 0, "knockback": 0, "tier": -2},
			{"name": "Lazy", "damage": 0, "speed": -0.08, "crit_chance": 0, "knockback": 0, "tier": -1},
			{"name": "Annoying", "damage": -0.2, "speed": -0.15, "crit_chance": 0, "knockback": 0, "tier": -2},
			{"name": "Nasty", "damage": 0.05, "speed": 0.1, "crit_chance": 0.02, "knockback": -0.1, "tier": 1},
		],
	commons.ItemPrefixGroup.LONGSWORD: [
			{"name": "Large", "damage": 0, "speed": 0, "crit_chance": 0, "size": 0.12, "knockback": 0, "tier": 1},
			{"name": "Massive", "damage": 0, "speed": 0, "crit_chance": 0, "size": 0.18, "knockback": 0, "tier": 1},
			{"name": "Dangerous", "damage": 0.05, "speed": 0, "crit_chance": 0.02, "size": 0.05, "knockback": 0, "tier": 1},
			{"name": "Savage", "damage": 0.1, "speed": 0, "crit_chance": 0, "size": 0.1, "knockback": 0.1, "tier": 2},
			{"name": "Sharp", "damage": 0.15, "speed": 0, "crit_chance": 0, "size": 0, "knockback": 0, "tier": 1},
			{"name": "Pointy", "damage": 0.1, "speed": 0, "crit_chance": 0, "size": 0, "knockback": 0, "tier": 1},
			{"name": "Tiny", "damage": 0, "speed": 0, "crit_chance": 0, "size": -0.18, "knockback": 0, "tier": -1},
			{"name": "Terrible", "damage": -0.15, "speed": 0, "crit_chance": 0, "size": -0.13, "knockback": -0.15, "tier": -2},
			{"name": "Small", "damage": 0,	 "speed": 0, "crit_chance": 0, "size": -0.1, "knockback": 0, "tier": -1},
			{"name": "Dull", "damage": -0.15, "speed": 0, "crit_chance": 0, "size": 0, "knockback": 0, "tier": -1},
			{"name": "Unhappy", "damage": 0, "speed": -0.1, "crit_chance": 0, "size": -0.1, "knockback": -0.1, "tier": -2},
			{"name": "Bulky", "damage": 0.05, "speed": -0.15, "crit_chance": 0, "size": 0.1, "knockback": 0.1, "tier": 1},
			{"name": "Shameful", "damage": -0.1, "speed": 0, "crit_chance": 0, "size": 0.1, "knockback": -0.2, "tier": -2},
			{"name": "Heavy", "damage": 0,  "speed": -0.1, "crit_chance": 0, "size": 0, "knockback": 0.15, "tier": 0},
			{"name": "Light", "damage": 0,  "speed": 0.15, "crit_chance": 0, "size": 0, "knockback": -0.1, "tier": 0},
			{"name": "Legendary", "damage": 0.15, "speed": 0.1, "crit_chance": 0.05, "size": 0.1, "knockback": 0.15, "tier": 2}
		],
		commons.ItemPrefixGroup.SHORTSWORD: [
			{"name": "Large", "damage": 0, "speed": 0, "crit_chance": 0, "size": 0.12, "knockback": 0, "tier": 1},
			{"name": "Massive", "damage": 0, "speed": 0, "crit_chance": 0, "size": 0.18, "knockback": 0, "tier": 1},
			{"name": "Dangerous", "damage": 0.05, "speed": 0, "crit_chance": 0.02, "size": 0.05, "knockback": 0, "tier": 1},
			{"name": "Savage", "damage": 0.1, "speed": 0, "crit_chance": 0, "size": 0.1, "knockback": 0.1, "tier": 2},
			{"name": "Sharp", "damage": 0.15, "speed": 0, "crit_chance": 0,	"size": 0, "knockback": 0, "tier": 1},
			{"name": "Pointy", "damage": 0.1, "speed": 0, "crit_chance": 0, "size": 0, "knockback": 0, "tier": 1},
			{"name": "Tiny", "damage": 0, "speed": 0, "crit_chance": 0, "size": -0.18, "knockback": 0, "tier": -1},
			{"name": "Terrible", "damage": -0.15, "speed": 0, "crit_chance": 0, "size": -0.13, "knockback": -0.15, "tier": -2},
			{"name": "Small", "damage": 0, "speed": 0, "crit_chance": 0, "size": -0.1, "knockback": 0, "tier": -1},
			{"name": "Dull", "damage": -0.15, "speed": 0, "crit_chance": 0, "size": 0, "knockback": 0, "tier": -1},
			{"name": "Unhappy", "damage": 0, "speed": -0.1, "crit_chance": 0, "size": -0.1, "knockback": -0.1, "tier": -2},
			{"name": "Bulky", "damage": 0.05, "speed": -0.15, "crit_chance": 0, "size": 0.1, "knockback": 0.1, "tier": 1},
			{"name": "Shameful", "damage": -0.1, "speed": 0, "crit_chance": 0, "size": 0.1, "knockback": -0.2, "tier": -2},
			{"name": "Heavy", "damage": 0, "speed": -0.1, "crit_chance": 0, "size": 0, "knockback": 0.15, "tier": 0},
			{"name": "Light", "damage": 0, "speed": 0.15, "crit_chance": 0, "size": 0, "knockback": -0.1, "tier": 0},
			{"name": "Legendary", "damage": 0.15, "speed": 0.1, "crit_chance": 0.05, "size": 0.1, "knockback": 0.15, "tier": 2},
		],
		commons.ItemPrefixGroup.RANGED: [
			{"name": "Sighted", "damage": 0.1, "speed": 0, "crit_chance": 0.03, "velocity": 0, "knockback": 0, "tier": 1},
			{"name": "Rapid", "damage": 0, "speed": 0.15, "crit_chance": 0, "velocity": 0.1, "knockback": 0, "tier": 2},
			{"name": "Hasty", "damage": 0, "speed": 0.1, "crit_chance": 0,	"velocity": 0.15, "knockback": 0, "tier": 2},
			{"name": "Intimidating", "damage": 0, "speed": 0, "crit_chance": 0,	"velocity": 0.05, "knockback": 0.15, "tier": 2},
			{"name": "Deadly", "damage": 0.1, "speed": 0.05, "crit_chance": 0.02, "velocity": 0.05, "knockback": 0.05, "tier": 2},
			{"name": "Staunch", "damage": 0.1, "speed": 0, "crit_chance": 0, "velocity": 0,	 "knockback": 0.15, "tier": 2},
			{"name": "Awful", "damage": -0.15, "speed": 0, "crit_chance": 0, "velocity": -0.1, "knockback": -0.1, "tier": -2},
			{"name": "Lethargic", "damage": 0, "speed": 0.15, "crit_chance": 0, "velocity": -0.1, "knockback": 0, "tier": -2},
			{"name": "Awkward", "damage": 0, "speed": -0.1,	"crit_chance": 0, "velocity": 0, "knockback": -0.2, "tier": -2},
			{"name": "Powerful", "damage": 0.15, "speed": -0.1, "crit_chance": 0.01, "velocity": 0, "knockback": 0, "tier": 1},
			{"name": "Frenzying", "damage": -0.15, "speed": 0.15, "crit_chance": 0, "velocity": 0, "knockback": 0, "tier": 0},
			{"name": "Unreal", "damage": 0.15, "speed": 0.1, "crit_chance": 0.05, "velocity": 0.1, "knockback": 0.15, "tier": 2},
		],
		commons.ItemPrefixGroup.MAGICAL: [
			{"name": "Mystic", "damage": 0.1, "speed": 0, "crit_chance": 0, "mana_cost": -0.15, "knockback": 0, "tier": 2},
			{"name": "Adept", "damage": 0, "speed": 0, "crit_chance": 0, "mana_cost": -0.15, "knockback": 0, "tier": 1},
			{"name": "Masterful", "damage": 0.15, "speed": 0, "crit_chance": 0, "mana_cost": -0.2, "knockback": 0.05, "tier": 2},
			{"name": "Inept", "damage": 0, "speed": 0, "crit_chance": 0, "mana_cost": 0.1, "knockback": 0, "tier": -1},
			{"name": "Ignorant", "damage": -0.1, "speed": 0, "crit_chance": 0, "mana_cost": 0.2, "knockback": 0, "tier": -2},
			{"name": "Deranged", "damage": -0.1, "speed": 0, "crit_chance": 0, "mana_cost": 0, "knockback": -0.1, "tier": -1},
			{"name": "Intense", "damage": 0.1, "speed": 0, "crit_chance": 0, "mana_cost": 0.15, "knockback": 0, "tier": -1},
			{"name": "Taboo", "damage": 0, "speed": 0.1, "crit_chance": 0, "mana_cost": 0.1, "knockback": 0.1, "tier": 1},
			{"name": "Celestial", "damage": 0.1, "speed": -0.1, "crit_chance": 0, "mana_cost": -0.1, "knockback": 0.1, "tier": 1},
			{"name": "Furious", "damage": 0.15,	"speed": 0, "crit_chance": 0, "mana_cost": 0.2, "knockback": 0.15, "tier": 1},
			{"name": "Manic", "damage": -0.1, "speed": 0.1, "crit_chance": 0, "mana_cost": -0.1, "knockback": 0, "tier": 1},
			{"name": "Mythical", "damage": 0.15, "speed": 0.1, "crit_chance": 0.05, "mana_cost": -0.1, "knockback": 0.15, "tier": 2}
		]
}

DEATH_LINES = {
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

TIPS = [
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

EXIT_MESSAGES = [
	"Are you sure you want to exit?",
	"Leaving so soon?",
	"You'll come back someday right?",
	"So this is goodbye?",
	"If you quit, I'll look for you, I will find you...",
	"Running won't help, they'll still get you...",
	"You're just gonna leave your slime friends?",
	"When you quit, you're killing slimes...",
	"You're just gonna play for two seconds then leave?",
]


def find_prefix_data_by_name(prefix_name):
	for prefix_dat in prefix_data[commons.ItemPrefixGroup.UNIVERSAL]:
		if prefix_dat["name"] == prefix_name:
			return [commons.ItemPrefixGroup.UNIVERSAL, prefix_dat]
	for prefix_dat in prefix_data[commons.ItemPrefixGroup.COMMON]:
		if prefix_dat["name"] == prefix_name:
			return [commons.ItemPrefixGroup.COMMON, prefix_dat]
	for prefix_dat in prefix_data[commons.ItemPrefixGroup.LONGSWORD]:
		if prefix_dat["name"] == prefix_name:
			return [commons.ItemPrefixGroup.LONGSWORD, prefix_dat]
	for prefix_dat in prefix_data[commons.ItemPrefixGroup.RANGED]:
		if prefix_dat["name"] == prefix_name:
			return [commons.ItemPrefixGroup.RANGED, prefix_dat]
	for prefix_dat in prefix_data[commons.ItemPrefixGroup.MAGICAL]:
		if prefix_dat["name"] == prefix_name:
			return [commons.ItemPrefixGroup.MAGICAL, prefix_dat]
	for prefix_dat in prefix_data[commons.ItemPrefixGroup.SHORTSWORD]:
		if prefix_dat["name"] == prefix_name:
			return [commons.ItemPrefixGroup.SHORTSWORD, prefix_dat]
	return None


def parse_item_data():
	global json_item_data
	json_item_data = commons.ITEM_DATA
	json_item_data = sorted(json_item_data, key=lambda x: int(x["id"]))

	# TODO So what's happening is that typeddict is only allowing specific keys and when I try to add keys not in typeddict, it is unable to do that. :/ I guess mess around with NotRequired or just delete and rework the extra keys.
	for item_data in json_item_data:
		try:
			loaded_surf = pygame.image.load(item_data["image_path"]).convert_alpha()
			if max(loaded_surf.get_width(), loaded_surf.get_height()) > 32:
				loaded_surf = pygame.transform.scale(loaded_surf, (loaded_surf.get_width() * (32 / max(loaded_surf.get_width(), loaded_surf.get_height())), loaded_surf.get_height() * (32 / max(loaded_surf.get_width(), loaded_surf.get_height()))))
			# loaded_surf = pygame.transform.scale(loaded_surf, (loaded_surf.get_width(), loaded_surf.get_height()))
			item_data["image"] = loaded_surf
			item_data["item_slot_offset_x"] = int(24 - item_data["image"].get_width() * 0.5)
			item_data["item_slot_offset_y"] = int(24 - item_data["image"].get_height() * 0.5)
		except FileNotFoundError:
			item_data["image"] = None

		if commons.ItemTag.WEAPON in item_data["tags"]:
			try:
				loaded_surf = pygame.image.load(item_data["world_override_image_path"]).convert_alpha()
				item_data["world_override_image"] = pygame.Surface((max(loaded_surf.get_width(), loaded_surf.get_height()), max(loaded_surf.get_width(), loaded_surf.get_height())))
			except FileNotFoundError:
				item_data["world_override_image"] = None

			item_data["prefixes"] = make_item_prefix_list(item_data["prefixes"])

		if commons.ItemTag.AMMO in item_data["tags"]:
			try:
				ammo_type_item_lists[item_data["ammo_type"]].append(item_data["id"])
			except KeyError:
				ammo_type_item_lists[item_data["ammo_type"]] = [item_data["id"]]

		if commons.ItemTag.GRAPPLE in item_data["tags"]:
			try:
				loaded_surf = pygame.image.load(item_data["grapple_chain_image_path"]).convert_alpha()
				item_data["grapple_chain_image"] = pygame.Surface((loaded_surf.get_width(), loaded_surf.get_height()))
			except FileNotFoundError:
				item_data["grapple_chain_image"] = None

			try:
				loaded_surf = pygame.image.load(item_data["grapple_claw_image_path"]).convert_alpha()
				item_data["grapple_claw_image"] = pygame.Surface((loaded_surf.get_width(), loaded_surf.get_height()))
				item_data["grapple_claw_image"].set_colorkey((255, 0, 255))
			except FileNotFoundError:
				item_data["grapple_claw_image"] = None


def get_item_by_id(item_id) -> Any:
	if item_id < len(json_item_data):
		return json_item_data[item_id]
	else:
		raise ValueError("Inserted item ID greater than maximum item ID length.")


def get_item_id_by_id_str(item_id_str: str) -> int:
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
		if commons.ItemTag.AMMO in item_data["tags"]:
			if item_data["ammo_type"] == ammo_type:
				ammo_item_ids.append(int(item_data["id"]))


def parse_tile_data():
	global json_tile_data

	json_tile_data = commons.TILE_DATA
	json_tile_data = sorted(json_tile_data, key=lambda x: int(x["id"]))

	for tile_data in json_tile_data:
		tile_data["strength_type"] = get_tile_strength_type_from_str(tile_data["strength_type"])
		tile_data["mask_type"] = get_tile_mask_type_from_str(tile_data["mask_type"])
		tile_data["light_reduction"] = int(tile_data["light_reduction"])
		tile_data["light_emission"] = int(tile_data["light_emission"])

		tile_data["tags"] = make_tile_tag_list(tile_data["tags"])
		try:
			tile_data["image"] = pygame.image.load(tile_data["image_path"]).convert_alpha()  # , (commons.BLOCK_SIZE, commons.BLOCK_SIZE)
			tile_data["average_color"] = pygame.transform.average_color(tile_data["image"])
		except FileNotFoundError:
			tile_data["image"] = None
		except pygame.error:
			tile_data["image"] = None

		if commons.TileTag.MULTITILE in tile_data["tags"]:
			tile_data["multitile_image"] = pygame.image.load(tile_data["multitile_image_path"]).convert_alpha()  # , (commons.BLOCK_SIZE * tile_data["multitile_dimensions"][0], commons.BLOCK_SIZE * tile_data["multitile_dimensions"][1])
			tile_data["average_color"] = pygame.transform.average_color(tile_data["multitile_image"])

		if commons.TileTag.DAMAGING in tile_data["tags"]:
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


def get_tile_by_id(tile_id: int):
	if tile_id < len(json_tile_data):
		return json_tile_data[tile_id]
	else:
		raise ValueError("Inserted tile ID greater than maximum tile ID length.")


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

	json_wall_data = commons.WALL_DATA
	json_wall_data = sorted(json_wall_data, key=lambda x: int(x["id"]))

	for wall_data in json_wall_data:
		wall_data["mask_type"] = get_tile_mask_type_from_str(wall_data["mask_type"])
		try:
			wall_data["image"] = pygame.transform.scale(pygame.image.load(wall_data["image_path"]).convert_alpha(), (commons.BLOCK_SIZE, commons.BLOCK_SIZE))
			wall_data["image"].set_colorkey((255, 0, 255))
			wall_data["average_color"] = pygame.transform.average_color(wall_data["image"])
		except FileNotFoundError:
			wall_data["image"] = None


def create_wall_id_str_hash_table():
	global wall_id_str_hash_table
	for wall_index in range(len(json_wall_data)):
		wall_id_str_hash_table[json_wall_data[wall_index]["id_str"]] = wall_index


def get_wall_by_id(wall_id):
	if wall_id < len(json_wall_data):
		return json_wall_data[wall_id]
	else:
		raise ValueError("Inserted wall ID greater than maximum wall ID length.")


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

	json_sound_data = commons.SOUND_DATA
	json_sound_data = sorted(json_sound_data, key=lambda x: int(x["id"]))

	for sound_data in json_sound_data:
		sound_data["id"] = int(sound_data["id"])
		sound_data["volume"] = float(sound_data["volume"])
		sound_data["variations"] = []
		for sound_variation in sound_data["variation_paths"]:
			try:
				sound = pygame.mixer.Sound(sound_variation)
				sound.set_volume(sound_data["volume"])
				sound_data["variations"].append(sound)
			except FileNotFoundError:
				pass


def create_sound_id_str_hash_table():
	global sound_id_str_hash_table
	for sound_index in range(len(json_sound_data)):
		sound_id_str_hash_table[json_sound_data[sound_index]["id_str"]] = sound_index


def get_sound_by_id(sound_id):
	if sound_id < len(json_sound_data):
		return json_sound_data[sound_id]
	else:
		raise ValueError("Inserted sound ID greater than maximum sound ID length.")


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


def play_sound(sound_id_str: str) -> None:
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

	json_structure_data = commons.STRUCTURE_DATA
	json_structure_data = sorted(json_structure_data, key=lambda x: int(x["id"]))

	for structure_data in json_structure_data:
		structure_data["id"] = int(structure_data["id"])
		structure_data["spawn_weight"] = int(structure_data["spawn_weight"])
		structure_data["width"] = int(structure_data["width"])
		structure_data["height"] = int(structure_data["height"])

		structure_data["connections"] = []
		structure_data["chest_loot"] = []

		tile_data = []
		for column in structure_data["tile_data"]:
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
	else:
		raise ValueError("Inserted structure ID greater than maximum structure ID length.")


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

	json_loot_data = commons.LOOT_DATA
	json_loot_data = sorted(json_loot_data, key=lambda x: int(x["id"]))

	for loot_data in json_loot_data:
		possible_item_strs = loot_data["item_list_data"]
		item_list_data = []
		for possible_item_properties_str in possible_item_strs:
			item_list_data.append([
				possible_item_properties_str["item_id_str"],
				possible_item_properties_str["item_spawn_weight"],
				possible_item_properties_str["item_spawn_depth_range"],
				possible_item_properties_str["item_stack_count_range"],
				possible_item_properties_str["item_slot_priority"],
				possible_item_properties_str["once_per_instance"]
			])
		loot_data["item_list_data"] = item_list_data

def create_loot_id_str_hash_table():
	global loot_id_str_hash_table
	for loot_index in range(len(json_loot_data)):
		loot_id_str_hash_table[json_loot_data[loot_index]["id_str"]] = loot_index


def get_loot_by_id(loot_id):
	if loot_id < len(json_loot_data):
		return json_loot_data[loot_id]
	else:
		raise ValueError("Inserted loot ID greater than maximum loot ID length.")


def get_loot_id_by_id_str(loot_id_str):
	return loot_id_str_hash_table[loot_id_str]


def get_loot_by_id_str(loot_id_str):
	return get_loot_by_id(get_loot_id_by_id_str(loot_id_str))


def parse_entity_data():
	global json_entity_data

	json_entity_data = commons.ENTITY_DATA
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
