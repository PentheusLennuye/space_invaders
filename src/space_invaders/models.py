"""The sprites."""

from dataclasses import dataclass
from typing import Protocol

import pygame

# constants

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 8
SCREEN_WIDTH = 224
SCREEN_HEIGHT = 256


class GameSprite(pygame.sprite.Sprite):
    """A basic sprite, used for all game pieces on the board."""

    def __init__(self, x: int, y: int, frames: list[pygame.Surface]):
        super().__init__()

        self.frames: list[pygame.Surface] = frames
        self.frame_index: int = 0
        self.image = self.frames[self.frame_index]
        self.rect: pygame.Rect = pygame.Rect(
            x, SCREEN_HEIGHT - (y * 10), SPRITE_WIDTH, SPRITE_HEIGHT
        )

    def update(self, x: int, y: int):
        """Change the rect and image."""
        self.frame_index = not self.frame_index
        self.image = self.frames[self.frame_index]
        self.rect.topleft = (x, SCREEN_HEIGHT - (y * 10))


@dataclass
class Piece(Protocol):  # "Protocol" permits the use of interfaces.
    """A piece is a any object on the board."""

    pos_x: int
    pos_y: int
    sprite: GameSprite


@dataclass
class Cannon(Piece):
    """The player's ride."""

    pos_x: int
    pos_y: int
    sprite: GameSprite


@dataclass
class Invader(Piece):
    """A squid, crab, octopus, or UFO."""

    pos_x: int
    pos_y: int
    sprite: GameSprite
    value: int


@dataclass
class SpriteCrop:
    """Where to find the sprint images in the sprite sheet."""

    cannon = ((0, 0), (16, 0), (32, 0))
    laser = ((0, 8), (16, 8), (32, 8))
    invaders = (
        ((0, 32), (16, 32), (16, 8)),  # OCTOPUS
        ((0, 24), (16, 24), (16, 8)),  # CRAB
        ((0, 16), (16, 16), (16, 8)),  # SQUID
    )
