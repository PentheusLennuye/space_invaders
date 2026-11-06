"""The sprites."""

from dataclasses import dataclass
from typing import Protocol

import pygame


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
