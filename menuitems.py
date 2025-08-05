import pygame
import sys
from settings import *

class MenuItems:
    def __init__(self, text, selected, rect):
        self.text = text
        self.selected = selected
        self.rect = rect