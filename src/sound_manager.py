#sound_manager.py

import pygame, random
from pygame.locals import *

import commons
import entity_manager

def Initialize():
	global sounds, soundVolume, musicVolume

	musicVolume = commons.CONFIG_MUSIC_VOLUME
	soundVolume = commons.CONFIG_SOUND_VOLUME

	if commons.MUSIC:
		try:
			pygame.mixer.music.load("res/sounds/day.mp3")
			pygame.mixer.music.set_volume(musicVolume)
			pygame.mixer.music.play()
			print("Running with music.")
		except pygame.error:
			print("Music failed to load, running without music.")
			commons.MUSIC = False
	if commons.SOUND:
		try:
			soundVolume = 0.5
			sounds = []
			sounds.append(pygame.mixer.Sound("res/sounds/tink_0.wav")); #0
			sounds.append(pygame.mixer.Sound("res/sounds/tink_1.wav")); #1
			sounds.append(pygame.mixer.Sound("res/sounds/tink_2.wav")); #2
			sounds.append(pygame.mixer.Sound("res/sounds/dig_0.wav")); #3
			sounds.append(pygame.mixer.Sound("res/sounds/dig_1.wav")); #4
			sounds.append(pygame.mixer.Sound("res/sounds/dig_2.wav")); #5
			sounds.append(pygame.mixer.Sound("res/sounds/jump.wav")); #6
			sounds.append(pygame.mixer.Sound("res/sounds/player_Hit_0.wav")); #7 
			sounds.append(pygame.mixer.Sound("res/sounds/player_Hit_1.wav")); #8
			sounds.append(pygame.mixer.Sound("res/sounds/player_Hit_2.wav")); #9
			sounds.append(pygame.mixer.Sound("res/sounds/grass.wav")); #10
			sounds.append(pygame.mixer.Sound("res/sounds/player_Killed.wav")); #11
			sounds.append(pygame.mixer.Sound("res/sounds/npc_hit_0.wav")); #12
			sounds.append(pygame.mixer.Sound("res/sounds/npc_killed_0.wav")); #13
			sounds.append(pygame.mixer.Sound("res/sounds/grab.wav")); #14
			sounds.append(pygame.mixer.Sound("res/sounds/run_0.wav")); #15
			sounds.append(pygame.mixer.Sound("res/sounds/run_1.wav")); #16
			sounds.append(pygame.mixer.Sound("res/sounds/run_2.wav")); #17
			sounds.append(pygame.mixer.Sound("res/sounds/coins.wav")); #18
			sounds.append(pygame.mixer.Sound("res/sounds/menu_Open.wav")); #19
			sounds.append(pygame.mixer.Sound("res/sounds/menu_Close.wav")); #20
			sounds.append(pygame.mixer.Sound("res/sounds/chat.wav")); #21
			sounds.append(pygame.mixer.Sound("res/sounds/door_Opened.wav")); #22
			sounds.append(pygame.mixer.Sound("res/sounds/door_Closed.wav")); #23
			for sound in sounds:
				sound.set_volume(soundVolume)
		except pygame.error:
			print("Sound failed to load, running without sound.")
			commons.SFX = False

def ChangeMusicVolume(amount):
	global musicVolume
	musicVolume += amount
	musicVolume = max(min(musicVolume, 1), 0)
	pygame.mixer.music.set_volume(musicVolume)
	entity_manager.AddMessage("Music volume set to " + str(round(musicVolume, 2)),  (255, 223, 10), outlineColor = (80, 70, 3))

def ChangeSoundVolume(amount):
	global soundVolume
	soundVolume += amount
	soundVolume = max(min(soundVolume, 1), 0)
	for sound in sounds:
		sound.set_volume(soundVolume)

# Plays the sound of the given tile being hit
def PlayHitSfx(tileID, volume = 1):	
	if tileID == 1 or tileID == 3 or tileID == 6 or tileID == 7:
		sounds[random.randint(0, 2)].play()
	elif tileID == 5 or tileID == 11 or tileID == 12:
		sounds[10].play()
	else:
		sounds[random.randint(3, 5)].play()