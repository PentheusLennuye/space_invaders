# The Game

In this description, nouns are written in **bold** when first mentioned and
verbs or verb groups are written in _italics_. Nouns become part of a finite
state machine's states, and the verbs are the permissible actions.

---

## Goal

The point of the **game** is for the **player** to _score_ as many **points**
as they can before the game _ends_.

## Description of Game Play

**Fleets** of **invaders** are _attempting to land_ on the **surface** in
**waves**. The player _controls_ three **cannons**, one at a time, from which
they _attempt to hit_ each **invader** with an energy bolt which we will call
the **laser**. Likewise, the invaders attempt to hit the cannons with their
own **bullets**. Note that the player has only one laser in play at a time,
while the invaders have many.

When the cannon _collides_ with a bullet, they are both _removed_ and the
player's **score** is _incremented by a correct **value** determined by the
**type** of invader. When the laser collides with an invader, the invader is
removed, the laser is _reset_, and the player's **score** is incremented by the
**value** assigned to the late invader.

The game _ends_ if the player _runs out_ of cannons or an invader _collides_
with the cannon. Each wave ends when the fleet has _lost_ its last invader.

## Description of the Pieces

### Invaders

The fleet is a 55x5 block of invaders. The fleet _starts_ several **rows** from
the surface, and _moves_ horizontally across the **board**, one pixel at a
time. When the **right-most invader** reaches the **right edge** of board, the
fleet descends one row and changes **direction**. Likewise, if the **left-most
invader** reaches the **left edge** of the field, the fleet descends one row
and changes direction.

If all the invaders in the fleet are removed, a new wave with a fresh fleet is
started, which its original strength in its original starting point.

### Cannon

The cannon starts in the **centre** of row above the surface. It moves under
the player's control horizontally, 2 pixels at a time. It cannot move past the
edges of the board.

### Laser

The laser moves in the cannon unless it has been _fired_. Once fired, it moves
up, 4 pixels at a time, independently of the cannon. If it reaches the top of
the board, it remains there for 16 **frames** before being _reset_ to its place
in the cannon.

### Bullet

An array of bullets originate randomly from the **positions** of any
**lowest-row** invaders. They descend independently of the invader from whence
it came. If it collides with the laser, they are both removed from the board
after a 16-frame delay.

[^1]: The on-screen representation. I am keeping the representation separate from game logic.
