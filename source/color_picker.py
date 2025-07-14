import commons
import pygame
from pygame.locals import Rect

"""=================================================================================================================
    color_picker.ColorPicker

    Stores information about a color picker
-----------------------------------------------------------------------------------------------------------------"""


class ColorPicker:
    def __init__(
        self,
        position: tuple[int, int],
        width: int,
        height: int,
        border_size: int = 5,
        surface_resolution: float = 0.5,
    ):
        self.position: tuple[int, int] = position
        self.width: int = width
        self.height: int = height
        self.section_width: float = width / 6
        self.border_size: int = border_size
        self.surface_resolution: float = surface_resolution
        self.colors: list[tuple[int, int, int]] = [
            (255, 0, 255),
            (255, 0, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 255, 255),
            (0, 0, 255),
            (255, 0, 255),
        ]
        self.selected_red: int = 0
        self.selected_green: int = 0
        self.selected_blue: int = 0
        self.selected_x: int = 0
        self.selected_y: int = height
        self.surface: pygame.Surface = pygame.Surface((0, 0))
        self.rect = Rect(
            self.position[0] + self.border_size,
            self.position[1] + self.border_size,
            width,
            height,
        )
        self.render_surface()

    """=================================================================================================================
        color_picker.ColorPicker.render_surface -> void

        Uses canvas and border size info to render the color picker surface
    -----------------------------------------------------------------------------------------------------------------"""

    def render_surface(self):
        self.surface = pygame.Surface((self.width + self.border_size * 2, self.height + self.border_size * 2))
        # Draw border
        pygame.draw.rect(
            self.surface,
            (90, 90, 90),
            Rect(
                0,
                0,
                self.width + self.border_size * 2,
                self.height + self.border_size * 2,
            ),
            0,
        )
        pygame.draw.rect(
            self.surface,
            (128, 128, 128),
            Rect(
                2,
                2,
                self.width + self.border_size * 2 - 4,
                self.height + self.border_size * 2 - 4,
            ),
            0,
        )
        pygame.draw.rect(
            self.surface,
            (110, 110, 110),
            Rect(
                4,
                4,
                self.width + self.border_size * 2 - 8,
                self.height + self.border_size * 2 - 8,
            ),
            0,
        )
        surf = pygame.Surface(
            (
                int(self.width * self.surface_resolution),
                int(self.height * self.surface_resolution),
            )
        )
        for y in range(int(self.height * self.surface_resolution)):
            for x in range(int(self.width * self.surface_resolution)):
                surf.set_at(
                    (x, y),
                    self.get_color(
                        int(x / self.surface_resolution),
                        int(y / self.surface_resolution),
                    ),
                )
        surf = pygame.transform.scale(surf, (self.width, self.height))
        self.surface.blit(surf, (self.border_size, self.border_size))

    """=================================================================================================================
        color_picker.ColorPicker.get_color -> tuple

        Generates the color of the surface at a given location
    -----------------------------------------------------------------------------------------------------------------"""

    def get_color(self, x: int, y: int) -> tuple[int, int, int]:
        base_color_index: int = int(x / self.section_width)  # Color to the left of the point
        next_color_index = base_color_index + 1  # Color to the right of the point
        blend = (x % self.section_width) / self.section_width
        shade = 1 - y / self.height

        col: list[int] = [0, 0, 0]

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
        return col[0], col[1], col[2]

    """=================================================================================================================
        color_picker.ColorPicker.update -> void

        If the mouse is clicked over the color picker, update the selected color and location
    -----------------------------------------------------------------------------------------------------------------"""

    def update(self) -> None:
        if pygame.mouse.get_pressed()[0] and not commons.WAIT_TO_USE and self.rect.collidepoint(commons.MOUSE_POSITION):
            self.selected_x = commons.MOUSE_POSITION[0] - self.position[0] - self.border_size
            self.selected_y = commons.MOUSE_POSITION[1] - self.position[1] - self.border_size
            self.selected_red, self.selected_green, self.selected_blue = self.get_color(
                self.selected_x, self.selected_y
            )
            self.selected_red = int(self.selected_red * 0.5)
            self.selected_green = int(self.selected_green * 0.5)
            self.selected_blue = int(self.selected_blue * 0.5)

    """=================================================================================================================
        color_picker.ColorPicker.draw -> void

        Draws the color picker's surface and draws the location of the selected color
    -----------------------------------------------------------------------------------------------------------------"""

    def draw(self):
        commons.screen.blit(self.surface, self.position)
        pygame.draw.circle(
            commons.screen,
            (128, 128, 128),
            (
                self.selected_x + self.position[0] + self.border_size,
                self.selected_y + self.position[1] + self.border_size,
            ),
            5,
            1,
        )
