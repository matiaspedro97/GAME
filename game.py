import pygame.color

from menu import Menu
from test import *


def generate_player(mode):
    avail_modes = {'PVE': [1, 0], 'PVP': [1, 1], 'EVE': [0, 0]}
    p1_type, p2_type = avail_modes.get(mode, [1, 1])

    keys1 = [K_LEFT, K_RIGHT, K_UP, K_SPACE]
    keys2 = [K_a, K_d, K_w, K_r]

    # Player icon
    p1 = Fighter(20, bg_img.get_height() - 30, 100, 200,
                      icon_path=["img/char1.png", "img/char1_rev.png"],
                      player=p1_type, screen=screen, keys=keys1, mac=None)
    p2 = Fighter(bg_img.get_width() - 230, bg_img.get_height() - 30, 100, 200,
                      icon_path=["img/char2_rev.png", "img/char2.png"],
                      player=p2_type, screen=screen, keys=keys2, mac=None)
    return p1, p2

class Game:
    def __init__(self, mode):
        self.mode =

        # Initialize pygame
        pygame.init()

        pygame.mixer.music.load("soundtrack/04. Battle Theme 1.wav")
        pygame.mixer.music.play(-1)


        print(K_a)

        # Background image
        bg_img = pygame.image.load('img/bg/bg1.gif')

        # Define constants for the screen width and height
        SCREEN_WIDTH = bg_img.get_width()
        SCREEN_HEIGHT = bg_img.get_height()

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Battle")


        self.RUN = True

    def display(self):




