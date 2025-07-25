import commons
import entity_manager
import pygame

music_volume = commons.CONFIG_MUSIC_VOLUME
sound_volume = commons.CONFIG_SOUND_VOLUME
sounds: list[pygame.mixer.Sound] = []

if commons.MUSIC:
    pygame.mixer.music.load("assets/sounds/day.mp3")
    pygame.mixer.music.set_volume(music_volume)
if commons.SOUND:
    sounds.append(pygame.mixer.Sound("assets/sounds/tink_0.wav"))
    # 0
    sounds.append(pygame.mixer.Sound("assets/sounds/tink_1.wav"))
    # 1
    sounds.append(pygame.mixer.Sound("assets/sounds/tink_2.wav"))
    # 2
    sounds.append(pygame.mixer.Sound("assets/sounds/dig_0.wav"))
    # 3
    sounds.append(pygame.mixer.Sound("assets/sounds/dig_1.wav"))
    # 4
    sounds.append(pygame.mixer.Sound("assets/sounds/dig_2.wav"))
    # 5
    sounds.append(pygame.mixer.Sound("assets/sounds/jump.wav"))
    # 6
    sounds.append(pygame.mixer.Sound("assets/sounds/player_hit_0.wav"))
    # 7
    sounds.append(pygame.mixer.Sound("assets/sounds/player_hit_1.wav"))
    # 8
    sounds.append(pygame.mixer.Sound("assets/sounds/player_hit_2.wav"))
    # 9
    sounds.append(pygame.mixer.Sound("assets/sounds/grass.wav"))
    # 10
    sounds.append(pygame.mixer.Sound("assets/sounds/player_killed.wav"))
    # 11
    sounds.append(pygame.mixer.Sound("assets/sounds/npc_hit_0.wav"))
    # 12
    sounds.append(pygame.mixer.Sound("assets/sounds/npc_killed_0.wav"))
    # 13
    sounds.append(pygame.mixer.Sound("assets/sounds/grab.wav"))
    # 14
    sounds.append(pygame.mixer.Sound("assets/sounds/run_0.wav"))
    # 15
    sounds.append(pygame.mixer.Sound("assets/sounds/run_1.wav"))
    # 16
    sounds.append(pygame.mixer.Sound("assets/sounds/run_2.wav"))
    # 17
    sounds.append(pygame.mixer.Sound("assets/sounds/coins.wav"))
    # 18
    sounds.append(pygame.mixer.Sound("assets/sounds/menu_open.wav"))
    # 19
    sounds.append(pygame.mixer.Sound("assets/sounds/menu_close.wav"))
    # 20
    sounds.append(pygame.mixer.Sound("assets/sounds/chat.wav"))
    # 21
    sounds.append(pygame.mixer.Sound("assets/sounds/door_opened.wav"))
    # 22
    sounds.append(pygame.mixer.Sound("assets/sounds/door_closed.wav"))
    # 23
    for sound in sounds:
        sound.set_volume(sound_volume)


def change_music_volume(amount: float) -> None:
    global music_volume
    music_volume += amount
    music_volume = max(min(music_volume, 1), 0)
    pygame.mixer.music.set_volume(music_volume)
    entity_manager.add_message(
        "Music volume set to " + str(round(music_volume, 2)),
        pygame.Color(255, 223, 10),
        outline_color=pygame.Color(80, 70, 3),
    )


def change_sound_volume(amount: float) -> None:
    global sound_volume
    sound_volume += amount
    sound_volume = max(min(sound_volume, 1), 0)
    for sound in sounds:
        sound.set_volume(sound_volume)


def play_music() -> None:
    pygame.mixer.music.play(loops=-1)


def stop_music() -> None:
    pygame.mixer.music.stop()
    pygame.mixer.music.rewind()
