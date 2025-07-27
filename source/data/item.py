from dataclasses import dataclass

from typing import TypedDict

from commons import ItemPrefixGroup, ItemTag
from pygame import Surface, image

@dataclass
class ItemData:
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    hold_offset: float
    pickup_sound: str
    drop_sound: str
    surface: Surface
    block_name: str


class PlaceableTileItemData(TypedDict):
    id: int
    id_str: int
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    hold_offset: float
    tile_id_str: str
    pickup_sound: str
    drop_sound: str
    image: Surface


class TileItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    tile_id_str: str
    pickup_sound: str
    drop_sound: str
    hold_offset: float
    image: Surface


class MaterialItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    pickup_sound: str
    drop_sound: str
    hold_offset: float
    image: Surface


class WallItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    hold_offset: float
    pickup_sound: str
    drop_sound: str
    wall_id_str: str
    image: Surface


class PickaxeItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    attack_speed: int
    attack_damage: int
    knockback: int
    crit_chance: float
    prefixes: list[ItemPrefixGroup]
    pickaxe_power: float
    pickup_sound: str
    drop_sound: str
    use_sound: str
    hold_offset: float
    image: Surface
    world_override_image: Surface | None


class HammerItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    attack_speed: int
    attack_damage: int
    knockback: float
    crit_chance: float
    prefixes: list[ItemPrefixGroup]
    pickup_sound: str
    drop_sound: str
    use_sound: str
    hammer_power: float
    hold_offset: float
    image: Surface
    world_override_image: Surface | None


class AxeItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    attack_speed: int
    attack_damage: int
    knockback: float
    crit_chance: float
    prefixes: list[ItemPrefixGroup]
    axe_power: float
    pickup_sound: str
    drop_sound: str
    use_sound: str
    hold_offset: float
    image: Surface
    world_override_image: Surface | None


class SwordItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    attack_speed: int
    attack_damage: int
    knockback: float
    crit_chance: float
    prefixes: list[ItemPrefixGroup]
    pickup_sound: str
    drop_sound: str
    use_sound: str
    hold_offset: float
    image: Surface
    world_override_image: Surface | None


class RangedItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    attack_speed: int
    attack_damage: int
    knockback: float
    crit_chance: float
    prefixes: list[ItemPrefixGroup]
    ranged_projectile_id_str: str
    ranged_ammo_type: list[str]
    ranged_projectile_speed: float
    ranged_accuracy: float
    ranged_num_projectiles: int
    pickup_sound: str
    drop_sound: str
    use_sound: str
    hold_offset: float
    image: Surface
    world_override_image: Surface | None


class AmmunitionItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    ammo_damage: float
    ammo_drag: float
    ammo_gravity_modifier: float
    ammo_knockback_modifier: float
    pickup_sound: str
    drop_sound: str
    hold_offset: float
    ricochet_amount: int
    image: Surface
    ammo_image: Surface


class GrapplingHookItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    grapple_speed: float
    grapple_chain_length: float
    grapple_max_chains: int
    pickup_sound: str
    drop_sound: str
    hold_offset: float
    image: Surface
    grapple_chain_image: Surface
    grapple_claw_image: Surface


class MagicalWeaponItemData(TypedDict):
    id: int
    id_str: str
    name: str
    tags: list[ItemTag]
    tier: int
    max_stack: int
    buy_price: int
    sell_price: int
    pickup_sound: str
    drop_sound: str
    prefixes: list[ItemPrefixGroup]
    attack_speed: int
    attack_damage: int
    knockback: float
    crit_chance: float
    hold_offset: float
    use_sound: str
    mana_cost: int
    image: Surface
    world_override_image: Surface | None


ITEM_DATA: list[
    TileItemData
    | MaterialItemData
    | WallItemData
    | PickaxeItemData
    | HammerItemData
    | AxeItemData
    | SwordItemData
    | RangedItemData
    | AmmunitionItemData
    | GrapplingHookItemData
    | MagicalWeaponItemData
    ] = [
    {
        "id": 0,
        "id_str": "item.INVALID",
        "name": "INVALID",
        "tags": [],
        "tier": 0,
        "max_stack": 9999,
        "buy_price": 0,
        "sell_price": 0,
        "hold_offset": 0.0,
        "tile_id_str": "tile.UNNAMED",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "image": Surface((0, 0)),
    },
    {
        "id": 1,
        "id_str": "item.iron_pickaxe",
        "name": "Iron Pickaxe",
        "tags": [ItemTag.PICKAXE, ItemTag.TOOL, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 0,
        "sell_price": 40,
        "attack_speed": 20,
        "attack_damage": 7,
        "knockback": 2,
        "crit_chance": 0.04,
        "prefixes": [ItemPrefixGroup.COMMON, ItemPrefixGroup.UNIVERSAL],
        "pickaxe_power": 40.0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": image.load("assets/images/items/iron_pickaxe.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 2,
        "id_str": "item.dirt_block",
        "name": "Dirt",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 1,
        "sell_price": 0,
        "hold_offset": 0.0,
        "tile_id_str": "tile.dirt",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "image": image.load("assets/images/items/dirt_block.png").convert_alpha(),
    },
    {
        "id": 3,
        "id_str": "item.stone_block",
        "name": "Stone",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 2,
        "sell_price": 0,
        "hold_offset": 0.0,
        "tile_id_str": "tile.stone",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "image": image.load("assets/images/items/stone_block.png").convert_alpha(),
    },
    {
        "id": 4,
        "id_str": "item.iron_broadsword",
        "name": "Iron Broadsword",
        "tags": [ItemTag.LONGSWORD, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 200,
        "sell_price": 20,
        "attack_speed": 20,
        "attack_damage": 12,
        "knockback": 5.5,
        "crit_chance": 0.04,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.LONGSWORD,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": image.load("assets/images/items/iron_broadsword.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 5,
        "id_str": "item.mushroom",
        "name": "Mushroom",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 1,
        "tile_id_str": "tile.mushroom",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/mushroom.png").convert_alpha(),
    },
    {
        "id": 6,
        "id_str": "item.iron_ore",
        "name": "Iron Ore",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 20,
        "sell_price": 10,
        "tile_id_str": "tile.pot_thick_brown",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/iron_ore.png").convert_alpha(),
    },
    {
        "id": 7,
        "id_str": "item.dirt_wall",
        "name": "Dirt Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 2,
        "sell_price": 0,
        "hold_offset": 0.0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "wall_id_str": "wall.dirt",
        "image": image.load("assets/images/items/dirt_wall.png").convert_alpha(),
    },
    {
        "id": 8,
        "id_str": "item.stone_wall",
        "name": "Stone Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 2,
        "sell_price": 0,
        "hold_offset": 0.0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "wall_id_str": "wall.stone",
        "image": image.load("assets/images/items/stone_wall.png").convert_alpha(),
    },
    {
        "id": 9,
        "id_str": "item.snow",
        "name": "Snow",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 2,
        "tile_id_str": "tile.snow",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/snow.png").convert_alpha(),
    },
    {
        "id": 10,
        "id_str": "item.snow_wall",
        "name": "Snow Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 2,
        "sell_price": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "wall_id_str": "wall.snow",
        "image": image.load("assets/images/items/snow_wall.png").convert_alpha(),
    },
    {
        "id": 11,
        "id_str": "item.ice",
        "name": "Ice",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 0,
        "tile_id_str": "tile.ice",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/ice.png").convert_alpha(),
    },
    {
        "id": 12,
        "id_str": "item.ice_wall",
        "name": "Ice Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 2,
        "sell_price": 5,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "wall_id_str": "wall.ice",
        "image": image.load("assets/images/items/ice_wall.png").convert_alpha(),
    },
    {
        "id": 13,
        "id_str": "item.wood",
        "name": "Wood",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 1,
        "tile_id_str": "tile.wood",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/wood.png").convert_alpha(),
    },
    {
        "id": 14,
        "id_str": "item.wood_wall",
        "name": "Wood Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 2,
        "sell_price": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "wall_id_str": "wall.wood",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/wood_wall.png").convert_alpha(),
    },
    {
        "id": 15,
        "id_str": "item.copper_ore",
        "name": "Copper Ore",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 10,
        "sell_price": 5,
        "tile_id_str": "tile.copper",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/copper_ore.png").convert_alpha(),
    },
    {
        "id": 16,
        "id_str": "item.silver_ore",
        "name": "Silver Ore",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 20,
        "sell_price": 10,
        "tile_id_str": "tile.pot_thick_brown",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/silver_ore.png").convert_alpha(),
    },
    {
        "id": 17,
        "id_str": "item.sand",
        "name": "Sand",
        "tags": [ItemTag.MATERIAL, ItemTag.TILE],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 10,
        "sell_price": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "tile_id_str": "tile.sand",
        "image": image.load("assets/images/items/sand.png").convert_alpha(),
    },
    {
        "id": 18,
        "id_str": "item.hardened_sand_wall",
        "name": "Hardened Sand Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 10,
        "sell_price": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "wall_id_str": "wall.hardened_sand",
        "image": image.load("assets/images/items/hardened_sand_wall.png").convert_alpha(),
    },
    {
        "id": 19,
        "id_str": "item.sandstone",
        "name": "Sandstone",
        "tags": [ItemTag.TILE, ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 0,
        "tile_id_str": "tile.sandstone",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/sandstone.png").convert_alpha(),
    },
    {
        "id": 20,
        "id_str": "item.sandstone_wall",
        "name": "Sandstone Wall",
        "tags": [ItemTag.WALL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "wall_id_str": "wall.sandstone",
        "image": image.load("assets/images/items/sandstone_wall.png").convert_alpha(),
    },
    {
        "id": 21,
        "id_str": "item.wood_platform",
        "name": "Wood Platform",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 20,
        "sell_price": 5,
        "tile_id_str": "tile.platform_wood",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/wood_platform.png").convert_alpha(),
    },
    {
        "id": 22,
        "id_str": "item.copper_broadsword",
        "name": "Copper Broadsword",
        "tags": [ItemTag.LONGSWORD, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 200,
        "sell_price": 20,
        "attack_speed": 45,
        "attack_damage": 5,
        "knockback": 10,
        "crit_chance": 0.03,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.LONGSWORD,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": image.load("assets/images/items/copper_broadsword.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 23,
        "id_str": "item.excalibur",
        "name": "Excalibur",
        "tags": [ItemTag.LONGSWORD, ItemTag.WEAPON],
        "tier": 10,
        "max_stack": 1,
        "buy_price": 100000000,
        "sell_price": 20000000,
        "attack_speed": 35,
        "attack_damage": 1337,
        "knockback": 0,
        "crit_chance": 0.0,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.LONGSWORD,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.9,
        "image": image.load("assets/images/items/excalibur.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 24,
        "id_str": "item.wood_broadsword",
        "name": "Wooden Sword",
        "tags": [ItemTag.LONGSWORD, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 100,
        "sell_price": 10,
        "attack_speed": 50,
        "attack_damage": 3,
        "knockback": 6,
        "crit_chance": 0.03,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.LONGSWORD,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": image.load("assets/images/items/wood_broadsword.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 25,
        "id_str": "item.wood_bow",
        "name": "Wooden Bow",
        "tags": [ItemTag.RANGED, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 150,
        "sell_price": 20,
        "attack_speed": 50,
        "attack_damage": 4,
        "knockback": 2,
        "crit_chance": 0.03,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.RANGED,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "ranged_projectile_id_str": "projectile.arrow",
        "ranged_ammo_type": ["item.wooden_arrow"],
        "ranged_projectile_speed": 75.0,
        "ranged_accuracy": 0.9,
        "ranged_num_projectiles": 1,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.bow",
        "hold_offset": 0.8,
        "image": image.load("assets/images/items/wood_bow.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 26,
        "id_str": "item.wooden_arrow",
        "name": "Wooden Arrow",
        "tags": [ItemTag.MATERIAL, ItemTag.AMMO],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 1,
        "ammo_damage": 4.0,
        "ammo_drag": 0.05,
        "ammo_gravity_modifier": 1.2,
        "ammo_knockback_modifier": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "ricochet_amount": 1,
        "image": image.load("assets/images/items/wooden_arrow.png").convert_alpha(),
        "ammo_image": image.load("assets/images/projectiles/wooden_arrow.png").convert_alpha(),
    },
    {
        "id": 27,
        "id_str": "item.musket",
        "name": "Musket",
        "tags": [ItemTag.RANGED, ItemTag.WEAPON],
        "tier": 1,
        "max_stack": 1,
        "buy_price": 5000,
        "sell_price": 250,
        "attack_speed": 75,
        "attack_damage": 12,
        "knockback": 4,
        "crit_chance": 0.03,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.RANGED,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "ranged_projectile_id_str": "projectile.bullet",
        "ranged_ammo_type": ["item.musket_ball"],
        "ranged_projectile_speed": 100.0,
        "ranged_accuracy": 0.95,
        "ranged_num_projectiles": 1,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.gun_shot",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/musket.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 28,
        "id_str": "item.musket_ball",
        "name": "Musket Ball",
        "tags": [ItemTag.MATERIAL, ItemTag.AMMO],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 7,
        "sell_price": 1,
        "ammo_damage": 7.0,
        "ammo_drag": 0.05,
        "ammo_gravity_modifier": 0.5,
        "ammo_knockback_modifier": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "ricochet_amount": 1,
        "image": image.load("assets/images/items/musket_ball.png").convert_alpha(),
        "ammo_image": image.load("assets/images/projectiles/musket_ball.png").convert_alpha(),
    },
    {
        "id": 29,
        "id_str": "item.copper_coin",
        "name": "Copper Coin",
        "tags": [ItemTag.AMMO, ItemTag.COIN],
        "tier": 0,
        "max_stack": 100,
        "buy_price": 0,
        "sell_price": 0,
        "ammo_damage": 2.0,
        "ammo_drag": 5.0,
        "ammo_gravity_modifier": 1.0,
        "ammo_knockback_modifier": 0,
        "pickup_sound": "sound.coins",
        "drop_sound": "sound.coins",
        "hold_offset": 0.0,
        "ricochet_amount": 1,
        "image": image.load("assets/images/items/copper_coin.png").convert_alpha(),
        "ammo_image": image.load("assets/images/projectiles/musket_ball.png").convert_alpha(),
    },
    {
        "id": 30,
        "id_str": "item.silver_coin",
        "name": "Silver Coin",
        "tags": [ItemTag.AMMO, ItemTag.COIN],
        "tier": 0,
        "max_stack": 100,
        "buy_price": 0,
        "sell_price": 0,
        "ammo_damage": 5.0,
        "ammo_drag": 2.5,
        "ammo_gravity_modifier": 0.75,
        "ammo_knockback_modifier": 0,
        "pickup_sound": "sound.coins",
        "drop_sound": "sound.coins",
        "hold_offset": 0.0,
        "ricochet_amount": 1,
        "image": image.load("assets/images/items/silver_coin.png").convert_alpha(),
        "ammo_image": image.load("assets/images/projectiles/musket_ball.png").convert_alpha(),
    },
    {
        "id": 31,
        "id_str": "item.gold_coin",
        "name": "Gold Coin",
        "tags": [ItemTag.AMMO, ItemTag.COIN],
        "tier": 0,
        "max_stack": 100,
        "buy_price": 0,
        "sell_price": 0,
        "ammo_damage": 50.0,
        "ammo_drag": 1.25,
        "ammo_gravity_modifier": 0.5,
        "ammo_knockback_modifier": 0,
        "pickup_sound": "sound.coins",
        "drop_sound": "sound.coins",
        "hold_offset": 0.0,
        "ricochet_amount": 1,
        "image": image.load("assets/images/items/gold_coin.png").convert_alpha(),
        "ammo_image": image.load("assets/images/projectiles/musket_ball.png").convert_alpha(),
    },
    {
        "id": 32,
        "id_str": "item.platinum_coin",
        "name": "Platinum Coin",
        "tags": [ItemTag.AMMO, ItemTag.COIN],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 0,
        "sell_price": 0,
        "ammo_damage": 100.0,
        "ammo_drag": 0.625,
        "ammo_gravity_modifier": 0.25,
        "ammo_knockback_modifier": 0,
        "pickup_sound": "sound.coins",
        "drop_sound": "sound.coins",
        "hold_offset": 0.0,
        "ricochet_amount": 1,
        "image": image.load("assets/images/items/platinum_coin.png").convert_alpha(),
        "ammo_image": image.load("assets/images/projectiles/musket_ball.png").convert_alpha(),
    },
    {
        "id": 33,
        "id_str": "item.copper_pickaxe",
        "name": "Copper Pickaxe",
        "tags": [ItemTag.PICKAXE, ItemTag.TOOL, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 150,
        "sell_price": 10,
        "attack_speed": 50,
        "attack_damage": 2,
        "knockback": 10,
        "crit_chance": 0.03,
        "prefixes": [ItemPrefixGroup.COMMON, ItemPrefixGroup.UNIVERSAL],
        "pickaxe_power": 35.0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": image.load("assets/images/items/copper_pickaxe.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 34,
        "id_str": "item.copper_hammer",
        "name": "Copper Hammer",
        "tags": [ItemTag.HAMMER, ItemTag.TOOL, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 150,
        "sell_price": 10,
        "attack_speed": 50,
        "attack_damage": 2,
        "knockback": 10,
        "crit_chance": 0.03,
        "prefixes": [ItemPrefixGroup.COMMON, ItemPrefixGroup.UNIVERSAL],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hammer_power": 0,
        "hold_offset": 0.8,
        "image": image.load("assets/images/items/copper_hammer.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 35,
        "id_str": "item.wood_hammer",
        "name": "Wood Hammer",
        "tags": [ItemTag.HAMMER, ItemTag.TOOL, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 150,
        "sell_price": 10,
        "attack_speed": 35,
        "attack_damage": 2,
        "knockback": 10,
        "crit_chance": 0.03,
        "prefixes": [ItemPrefixGroup.COMMON, ItemPrefixGroup.UNIVERSAL],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hammer_power": 0,
        "hold_offset": 0.8,
        "image": image.load("assets/images/items/wood_hammer.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 36,
        "id_str": "item.gel",
        "name": "Blue Gel",
        "tags": [ItemTag.MATERIAL],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 5,
        "sell_price": 1,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/gel.png").convert_alpha(),
    },
    {
        "id": 37,
        "id_str": "item.wood_chest",
        "name": "Wooden Chest",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 99,
        "buy_price": 50,
        "sell_price": 5,
        "tile_id_str": "tile.chest_wood",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/wood_chest.png").convert_alpha(),
    },
    {
        "id": 38,
        "id_str": "item.workbench",
        "name": "Workbench",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 99,
        "buy_price": 50,
        "sell_price": 5,
        "tile_id_str": "tile.crafting_table_wood",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/workbench.png").convert_alpha(),
    },
    {
        "id": 39,
        "id_str": "item.wood_door",
        "name": "Wooden Door",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 99,
        "buy_price": 50,
        "sell_price": 5,
        "tile_id_str": "tile.door_wood_closed",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/wood_door.png").convert_alpha(),
    },
    {
        "id": 40,
        "id_str": "item.torch",
        "name": "Torch",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 20,
        "sell_price": 2,
        "tile_id_str": "tile.torch",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/torch.png").convert_alpha(),
    },
    {
        "id": 41,
        "id_str": "item.spike",
        "name": "Spike",
        "tags": [ItemTag.TILE],
        "tier": 0,
        "max_stack": 999,
        "buy_price": 15,
        "sell_price": 0,
        "tile_id_str": "tile.spike",
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/spike.png").convert_alpha(),
    },
    {
        "id": 42,
        "id_str": "item.grappling_hook",
        "name": "Grappling Hook",
        "tags": [ItemTag.GRAPPLE, ItemTag.TOOL],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 10000,
        "sell_price": 500,
        "grapple_speed": 10.0,
        "grapple_chain_length": 100.0,
        "grapple_max_chains": 1,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "hold_offset": 0.0,
        "image": image.load("assets/images/items/grappling_hook.png").convert_alpha(),
        "grapple_chain_image": image.load("assets/images/chains/grappling_hook_chain.png").convert_alpha(),
        "grapple_claw_image": image.load("assets/images/projectiles/grappling_hook_claw.png").convert_alpha(),
    },
    {
        "id": 43,
        "id_str": "item.water_bolt",
        "name": "Water Bolt",
        "tags": [ItemTag.MAGICAL, ItemTag.WEAPON],
        "tier": 3,
        "max_stack": 999,
        "buy_price": 10000,
        "sell_price": 750,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "prefixes": [],
        "attack_speed": 12,
        "attack_damage": 5,
        "knockback": 0,
        "crit_chance": 0.03,
        "hold_offset": 0.0,
        "use_sound": "sound.swing",
        "mana_cost": 20,
        "image": image.load("assets/images/items/water_bolt.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 44,
        "id_str": "item.painting_a",
        "name": "Painting A",
        "tags": [ItemTag.TILE],
        "tier": 3,
        "max_stack": 999,
        "buy_price": 1000,
        "sell_price": 100,
        "hold_offset": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "tile_id_str": "tile.painting_a",
        "image": image.load("assets/images/items/painting_a.png").convert_alpha(),
    },
    {
        "id": 45,
        "id_str": "item.painting_b",
        "name": "Painting B",
        "tags": [ItemTag.TILE],
        "tier": 3,
        "max_stack": 999,
        "buy_price": 1000,
        "sell_price": 100,
        "hold_offset": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "tile_id_str": "tile.painting_b",
        "image": image.load("assets/images/items/painting_b.png").convert_alpha(),
    },
    {
        "id": 46,
        "id_str": "item.painting_c",
        "name": "Painting C",
        "tags": [ItemTag.TILE],
        "tier": 3,
        "max_stack": 999,
        "buy_price": 1000,
        "sell_price": 100,
        "hold_offset": 0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "tile_id_str": "tile.painting_c",
        "image": image.load("assets/images/items/painting_c.png").convert_alpha(),
    },
    {
        "id": 47,
        "id_str": "item.copper_axe",
        "name": "Copper Axe",
        "tags": [ItemTag.AXE, ItemTag.TOOL, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 150,
        "sell_price": 10,
        "attack_speed": 50,
        "attack_damage": 2,
        "knockback": 10,
        "crit_chance": 0.03,
        "prefixes": [ItemPrefixGroup.COMMON, ItemPrefixGroup.UNIVERSAL],
        "axe_power": 55.0,
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": image.load("assets/images/items/copper_axe.png").convert_alpha(),
        "world_override_image": None,
    },
    {
        "id": 48,
        "id_str": "item.iron_shortsword",
        "name": "Iron Shortsword",
        "tags": [ItemTag.SHORTSWORD, ItemTag.WEAPON],
        "tier": 0,
        "max_stack": 1,
        "buy_price": 200,
        "sell_price": 20,
        "attack_speed": 20,
        "attack_damage": 12,
        "knockback": 5.5,
        "crit_chance": 0.04,
        "prefixes": [
            ItemPrefixGroup.COMMON,
            ItemPrefixGroup.SHORTSWORD,
            ItemPrefixGroup.UNIVERSAL,
        ],
        "pickup_sound": "sound.grab",
        "drop_sound": "sound.grab",
        "use_sound": "sound.swing",
        "hold_offset": 0.8,
        "image": image.load("assets/images/items/iron_shortsword.png").convert_alpha(),
        "world_override_image": None,
    },
]
