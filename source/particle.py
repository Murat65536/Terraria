import math
import random

import commons
import entity_manager
import pygame


class Particle:
    """
    Holds all the information required to update and draw a single particle
    """
    def __init__(
        self,
        position,
        color,
        life,
        magnitude,
        size,
        angle,
        spread,
        gravity,
        velocity: float = 0,
        outline=True,
    ):
        self.position = position
        self.life = life + (random.random() * life * 0.1 - life * 0.05)  # How long it lasts for (randomized slightly)
        self.initLife = self.life
        self.color = color
        self.size = size + random.random() * size * 0.1 - size * 0.05  # How large it will be (randomized slightly)
        self.initSize = self.size
        self.outline = outline
        if velocity == 0:
            if angle == 0:
                angle = random.random() * math.pi * 2 - math.pi  # Random angle
            else:
                angle += random.random() * spread - spread * 0.5  # Set angle + random spread in set range
            self.velocity = (
                math.cos(angle) * magnitude,
                math.sin(angle) * magnitude,
            )  # Velocity from angle and magnitude
        else:
            self.velocity = (velocity, velocity)
        self.gravity = gravity

    def update(self):
        """
        Moves the particle, updates it's time remaining and uses this time remaining to calculate it's size
        """
        drag_factor = 1.0 - commons.DELTA_TIME * 2

        self.velocity = (
            self.velocity[0] * drag_factor,
            self.velocity[1] * drag_factor + self.gravity * commons.GRAVITY * commons.DELTA_TIME,
        )
        self.position = (
            self.position[0] + self.velocity[0] * commons.DELTA_TIME * commons.BLOCK_SIZE,
            self.position[1] + self.velocity[1] * commons.DELTA_TIME * commons.BLOCK_SIZE,
        )

        self.life -= commons.DELTA_TIME  # Change life

        self.size = self.initSize * self.life / self.initLife  # Change size based on life and initial size

        if self.life <= 0:  # Remove the particle
            entity_manager.particles.remove(self)

    def draw(self):
        """
        Draws the particle instance
        """
        if self.outline:
            border = pygame.Surface((self.size + 2, self.size + 2), pygame.SRCALPHA)
            border.fill((0, 0, 0))
            border = pygame.transform.rotate(border, self.velocity[0] * self.velocity[1] * 10)
            rect = border.get_rect()
            rect.center = (
                self.position[0] - self.size * 0.5 - entity_manager.camera_position[0] + commons.WINDOW_WIDTH * 0.5,
                self.position[1] - self.size * 0.5 - entity_manager.camera_position[1] + commons.WINDOW_HEIGHT * 0.5,
            )
            commons.screen.blit(border, rect)
        particle = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        particle.fill(self.color)
        particle = pygame.transform.rotate(particle, self.velocity[0] * self.velocity[1] * 10)
        rect = particle.get_rect()
        rect.center = (
            self.position[0] - self.size * 0.5 - entity_manager.camera_position[0] + commons.WINDOW_WIDTH * 0.5,
            self.position[1] - self.size * 0.5 - entity_manager.camera_position[1] + commons.WINDOW_HEIGHT * 0.5,
        )
        commons.screen.blit(particle, rect)
