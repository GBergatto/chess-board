import pygame.font
from settings import BOARD_SIZE
from settings import TEXT_COLOR
from settings import TEXT_BG_COLOR


class Scoreboard():
    """Class to display game over text"""

    def __init__(self, engine, window):
        self.font = pygame.font.SysFont("Roboto ", 28, bold=True)
        self.engine = engine
        self.window = window

    def show_text(self):
        if self.engine.checkmate:
            winning_color = "White" if not self.engine.white_to_move else "Black"
            message = f"{winning_color} won by checkmate!"
        elif self.engine.stalemate:
            losing_color = "White" if self.engine.white_to_move else "Black"
            message = f"Stalemate! No valid moves for {losing_color}"

        text = self.font.render(message, True, TEXT_COLOR, TEXT_BG_COLOR)
        text_rect = text.get_rect()
        text_rect.center = (BOARD_SIZE // 2, BOARD_SIZE // 2)

        self.window.blit(text, text_rect)
