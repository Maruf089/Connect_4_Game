import pygame
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates 
import numpy as np
import sys
import math
import before_ai
import Ai_hard
import Ai_medium
import Ai_Easy



BLUE = (106, 159, 181)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT=6
COLUMN_COUNT=7

SQUARESIZE = 100

width = (COLUMN_COUNT) * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

pygame.init()

def create_surface_with_text(text, font_size, text_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb)
    return surface.convert_alpha()


class UIElement(Sprite):
    """ An user interface element that can be added to a surface """

    def __init__(self, center_position, text, font_size, text_rgb, action=None):

        self.mouse_over = False 

        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb
        )

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        self.action = action

        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
            	return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        """ Draws element onto a surface """
        surface.blit(self.image, self.rect)

class Player:
    """ Stores information about a player """

    def __init__(self, score=0, current_level=1):
        self.score = score
        self.current_level = current_level

class GameState(Enum):
    HUMAN = 3
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    AI = 2
    AI_easy = 5
    AI_medium = 7
    AI_hard = 9


#pygame.display.init()
pygame.display.set_mode()
background_image = pygame.image.load("bg1.jpg").convert()


def title_screen(screen):
    start_btn = UIElement(
        center_position=(350, 300),
        font_size=40,
        text_rgb=BLACK,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(350, 400),
        font_size=40,
        text_rgb=BLACK,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = RenderUpdates(start_btn, quit_btn)

    return game_loop(screen, buttons)


def play_level(screen, player):
    return_btn = UIElement(
        center_position=(110, 670),
        font_size=30,
        text_rgb=BLACK,
        text="Main menu",
        action=GameState.TITLE,
    )

    humlevel_btn = UIElement(
        center_position=(400, 200),
        font_size=40,
        text_rgb=BLACK,
        text="Human v/s Human",
        action=GameState.HUMAN,
    )

    AIlevel_btn = UIElement(
        center_position=(400, 300),
        font_size=40,
        text_rgb=BLACK,
        text="Human v/s AI",
        action=GameState.AI,
    )


    buttons = RenderUpdates(return_btn, humlevel_btn, AIlevel_btn)

    return game_loop(screen, buttons)


def ai_level(screen, player):
    return_btn = UIElement(
        center_position=(80, 670),
        font_size=30,
        text_rgb=BLACK,
        text="Back",
        action=GameState.NEWGAME,
    )

    easy_btn = UIElement(
        center_position=(400, 200),
        font_size=40,
        text_rgb=BLACK,
        text="EASY",
        action=GameState.AI_easy,
    )

    medium_btn = UIElement(
        center_position=(400, 300),
        font_size=40,
        text_rgb=BLACK,
        text="Medium",
        action=GameState.AI_medium,
    )

    hard_btn = UIElement(
        center_position=(400, 400),
        font_size=40,
        #bg_rgb=BLUE,
        text_rgb=BLACK,
        text="Hard",
        action=GameState.AI_hard,
    )

    buttons = RenderUpdates(return_btn, easy_btn, medium_btn, hard_btn)

    return game_loop(screen, buttons)

    

def game_loop(screen, buttons):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        
        screen.blit(background_image,[0,0])
        buttons.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((700,700))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            player = Player()
            game_state = play_level(screen, player)

        if game_state == GameState.AI:
            player = Player()
            game_state = ai_level(screen, player)

        if game_state == GameState.HUMAN:
            before_ai.human_vs_human_game_play()
            game_state = play_level(screen, player)

        if game_state == GameState.AI_easy:
            Ai_Easy.AI_vs_Human_easy()
            game_state = play_level(screen, player)

        if game_state == GameState.AI_medium:
            Ai_medium.AI_vs_Human_medium()
            game_state = play_level(screen, player)

        if game_state == GameState.AI_hard:
            Ai_hard.AI_vs_Human_hard()
            game_state = play_level(screen, player)

        if game_state == GameState.QUIT:
            pygame.quit()