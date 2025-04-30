from typing import Generator
from pygame.image import load
from pygame import Surface
from random import randint
from enum import Enum
from commons import screen, WINDOW_WIDTH, WINDOW_HEIGHT
from math import ceil


class Biome(Enum):
    TREE = 1
    CORRUPT = 2
    JUNGLE = 3
    SNOW = 4
    HALLOW = 5
    CRIMSON = 6
    DESERT = 7
    OCEAN = 8


class Background:
    def __init__(
        self, images: tuple[str, ...], offset: int, animation_delay: float=0
    ) -> None:
        self.images: tuple[str, ...] = images
        self.offset: int = offset
        self.frame: int = 0
        self.animation_delay: float = animation_delay
        self.animation_interval: float = 0
        self.surfaces: tuple[Surface, ...] = tuple(
            load(image).convert_alpha() for image in self.images
        )
        self.position: float = randint(
            0, min(surface.get_width() for surface in self.surfaces)
        )

    def get_width(self) -> int:
        return self.surfaces[self.frame].get_width()

    def get_height(self) -> int:
        return self.surfaces[self.frame].get_height()

    def get_surface(self) -> Surface:
        return self.surfaces[self.frame]

    def move(self, amount: float) -> None:
        self.position = (
            self.position + amount
            if self.surfaces[self.frame].get_width() - self.position - amount > 0
            else 0
        )

    def animate(self, interval: float) -> None:
        if self.animation_interval >= self.animation_delay:
            self.animation_interval = 0
            self.frame = self.frame + 1 if self.frame < len(self.surfaces) - 1 else 0
        else:
            self.animation_interval += interval


class BackgroundData:
    def __init__(
        self, parallaxes: dict[Biome, tuple[tuple[Background, ...], ...]]
    ) -> None:
        self.parallaxes: dict[Biome, tuple[tuple[Background, ...], ...]] = parallaxes
        self.biome: Biome = tuple(self.parallaxes.keys())[0]
        self.selected: int = randint(0, len(self.parallaxes[self.biome]) - 1)

    def __iter__(self) -> Generator[Background, None, None]:
        for parallax in self.parallaxes[self.biome][self.selected]:
            yield parallax

    def randomize_selected(self) -> None:
        self.selected = randint(0, len(self.parallaxes[self.biome]) - 1)

    def update(self, interval: float) -> None:
        for background in self:
            background.animate(interval)

    def shift(self, increment: float, multiplier: float) -> None:
        for number, background in enumerate(self):
            background.move(increment + number * multiplier)

    def update_biome(self, biome: Biome):
        if self.biome != biome:
            self.biome = biome
            self.selected = randint(0, len(self.parallaxes[self.biome]) - 1)

    def render(self, offset_x: float=0, offset_y: float=0, magnitude: float=1) -> None:
        for number, background in enumerate(self.parallaxes[self.biome][self.selected]):
            for tile in range(ceil(WINDOW_WIDTH * 2 / background.get_width())):
                screen.blit(
                    background.get_surface(),
                    (
                        tile * background.get_width() - background.position + number * magnitude * offset_x,
                        WINDOW_HEIGHT - background.get_height() + background.offset + number * magnitude * offset_y,
                    )
                )


BACKGROUND_DATA: BackgroundData = BackgroundData(
    {
        Biome.TREE: (
            (
                Background(
                    (
                        "assets/images/backgrounds/game_backgrounds/Background_0.png",
                    ),
                    0,
                ),
                Background(
                    (
                        "assets/images/backgrounds/game_backgrounds/Background_7.png",
                    ),
                    -100,
                ),
                Background(
                    (
                        "assets/images/backgrounds/game_backgrounds/Background_8.png",
                    ),
                    -50,
                ),
                Background(
                    (
                        "assets/images/backgrounds/game_backgrounds/Background_9.png",
                    ),
                    -50,
                ),
                Background(
                    (
                        "assets/images/backgrounds/game_backgrounds/Background_10.png",
                    ),
                    0,
                ),
                Background(
                    (
                        "assets/images/backgrounds/game_backgrounds/Background_11.png",
                    ),
                    200,
                ),
            ),
            (
                Background(
                    (
                        "assets/images/backgrounds/game_backgrounds/Background_0.png",
                    ),
                    0
                ),
                Background(
                    (
                        "assets/images/backgrounds/game_backgrounds/Background_7.png",
                    ),
                    -100,
                ),
                Background(
                    (
                        "assets/images/backgrounds/game_backgrounds/Background_8.png",
                    ),
                    -50,
                ),
                Background(
                    (
                        "assets/images/backgrounds/game_backgrounds/Background_50.png",
                    ),
                    75,
                ),
                Background(
                    (
                        "assets/images/backgrounds/game_backgrounds/Background_51.png",
                    ),
                    125,
                ),
                Background(
                    (
                        "assets/images/backgrounds/game_backgrounds/Background_52.png",
                    ),
                    175,
                ),
            ),
        )
    }
)
