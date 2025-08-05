import pygame
import random
import sys
from collections import deque
from settings import *
import time
from objects import *

def game_loop(rows, cols, algo):
    tilesize = WIDTH // cols

    grid = Grid(rows, cols)
    stack = []
    current_cell = grid.grid[0][0]
    done = False
    text_highlight = False
    generated = False
            
    grid.grid[0][0].start = True
    grid.grid[rows - 1][cols - 1].end = True

    def recursive_bfs(current, arr):
        time.sleep(0.02)
        current.searched = True
        current.draw(tilesize)
        current.addNeighbors(tilesize)
        pygame.display.update()

        if current.end:
            return arr

        for neighbor in current.neighbors:
            result = recursive_bfs(neighbor, arr + [neighbor])
            if result:
                return result
        
        return None

    while not done:
        screen.fill(BGCOLOR)
        text = FONT.render("GENERATING..." if not generated else "SOLVE MAZE", True, COLOR_INACTIVE if (text_highlight and generated) else TEXT_COLOR)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + 40))
        screen.blit(text, text_rect)

        current_cell.visited = True
        current_cell.current = True

        for row in grid.grid:
            for cell in row:
                cell.draw(tilesize)

        next_cell = grid.checkNeighbors(current_cell, tilesize, rows, cols)

        if next_cell:
            current_cell.neighbors = []
            stack.append(current_cell)
            current_cell.removeWalls(next_cell, tilesize)
            current_cell.current = False
            current_cell = next_cell

        elif stack:
            current_cell.current = False
            current_cell = stack.pop()
        else:
            generated = True

        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                done = True
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                text_highlight = text_rect.collidepoint(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and text_rect.collidepoint(mouse_x, mouse_y):
                    if generated:
                        path = recursive_bfs(current_cell, [current_cell])
                        if path:
                            for i in path:
                                i.path = True

        pygame.display.flip()
        clock.tick(60)
