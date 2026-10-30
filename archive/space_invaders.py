#!/usr/bin/env python3
"""
Space Invaders

An exercise in computer language migration. Plus it might be fun.
"""

from dataclasses import dataclass

import pygame

from spaceinvaders.models import Cannon, GameSprite, Invader, Laser

# Constants ───────────────────────────────────────────────────────────────────

SCREEN_X = 224
SCREEN_Y = 256

SPRITE_SIZE_X = 16
SPRITE_SIZE_Y = 8

# Time
FPS = 60  # Maximum frames per second
READY_DELAY_MS = 2000  # Prepare time for the player
GAME_OVER_DELAY_MS = 2000  # Breathing time for the player
LASER_SPEED = 4  # Pixels per frame
BULLET_SPEED = 4
CANNON_SPEED = 2
INVADER_STARTING_DELAY = 60  # One pixel per second

# Invader start
INVADER_START_ROW = 16
INVADER_NUM_ROWS = 11

# "Macros" ────────────────────────────────────────────────────────────────────
P_LEFT = pygame.K_a
P_RIGHT = pygame.K_s
P_FIRE = pygame.K_SPACE
P_QUIT = pygame.K_q  # Python does not use macros, so we cannot add a SUPER.

# Collision masks
C_CANNON = 1  # Enemy bullet hits cannon
C_TOP = 2  # Player laser hits top
C_INVADER = 4  # Player laser hits invader
C_INVADER_EXPLODING = 8

# indexes
CANNON = 0
LASER = 1
SQUID = 2
CRAB = 3
OCTOPUS = 4

LEFT = 0
RIGHT = 1


@dataclass
class GameState:
    """The game state."""

    current_player: int = 0
    p1_score: int = 0
    p1_level: int = 0
    p2_score: int = 0
    p2_level: int = 0
    num_invaders: int = 55
    num_cannons: int = 3


def main():
    """Start here."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    sprite_sheet = pygame.image.load("data/sprite_sheet.png").convert_alpha()
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


def player_quits(event: pygame.Event) -> bool:
    """Check all the ways the player can signal quit."""
    if event.type == pygame.QUIT:
        return True
    return (
        event.type == pygame.KEYDOWN
        and event.key == P_QUIT
        and (event.mod & pygame.KMOD_CTRL != 0)
    )


def game(screen: pygame.Surface, sprite_sheet: pygame.Surface) -> bool:
    """This is why people lost their dimes in 1978."""
    s = GameState()

    c = create_sprite(
        sprite_sheet, CANNON, int(SCREEN_X / 2) - int(SPRITE_SIZE_X / 2), 8
    )
    l = create_sprite(sprite_sheet, LASER, int(SCREEN_X / 2), 8)
    f = create_fleet(sprite_sheet)
    all_sprites = f + [l, c]

    collisions: int = 0
    fleet_x: int = RIGHT
    fleet_y: bool = False
    fleet_pause: int = 0
    l.reset(c)

    clock = pygame.time.Clock()

    # Loop ───────────────────────────────────────────────────────────────────────────────────────
    targets: list = []
    tick = 54
    while not game_end_conditions_met(s, f):
        if s.num_invaders == 0:
            break

        # Collision detection
        collisions, targets = check_laser_collisions(collisions, targets, c, l, f)
        fleet_x, fleet_y = check_fleet_collision(tick, fleet_x, f)

        # Invader hit
        if collisions & C_INVADER > 0:
            collisions = collisions & ones_complement(C_INVADER)
            collisions = collisions | C_INVADER_EXPLODING
            fleet_pause = 16
            explode_invaders(s, c, l, f, targets)

        # Invaders move only if there is no more debris
        if fleet_pause > 1:  # Debris disappears
            for target in targets:
                f[target].frame_index = -1  # Gone, poof!
        if fleet_pause > 0:
            fleet_pause -= 1
        else:
            # Dissipate debris
            if collisions & C_INVADER_EXPLODING > 0:
                collisions = collisions & ones_complement(C_INVADER_EXPLODING)
                for target in targets:
                    f.pop(target)
                    targets.pop(targets.index(target))

            if fleet_y:
                fleet_y = False  # Only one y movement per traverse
                for i in f:
                    i.pos_y -= SPRITE_SIZE_Y - 2

            # Simulate original hardware
            tick = (tick + 1) % s.num_invaders
            f[tick].pos_x += 1 if fleet_x == 1 else -1
            f[tick].frame_index = not f[tick].frame_index

        # Player interaction, dictated by external controls
        for event in pygame.event.get():
            if player_quits(event):
                return False
            c.set_fired(check_trigger(c, event))
        keys = pygame.key.get_pressed()
        c.pos_x = move_player(keys, c)

        # Laser Movement
        if not (collisions & C_TOP):
            l.pos_x, l.pos_y = move_laser(c, l)
        else:
            l.frame_index, collisions = laser_miss(l, collisions)
            if not (collisions & C_TOP):
                c.set_fired(False)
                l.reset(c)

        # Bullet Movement

        # Draw screen
        screen.fill((0, 0, 0))
        for sprite in all_sprites:
            sprite.update()
            screen.blit(sprite.image, (sprite.pos_x, SCREEN_Y - sprite.pos_y))
        pygame.display.flip()

        # FPS wait
        clock.tick(FPS)

    print("GAME OVER")
    pygame.time.delay(GAME_OVER_DELAY_MS)
    return True  # The system is still running


def game_end_conditions_met(s: GameState, fleet: list[Invader]) -> bool:
    """If the number of cannons is zero, or the invaders have landed."""
    if s.num_cannons <= 0:
        return True

    for i in fleet:
        if i.pos_y <= 0:
            return True

    return False


def check_trigger(c: GameSprite, event) -> bool:
    """Fire the laser on space bar."""
    if c.get_fired():
        return True
    return event.type == pygame.KEYDOWN and event.key == P_FIRE


def move_player(keys: pygame.key.ScancodeWrapper, c: Cannon) -> int:
    """Move the player right or left according to the command, up to screen limits."""
    if keys[P_LEFT] and keys[P_RIGHT]:
        return c.pos_x
    if keys[P_RIGHT]:
        return min(c.pos_x + CANNON_SPEED, SCREEN_X - SPRITE_SIZE_X)
    elif keys[P_LEFT]:
        return max(c.pos_x - CANNON_SPEED, 0)
    else:
        return c.pos_x


def move_laser(c: Cannon, l: Laser) -> tuple[int, int]:
    """Move the laser at laser speed."""
    if not c.fired:
        return c.pos_x, l.pos_y
    return l.pos_x, min(SCREEN_Y, l.pos_y + LASER_SPEED)


def laser_miss(l: Laser, collisions: int) -> tuple[int, int]:
    """
    Animate the laser splash for a delay, then cancel the collision.

    This unsophisticated, just using a counter, but that was Space Invaders for
    you.
    """
    # Simulate a static variable
    if not hasattr(laser_miss, "delay"):
        laser_miss.delay = 0

    if laser_miss.delay < 16:
        laser_miss.delay += 1
        return 2, collisions
    laser_miss.delay = 0
    return 0, collisions & ones_complement(C_TOP)


def create_sprite(sheet: pygame.Surface, t: int, x: int, y: int) -> GameSprite:
    """This factory generates sprites."""
    sprite_crop = (
        ((0, 0), (16, 0), (32, 0)),  # cannon
        ((0, 8), (16, 8), (32, 8)),  # laser
        ((0, 16), (16, 16), (16, 8)),  # squid
        ((0, 24), (16, 24), (16, 8)),  # crab
        ((0, 32), (16, 32), (16, 8)),  # octopus
    )
    sprites = (Cannon, Laser, Invader, Invader, Invader)
    frames = []
    for i in sprite_crop[t]:
        frames.append(get_frame(sheet, i[0], i[1], SPRITE_SIZE_X, SPRITE_SIZE_Y))
    return sprites[t](frames, x, y)


def get_frame(sheet, x, y, width, height):
    """Create a sprite subsurface reference."""
    return sheet.subsurface(pygame.Rect(x, y, width, height))


def create_fleet(sheet: pygame.Surface) -> list[Invader]:
    """Return a list of ready-to-murder invaders."""
    f = []
    start_x = int(SCREEN_X / 2) - 88
    x = start_x
    y = (INVADER_START_ROW + 5) * SPRITE_SIZE_Y

    for j in range(INVADER_NUM_ROWS):
        f.append(create_sprite(sheet, SQUID, x, y))
        x += SPRITE_SIZE_X
    for i in range(2):
        x = start_x
        y -= SPRITE_SIZE_Y + 2
        for j in range(INVADER_NUM_ROWS):
            f.append(create_sprite(sheet, CRAB, x, y))
            x += SPRITE_SIZE_X
    for i in range(INVADER_NUM_ROWS):
        x = start_x
        y -= SPRITE_SIZE_Y + 2
        for j in range(11):
            f.append(create_sprite(sheet, OCTOPUS, x, y))
            x += SPRITE_SIZE_X

    return f


def check_laser_collisions(
    collisions: int,
    targets: list[int],
    c: GameSprite,
    l: GameSprite,
    f: list[GameSprite],
) -> tuple[int, list[int]]:
    """Return a binary value of things that were hit."""

    # Laser hits top
    if l.pos_y >= SCREEN_Y:
        return collisions | C_TOP, targets  # Bitwise operator

    # Laser hits invader
    i: int = 0
    for i in range(len(f)):
        if f[i].rect.colliderect(l.rect):
            collisions = collisions | C_INVADER
            targets.append(i)

    return collisions, targets


def check_fleet_collision(
    tick: int, fleet_x: int, fleet: list[Invader]
) -> tuple[int, bool]:
    """Check for border collision and send order to change direction."""
    if tick != 0:
        return fleet_x, False

    for i in fleet:
        if i.pos_x + SPRITE_SIZE_X >= SCREEN_X and fleet_x == RIGHT:
            return LEFT, True
        if i.pos_x <= 0 and fleet_x == LEFT:
            return RIGHT, True
    return fleet_x, False  # no change


def explode_invaders(
    s: GameState,
    c: GameSprite,
    l: GameSprite,
    f: list[GameSprite],
    targets: list[int],
) -> None:
    """Explode the invader and cause game state ruckus."""
    s.num_invaders -= 1
    c.set_fired(False)  # The cannon reloads immediately. Morale good.
    l.reset(c)
    for target in targets:
        f[target].frame_index = -2  # Kaboom!


def ones_complement(n: int) -> int:
    """Reverse the bits of a given number"""
    if n == 0:
        return 1

    mask: int = (1 << n.bit_length()) - 1
    return n ^ mask  # XOR


if __name__ == "__main__":
    main()
