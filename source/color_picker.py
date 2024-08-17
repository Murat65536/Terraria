# color_picker.py

import pygame
from pygame.locals import Rect

import commons


"""================================================================================================================= 
	color_picker.COLOR_PICKER

	Stores information about a color picker
-----------------------------------------------------------------------------------------------------------------"""
class COLOR_PICKER:
	def __init__(self, position, width, height, border_size=5, surface_resolution=0.5):
		self.position = position
		self.width = width
		self.height = height
		self.section_width = width / 6
		self.border_size = border_size
		self.surface_resolution = surface_resolution
		self.colors = [
			(255, 0, 255),
			(255, 0, 0),
			(255, 255, 0),
			(0, 255, 0),
			(0, 255, 255),
			(0, 0, 255),
			(255, 0, 255)
		]
		self.selected_color = (0, 0, 0)
		self.selected_x = 0
		self.selected_y = height
		self.surface = None
		self.render_surface()
		self.rect = Rect(self.position[0] + self.border_size, self.position[1] + self.border_size, width, height)

	"""================================================================================================================= 
		color_picker.COLOR_PICKER.render_surface -> void

		Uses canvas and border size info to render the color picker surface 
	-----------------------------------------------------------------------------------------------------------------"""
	def render_surface(self):
		self.surface = pygame.Surface((self.width + self.border_size * 2,  self.height + self.border_size * 2))
		# Draw border
		pygame.draw.rect(self.surface, (90, 90, 90), Rect(0, 0, self.width+self.border_size * 2, self.height+self.border_size * 2), 0)
		pygame.draw.rect(self.surface, (128, 128, 128), Rect(2, 2, self.width+self.border_size * 2 - 4, self.height + self.border_size * 2 - 4), 0)
		pygame.draw.rect(self.surface, (110, 110, 110), Rect(4, 4, self.width+self.border_size * 2 - 8, self.height + self.border_size * 2 - 8), 0)
		surf = pygame.Surface((int(self.width * self.surface_resolution), int(self.height * self.surface_resolution)))
		for j in range(int(self.height * self.surface_resolution)):
			for i in range(int(self.width * self.surface_resolution)):
				surf.set_at((i, j), self.get_color(i / self.surface_resolution, j / self.surface_resolution))
		surf = pygame.transform.scale(surf, (self.width, self.height))
		self.surface.blit(surf, (self.border_size, self.border_size))

	"""================================================================================================================= 
		color_picker.COLOR_PICKER.get_color -> tuple

		Generates the color of the surface at a given location
	-----------------------------------------------------------------------------------------------------------------"""
	def get_color(self, i, j):
		base_color_index = int(i // self.section_width)  # Color to the left of the point
		next_color_index = (base_color_index + 1)  # Color to the right of the point
		blend = (i % self.section_width) / self.section_width
		shade = 1 - j / self.height

		col = [0, 0, 0]

		for index in range(3):
			base_color_channel = int(self.colors[base_color_index][index])
			next_color_channel = int(self.colors[next_color_index][index])

			channel = int(round(base_color_channel * (1 - blend) + next_color_channel * blend))
			if shade < 0.5:
				channel = int(channel * shade * 2)
			elif shade > 0.5:
				new_shade = shade - 0.5
				channel = int(channel * (0.5 - new_shade) * 2 + 255 * new_shade * 2)

			col[index] = channel
		return tuple(col)

	"""================================================================================================================= 
		color_picker.COLOR_PICKER.update -> void

		If the mouse is clicked over the color picker, update the selected color and location
	-----------------------------------------------------------------------------------------------------------------"""
	def update(self):
		if pygame.mouse.get_pressed()[0] and not commons.WAIT_TO_USE:
			if self.rect.collidepoint(commons.MOUSE_POSITION):
				self.selected_x = commons.MOUSE_POSITION[0] - self.position[0] - self.border_size
				self.selected_y = commons.MOUSE_POSITION[1] - self.position[1] - self.border_size
				self.selected_color = self.get_color(self.selected_x, self.selected_y)
				self.selected_color = (self.selected_color[0] * 0.5, self.selected_color[1] * 0.5, self.selected_color[2] * 0.5)

	"""================================================================================================================= 
		color_picker.COLOR_PICKER.draw -> void

		Draws the color picker's surface and draws the location of the selected color
	-----------------------------------------------------------------------------------------------------------------"""
	def draw(self):
		if (self.surface != None):
			commons.screen.blit(self.surface, self.position)

		if self.selected_x and self.selected_y != None:
			pygame.draw.circle(commons.screen, (128, 128, 128), (self.selected_x + self.position[0] + self.border_size, self.selected_y + self.position[1] + self.border_size), 5, 1)
