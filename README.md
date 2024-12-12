# Hasami Shogi

A variant of Shogi where one player must capture all but one of the other player’s pawns.

## Overview

This project was originally developed as a text-based game for an Introduction to Computer Science II class. As an approved portfollio project, I decided to enhance it it with graphical elements using **Pygame**.

![Gameplay Example Image](/images/gameplay.png)


### Objective
The game rules are based upon **Variant 1** of [Hasami Shogi](https://en.wikipedia.org/wiki/Hasami_shogi)
The game is won by capturing all but one of your opponent's pieces. You capture pieces by trapping them between two of your own pieces along a row or column. You may also corner capture opponent pieces by surrounding them orthogonally.

### How to Play
1. The game is played on a 9x9 grid.
2. Each player starts with 9 pieces placed in the first row closest to them.
3. Players take turns moving their pieces. A piece can move any number of squares horizontally or vertically, but it cannot jump over other pieces.
4. To capture an opponent’s piece, you must surround it with your own pieces on a horizontal or vertical line, or surround it in a corner.
5. The first player to capture all but one of their opponent's pieces wins the game.



### Prerequisites

To run this project, make sure you have Python 3 and Pygame installed. You can install Pygame with pip:

```bash
pip install pygame
```

Then run **game.py** in the project root to start the game.

![Screenshot demonstrating Game Over message](/images/black-wins.png)