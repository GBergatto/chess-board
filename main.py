import sys
import pygame

from chess_engine import ChessEngine
from scoreboard import Scoreboard
import program_functions as pf
from settings import BOARD_SIZE


def main():
    pygame.init()
    window = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    images = pf.load_pieces()

    ######################################

    chess_engine = ChessEngine()
    scoreboard = Scoreboard(chess_engine, window)

    coordinates = []
    valid_moves = chess_engine.get_valid_moves()

    pf.draw_board(window, images, chess_engine.board,
                  coordinates, valid_moves)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # undo last move
                    coord = chess_engine.undo_move()
                    # calculate new valid moves
                    valid_moves = chess_engine.get_valid_moves()
                    pf.draw_board(window, images,
                                  chess_engine.board, coord, valid_moves)

            if valid_moves:
                if pygame.mouse.get_pressed()[0]:
                    pf.move_pieces(window, images, chess_engine,
                                   valid_moves, coordinates)

        if not valid_moves:  # game over
            scoreboard.show_text()

        pygame.display.flip()


if __name__ == "__main__":
    main()
