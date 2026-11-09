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
CANNON_START_X = int(models.SCREEN_WIDTH / 2) - int(models.SPRITE_WIDTH / 2)
CANNON_START_Y = 2
LASER_START_X = int(models.SCREEN_WIDTH / 2)  # Inside the cannon
LASER_START_Y = 2 * 10  # projectiles y is in pixels, not rows

# Constants
FPS = 60  # Simulate 1978 technology. 60 frames per second.
RIGHT = 1
LEFT = -1
CONCURRENT_INVADER_BULLETS = 5

# Invaders

OCTOPUS = 0
CRAB = 1
SQUID = 2
CANNON = 3
LASER = 4
BULLETS = 5

POINTS_VALUE = (10, 20, 30)

# "Macros" used for easy modification
P_QUIT = pygame.K_q
P_LEFT = pygame.K_a
P_RIGHT = pygame.K_s
P_FIRE = pygame.K_SPACE


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

    # Now, the cannon
    animations.append([])
    for i in models.SpriteCrop.cannon:
        animations[CANNON].append(
            sheet.subsurface(
                pygame.Rect(
                    i[0], i[1], models.SPRITE_WIDTH, models.SPRITE_HEIGHT
                )
            )
        )

    # The laser
    animations.append([])
    for i in models.SpriteCrop.laser:
        animations[LASER].append(
            sheet.subsurface(pygame.Rect(i[0], i[1], 3, 8))
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
    fired: bool = False
    fleet = deploy_fleet(animations)
    fleet_direction = RIGHT
    invader_move_index = 55  # Used to simulate 1978
    cannon = deploy_cannon(animations[CANNON])
    laser = deploy_laser(cannon, animations[LASER])
    laser_delay_frames = 16  # Missing aliens delays reload for 16 frames.

    while True:
        invader_move_index -= 1
        # Check collision ──────────────────────────────────────────────

        # Get player input ─────────────────────────────────────────────
        for event in pygame.event.get():
            # Quit the game if the boss shows up.
            if player_quits(event):
                return False

            # Send the laser on its way
            fired = fired | player_fires(event)

        # Get the cannon movement. get_pressed() is used for held-down
        # keys.
        keys = pygame.key.get_pressed()

        # Move player ──────────────────────────────────────────────────
        cannon.pos_x = move_cannon_on_command(keys, cannon)

        # Delays ───────────────────────────────────────────────────────

        # Delay projectiles
        if fired:
            laser.pos_x, laser.pos_y, laser_delay_frames, fired = delay_reload(
                laser_delay_frames, laser, cannon
            )

        # Move projectiles ─────────────────────────────────────────────
        laser.pos_x, laser.pos_y = move_laser(fired, cannon, laser)

        # Move enemy, one invader per frame ────────────────────────────
        if invader_move_index >= len(fleet) - 1:
            fleet_direction, fleet = move_fleet(fleet_direction, fleet)

        # Pygame screen drawing ────────────────────────────────────────
        procedure_update_sprites(cannon, fleet, laser, invader_move_index)
        procedure_draw_screen(screen, cannon, laser, fleet)

        # Update invader index
        if invader_move_index < 0:
            invader_move_index = len(fleet)
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


def deploy_cannon(
    animations: list[pygame.Surface],
) -> models.Piece:
    """Set up a single cannon in the right place."""

    return models.Cannon(
        CANNON_START_X,
        CANNON_START_Y,
        models.GameSprite(CANNON_START_X, CANNON_START_Y, animations),
    )


def deploy_laser(
    cannon: models.Piece,
    animations: list[pygame.Surface],
) -> models.Projectile:
    """Set up a single laser bolt in the right place."""

    return models.Laser(
        cannon.pos_x + int(models.SPRITE_WIDTH / 2),
        LASER_START_Y,
        models.GameProjectileSprite(
            cannon.pos_x + int(models.SPRITE_WIDTH / 2),
            LASER_START_Y,
            animations,
        ),
    )


def player_fires(event):
    """Did the player hit fire or not."""
    return event.type == pygame.KEYDOWN and event.key == P_FIRE


def move_cannon_on_command(
    keys: pygame.key.ScancodeWrapper, cannon: models.Piece
):
    """Interpret the player mashing the keys."""
    player_move = 0
    if keys[P_RIGHT]:
        player_move += RIGHT
    if keys[P_LEFT]:
        player_move += LEFT
    return move_cannon(player_move, cannon)


def move_cannon(command: int, cannon: models.Piece) -> int:
    """Move cannon horizontally but not past the screen edge."""

    if (
        command == RIGHT
        and cannon.pos_x >= models.SCREEN_WIDTH - models.SPRITE_WIDTH
    ):
        return cannon.pos_x

    if command == LEFT and cannon.pos_x <= 0:
        return cannon.pos_x

    return cannon.pos_x + command


def delay_reload(
    laser_delay_frames: int,
    laser: models.Projectile,
    cannon: models.Piece,
) -> tuple[int, int, int, bool]:
    """
    If the player missed the aliens, delay 16 frames before
    reload.
    """
    if laser.pos_y >= models.SCREEN_HEIGHT - 20:
        if laser_delay_frames > 0:
            return laser.pos_x, laser.pos_y, laser_delay_frames - 1, True
        return cannon.pos_x, LASER_START_Y, 16, False
    return laser.pos_x, laser.pos_y, 16, True


def move_laser(
    fired: bool, cannon: models.Piece, laser: models.Projectile
) -> tuple[int, int]:
    """
    Move laser horizontally with the cannon, but freely when fired 4
    pixels per frame.
    """
    if laser.pos_y == models.SCREEN_HEIGHT - 20:
        return laser.pos_x, laser.pos_y
    if fired:
        return laser.pos_x, laser.pos_y + 4
    return cannon.pos_x + 7, laser.pos_y


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


# ──────────────────────────────────────────────────────────────────────
# PYGAME procedures outside game logic
# ──────────────────────────────────────────────────────────────────────


def procedure_update_sprites(
    cannon: models.Piece,
    fleet: list[models.Invader],
    laser: models.Projectile,
    invader_move_index: int,
) -> None:
    """Procedure to make sure the sprint boxes match the positions."""
    cannon.sprite.update(cannon.pos_x, cannon.pos_y)
    fleet[invader_move_index].sprite.update(
        fleet[invader_move_index].pos_x,
        fleet[invader_move_index].pos_y,
        not fleet[invader_move_index].sprite.frame_index,
    )
    laser.sprite.update(laser.pos_x, laser.pos_y)


def procedure_draw_screen(
    screen: pygame.Surface,
    cannon: models.Piece,
    laser: models.Projectile,
    fleet: list[models.Invader],
) -> None:
    """Procedure to draw the game on screen."""
    screen.fill((0, 0, 0))
    screen.blit(cannon.sprite.image, cannon.sprite.rect)
    for i in fleet:
        screen.blit(i.sprite.image, i.sprite.rect)
    screen.blit(laser.sprite.image, laser.sprite.rect)

    pygame.display.flip()


if __name__ == "__main__":
    # In Python, the highest scope is called main.
    start()
