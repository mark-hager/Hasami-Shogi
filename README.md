# Hasami Shogi

A variant of Shogi where one player must capture all but one of the other player’s pawns.

## Overview

This project is a Hasami Shogi game, a variant of Shogi in which the objective is to capture all but one of your opponent's pieces. Originally developed as an ASCII-based game, the project was later enhanced with graphical elements using **Pygame**.

### Objective
Capture all but one of your opponent's pieces. You capture pieces by trapping them between two of your own pieces along a row or column.

### How to Play
1. The game is played on a 9x9 grid.
2. Each player starts with 9 pieces placed in the first row closest to them.
3. Players take turns moving their pieces. A piece can move any number of squares horizontally or vertically, but it cannot jump over other pieces.
4. To capture an opponent’s piece, you must surround it with your own pieces on a horizontal or vertical line.
5. The first player to capture all but one of their opponent's pieces wins the game.

## Getting Started

### Prerequisites

To run this project locally, make sure you have Python 3 and Pygame installed. You can install Pygame with pip:

```bash
pip install pygame
