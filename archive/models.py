#!/usr/bin/env python3
"""
Space Invaders

An exercise in computer language migration. Plus it might be fun.
"""

from typing import Protocol, Self

import pygame

# Constants ───────────────────────────────────────────────────────────────────

SCREEN_X = 224
SCREEN_Y = 256

SPRITE_SIZE_X = 16
SPRITE_SIZE_Y = 8


class GameSprite(Protocol):
    """Python Interface."""

    frames: list[pygame.Surface]
    frame_index: int
    image: pygame.Surface
    rect: pygame.Rect
    pos_x: int
    pos_y: int

    def update(self) -> None:
        """Ensure internal consistency."""

    def get_fired(self) -> bool:
        """Getter fired"""
        return False

    def set_fired(self) -> None:
        """Setter fired"""

    def get_pos_x(self) -> int:
        """Getter pos_x"""
        return 0

    def get_pos_y(self) -> int:
        """Getter pos_y"""
        return 0

    def reset(self, c: Self) -> None:
        """Return to the starting state."""


class Cannon(pygame.sprite.Sprite):
    """Keep the image separate from the logic."""

    def __init__(self, frames: list[pygame.Surface], x: int, y: int):
        super().__init__()
        self.fired: bool = False
        self.frames: list[pygame.Surface] = frames
        self.frame_index: int = 0
        self.image: pygame.Surface = self.frames[self.frame_index]
        self.rect: pygame.Rect = pygame.Rect(x, y, SPRITE_SIZE_X, SPRITE_SIZE_Y)
        self.pos_x: int = x
        self.pos_y: int = y
        self.update()

    def update(self):
        """Ensure the rect matches pos_x"""
        self.rect.topleft = (self.pos_x, SCREEN_Y - self.pos_y)
        self.image = self.frames[self.frame_index]

    def get_fired(self) -> bool:
        """Getter fired"""
        return self.fired

    def set_fired(self, fired: bool) -> None:
        """Setter fired"""
        self.fired = fired

    def get_pos_x(self) -> int:
        return self.pos_x

    def get_pos_y(self) -> int:
        return self.pos_x

    def reset(self) -> None:
        """Come back to the starting state."""


class Laser(pygame.sprite.Sprite):
    """Attributes pertaining to the player's shot."""

    def __init__(self, frames: list[pygame.Surface], x: int, y: int):
        super().__init__()
        self.frames: list[pygame.Surface] = frames
        self.frame_index: int = 0
        self.image: pygame.Surface = self.frames[self.frame_index]
        self.rect: pygame.Rect = pygame.Rect(x, y, 1, 6)  # Thin bullet
        self.pos_x: int = x
        self.pos_y: int = y

    def update(self):
        """Ensure the rect matches pos_x, pos_y"""
        self.rect.topleft = (self.pos_x, SCREEN_Y - self.pos_y)
        self.image = self.frames[self.frame_index]

    def get_fired(self) -> bool:
        """Getter fired"""
        return False

    def set_fired(self) -> None:
        """Setter fired"""

    def get_pos_x(self) -> int:
        return self.pos_x

    def get_pos_y(self) -> int:
        return self.pos_x

    def reset(self, c: GameSprite) -> None:
        """Reload into the cannon."""
        self.pos_x = c.get_pos_x()
        self.pos_y = SPRITE_SIZE_Y
        self.frame_index = 0


class Invader(pygame.sprite.Sprite):
    """The bad guy in all its glory."""

    def __init__(self, frames: list[pygame.Surface], x: int = 0, y: int = 0):
        super().__init__()
        self.frames: list[pygame.Surface] = frames

        self.frame_index: int = 0
        self.image: pygame.Surface = self.frames[self.frame_index]
        self.rect: pygame.Rect = pygame.Rect(x, y, SPRITE_SIZE_X, SPRITE_SIZE_Y)
        self.pos_x: int = x
        self.pos_y: int = y

        self._create_absence()

    def _create_absence(self):
        """If blown up, let darkness take my place."""
        self.frames.append(
            pygame.Surface((SPRITE_SIZE_X, SPRITE_SIZE_Y), pygame.SRCALPHA)
        )
        self.frames[-1].fill((0, 0, 0, 0))

    def update(self):
        """Ensure the rect matches pos_x, pos_y"""
        self.rect.topleft = (self.pos_x, SCREEN_Y - self.pos_y)
        self.image = self.frames[self.frame_index]

    def get_fired(self) -> bool:
        """Getter fired"""
        return False

    def set_fired(self) -> None:
        """Setter fired"""

    def get_pos_x(self) -> int:
        return self.pos_x

    def get_pos_y(self) -> int:
        return self.pos_x

    def reset(self, c: GameSprite) -> None:
        """There is no resetting an Invader."""
