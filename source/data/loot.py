from typing import TypedDict

class ItemLootData(TypedDict):
    item_id_str: str
    item_spawn_weight: int
    item_spawn_depth_range: tuple[int, int]
    item_stack_count_range: tuple[int, int]
    item_slot_priority: int
    once_per_instance: bool


class LootData(TypedDict):
    id: int
    id_str: str
    name: str
    item_spawn_count_range: tuple[int, int]
    item_list_data: list[ItemLootData]
    coin_spawn_range: tuple[int, int]

LOOT_DATA: list[LootData] = [
    {
        "id": 0,
        "id_str": "loot.INVALID",
        "name": "INVALID",
        "item_spawn_count_range": (0, 0),
        "item_list_data": [
            {
                "item_id_str": "item.INVALID",
                "item_spawn_weight": 100,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (0, 0),
                "item_slot_priority": 0,
                "once_per_instance": False,
            }
        ],
        "coin_spawn_range": (0, 0),
    },
    {
        "id": 1,
        "id_str": "loot.pot",
        "name": "Pot",
        "item_spawn_count_range": (1, 2),
        "item_list_data": [
            {
                "item_id_str": "item.torch",
                "item_spawn_weight": 100,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (3, 15),
                "item_slot_priority": 3,
                "once_per_instance": False,
            },
            {
                "item_id_str": "item.wood_platform",
                "item_spawn_weight": 50,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (5, 15),
                "item_slot_priority": 3,
                "once_per_instance": False,
            },
            {
                "item_id_str": "item.spike",
                "item_spawn_weight": 50,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (2, 6),
                "item_slot_priority": 2,
                "once_per_instance": False,
            },
            {
                "item_id_str": "item.musket_ball",
                "item_spawn_weight": 25,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (5, 20),
                "item_slot_priority": 1,
                "once_per_instance": False,
            },
            {
                "item_id_str": "item.copper_coin",
                "item_spawn_weight": 5,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (1, 1),
                "item_slot_priority": 0,
                "once_per_instance": True,
            },
            {
                "item_id_str": "item.wooden_arrow",
                "item_spawn_weight": 35,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (7, 25),
                "item_slot_priority": 1,
                "once_per_instance": False,
            },
        ],
        "coin_spawn_range": (75, 150),
    },
    {
        "id": 2,
        "id_str": "loot.chest_wood",
        "name": "Wood Chest",
        "item_spawn_count_range": (2, 6),
        "item_list_data": [
            {
                "item_id_str": "item.musket",
                "item_spawn_weight": 100,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (1, 1),
                "item_slot_priority": 0,
                "once_per_instance": True,
            },
            {
                "item_id_str": "item.wood_bow",
                "item_spawn_weight": 100,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (1, 1),
                "item_slot_priority": 0,
                "once_per_instance": True,
            },
            {
                "item_id_str": "item.water_bolt",
                "item_spawn_weight": 100,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (1, 1),
                "item_slot_priority": 0,
                "once_per_instance": False,
            },
            {
                "item_id_str": "item.wooden_arrow",
                "item_spawn_weight": 600,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (5, 20),
                "item_slot_priority": 2,
                "once_per_instance": False,
            },
            {
                "item_id_str": "item.musket_ball",
                "item_spawn_weight": 600,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (5, 20),
                "item_slot_priority": 2,
                "once_per_instance": False,
            },
        ],
        "coin_spawn_range": (750, 2000),
    },
    {
        "id": 3,
        "id_str": "loot.chest_gold",
        "name": "Gold Chest",
        "item_spawn_count_range": (2, 5),
        "item_list_data": [
            {
                "item_id_str": "item.dirt_block",
                "item_spawn_weight": 100,
                "item_spawn_depth_range": (0, 0),
                "item_stack_count_range": (0, 0),
                "item_slot_priority": 0,
                "once_per_instance": False,
            }
        ],
        "coin_spawn_range": (5000, 15000),
    },
]