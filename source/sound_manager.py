#sound_manager.py

import pygame, random

import commons
import entity_manager

music_volume = commons.CONFIG_MUSIC_VOLUME
sound_volume = commons.CONFIG_SOUND_VOLUME
sounds = []

if commons.MUSIC:
	pygame.mixer.music.load("assets/sounds/day.mp3")
	pygame.mixer.music.set_volume(music_volume)
if commons.SOUND:
	sounds.append(pygame.mixer.Sound("assets/sounds/tink_0.wav")); #0
	sounds.append(pygame.mixer.Sound("assets/sounds/tink_1.wav")); #1
	sounds.append(pygame.mixer.Sound("assets/sounds/tink_2.wav")); #2
	sounds.append(pygame.mixer.Sound("assets/sounds/dig_0.wav")); #3
	sounds.append(pygame.mixer.Sound("assets/sounds/dig_1.wav")); #4
	sounds.append(pygame.mixer.Sound("assets/sounds/dig_2.wav")); #5
	sounds.append(pygame.mixer.Sound("assets/sounds/jump.wav")); #6
	sounds.append(pygame.mixer.Sound("assets/sounds/player_Hit_0.wav")); #7 
	sounds.append(pygame.mixer.Sound("assets/sounds/player_Hit_1.wav")); #8
	sounds.append(pygame.mixer.Sound("assets/sounds/player_Hit_2.wav")); #9
	sounds.append(pygame.mixer.Sound("assets/sounds/grass.wav")); #10
	sounds.append(pygame.mixer.Sound("assets/sounds/player_Killed.wav")); #11
	sounds.append(pygame.mixer.Sound("assets/sounds/npc_hit_0.wav")); #12
	sounds.append(pygame.mixer.Sound("assets/sounds/npc_killed_0.wav")); #13
	sounds.append(pygame.mixer.Sound("assets/sounds/grab.wav")); #14
	sounds.append(pygame.mixer.Sound("assets/sounds/run_0.wav")); #15
	sounds.append(pygame.mixer.Sound("assets/sounds/run_1.wav")); #16
	sounds.append(pygame.mixer.Sound("assets/sounds/run_2.wav")); #17
	sounds.append(pygame.mixer.Sound("assets/sounds/coins.wav")); #18
	sounds.append(pygame.mixer.Sound("assets/sounds/menu_Open.wav")); #19
	sounds.append(pygame.mixer.Sound("assets/sounds/menu_Close.wav")); #20
	sounds.append(pygame.mixer.Sound("assets/sounds/chat.wav")); #21
	sounds.append(pygame.mixer.Sound("assets/sounds/door_Opened.wav")); #22
	sounds.append(pygame.mixer.Sound("assets/sounds/door_Closed.wav")); #23
	for sound in sounds:
		sound.set_volume(sound_volume)

def change_music_volume(amount):
	global music_volume
	music_volume += amount
	music_volume = max(min(music_volume, 1), 0)
	pygame.mixer.music.set_volume(music_volume)
	entity_manager.add_message("Music volume set to " + str(round(music_volume, 2)),  (255, 223, 10), outline_color= (80, 70, 3))

def change_sound_volume(amount):
	global sound_volume
	sound_volume += amount
	sound_volume = max(min(sound_volume, 1), 0)
	for sound in sounds:
		sound.set_volume(sound_volume)

def play_music():
	pygame.mixer.music.play(loops=-1)

def stop_music():
	pygame.mixer.music.stop()
	pygame.mixer.music.rewind()