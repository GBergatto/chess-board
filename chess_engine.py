from moves import Move
from moves import CastlingRights
from moves import CastlingMove
from moves import EnPassantMove


class ChessEngine():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.move_functions = {
            "P": self.get_pawn_moves,
            "N": self.get_knight_moves,
            "B": self.get_bishop_moves,
            "R": self.get_rook_moves,
            "Q": self.get_queen_moves,
            "K": self.get_king_moves
        }

        self.white_to_move = True
        self.move_log = []
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)

        self.checkmate = False
        self.stalemate = False

    def make_move(self, move):
        self.move_log.append(move)
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece

        if move.piece[1] == "K":
            if isinstance(move, CastlingMove):
                self.board[move.start_row][move.r_end_col] = move.piece[0] + "R"
                self.board[move.start_row][move.r_start_col] = "--"

            if move.piece[0] == "w":
                self.white_king_pos = (move.end_row, move.end_col)
            elif move.piece[0] == "b":
                self.black_king_pos = (move.end_row, move.end_col)
        elif move.piece[1] == "P":
            if isinstance(move, EnPassantMove):
                # remove captured pawn
                self.board[move.captured_row][move.captured_col] = "--"

        self.white_to_move = not self.white_to_move

    def undo_move(self):
        if self.move_log:

            self.checkmate = False
            self.stalemate = False

            last_move = self.move_log.pop()
            self.board[last_move.start_row][last_move.start_col] = last_move.piece
            self.board[last_move.end_row][last_move.end_col] = last_move.captured

            if last_move.piece[1] == "K":
                if isinstance(last_move, CastlingMove):
                    # move rook to original square
                    self.board[last_move.start_row][last_move.r_end_col] = "--"
                    self.board[last_move.start_row][last_move.r_start_col] = last_move.piece[0] + "R"
                if last_move.piece[0] == "w":
                    self.white_king_pos = (
                        last_move.start_row, last_move.start_col)
                else:
                    self.black_king_pos = (
                        last_move.start_row, last_move.start_col)
            elif last_move.piece[1] == "P":
                if isinstance(last_move, EnPassantMove):
                    self.board[last_move.captured_row][last_move.captured_col] = last_move.captured
                    self.board[last_move.end_row][last_move.end_col] = "--"
            elif last_move.is_promotion:
                self.board[last_move.start_row][last_move.start_col] = last_move.piece[0] + "P"

            self.white_to_move = not self.white_to_move

            if self.move_log:
                return [
                    (self.move_log[-1].start_row, self.move_log[-1].start_col),
                    (self.move_log[-1].end_row, self.move_log[-1].end_col)]

        return []

    def get_possible_moves(self):
        moves = []

        for row in range(8):
            for col in range(8):
                piece_color = self.board[row][col][0]
                if piece_color == ("w" if self.white_to_move else "b"):
                    piece = self.board[row][col][1]
                    self.move_functions[piece](moves, row, col, piece_color)

        if self.move_log:
            moves.extend(self.get_en_passant_moves())

        return moves

    def get_valid_moves(self):
        possible_moves = self.get_possible_moves()
        # remove invalid moves (checks)
        for move in reversed(possible_moves):
            self.make_move(move)
            if self.enemy_king_nearby(move):
                possible_moves.remove(move)
            elif self.king_in_check(move.piece[0]):
                possible_moves.remove(move)
            self.undo_move()
        # add castling moves
        castling_rights = self.can_castle()
        king_row = 7 if self.white_to_move else 0
        if castling_rights.long:
            possible_moves.append(CastlingMove(
                [(king_row, 4), (king_row, 2)], self.board, 0))
        if castling_rights.short:
            possible_moves.append(CastlingMove(
                [(king_row, 4), (king_row, 6)], self.board, 7))

        self.is_gameover(possible_moves)

        return possible_moves

    def is_gameover(self, possible_moves):
        """Check for possible checkmate or stalemate and update stats accordingly"""
        if len(possible_moves) == 0:
            print("no more moves")
            losing_color = "w" if self.white_to_move else "b"
            if self.king_in_check(losing_color):
                self.checkmate = True
                self.stalemate = False
            else:
                self.stalemate = True
                self.checkmate = False


    def get_en_passant_moves(self):
        moves = []
        last_move = self.move_log[-1]

        if last_move.piece[1] == "P":
            if abs(last_move.end_row - last_move.start_row) == 2:
                # enemy pawn has just advanced by 2 squares
                enemy_color = last_move.piece[0]
                color = "b" if enemy_color == "w" else "w"
                col_directions = (1, -1)

                # check if pawn on horizontally adjacent squares
                for col_direction in col_directions:
                    checked_col = last_move.end_col + col_direction
                    if 0 <= checked_col <= 7:
                        if self.board[last_move.end_row][checked_col] == color + "P":
                            end_row = (last_move.end_row +
                                       last_move.start_row) // 2
                            move = EnPassantMove(
                                [(last_move.end_row, checked_col), (end_row, last_move.end_col)], self.board)
                            moves.append(move)

        return moves

    def can_castle(self):
        if self.white_to_move:
            color = "w"
            enemy_color = "b"
            king_pos = self.white_king_pos
            original_king_pos = (7, 4)
            row = 7
        else:
            color = "b"
            enemy_color = "w"
            king_pos = self.black_king_pos
            original_king_pos = (0, 4)
            row = 0

        if king_pos != original_king_pos:
            return CastlingRights(False, False)

        if self.king_in_check(color):
            return CastlingRights(False, False)

        long = True
        short = True
        # long castle
        for l in range(1, 4):
            current_col = king_pos[1] - 1 * l
            if self.board[row][current_col] == "--":
                if l < 3:  # check only first 2 square for attacks
                    if self.square_under_attack(row, current_col, color, enemy_color):
                        long = False
                        break
            else:
                long = False
                break
        # short castle
        for s in range(1, 3):
            current_col = king_pos[1] + 1 * s
            if self.board[row][current_col] == "--":
                # if square is empty, check for attacks
                if self.square_under_attack(row, current_col, color, enemy_color):
                    short = False
                    break
            else:
                short = False
                break
        for move in self.move_log:
            if move.piece == color + "K":
                return CastlingRights(False, False)
            if move.piece == color + "R":
                if move.start_col == 0:
                    long = False
                elif move.start_col == 7:
                    short = False

        return CastlingRights(long, short)

    def enemy_king_nearby(self, move):
        if move.piece[1] == "K":
            if move.piece[0] == "b":
                enemy_king_pos = self.white_king_pos
            else:
                enemy_king_pos = self.black_king_pos
            king_directions = ((1, 0), (-1, 0), (0, 1),
                               (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1))
            for direction in king_directions:
                checked_row = enemy_king_pos[0] + direction[0]
                checked_col = enemy_king_pos[1] + direction[1]
                if checked_row == move.end_row and checked_col == move.end_col:
                    return True
        return False

    def king_in_check(self, color):
        if color == "w":
            king_row = self.white_king_pos[0]
            king_col = self.white_king_pos[1]
            enemy_color = "b"
        else:
            king_row = self.black_king_pos[0]
            king_col = self.black_king_pos[1]
            enemy_color = "w"
        return self.square_under_attack(king_row, king_col, color, enemy_color)

    def square_under_attack(self, row, col, color, enemy_color):
        # check knights squares
        knight_moves = ((-1, -2), (-1, 2), (-2, -1), (-2, 1),
                        (1, -2), (1, 2), (2, -1), (2, 1))
        for k_move in knight_moves:
            checked_row = row + k_move[0]
            checked_col = col + k_move[1]
            if 0 <= checked_row <= 7 and 0 <= checked_col <= 7:
                if self.board[checked_row][checked_col] == enemy_color + "N":
                    return True

        # check pawns
        for i in [-1, 1]:
            checked_row = row + (1 if color == "b" else -1)
            checked_col = col + i
            if 0 <= checked_row <= 7 and 0 <= checked_col <= 7:
                if self.board[checked_row][checked_col] == enemy_color + "P":
                    return True

        # check rows, cols, and diagonals
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, -1), (-1, 1), (1, -1))

        for direction in directions:
            n = 1
            checked_row = row + direction[0]
            checked_col = col + direction[1]

            while 0 <= checked_row <= 7 and 0 <= checked_col <= 7:
                square = self.board[checked_row][checked_col]

                if square[0] == color:
                    # any friendly piece would block possible checks on that direction
                    break
                if square[0] == enemy_color:
                    if square[1] == "Q":
                        return True
                    if square[1] == "R" and direction[0] * direction[1] == 0:
                        return True
                    if square[1] == "B" and direction[0] * direction[1] != 0:
                        return True
                    # any other enemy piece would block possible checks on that direction
                    break

                n += 1
                checked_row = row + direction[0] * n
                checked_col = col + direction[1] * n

        return False

    def get_pawn_moves(self, moves, row, col, color):
        if color == "w":
            # check square(s) in front
            if row-1 >= 0:
                if self.board[row-1][col] == "--":
                    # advance by one square
                    moves.append(Move([(row, col), (row-1, col)], self.board))
                    if row == 6:
                        if self.board[row-2][col] == "--":
                            # advance by two squares
                            moves.append(
                                Move([(row, col), (row - 2, col)], self.board))
            if col+1 <= 7:  # capture to the right
                if self.board[row-1][col+1][0] == "b":
                    moves.append(
                        Move([(row, col), (row-1, col+1)], self.board))
            if col-1 >= 0:  # capture to the left
                if self.board[row-1][col-1][0] == "b":
                    moves.append(
                        Move([(row, col), (row-1, col-1)], self.board))
        else:
            if row+1 <= 7:
                if self.board[row+1][col] == "--":
                    # advance by one square
                    moves.append(Move([(row, col), (row+1, col)], self.board))
                    if row == 1:
                        if self.board[row+2][col] == "--":
                            # advance by two squares
                            moves.append(
                                Move([(row, col), (row+2, col)], self.board))
            if col+1 <= 7:  # capture to the right
                if self.board[row+1][col+1][0] == "w":
                    moves.append(
                        Move([(row, col), (row+1, col+1)], self.board))
            if col-1 >= 0:  # capture to the left
                if self.board[row+1][col-1][0] == "w":
                    moves.append(
                        Move([(row, col), (row+1, col-1)], self.board))

    def get_knight_moves(self, moves, row, col, color):
        knight_moves = ((-1, -2), (-1, 2), (-2, -1), (-2, 1),
                        (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knight_moves:
            new_row = row + m[0]
            new_col = col + m[1]

            if 0 <= new_row <= 7 and 0 <= new_col <= 7:
                if self.board[new_row][new_col][0] != color:
                    moves.append(
                        Move([(row, col), (new_row, new_col)], self.board))

    def get_bishop_moves(self, moves, row, col, color):
        directions = ((1, 1), (-1, -1), (-1, 1), (1, -1))

        for direction in directions:
            n = 1
            new_row = row + direction[0]
            new_col = col + direction[1]

            while 0 <= new_col <= 7 and 0 <= new_row <= 7 and self.board[new_row][new_col][0] != color:
                moves.append(
                    Move([(row, col), (new_row, new_col)], self.board))
                if self.board[new_row][new_col] != "--":
                    break

                n += 1
                new_row = row + direction[0] * n
                new_col = col + direction[1] * n

    def get_rook_moves(self, moves, row, col, color):
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

        for direction in directions:
            n = 1
            new_row = row + direction[0]
            new_col = col + direction[1]

            while 0 <= new_col <= 7 and 0 <= new_row <= 7 and self.board[new_row][new_col][0] != color:
                moves.append(
                    Move([(row, col), (new_row, new_col)], self.board))
                if self.board[new_row][new_col] != "--":
                    break

                n += 1
                new_row = row + direction[0] * n
                new_col = col + direction[1] * n

    def get_queen_moves(self, moves, row, col, color):
        self.get_bishop_moves(moves, row, col, color)
        self.get_rook_moves(moves, row, col, color)

    def get_king_moves(self, moves, row, col, color):
        directions = ((1, 1), (1, 0), (1, -1), (0, -1),
                      (-1, -1), (-1, 0), (-1, 1), (0, 1))
        for direction in directions:
            new_row = row + direction[0]
            new_col = col + direction[1]

            if 0 <= new_col <= 7 and 0 <= new_row <= 7:
                if self.board[new_row][new_col][0] != color:
                    moves.append(
                        Move([(row, col), (new_row, new_col)], self.board))
