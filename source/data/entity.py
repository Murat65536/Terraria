from dataclasses import dataclass

from pygame import Color


@dataclass
class EntityData:
    @dataclass
    class ItemDrop:
        name: str
        drop_range: tuple[int, int]

    name: str
    species: str
    health: float
    defense: int
    knockback_resistance: float
    attack_damage: int
    color: Color
    item_drops: list[ItemDrop]
    coin_drop_range: tuple[int, int]


ENTITY_DATA: list[EntityData] = [
    EntityData(
        "INVALID",
        "Slime",
        0,
        0,
        0,
        0,
        Color(0, 0, 0),
        [
            EntityData.ItemDrop(
                "item.INVALID",
                (0, 0),
            )
        ],
        (0, 0),
    ),
    EntityData(
        "Green Slime",
        "Slime",
        14,
        0,
        -2,
        6,
        Color(10, 200, 10),
        [
            EntityData.ItemDrop(
                "item.gel",
                (1, 2),
            )
        ],
        (5, 30),
    ),
    EntityData(
        "Blue Slime",
        "Slime",
        25,
        2,
        0,
        7,
        Color(10, 10, 200),
        [
            EntityData.ItemDrop(
                "item.gel",
                (1, 2),
            )
        ],
        (15, 50),
    ),
    EntityData(
        "Red Slime",
        "Slime",
        35,
        4,
        0,
        12,
        Color(200, 10, 10),
        [
            EntityData.ItemDrop(
                "item.gel",
                (2, 5),
            ),
        ],
        (25, 75),
    ),
    EntityData(
        "Purple Slime",
        "Slime",
        40,
        6,
        0.1,
        12,
        Color(200, 10, 200),
        [
            EntityData.ItemDrop(
                "item.gel",
                (2, 5),
            )
        ],
        (35, 110),
    ),
    EntityData(
        "Yellow Slime",
        "Slime",
        45,
        7,
        0,
        15,
        Color(200, 150, 100),
        [
            EntityData.ItemDrop(
                "item.gel",
                (2, 5),
            )
        ],
        (45, 130),
    ),
]
