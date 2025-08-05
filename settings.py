import pygame
import random

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BGCOLOR = (61, 68, 194)
COLOR_INACTIVE = (255, 255, 255)
TEXT_COLOR = (200, 200, 200)
WIDTH = 700
HEIGHT = 700
TITLE = "Maze Generator and Solver"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT + 80))
clock = pygame.time.Clock()
pygame.display.set_caption(TITLE)
FONT = pygame.font.SysFont(pygame.font.get_default_font(), 50)
