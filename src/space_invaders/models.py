"""The sprites."""

from dataclasses import dataclass
from typing import Protocol

import pygame

# constants

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 8
SCREEN_WIDTH = 224
SCREEN_HEIGHT = 256


@dataclass  # This effectively turns the object into a struct
class Piece(Protocol):
    """A piece is a any object on the board."""

    pos_x: int = 0
    pos_y: int = 0
    sprite: pygame.sprite.Sprite | None = None


@dataclass
class Invader(Piece):
    """A squid, crab, octopus, or UFO."""

    value: int = 0


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


class GameSprite(pygame.sprite.Sprite):
    """A basic sprite, used for all game pieces on the board."""

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((SPRITE_WIDTH, SPRITE_HEIGHT))
        self.rect: pygame.Rect = pygame.Rect(x, y, SPRITE_WIDTH, SPRITE_HEIGHT)

    def update(self, image: pygame.Surface, x: int, y: int):
        """Change the rect and image."""
        self.image = image
        self.rect.topleft = (x, SCREEN_HEIGHT - (y * 8 + 2))
