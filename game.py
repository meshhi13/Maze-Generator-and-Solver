import pygame
import random
import sys
from collections import deque
from settings import *
import time
from objects import *

def game_loop(rows, cols, algo, path):
    tilesize = WIDTH // cols

    path = []
    grid = Grid(rows, cols, algo)
    stack = []
    current_cell = grid.grid[0][0]
    text_highlight = False
    STATE_GENERATE = False
    STATE_SOLVE = False
    STATE_DONE = False
    text = ""

            
    grid.grid[0][0].start = True
    grid.grid[rows - 1][cols - 1].end = True

    screen.fill(BGCOLOR)

    while not STATE_DONE:
        pygame.draw.rect(screen, BGCOLOR, (0, HEIGHT, WIDTH, 80))
        if not STATE_GENERATE:
            text = "GENERATING..."
        elif not STATE_SOLVE:
            text = "SOLVE MAZE"
        else:
            text = "RESTART"

        if not STATE_GENERATE or not STATE_SOLVE:
            for row in grid.grid:
                for cell in row:
                    cell.draw(tilesize)

        text = FONT.render(text, True, COLOR_INACTIVE if STATE_GENERATE and text_highlight else TEXT_COLOR)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + 40))
        screen.blit(text, text_rect)

        current_cell.visited = True
        current_cell.current = True

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
            STATE_GENERATE = True

        for event in pygame.event.get():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                STATE_DONE = True
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                text_highlight = text_rect.collidepoint(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect.collidepoint(mouse_x, mouse_y):
                    if STATE_GENERATE and not STATE_SOLVE:
                        match grid.algo:
                            case "DFS":
                                path, cost = grid.recursive_dfs(current_cell, [current_cell], tilesize)
                            case "BFS":
                                path, cost = grid.iterative_bfs(current_cell, [current_cell], tilesize)
                                path.reverse()
                            case "A*":
                                path, cost = grid.a_star(current_cell, [current_cell], tilesize)

                        if path:
                            grid.draw_path_line(path, tilesize)
                            pygame.display.update()


                        STATE_SOLVE = True
                    elif STATE_GENERATE and STATE_SOLVE:
                        STATE_DONE = True


        pygame.display.flip()
        clock.tick(60)
