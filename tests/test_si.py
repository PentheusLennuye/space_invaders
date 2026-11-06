"""Testing the functions in space invaders."""

import pytest

from space_invaders import si

# ──────────────────────────────────────────────────────────────────────
# Test the fleet deployment per wave to ensure all invaders are in
# place.
# ──────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "index, x, y, points_value",
    [
        (0, 24, 24, 10),
        (1, 24, 25, 10),
        (2, 24, 26, 20),
        (3, 24, 27, 20),
        (4, 24, 28, 30),
        (5, 40, 24, 10),
        (6, 40, 25, 10),
        (7, 40, 26, 20),
        (8, 40, 27, 20),
        (9, 40, 28, 30),
        (50, 184, 24, 10),
        (51, 184, 25, 10),
        (52, 184, 26, 20),
        (53, 184, 27, 20),
        (54, 184, 28, 30),
    ],
)
def test_deploy_fleet(index, x, y, points_value):
    """
    Do we get the fleet we want? Only indexes 0-9, and 50-54 need
    testing.
    """

    fleet = si.deploy_fleet()

    assert fleet[index].pos_x == x
    assert fleet[index].pos_y == y
    assert fleet[index].value == points_value
    assert len(fleet) == 55


# ──────────────────────────────────────────────────────────────────────
# Test the fleet movement
# ──────────────────────────────────────────────────────────────────────


def test_move_fleet():
    """Ensure the fleet moves as one, right, left, or down."""

    # If going right, but the next move > the right edge, change dir
    # left and move down one row.
    fleet = si.deploy_fleet()
    for i in fleet:
        i.pos_x += 24
    direction, fleet = si.move_fleet(si.RIGHT, fleet)

    assert direction == si.LEFT
    assert fleet[0].pos_x == 48  # No move on x
    assert fleet[0].pos_y == 25  # Move y down one level

    # Otherwise move one pixel right.
    fleet = si.deploy_fleet()
    direction, fleet = si.move_fleet(si.RIGHT, fleet)

    assert direction == si.RIGHT
    assert fleet[0].pos_x == 25
    assert fleet[0].pos_y == 24  # No move on y

    # If going left, but the next move < the left edge, change dir
    # right and move down one row.
    fleet = si.deploy_fleet()
    for i in fleet:
        i.pos_x -= 24
    direction, fleet = si.move_fleet(si.LEFT, fleet)

    assert direction == si.RIGHT
    assert fleet[-1].pos_x == 160  # No move on x
    assert fleet[-1].pos_y == 29  # Move y down one level

    # Otherwise move one pixel left.
    fleet = si.deploy_fleet()
    direction, fleet = si.move_fleet(si.LEFT, fleet)

    assert direction == si.LEFT
    assert fleet[-1].pos_x == 183
    assert fleet[-1].pos_y == 28  # No move on y
