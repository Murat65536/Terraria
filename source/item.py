# item.py

import random
import pygame

import game_data
from commons import ItemPrefixGroup, ItemTag

from enum import Enum


class ItemLocation(Enum):
    HOTBAR = 0
    INVENTORY = 1
    CHEST = 2
    CRAFTING_MENU = 3


class ItemSlotClickResult(Enum):
    GAVE_ALL = 0
    GAVE_SOME = 1
    SWAPPED = 2


"""================================================================================================================= 
    item.get_random_item_prefix -> [prefix category, prefix]

    Gets a random prefix from the prefix category
-----------------------------------------------------------------------------------------------------------------"""


def get_random_item_prefix(prefix_category):
    return [
        prefix_category,
        game_data.prefix_data[prefix_category][
            random.randint(0, len(game_data.prefix_data[prefix_category]) - 1)
        ],
    ]


"""================================================================================================================= 
    item.Item

    Stores information about an item
    
    Weapons, pickaxes etc will be automatically given a random prefix from the appropriate category when
    constructed
-----------------------------------------------------------------------------------------------------------------"""


class Item:
    def __init__(self, item_id, amount=1, auto_assign_prefix=False, prefix_name=None):
        self.json_item = game_data.get_item_by_id(item_id)

        self.item_id = item_id
        self.amount = amount
        self.has_prefix = False
        self.prefix_data = None

        # Auto assign prefix
        if prefix_name is None or prefix_name == "":
            if self.json_item != None:
                if auto_assign_prefix and ItemTag.WEAPON in self.json_item["tags"]:
                    # 15% chance to be given a prefix if it has a prefix category
                    if len(self.json_item["prefixes"]) > 0 and random.random() < 0.85:
                        self.prefix_data = get_random_item_prefix(
                            self.json_item["prefixes"][
                                random.randint(0, len(self.json_item["prefixes"]) - 1)
                            ]
                        )
                        self.has_prefix = True

        else:
            self.assign_prefix(prefix_name)

    def copy(self, new_amount=None):
        if new_amount is None:
            new_amount = self.amount
        return Item(self.item_id, new_amount, False, self.get_prefix_name())

    def has_tag(self, tag):
        if self.json_item != None:
            if tag in self.json_item["tags"]:
                return True
        return False

    def get_prefix_name(self):
        if self.prefix_data != None:
            if self.has_prefix:
                return self.prefix_data[1]["name"]
        return ""

    def get_attack_damage(self):
        if self.prefix_data != None:
            return self.json_item["attack_damage"] * (1 + self.prefix_data[1]["damage"])
        else:
            return self.json_item["attack_damage"]

    def get_crit_chance(self):
        if self.prefix_data != None:
            if self.prefix_data[0] == ItemPrefixGroup.UNIVERSAL:
                return max(
                    min(
                        1.0,
                        self.json_item["crit_chance"]
                        + self.prefix_data[1]["crit_chance"],
                    ),
                    0.0,
                )
            else:
                return max(
                    min(
                        1.0,
                        self.json_item["crit_chance"]
                        + self.prefix_data[1]["crit_chance"],
                    ),
                    0.0,
                )
        else:
            return self.json_item["crit_chance"]

    def get_knockback(self):
        if self.prefix_data != None:
            if self.prefix_data[0] == ItemPrefixGroup.UNIVERSAL:
                return self.json_item["knockback"] * (
                    1 + self.prefix_data[1]["knockback"]
                )
            elif self.prefix_data[0] == ItemPrefixGroup.COMMON:
                return self.json_item["knockback"] * (
                    1 + self.prefix_data[1]["knockback"]
                )
            else:
                return self.json_item["knockback"] * (
                    1 + self.prefix_data[1]["knockback"]
                )
        else:
            return self.json_item["knockback"]

    def get_tier(self):
        if self.json_item != None:
            if self.prefix_data != None:
                if self.prefix_data[0] == ItemPrefixGroup.UNIVERSAL:
                    return min(
                        max(self.json_item["tier"] + self.prefix_data[1]["tier"], 0), 10
                    )
                elif self.prefix_data[0] == ItemPrefixGroup.COMMON:
                    return min(
                        max(self.json_item["tier"] + self.prefix_data[1]["tier"], 0), 10
                    )
                else:
                    return min(
                        max(self.json_item["tier"] + self.prefix_data[1]["tier"], 0), 10
                    )
            else:
                return self.json_item["tier"]

    def get_attack_speed(self):
        if self.prefix_data != None:
            return round(
                self.json_item["attack_speed"] * (1 - self.prefix_data[1]["speed"])
            )  # The zero is the total attack speed modifiers. Change when attack speed modifiers are added.
        else:
            return round(self.json_item["attack_speed"])

    def get_scale(self):
        if self.prefix_data != None:
            if (
                self.prefix_data[0] == ItemPrefixGroup.LONGSWORD
                or self.prefix_data[0] == ItemPrefixGroup.SHORTSWORD
            ):
                return 1 + self.prefix_data[1]["size"]
        return 1.0

    def get_ranged_projectile_speed(self):
        if self.json_item != None:
            if (
                self.prefix_data != None
                and self.prefix_data[0] == ItemPrefixGroup.RANGED
            ):
                return self.json_item["ranged_projectile_speed"] * (
                    1 + self.prefix_data[1]["velocity"]
                )
            return self.json_item["ranged_projectile_speed"]

    def get_mana_cost(self):
        if self.json_item != None:
            if (
                self.prefix_data is not None
                and self.prefix_data[0] == ItemPrefixGroup.MAGICAL
            ):
                return self.json_item["mana_cost"] * (
                    1 + self.prefix_data[1]["mana_cost"]
                )
            return self.json_item["mana_cost"]

    def get_name(self):
        if self.json_item != None:
            if self.has_prefix:
                return self.get_prefix_name() + " " + self.json_item["name"]
            else:
                return self.json_item["name"]

    def get_id_str(self):
        if self.json_item != None:
            return self.json_item["id_str"]

    def get_ammo_damage(self):
        if self.json_item != None:
            return self.json_item["ammo_damage"]

    def get_ammo_drag(self):
        return self.json_item["ammo_drag"]

    def get_ammo_gravity_modifier(self):
        return self.json_item["ammo_gravity_modifier"]

    def get_ammo_knockback_modifier(self):
        return self.json_item["ammo_knockback_modifier"]

    def assign_prefix(self, prefix_name):
        self.prefix_data = game_data.find_prefix_data_by_name(prefix_name)
        if self.prefix_data is not None:
            self.has_prefix = True
        else:
            self.has_prefix = False

    def get_image(self) -> pygame.Surface:
        if type(self.json_item["image"]) is pygame.Surface:
            return self.json_item["image"]
        else:
            raise ValueError("Item image is not set.")

    def get_resized_image(self):
        if type(self.json_item["image"]) is pygame.Surface:
            image = self.json_item["image"]
            if max(image.get_width(), image.get_height()) > 32:
                image = pygame.transform.scale(
                    image,
                    (
                        image.get_width()
                        * (32 / max(image.get_width(), image.get_height())),
                        image.get_height()
                        * (32 / max(image.get_width(), image.get_height())),
                    ),
                )
            return image
        else:
            raise ValueError("Item image is not set.")

    def get_offset_x(self):
        if type(self.json_item["image"]) is pygame.Surface:
            return int(24 - self.json_item["image"].get_width() * 0.5)
        return 8

    def get_offset_y(self):
        if type(self.json_item["image"]) is pygame.Surface:
            return int(24 - self.json_item["image"].get_height() * 0.5)
        return 8

    def get_resized_offset_x(self):
        if type(self.json_item["image"]) is pygame.Surface:
            if (
                max(
                    self.json_item["image"].get_width(),
                    self.json_item["image"].get_height(),
                )
                > 32
            ):
                return int(
                    24
                    - self.json_item["image"].get_width()
                    * 32
                    / max(
                        self.json_item["image"].get_width(),
                        self.json_item["image"].get_height(),
                    )
                    * 0.5
                )
            return int(24 - self.json_item["image"].get_width() * 0.5)

    def get_resized_offset_y(self):
        if type(self.json_item["image"]) is pygame.Surface:
            if (
                max(
                    self.json_item["image"].get_width(),
                    self.json_item["image"].get_height(),
                )
                > 32
            ):
                return int(
                    24
                    - self.json_item["image"].get_height()
                    * 32
                    / max(
                        self.json_item["image"].get_width(),
                        self.json_item["image"].get_height(),
                    )
                    * 0.5
                )
            return int(24 - self.json_item["image"].get_height() * 0.5)

    def get_world_override_image(self):
        if self.json_item != None:
            try:
                return self.json_item["world_override_image"]
            except KeyError:
                return

    def get_tile_id_str(self):
        if self.json_item != None:
            return self.json_item["tile_id_str"]

    def get_wall_id_str(self):
        if self.json_item != None:
            return self.json_item["wall_id_str"]

    def get_hold_offset(self):
        if self.json_item != None:
            return self.json_item["hold_offset"]

    def get_ranged_projectile_id_str(self):
        if self.json_item != None:
            return self.json_item["ranged_projectile_id_str"]

    def get_ranged_ammo_type(self):
        if self.json_item != None:
            return self.json_item["ranged_ammo_type"]

    def get_ranged_accuracy(self):
        if self.json_item != None:
            return self.json_item["ranged_accuracy"]

    def get_ranged_num_projectiles(self):
        if self.json_item != None:
            return self.json_item["ranged_num_projectiles"]

    def get_pickaxe_power(self):
        if self.json_item != None:
            return self.json_item["pickaxe_power"]

    def get_axe_power(self):
        if self.json_item != None:
            return self.json_item["axe_power"]

    def get_hammer_power(self):
        if self.json_item != None:
            return self.json_item["hammer_power"]

    def get_grapple_speed(self):
        if self.json_item != None:
            return self.json_item["grapple_speed"]

    def get_grapple_chain_length(self):
        if self.json_item != None:
            return self.json_item["grapple_chain_length"]

    def get_grapple_max_chains(self):
        if self.json_item != None:
            return self.json_item["grapple_max_chains"]

    def get_grapple_chain_image(self):
        if self.json_item != None:
            return self.json_item["grapple_chain_image"]

    def get_grapple_claw_image(self):
        if self.json_item != None:
            return self.json_item["grapple_claw_image"]

    def get_max_stack(self):
        if self.json_item != None:
            return self.json_item["max_stack"]

    def get_buy_price(self):
        if self.json_item != None:
            return self.json_item["buy_price"]

    def get_sell_price(self):
        if self.json_item != None:
            return self.json_item["sell_price"]

    def get_pickup_sound_id_str(self):
        if self.json_item != None:
            return self.json_item["pickup_sound"]

    def get_drop_sound_id_str(self):
        if self.json_item != None:
            return self.json_item["drop_sound"]


def get_coins_from_int(coin_int: int) -> list[Item]:
    plat_coins: int = coin_int // 1000000
    gold_coins: int = (coin_int // 10000) % 100
    silver_coins: int = (coin_int // 100) % 100
    copper_coins: int = coin_int % 100

    item_list: list[Item] = []
    if plat_coins != 0:
        item_list.append(
            Item(game_data.get_item_id_by_id_str("item.platinum_coin"), plat_coins)
        )
    if gold_coins != 0:
        item_list.append(
            Item(game_data.get_item_id_by_id_str("item.gold_coin"), gold_coins)
        )
    if silver_coins != 0:
        item_list.append(
            Item(game_data.get_item_id_by_id_str("item.silver_coin"), silver_coins)
        )
    if copper_coins != 0:
        item_list.append(
            Item(game_data.get_item_id_by_id_str("item.copper_coin"), copper_coins)
        )

    return item_list


def generate_loot_items(loot_id_str, tile_pos, fill_with_none):
    loot_data = game_data.get_loot_by_id_str(loot_id_str)
    item_count_range = loot_data["item_spawn_count_range"]
    item_count = random.randint(item_count_range[0], item_count_range[1])
    possible_items = loot_data["item_list_data"]

    spawn_list = []
    void_indices = []

    for _ in range(item_count):
        total_weight = 0
        possible_item_indices = []

        for possible_item_index in range(len(possible_items)):
            if possible_item_index not in void_indices:
                possible_item = possible_items[possible_item_index]
                if (
                    possible_item[2][0] == possible_item[2][1]
                    or possible_item[2][0] < tile_pos[1] < possible_item[2][1]
                ):
                    total_weight += possible_item[1]
                    possible_item_indices.append(possible_item_index)

        random_num = random.randint(0, total_weight)

        for possible_item_index in possible_item_indices:
            if possible_item_index not in void_indices:
                possible_item = possible_items[possible_item_index]
                if random_num <= possible_item[1]:
                    random_count = random.randint(
                        possible_item[3][0], possible_item[3][1]
                    )
                    new_item_id = game_data.get_item_id_by_id_str(possible_item[0])

                    should_add_instance = True
                    for item_index in range(len(spawn_list)):
                        if spawn_list[item_index][0] == new_item_id:
                            spawn_list[item_index][1] += random_count
                            if spawn_list[item_index][0] != None:
                                max_stack = game_data.get_item_by_id(
                                    spawn_list[item_index][0]
                                )["max_stack"]
                                if spawn_list[item_index][1] > max_stack:
                                    random_count = spawn_list[item_index][1] - max_stack
                                    spawn_list[item_index][1] = max_stack
                            else:
                                should_add_instance = False

                    if should_add_instance:
                        spawn_list.append([new_item_id, random_count, possible_item[4]])

                        if possible_item[5]:  # Only once
                            void_indices.append(possible_item_index)
                        break
                else:
                    random_num -= possible_item[1]

    # Sort the spawn list and insert actual items
    spawn_list = sorted(spawn_list, key=lambda x: int(x[2]))
    for item_index in range(len(spawn_list)):
        spawn_item_data = spawn_list[item_index]
        spawn_list[item_index] = Item(
            spawn_item_data[0], spawn_item_data[1], auto_assign_prefix=True
        )

    # Coins
    assert loot_data is not None

    random_coin_range = loot_data["coin_spawn_range"]
    random_coin_count = random.randint(random_coin_range[0], random_coin_range[1])
    coin_items = get_coins_from_int(random_coin_count)
    for coin_item in coin_items:
        spawn_list.append(coin_item)

    if fill_with_none:
        for _ in range(20 - len(spawn_list)):
            spawn_list.append(None)

    return spawn_list


item_holding: Item = Item(0)