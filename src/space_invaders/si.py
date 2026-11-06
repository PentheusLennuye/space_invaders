#!/usr/bin/env python3
"""
SI a Space Invaders clone.

The point of the exercise is to write out a simple arcade game using
computer science techniques rather than just hacking away.

The first attempt will be in Python, my work language, and then use it
as pseudo-code for other, more difficult languages.
"""

import pygame

from space_invaders import models

SCREEN_X = 224
SCREEN_Y = 256
SPRITE_WIDTH = 16
SPRITE_HEIGHT = 8
INVADER_START_X = int(SCREEN_X / 2) - (int(SPRITE_WIDTH / 2) * 11)
INVADER_START_Y = 24  # The bottom row of the invaders. 1 row = 8 pixels.


# Constants
FPS = 60  # Simulate 1978 technology. 60 frames per second.
RIGHT = 1
LEFT = -1

# Invaders

OCTOPUS = 0
CRAB = 1
SQUID = 2

POINTS_VALUE = (10, 20, 30)

# "Macros" used for easy modification
P_QUIT = pygame.K_q


def start():
    """
    Load sprites into memory, set up the attract mode, and wait for
    'coins'.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    sprite_sheet = pygame.image.load(
        "src/extra/sprite_sheet.png"
    ).convert_alpha()
    running = True
    while running is True:
        for event in pygame.event.get():
            if player_quits(event):
                running = False
                break
        # Loop ─────────────────────────────────────────────────────╮
        #   Attract screen                                          ↓
        # ↑ Coin accepted screen
        # ╰─────────────────────────────────────────────────────────╯

    running = game(screen, sprite_sheet)
    pygame.quit()


def player_quits(event: pygame.event.Event) -> bool:
    """Check all the ways the player can signal quit."""
    if event.type == pygame.QUIT:
        return True
    return (
        event.type == pygame.KEYDOWN
        and event.key == P_QUIT
        and (event.mod & pygame.KMOD_CTRL != 0)
    )


def game(screen: pygame.Surface, sprite_sheet: pygame.Surface) -> bool:
    """The main game loop. 10 cents a pop in 1978!"""

    clock = pygame.time.Clock()
    fleet = deploy_fleet(sprite_sheet)
    fleet_direction = RIGHT

    while True:
        # Check collision ──────────────────────────────────────────────

        # Get player input ─────────────────────────────────────────────

        # Move player ──────────────────────────────────────────────────

        # Move enemy ───────────────────────────────────────────────────
        fleet_direction, fleet = move_fleet(fleet_direction, fleet)

        # Move projectiles ─────────────────────────────────────────────

        # Draw screen ──────────────────────────────────────────────────
        screen.fill((0, 0, 0))
        pygame.display.flip()

        # Player interaction, dictated by external controls
        # Quit the game if the boss shows up.
        for event in pygame.event.get():
            if player_quits(event):
                return False

        # FPS wait
        clock.tick(FPS)


def deploy_fleet(sheet: pygame.Surface | None = None) -> list[models.Invader]:
    """
    Create the 11x5 block of invaders.

    The array is arranged top-to-bottom, left-to-right so that the first
    element is the left-most invader, and the last one is the right-most
    invader.

    The sprites are attached in runtime.
    """
    invaders: list[models.Invader] = []
    x = INVADER_START_X
    i: int = 0

    while i < 11:
        i += 1
        y = INVADER_START_Y
        for invader_type in (OCTOPUS, OCTOPUS, CRAB, CRAB, SQUID):
            invaders.append(
                models.Invader(
                    x, y, assign_sprite(sheet), POINTS_VALUE[invader_type]
                )
            )
            y += 1
        x += SPRITE_WIDTH

    return invaders


def assign_sprite(
    sheet: pygame.Surface | None = None,
) -> pygame.sprite.Sprite | None:
    """Assign the animations and hit boxes to the invaders."""
    if sheet is None:
        return None
    return None


def move_fleet(
    direction: int, fleet: list[models.Invader]
) -> tuple[int, list[models.Invader]]:
    """
    Move the fleet left, right or down.

    Although the game is simple, I will still use immutable data.
    """
    w_fleet: list[models.Invader] = fleet.copy()

    if direction == RIGHT and w_fleet[-1].pos_x >= SCREEN_X - SPRITE_WIDTH:
        for i in w_fleet:
            i.pos_y += 1
        return LEFT, w_fleet

    if direction == LEFT and w_fleet[0].pos_x <= 0:
        for i in w_fleet:
            i.pos_y += 1
        return RIGHT, w_fleet

    for i in w_fleet:
        i.pos_x += direction

    return direction, w_fleet


if __name__ == "__main__":
    # In Python, the highest scope is called main.
    start()
