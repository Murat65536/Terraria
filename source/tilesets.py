import pygame
import commons
from os import listdir


class Tileset:
    def __init__(
        self,
        folder_path: str,
        width: int,
        height: int,
        rows: int = 1,
        columns: int = 1,
        x_offset: int = 0,
        y_offset: int = 0,
        scale_width: int | None = None,
        scale_height: int | None = None,
        colorkey: pygame.Color | None = None,
        alpha: int = 255,
    ) -> None:
        self.tileset: list[list[pygame.Surface]] = []
        for image_path in listdir(folder_path):
            tiles: list[pygame.Surface] = []
            image: pygame.Surface = pygame.image.load(
                folder_path + image_path
            ).convert_alpha()
            for column in range(columns):
                for row in range(rows):
                    surface = pygame.Surface(
                        (width, height),
                        pygame.SRCALPHA,
                    )
                    surface.blit(
                        image,
                        (
                            -row * (width + x_offset),
                            -column * (height + y_offset),
                        ),
                    )
                    if scale_width is not None:
                        surface = pygame.transform.scale(
                            surface, (scale_width, surface.get_height())
                        )
                    if scale_height is not None:
                        surface = pygame.transform.scale(
                            surface, (surface.get_width(), scale_height)
                        )
                    surface.set_colorkey(colorkey)
                    surface.set_alpha(alpha)
                    tiles.append(surface)
            self.tileset.append(tiles)

    def __getitem__(self, index) -> tuple[pygame.Surface]:
        return tuple(self.tileset[index])


tile_masks: Tileset = Tileset(
    "assets/images/tile_masks/",
    8,
    8,
    rows=13,
    columns=5,
    x_offset=1,
    y_offset=1,
    scale_width=commons.BLOCK_SIZE,
    scale_height=commons.BLOCK_SIZE,
)
misc_gui: Tileset = Tileset(
    "assets/images/gui/",
    48,
    48,
    rows=11,
    colorkey=pygame.Color(255, 0, 255),
)
torsos: Tileset = Tileset(
    "assets/images/player/body/",
    width=20,
    height=30,
    rows=19,
    columns=4,
    scale_width=40,
    scale_height=60,
    colorkey=pygame.Color(255, 0, 255),
)
slimes: Tileset = Tileset(
    "assets/images/enemies/slime/",
    16,
    12,
    rows=3,
    columns=5,
    scale_width=32,
    scale_height=24,
    colorkey=pygame.Color(255, 0, 255),
    alpha=120,
)
head: Tileset = Tileset(
    "assets/images/player/head/",
    40,
    56,
    columns=20,
    scale_width=50,
    scale_height=70,
)
hair: Tileset = Tileset(
    "assets/images/player/hair/",
    40,
    56,
    columns=14,
    scale_width=50,
    scale_height=70,
)
