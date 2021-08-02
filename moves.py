"""Module containing all classses that handle different moves

Classes:
    Move
    CastlingMove
    EnPassantMove
    CastlingRights
"""


class Move():
    """class used to store and easily access info about moves"""

    def __init__(self, coordinates, board):
        self.start_row = coordinates[0][0]
        self.start_col = coordinates[0][1]

        self.end_row = coordinates[1][0]
        self.end_col = coordinates[1][1]

        self.move_id = self.start_row * 1000 + self.start_col * \
            100 + self.end_row * 10 + self.end_col

        self.piece = board[self.start_row][self.start_col]
        # store piece at end position to revert move if needed
        self.captured = board[self.end_row][self.end_col]

        self.is_promotion = False
        if self.piece[1] == "P":
            if self.end_row == 0 or self.end_row == 7:
                self.is_promotion = True

    def __repr__(self):
        piece_notation = self.piece[-1]
        promotion_notation = ""
        if self.piece[-1] == 'P' or self.is_promotion:
            piece_notation = ""
        if self.is_promotion:
            promotion_notation = "=" + self.piece[-1]

        start = self.get_letter_number(self.start_row, self.start_col)
        end = self.get_letter_number(self.end_row, self.end_col)

        # TODO: print starting position [start] if both pieces can get to end position
        if self.captured != "--":
            if piece_notation:
                return piece_notation + "x" + end + promotion_notation

            return start[0] + "x" + end + promotion_notation

        return piece_notation + end + promotion_notation

    # method to compare instances of Move
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_letter_number(self, row, col):
        rows_notation = [str(r) for r in range(8, 0, -1)]
        cols_notation = "abcdefgh"

        letter = cols_notation[col]
        number = rows_notation[row]

        return letter + number


class CastlingMove(Move):
    """Child class of Move used to handle castling"""

    def __init__(self, coordinates, board, r_start_col):
        super().__init__(coordinates, board)

        self.r_start_col = r_start_col
        if self.r_start_col == 0:
            self.r_end_col = 3
        else:
            self.r_end_col = 5

    def __repr__(self):
        return "0-0-0" if self.r_start_col == 0 else "0-0"


class EnPassantMove(Move):
    """Child class of Move used to handle en passant captures"""

    def __init__(self, coordinates, board):
        super().__init__(coordinates, board)
        self.captured_row = self.start_row
        self.captured_col = self.end_col

        self.captured = board[self.captured_row][self.captured_col]


class CastlingRights():
    """Class used to store a player's castling rights"""

    def __init__(self, long, short):
        self.long = long
        self.short = short

    def __repr__(self):
        return "Long: " + str(self.long) + " Short: " + str(self.short)
