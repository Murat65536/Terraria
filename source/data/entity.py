from typing import TypedDict
from pygame import Color

class EntityItemData(TypedDict):
    item_name: str
    item_minimum_drops: int
    item_maximum_drops: int
    item_weight: int

class EntityData(TypedDict):
    id: int
    id_str: str
    name: str
    type: str
    health: int
    defense: int
    knockback_resistance: float
    attack_damage: int
    color: Color
    item_drops: list[EntityItemData]
    coin_drop_range: tuple[int, int]

ENTITY_DATA: list[EntityData] = [
    {
        "id": 0,
        "id_str": "entity.INVALID",
        "name": "INVALID",
        "type": "Slime",
        "health": 0,
        "defense": 0,
        "knockback_resistance": 0,
        "attack_damage": 0,
        "color": Color(0, 0, 0),
        "item_drops": [
            {
                "item_name": "item.INVALID",
                "item_minimum_drops": 0,
                "item_maximum_drops": 0,
                "item_weight": 0,
            }
        ],
        "coin_drop_range": (0, 0),
    },
    {
        "id": 1,
        "id_str": "entity.green_slime",
        "name": "Green Slime",
        "type": "Slime",
        "health": 14,
        "defense": 0,
        "knockback_resistance": -2,
        "attack_damage": 6,
        "color": Color(10, 200, 10),
        "item_drops": [
            {
                "item_name": "item.gel",
                "item_minimum_drops": 1,
                "item_maximum_drops": 2,
                "item_weight": 100,
            }
        ],
        "coin_drop_range": (5, 30),
    },
    {
        "id": 2,
        "id_str": "entity.blue_slime",
        "name": "Blue Slime",
        "type": "Slime",
        "health": 25,
        "defense": 2,
        "knockback_resistance": 0,
        "attack_damage": 7,
        "color": Color(10, 10, 200),
        "item_drops": [
            {
                "item_name": "item.gel",
                "item_minimum_drops": 1,
                "item_maximum_drops": 2,
                "item_weight": 100,
            }
        ],
        "coin_drop_range": (15, 50),
    },
    {
        "id": 3,
        "id_str": "entity.red_slime",
        "name": "Red Slime",
        "type": "Slime",
        "health": 35,
        "defense": 4,
        "knockback_resistance": 0,
        "attack_damage": 12,
        "color": Color(200, 10, 10),
        "item_drops": [
            {
                "item_name": "item.gel",
                "item_minimum_drops": 2,
                "item_maximum_drops": 5,
                "item_weight": 100,
            }
        ],
        "coin_drop_range": (25, 75),
    },
    {
        "id": 4,
        "id_str": "entity.purple_slime",
        "name": "Purple Slime",
        "type": "Slime",
        "health": 40,
        "defense": 6,
        "knockback_resistance": 0.1,
        "attack_damage": 12,
        "color": Color(200, 10, 200),
        "item_drops": [
            {
                "item_name": "item.gel",
                "item_minimum_drops": 2,
                "item_maximum_drops": 5,
                "item_weight": 100,
            }
        ],
        "coin_drop_range": (35, 110),
    },
    {
        "id": 5,
        "id_str": "entity.yellow_slime",
        "name": "Yellow Slime",
        "type": "Slime",
        "health": 45,
        "defense": 7,
        "knockback_resistance": 0,
        "attack_damage": 15,
        "color": Color(200, 150, 100),
        "item_drops": [
            {
                "item_name": "item.gel",
                "item_minimum_drops": 2,
                "item_maximum_drops": 5,
                "item_weight": 100,
            }
        ],
        "coin_drop_range": (45, 130),
    },
]