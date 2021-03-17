import math
import numpy as np
import copy


# visually formats the board
def format_board(board, l):
    base = math.floor(math.sqrt(l))
    side = l

    def expand_line(line, base):
        return line[0] + line[5:9].join([line[1:5] * (base - 1)] * base) + line[9:13]

    line0 = expand_line("╔═══╤═══╦═══╗", base)
    line1 = expand_line("║ . │ . ║ . ║", base)
    line2 = expand_line("╟───┼───╫───╢", base)
    line3 = expand_line("╠═══╪═══╬═══╣", base)
    line4 = expand_line("╚═══╧═══╩═══╝", base)

    symbol = " 1234567890"  # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    nums = [[""] + [symbol[n] for n in row] for row in board]
    print(line0)
    for r in range(1, side + 1):
        print("".join(n + s for n, s in zip(nums[r - 1], line1.split("."))))
        print([line2, line3, line4][(r % side == 0) + (r % base == 0)])


# Checks if a spot can be played using a certain number
def check_spot(board, x, y, n, l):
    for i in range(0, l):
        if board[x][i] == n or board[i][y] == n:
            return False
    sqrt_l = math.floor(math.sqrt(l))
    x0 = (x // sqrt_l) * sqrt_l
    y0 = (y // sqrt_l) * sqrt_l
    for i in range(0, sqrt_l):
        for j in range(0, sqrt_l):
            if board[x0 + i][y0 + j] == n:
                return False
    return True


# checks if board is completely filled
def board_complete(board, l):
    complete = True
    for x in range(0, l):
        for y in range(0, l):
            if board[x][y] == 0:
                complete = False
                return complete
    return complete


# Solves a sudoku board
def solve(board, l):
    answer = []
    for x in range(0, l):
        for y in range(0, l):
            if board[x][y] == 0:
                for n in range(1, l + 1):
                    if check_spot(board, x, y, n, l):
                        board[x][y] = n
                        board = solve(board, l)
                        if board_complete(board, l):
                            answer = copy.deepcopy(board)
                        else:
                            board[x][y] = 0
            return board


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
    # board = format_board(board, l)
    return board


length = 9
play_board = random_board(length)
print(np.matrix(play_board))
print(np.matrix(solve(play_board, length)))
# solve(length)
# print(np.matrix(play_board))
