SIZE = 8


def is_king(piece):
    return piece in ("RK", "BK")


def belongs_to_player(piece, player):
    return piece in (player, player + "K")


def get_directions(board, player, start):
    """
    Return legal movement directions for a piece.

    Normal pieces move only forward.
    Kings move in both directions.
    """
    r, c = start
    piece = board[r][c]

    if piece == player + "K":
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    if player == "R":
        return [(-1, -1), (-1, 1)]

    return [(1, -1), (1, 1)]


def simple_move(board, player, start, end):
    """
    Check whether a normal one-square diagonal move is legal.
    """
    sr, sc = start
    er, ec = end

    if not belongs_to_player(board[sr][sc], player):
        return False

    if board[er][ec] != ".":
        return False

    dr = er - sr
    dc = ec - sc

    return (dr, dc) in get_directions(board, player, start)


def capture_move(board, player, start, end):
    """
    Check whether a two-square diagonal capture is legal.
    """
    sr, sc = start
    er, ec = end

    if not belongs_to_player(board[sr][sc], player):
        return False

    if board[er][ec] != ".":
        return False

    dr = er - sr
    dc = ec - sc

    # Must move exactly two squares diagonally
    if abs(dr) != 2 or abs(dc) != 2:
        return False

    # Find the jumped piece
    mr = (sr + er) // 2
    mc = (sc + ec) // 2

    middle_piece = board[mr][mc]

    # There must be an opponent piece in the middle
    if middle_piece == "." or belongs_to_player(middle_piece, player):
        return False

    # Check whether the direction is legal
    valid_directions = get_directions(board, player, start)

    # Convert the 2-square movement into its direction
    direction = (dr // 2, dc // 2)

    return direction in valid_directions


def get_captured_position(start, end):
    """
    Return the position of the piece being jumped.
    """
    sr, sc = start
    er, ec = end

    return ((sr + er) // 2, (sc + ec) // 2)


def get_capture_moves(board, player, start):
    """
    Return all possible captures for a particular piece.
    """
    moves = []

    sr, sc = start

    if not belongs_to_player(board[sr][sc], player):
        return moves

    for dr, dc in get_directions(board, player, start):
        end = (sr + 2 * dr, sc + 2 * dc)

        er, ec = end

        if 0 <= er < SIZE and 0 <= ec < SIZE:
            if capture_move(board, player, start, end):
                moves.append(end)

    return moves


def get_simple_moves(board, player, start):
    """
    Return all possible non-capturing moves for a particular piece.
    """
    moves = []

    sr, sc = start

    if not belongs_to_player(board[sr][sc], player):
        return moves

    for dr, dc in get_directions(board, player, start):
        end = (sr + dr, sc + dc)

        er, ec = end

        if 0 <= er < SIZE and 0 <= ec < SIZE:
            if simple_move(board, player, start, end):
                moves.append(end)

    return moves


def player_has_capture(board, player):
    """
    Check whether the player has at least one possible capture.
    """
    for r in range(SIZE):
        for c in range(SIZE):
            if belongs_to_player(board[r][c], player):
                if get_capture_moves(board, player, (r, c)):
                    return True

    return False


def player_has_legal_move(board, player):
    """
    Check whether the player has any legal move.

    A capture is mandatory if one exists.
    """
    must_capture = player_has_capture(board, player)

    for r in range(SIZE):
        for c in range(SIZE):

            if not belongs_to_player(board[r][c], player):
                continue

            position = (r, c)

            if must_capture:
                if get_capture_moves(board, player, position):
                    return True
            else:
                if get_simple_moves(board, player, position):
                    return True

    return False


def player_has_pieces(board, player):
    """
    Check whether the player still has at least one piece.
    """
    for row in board:
        for piece in row:
            if belongs_to_player(piece, player):
                return True

    return False


def promote(board):
    """
    Promote pieces that reach the opposite back row.
    """
    promoted = []

    for c in range(SIZE):

        if board[0][c] == "R":
            board[0][c] = "RK"
            promoted.append("R")

        if board[SIZE - 1][c] == "B":
            board[SIZE - 1][c] = "BK"
            promoted.append("B")

    return promoted