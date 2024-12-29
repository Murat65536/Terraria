from typing import Generator
from pygame.image import load
from pygame import Surface
from random import randint
from enum import Enum

class Biome(Enum):
    FOREST = 1

class Background:
    def __init__(
        self, images: tuple[str, ...], offset: int, animation_delay: float
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
    def __init__(self, parallaxes: dict[Biome, tuple[tuple[Background, ...], ...]]) -> None:
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


BACKGROUND_DATA: BackgroundData = BackgroundData(
    {
        Biome.FOREST:
    (
        (
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_0/background_0.png",
                ),
                0,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_0/background_1.png",
                ),
                25,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_0/background_2.png",
                ),
                25,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_0/background_3.png",
                ),
                -100,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_0/background_4.png",
                ),
                -50,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_0/background_5.png",
                ),
                175,
                0,
            ),
        ),
        (
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_1/background_0.png",
                ),
                0,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_1/background_1.png",
                ),
                -50,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_1/background_2.png",
                ),
                -25,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_1/background_3.png",
                ),
                25,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_1/background_4.png",
                ),
                100,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_1/background_5.png",
                ),
                175,
                0,
            ),
        ),
        (
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_2/background_0.png",
                ),
                0,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_2/background_1.png",
                ),
                -50,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_2/background_2.png",
                ),
                -25,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_2/background_3.png",
                ),
                25,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_2/background_4.png",
                ),
                100,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_2/background_5.png",
                ),
                175,
                0,
            ),
        ),
        (
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_3/background_0.png",
                ),
                0,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_3/background_1.png",
                ),
                -25,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_3/background_2.png",
                ),
                0,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_3/background_3.png",
                ),
                75,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_3/background_4.png",
                ),
                350,
                0,
            ),
        ),
        (
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_4/background_0.png",
                ),
                0,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_4/background_1.png",
                    "assets/images/backgrounds/backgrounds/background_4/background_2.png",
                    "assets/images/backgrounds/backgrounds/background_4/background_3.png",
                ),
                100,
                0.5,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_4/background_4.png",
                    "assets/images/backgrounds/backgrounds/background_4/background_5.png",
                    "assets/images/backgrounds/backgrounds/background_4/background_6.png",
                ),
                225,
                0.5,
            ),
        ),
        (
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_5/background_0.png",
                ),
                0,
                0,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_5/background_1.png",
                    "assets/images/backgrounds/backgrounds/background_5/background_2.png",
                    "assets/images/backgrounds/backgrounds/background_5/background_3.png",
                ),
                100,
                0.5,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_5/background_4.png",
                    "assets/images/backgrounds/backgrounds/background_5/background_5.png",
                    "assets/images/backgrounds/backgrounds/background_5/background_6.png",
                ),
                225,
                0.5,
            ),
            Background(
                (
                    "assets/images/backgrounds/backgrounds/background_5/background_7.png",
                ),
                200,
                0,
            ),
        ),
    )
    }
)
