from typing import TypedDict


class SoundData(TypedDict):
    id: int
    id_str: str
    variation_paths: list[str]
    volume: float


SOUND_DATA: list[SoundData] = [
    {"id": 0, "id_str": "sound.INVALID", "variation_paths": [], "volume": 1},
    {
        "id": 1,
        "id_str": "sound.tink",
        "variation_paths": [
            "assets/sounds/tink_0.wav",
            "assets/sounds/tink_1.wav",
            "assets/sounds/tink_2.wav",
        ],
        "volume": 1,
    },
    {
        "id": 2,
        "id_str": "sound.dig",
        "variation_paths": [
            "assets/sounds/dig_0.wav",
            "assets/sounds/dig_1.wav",
            "assets/sounds/dig_2.wav",
        ],
        "volume": 1,
    },
    {
        "id": 3,
        "id_str": "sound.jump",
        "variation_paths": ["assets/sounds/jump.wav"],
        "volume": 1,
    },
    {
        "id": 4,
        "id_str": "sound.player_hurt",
        "variation_paths": [
            "assets/sounds/player_hit_0.wav",
            "assets/sounds/player_hit_1.wav",
            "assets/sounds/player_hit_2.wav",
        ],
        "volume": 1,
    },
    {
        "id": 5,
        "id_str": "sound.grass",
        "variation_paths": ["assets/sounds/grass.wav"],
        "volume": 1,
    },
    {
        "id": 6,
        "id_str": "sound.player_death",
        "variation_paths": ["assets/sounds/player_killed.wav"],
        "volume": 1,
    },
    {
        "id": 7,
        "id_str": "sound.mirror",
        "variation_paths": ["assets/sounds/mirror.wav"],
        "volume": 0.1,
    },
    {
        "id": 8,
        "id_str": "sound.slime_hurt",
        "variation_paths": ["assets/sounds/npc_hit_0.wav"],
        "volume": 1,
    },
    {
        "id": 9,
        "id_str": "sound.slime_death",
        "variation_paths": ["assets/sounds/npc_killed_0.wav"],
        "volume": 1,
    },
    {
        "id": 10,
        "id_str": "sound.swing",
        "variation_paths": ["assets/sounds/swing.wav"],
        "volume": 1,
    },
    {
        "id": 11,
        "id_str": "sound.bow",
        "variation_paths": ["assets/sounds/bow.wav"],
        "volume": 1,
    },
    {
        "id": 12,
        "id_str": "sound.gun_shot",
        "variation_paths": ["assets/sounds/gun_shot.wav"],
        "volume": 0.2,
    },
    {
        "id": 13,
        "id_str": "sound.bullet_hit",
        "variation_paths": ["assets/sounds/bullet_hit.wav"],
        "volume": 1,
    },
    {
        "id": 14,
        "id_str": "sound.grab",
        "variation_paths": ["assets/sounds/grab.wav"],
        "volume": 1,
    },
    {
        "id": 15,
        "id_str": "sound.run",
        "variation_paths": [
            "assets/sounds/run_0.wav",
            "assets/sounds/run_1.wav",
            "assets/sounds/run_2.wav",
        ],
        "volume": 1,
    },
    {
        "id": 16,
        "id_str": "sound.coins",
        "variation_paths": ["assets/sounds/coins.wav"],
        "volume": 0.3,
    },
    {
        "id": 17,
        "id_str": "sound.menu_open",
        "variation_paths": ["assets/sounds/menu_open.wav"],
        "volume": 0.3,
    },
    {
        "id": 18,
        "id_str": "sound.menu_close",
        "variation_paths": ["assets/sounds/menu_close.wav"],
        "volume": 0.3,
    },
    {
        "id": 19,
        "id_str": "sound.menu_select",
        "variation_paths": ["assets/sounds/menu_select.wav"],
        "volume": 0.3,
    },
    {
        "id": 20,
        "id_str": "sound.chat",
        "variation_paths": ["assets/sounds/chat.wav"],
        "volume": 0.3,
    },
    {
        "id": 21,
        "id_str": "sound.door_opened",
        "variation_paths": ["assets/sounds/door_opened.wav"],
        "volume": 1,
    },
    {
        "id": 22,
        "id_str": "sound.door_closed",
        "variation_paths": ["assets/sounds/door_closed.wav"],
        "volume": 1,
    },
]
