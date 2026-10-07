SIZE = 8


def initial_board():
    board = [["." for _ in range(SIZE)] for _ in range(SIZE)]

    # Black pieces
    for r in range(3):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "B"

    # Red pieces
    for r in range(5, 8):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "R"

    return board


def move_piece(board, start, end):
    """Move a piece from start to end."""
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = "."


def remove_piece(board, position):
    """Remove a piece from the board."""
    r, c = position
    board[r][c] = "."