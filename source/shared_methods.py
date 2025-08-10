import math

import commons
import pygame
import tilesets

def normalize_vec_2(vector):
    """
    Performs vector normalization on the given vector (scalar tuple)
    """
    magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    return vector[0] / magnitude, vector[1] / magnitude

def get_on_off(bool_var):
    """
    Given a bool, returns either "on" or "off"
    """
    return "on" if bool_var else "off"

def darken_color(color: pygame.Color, factor: float = 0.6):
    """
    Multiplies all three parts of a color tuple by a given float
    """
    return int(color.r * factor), int(color.g * factor), int(color.b * factor)

def get_tier_color(tier) -> pygame.Color:
    """
    Given an item tier, a color representing that tier is returned
    """
    if tier < 0:
        return pygame.Color(150, 150, 150)  # Gray
    elif tier == 1:
        return pygame.Color(146, 146, 249)  # Blue
    elif tier == 2:
        return pygame.Color(146, 249, 146)  # Green
    elif tier == 3:
        return pygame.Color(233, 182, 137)  # Orange
    elif tier == 4:
        return pygame.Color(253, 148, 148)  # Light Red
    elif tier == 5:
        return pygame.Color(249, 146, 249)  # Pink
    elif tier == 6:
        return pygame.Color(191, 146, 233)  # Light Purple
    elif tier == 7:
        return pygame.Color(139, 237, 9)  # Lime
    elif tier == 8:
        return pygame.Color(233, 233, 9)  # Yellow
    elif tier == 9:
        return pygame.Color(3, 138, 177)  # Cyan
    elif tier == 10:
        return pygame.Color(229, 35, 89)  # Red
    elif tier > 10:
        return pygame.Color(170, 37, 241)  # Purple
    else:
        return pygame.Color(255, 255, 255)  # White

def rotate_surface(image, angle):
    """
    Given a surface and an angle, a rotation preserving edges is performed on the surface and returned
    """
    original_rect = image.get_rect()
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = original_rect.copy()
    rotated_rect.center = rotated_image.get_rect().center
    # rotated_image = rotated_image.subsurface(rotated_rect).copy()
    return rotated_image

def outline_text(
    string, color: pygame.Color, font: pygame.font.Font, outline_color: pygame.Color = pygame.Color(0, 0, 0)
):
    """
    Used to draw most text in the game, renders some text and draws it several times at varying offsets to create an outline effect
    """
    text1 = font.render(string, False, color)
    if commons.FANCY_TEXT:
        text2 = font.render(string, False, outline_color)
        surf = pygame.Surface((text2.get_width() + 2, text2.get_height() + 2))
        surf.fill((255, 0, 255))
        surf.set_colorkey((255, 0, 255))
        surf.blit(text2, (-1, -1))
        surf.blit(text2, (0, -1))
        surf.blit(text2, (1, -1))
        surf.blit(text2, (-1, 0))
        surf.blit(text2, (1, 0))
        surf.blit(text2, (-1, 1))
        surf.blit(text2, (0, 1))
        surf.blit(text2, (1, 1))

        surf.blit(text1, (0, 0))
        return surf
    else:
        return text1

def create_menu_surface(width, height, body):
    """
    Using a few measurements, and the images in the UI image list, a bordered surface image is created, with some optional text (measurements in multiples of 48 px)
    """
    surf = pygame.Surface((width * 48, height * 48))
    surf.fill((255, 0, 255))
    surf.set_colorkey((255, 0, 255))
    for i in range(width):
        for j in range(height):
            if i == 0:
                if j == 0:
                    index = 5
                elif j == height - 1:
                    index = 6
                else:
                    index = 2
            elif i == width - 1:
                if j == 0:
                    index = 8
                elif j == height - 1:
                    index = 7
                else:
                    index = 4
            elif j == 0:
                index = 1
            elif j == height - 1:
                index = 3
            else:
                index = 9

            surf.blit(tilesets.misc_gui[index], (i * 48, j * 48))
    usable_width = width * 48 - 60
    lines = [""]
    words = body.split(" ")
    line_width = 0
    for word in words:
        line_width += commons.DEFAULT_FONT.size(" " + word)[0]
        if line_width > usable_width:
            line_width = 0
            lines.append(word)
        else:
            lines[-1] += " " + word
    for i in range(len(lines)):
        surf.blit(
            outline_text(lines[i], pygame.Color(255, 255, 255), commons.DEFAULT_FONT),
            (15, 15 + i * 20),
        )
    return surf

def color_surface(gray_surf, col) -> pygame.Surface:
    """
    Uses the pygame.BLEND_RGB_ADD blend flag to color a grayscale image with the given color
    """
    if col == ():
        col = (0, 0, 0)
    x = gray_surf.get_width()
    y = gray_surf.get_height()
    surf = pygame.Surface((x, y))
    surf.fill((255, 255, 255))
    surf.set_colorkey((255, 255, 255))  # set the colorkey to white
    surf.blit(gray_surf, (0, 0))  # create a surf with the given hair and white background
    color = pygame.Surface((x, y))
    color.fill(col)  # create a blank surf with the color of the hair
    surf.blit(color, (0, 0), None, pygame.BLEND_RGB_ADD)  # blit the new surf to the hair with an add blend flag
    return surf

def transparent_color_surface(surface: pygame.Surface, col: pygame.Color) -> pygame.Surface:
    """
    Uses the pygame.BLEND_RGB_ADD blend flag to color a transparent grayscale image with the given color
    """
    colored_surface = surface.copy()
    color = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    color.fill(col)
    colored_surface.blit(color, (0, 0), None, pygame.BLEND_RGB_MULT)
    return colored_surface

def lerp_float(a, b, t):
    """
    Simple linear interpolation
    """
    return a + (b - a) * t


def smooth_zero_to_one(zero_to_one_float, iterations):
    for _ in range(iterations):
        zero_to_one_float = math.sin(zero_to_one_float * math.pi - math.pi * 0.5)
        zero_to_one_float = zero_to_one_float * 0.5 + 0.5
    return zero_to_one_float


def ease_out_zero_to_one(zero_to_one_float, iterations):
    for _ in range(iterations):
        zero_to_one_float = math.sin(zero_to_one_float * math.pi * 0.5)
    return zero_to_one_float


def ease_in_zero_to_one(zero_to_one_float, iterations):
    for _ in range(iterations):
        zero_to_one_float = 1.0 + math.sin(zero_to_one_float * math.pi * 0.5 - math.pi * 0.5)
    return zero_to_one_float

def draw_hitbox(
    camera_position_x: float, camera_position_y: float, x: float, y: float, width: float, height: float
) -> None:
    """
    Draws a hitbox
    """
    if commons.HITBOXES:
        pygame.draw.rect(
            commons.screen,
            (255, 0, 0),
            pygame.Rect(
                x - camera_position_x + commons.WINDOW_WIDTH * 0.5,
                y - camera_position_y + commons.WINDOW_HEIGHT * 0.5,
                width,
                height,
            ),
            1,
        )
