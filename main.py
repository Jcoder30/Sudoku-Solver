import numpy as np
import math


# Generates a random sudoku board
def random_board(l):
    base = math.floor(math.sqrt(l))
    side = base * base

    # pattern for a baseline valid solution
    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    # randomize rows, columns and numbers (of valid base pattern)
    from random import sample

    def shuffle(s):
        return sample(s, len(s))

    r_base = range(base)
    rows = [g * base + r for g in shuffle(r_base) for r in shuffle(r_base)]
    cols = [g * base + c for g in shuffle(r_base) for c in shuffle(r_base)]
    nums = shuffle(range(1, base * base + 1))

    # produce board using randomized baseline pattern
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = side * side
    empties = squares * 3 // 4
    for p in sample(range(squares), empties):
        board[p // side][p % side] = 0

    return board


def possible(board, x, y, n, l):
    # Is the number appearing in the given row?
    for i in range(0, l):
        if board[x][i] == n or board[i][y] == n:
            return False

    # Is the number appearing in the given square?
    sqrt_l = math.floor(math.sqrt(l))
    x0 = (y // sqrt_l) * sqrt_l
    y0 = (x // sqrt_l) * sqrt_l
    for i in range(0, sqrt_l):
        for j in range(0, sqrt_l):
            if board[y0 + i][x0 + j] == n:
                return False

    return True


def solve(board, l):
    board_number = 1
    for x in range(0, l):
        for y in range(0, l):
            if board[x][y] == 0:
                for n in range(1, l + 1):
                    if possible(board, x, y, n, l):
                        board[x][y] = n
                        solve(board, l)
                        board[x][y] = 0

                return

    print('New Solution' + '\n', np.matrix(board))
    board_number += 1
    input('Next possible solution?')


# test 9 by 9 board with only one solution
test_board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
              [6, 0, 0, 1, 9, 5, 0, 0, 0],
              [0, 9, 8, 0, 0, 0, 0, 6, 0],
              [8, 0, 0, 0, 6, 0, 0, 0, 3],
              [4, 0, 0, 8, 0, 3, 0, 0, 1],
              [7, 0, 0, 0, 2, 0, 0, 0, 6],
              [0, 6, 0, 0, 0, 0, 2, 8, 0],
              [0, 0, 0, 0, 1, 9, 0, 0, 5],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Length must be a perfect square
length = 9
# creates random board depending on the length (the board may have more than one solution)
play_board = random_board(length)
print('Starting Board\n', np.matrix(play_board))
solve(play_board, length)
