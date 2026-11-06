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

INVADER_START_X = int(models.SCREEN_WIDTH / 2) - (
    int(models.SPRITE_WIDTH / 2) * 11
)
INVADER_START_Y = 18  # The bottom row of the invaders. 1 row = 8 pixels.


# Constants
FPS = 60  # Simulate 1978 technology. 60 frames per second.
RIGHT = 1
LEFT = -1

# Invaders

OCTOPUS = 0
CRAB = 1
SQUID = 2
BULLETS = 3
CANNON = 4
LASER = 5

POINTS_VALUE = (10, 20, 30)

# "Macros" used for easy modification
P_QUIT = pygame.K_q


def start():
    """
    Load sprites into memory, set up the attract mode, and wait for
    'coins'.
    """
    pygame.init()
    screen = pygame.display.set_mode(
        (models.SCREEN_WIDTH, models.SCREEN_HEIGHT)
    )
    animations = create_sprite_animations(
        pygame.image.load("src/extra/sprite_sheet.png").convert_alpha()
    )
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

        running = game(screen, animations)
    pygame.quit()


def create_sprite_animations(
    sheet: pygame.Surface,
) -> list[list[pygame.Surface]]:
    """Place the sprite images into nicely accessible memory"""
    animations = []

    # First, the aliens ------------------
    for i in range(3):
        animations.append([])
        for j in models.SpriteCrop.invaders[i]:
            animations[i].append(
                sheet.subsurface(
                    pygame.Rect(
                        j[0], j[1], models.SPRITE_WIDTH, models.SPRITE_HEIGHT
                    )
                )
            )

    # All done! --------------------------

    return animations


def player_quits(event: pygame.event.Event) -> bool:
    """Check all the ways the player can signal quit."""
    if event.type == pygame.QUIT:
        return True
    return (
        event.type == pygame.KEYDOWN
        and event.key == P_QUIT
        and (event.mod & pygame.KMOD_CTRL != 0)
    )


def game(
    screen: pygame.Surface, animations: list[list[pygame.Surface]]
) -> bool:
    """The main game loop. 10 cents a pop in 1978!"""

    clock = pygame.time.Clock()
    fleet = deploy_fleet(animations)
    fleet_direction = RIGHT
    invader_move_index = 55  # Used to simulate 1978

    while True:
        invader_move_index -= 1
        # Check collision ──────────────────────────────────────────────

        # Get player input ─────────────────────────────────────────────
        # Quit the game if the boss shows up.
        for event in pygame.event.get():
            if player_quits(event):
                return False

        # Move player ──────────────────────────────────────────────────

        # Move enemy ───────────────────────────────────────────────────
        if invader_move_index >= 54:
            fleet_direction, fleet = move_fleet(fleet_direction, fleet)

        # Move projectiles ─────────────────────────────────────────────

        # Update sprites ───────────────────────────────────────────────
        screen.fill((0, 0, 0))
        fleet[invader_move_index].sprite.update(
            fleet[invader_move_index].pos_x, fleet[invader_move_index].pos_y
        )
        for i in fleet:
            screen.blit(i.sprite.image, i.sprite.rect)

        # Draw screen ──────────────────────────────────────────────────
        pygame.display.flip()

        # Update invader index
        if invader_move_index < 0:
            invader_move_index = 55
        # FPS wait
        clock.tick(FPS)


def deploy_fleet(
    animations: list[list[pygame.Surface]],
) -> list[models.Invader]:
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
                    x,
                    y,
                    models.GameSprite(x, y, animations[invader_type]),
                    POINTS_VALUE[invader_type],
                )
            )
            y += 1
        x += models.SPRITE_WIDTH

    return invaders


def move_fleet(
    direction: int, fleet: list[models.Invader]
) -> tuple[int, list[models.Invader]]:
    """
    Move the fleet left, right or down.

    Although the game is simple, I will still use immutable data.
    """
    w_fleet: list[models.Invader] = fleet.copy()

    if (
        direction == RIGHT
        and w_fleet[-1].pos_x >= models.SCREEN_WIDTH - models.SPRITE_WIDTH
    ):
        for i in w_fleet:
            i.pos_y -= 1
        return LEFT, w_fleet

    if direction == LEFT and w_fleet[0].pos_x <= 0:
        for i in w_fleet:
            i.pos_y -= 1
        return RIGHT, w_fleet

    for i in w_fleet:
        i.pos_x += direction

    return direction, w_fleet


if __name__ == "__main__":
    # In Python, the highest scope is called main.
    start()
