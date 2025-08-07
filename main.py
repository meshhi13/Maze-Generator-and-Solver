import random
import pygame
from gamestate import GameState
from game import game_loop
from menu import menu_loop

while True:
    state = GameState()
    menu_loop(state)
    game_loop(state, state.rows, state.cols, state.algorithm, [])
