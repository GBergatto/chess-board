import pygame
import sys

from settings import SQ_SIZE
from settings import LIGHT_COLOR
from settings import DARK_COLOR
from settings import MOVE_COLOR
from settings import VALID_COLOR
from moves import Move


def load_pieces():
    images = {}
    pieces = ["wK", "wQ", "wR", "wB", "wN", "wP",
              "bK", "bQ", "bR", "bB", "bN", "bP"]
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(
            f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

    return images


def draw_board(win, images, pieces, squares, valid_squares):
    draw_squares(win)
    draw_highlights(win, squares, valid_squares)
    draw_pieces(win, images, pieces)


def draw_squares(win):
    colors = [LIGHT_COLOR, DARK_COLOR]

    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(win, color, (col * SQ_SIZE,
                                          row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_highlights(win, move_squares, valid_squares):
    move_highlight = pygame.Surface((SQ_SIZE, SQ_SIZE))
    move_highlight.set_alpha(130)
    move_highlight.fill(MOVE_COLOR)

    valid_highlight = pygame.Surface((SQ_SIZE, SQ_SIZE))
    valid_highlight.set_alpha(130)
    valid_highlight.fill(VALID_COLOR)

    # move_squares = [(0, 0), (6, 7)]
    for n, move_square in enumerate(move_squares):
        row = move_square[0]
        col = move_square[1]
        win.blit(move_highlight, (col * SQ_SIZE, row * SQ_SIZE))

        if not n:  # run only on starting coordinates
            for valid_move in valid_squares:
                if valid_move.start_row == row and valid_move.start_col == col:
                    win.blit(valid_highlight, (valid_move.end_col *
                                               SQ_SIZE, valid_move.end_row * SQ_SIZE))


def draw_pieces(win, images, pieces):
    for row in range(8):
        for col in range(8):
            piece = pieces[row][col]
            if piece != "--":
                win.blit(images[piece], (col * SQ_SIZE,
                                         row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def get_row_col(pos):
    x, y = pos
    row = y // SQ_SIZE
    col = x // SQ_SIZE

    return row, col


def move_pieces(window, images, chess_engine, valid_moves, coordinates):
    location = pygame.mouse.get_pos()
    row, col = get_row_col(location)
    selected_piece = chess_engine.board[row][col]
    move_made = False

    if len(coordinates) == 0:
        # allow to select first square only if it has a piece of the right color
        if selected_piece[0] == ("w" if chess_engine.white_to_move else "b"):
            coordinates.append((row, col))
    elif len(coordinates) == 1:
        coordinates.append((row, col))

    if len(coordinates) == 2:

        if coordinates[0] != coordinates[1]:
            user_move = Move(coordinates, chess_engine.board)
            for move in valid_moves:
                if user_move == move:
                    # promotion?
                    if move.is_promotion:
                        move.piece = move.piece[0] + get_promotion_piece()

                    # make move
                    move_made = True
                    chess_engine.make_move(move)
                    print(move)

                    # calculate new valid moves
                    valid_moves.clear()
                    valid_moves.extend(chess_engine.get_valid_moves())
                    break
        if not move_made:  # invalid move
            copy = coordinates[:]
            coordinates.clear()
            if copy[0] != copy[1]:  # didn't click on same square
                if selected_piece[0] == ("w" if chess_engine.white_to_move else "b"):
                    # different piece selected
                    coordinates.append((row, col))

    draw_board(window, images, chess_engine.board,
               coordinates, valid_moves)
    if move_made:
        coordinates.clear()


def get_promotion_piece():
    print("Promoting... Press Q, R, N, or B")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "R"
                if event.key == pygame.K_q:
                    return "Q"
                if event.key == pygame.K_b:
                    return "B"
                if event.key == pygame.K_n:
                    return "N"
