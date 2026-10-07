from board import initial_board, move_piece, remove_piece, SIZE
from rules import (
    simple_move,
    capture_move,
    promote,
    player_has_capture,
    player_has_legal_move,
    player_has_pieces,
    get_capture_moves,
    get_captured_position,
    belongs_to_player,
)


class Checkers:

    def __init__(self):
        self.board = initial_board()
        self.player = "R"

    def print_board(self):
        print("\n   " + " ".join(str(c) for c in range(SIZE)))

        for r, row in enumerate(self.board):
            print(f"{r}  " + " ".join(row))

    def switch_player(self):
        self.player = "B" if self.player == "R" else "R"

    def check_game_over(self):
        """
        Check whether the current player has lost.

        A player loses if:
        1. They have no pieces.
        2. They have pieces but no legal moves.
        """
        if not player_has_pieces(self.board, self.player):
            winner = "B" if self.player == "R" else "R"
            print(f"\n{self.player} has no pieces left.")
            print(f"Player {winner} wins!")
            return True

        if not player_has_legal_move(self.board, self.player):
            winner = "B" if self.player == "R" else "R"
            print(f"\n{self.player} has no legal moves.")
            print(f"Player {winner} wins!")
            return True

        return False

    def make_capture(self, start, end):
        """
        Perform a capture.

        Returns:
            True if successful.
            False otherwise.
        """
        if not capture_move(self.board, self.player, start, end):
            return False

        # Save the moving piece
        piece = self.board[start[0]][start[1]]

        # Find and remove the captured piece
        captured = get_captured_position(start, end)
        remove_piece(self.board, captured)

        # Move the original piece
        move_piece(self.board, start, end)

        return True

    def make_simple_move(self, start, end):
        """
        Perform a normal one-square move.
        """
        if not simple_move(self.board, self.player, start, end):
            return False

        move_piece(self.board, start, end)

        return True

    def multi_capture(self, start):
        """
        Continue capturing with the same piece while captures are available.

        Returns:
            True if at least one capture was made.
            False otherwise.
        """
        current = start
        capture_count = 0
        promoted = False

        while True:

            available = get_capture_moves(
                self.board,
                self.player,
                current
            )

            if not available:
                break

            print(
                f"{self.player}: additional capture available "
                f"from {current[0]} {current[1]}."
            )

            raw = input("capture> ").strip().lower().split()

            if raw == ["q"]:
                return False

            if len(raw) != 4:
                print("Enter four coordinates.")
                continue

            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue

            if (sr, sc) != current:
                print(
                    f"You must continue with the same piece "
                    f"at {current[0]} {current[1]}."
                )
                continue

            if not all(
                0 <= x < SIZE
                for x in (sr, sc, er, ec)
            ):
                print("Outside board.")
                continue

            end = (er, ec)

            if end not in available:
                print("That is not a valid capture.")
                continue

            if not self.make_capture(current, end):
                print("Invalid capture.")
                continue

            capture_count += 1
            current = end

            # Check promotion after this capture.
            promoted_now = promote(self.board)

            if promoted_now:
                promoted = True

                # Standard checkers rule:
                # promotion ends the turn.
                break

        return capture_count > 0

    def run(self):
        print("Checkers — move: sr sc er ec")
        print("Enter q to quit.")

        while True:

            # Check whether current player has lost
            if self.check_game_over():
                self.print_board()
                return

            self.print_board()

            # Tell player if a capture is mandatory
            mandatory_capture = player_has_capture(
                self.board,
                self.player
            )

            if mandatory_capture:
                print(f"{self.player}: capture is mandatory.")

            raw = input(
                f"{self.player}> "
            ).strip().lower().split()

            if raw == ["q"]:
                print("Game ended.")
                return

            if len(raw) != 4:
                print("Enter four coordinates.")
                continue

            try:
                sr, sc, er, ec = map(int, raw)
            except ValueError:
                print("Coordinates must be numbers.")
                continue

            if not all(
                0 <= x < SIZE
                for x in (sr, sc, er, ec)
            ):
                print("Outside board.")
                continue

            start = (sr, sc)
            end = (er, ec)

            # Check ownership
            if not belongs_to_player(
                self.board[sr][sc],
                self.player
            ):
                print("That is not your piece.")
                continue

            # --------------------------------------------------
            # CAPTURE
            # --------------------------------------------------
            if mandatory_capture:

                if not capture_move(
                    self.board,
                    self.player,
                    start,
                    end
                ):
                    print("You must make a capture.")
                    continue

                if not self.make_capture(start, end):
                    print("Invalid capture.")
                    continue

                # Check promotion after the capture
                promoted = promote(self.board)

                # Continue multi-capture
                current = end

                additional_capture = get_capture_moves(
                    self.board,
                    self.player,
                    current
                )

                if additional_capture and not promoted:
                    self.multi_capture(current)

                # One player-facing result for the whole turn
                print(
                    f"{self.player} captured piece(s)."
                )

            # --------------------------------------------------
            # NORMAL MOVE
            # --------------------------------------------------
            else:

                if not self.make_simple_move(start, end):
                    print("Invalid move.")
                    continue

                promoted = promote(self.board)

                if promoted:
                    print(
                        f"{self.player} moved "
                        f"from {start} to {end} and was promoted."
                    )
                else:
                    print(
                        f"{self.player} moved "
                        f"from {start} to {end}."
                    )

            # Switch player after the entire turn
            self.switch_player()