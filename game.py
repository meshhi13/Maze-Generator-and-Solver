import pygame
import random
import sys
from collections import deque
from settings import *
import time
from objects import *

def game_loop(state, rows, cols, algo, path):
    tilesize = WIDTH // cols

    path = []
    grid = Grid(rows, cols, algo)
    stack = []
    cost = []
    current_cell = grid.grid[0][0]
    text_highlight1 = False
    text_highlight2 = False
    text_highlight3 = False
    STATE_GENERATE = False
    STATE_SOLVE = False
    STATE_DONE = False
    text_first= ""
    button_first = ""
    button_second = ""
    button_third = ""

            
    grid.grid[0][0].start = True
    grid.grid[rows - 1][cols - 1].end = True

    screen.fill(BGCOLOR)

    while not STATE_DONE:
        pygame.draw.rect(screen, BGCOLOR, (0, HEIGHT, WIDTH, 120))
        if not STATE_GENERATE:
            button_third = "RESTART"
            text_first = "GENERATING..."
        elif not STATE_SOLVE:
            button_first = "SOLVE MAZE"
            button_second = f"ALGO: {grid.algo}"
            text_first = "WAITING..."
        else:
            button_first = "CLEAR MAZE"
            text_first = f"COST: {cost}"

        if not STATE_GENERATE or not STATE_SOLVE:
            for row in grid.grid:
                for cell in row:
                    cell.draw(tilesize)

        text1 = FONT.render(text_first, True, TEXT_COLOR)
        text1_rect = text1.get_rect(center=(WIDTH // 2, HEIGHT + 22))

        button1 = FONT.render(button_first, True, WHITE if text_highlight1 else TEXT_COLOR)
        button1_rect = button1.get_rect(center=(WIDTH // 4, HEIGHT + 62))

        button2 = FONT.render(button_second, True, WHITE if text_highlight2 else TEXT_COLOR)
        button2_rect = button2.get_rect(center=(3 * WIDTH // 4, HEIGHT + 62))

        button3 = FONT.render(button_third, True, WHITE if text_highlight3 else TEXT_COLOR)
        button3_rect = button3.get_rect(center=(WIDTH // 2, HEIGHT + 102))
        
        pygame.draw.line(screen, BLACK, (WIDTH // 2, HEIGHT + 40), (WIDTH // 2, HEIGHT + 80), 1)
        pygame.draw.line(screen, BLACK, (0, HEIGHT + 40), (WIDTH, HEIGHT + 40), 1)
        pygame.draw.line(screen, BLACK, (0, HEIGHT + 80), (WIDTH, HEIGHT + 80), 1)

        screen.blit(button1, button1_rect)
        screen.blit(button2, button2_rect)
        screen.blit(button3, button3_rect)
        screen.blit(text1, text1_rect)
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
                text_highlight1 = button1_rect.collidepoint(mouse_x, mouse_y)
                text_highlight2 = button2_rect.collidepoint(mouse_x, mouse_y)
                text_highlight3 = button3_rect.collidepoint(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(mouse_x, mouse_y):
                    if STATE_GENERATE and not STATE_SOLVE:
                        match grid.algo:
                            case "DFS":
                                path, cost = grid.recursive_dfs(current_cell, [current_cell], tilesize)
                            case "BFS":
                                path, cost = grid.iterative_bfs(current_cell, [current_cell], tilesize)
                                path.reverse()
                            case "A*":
                                path, cost = grid.a_star(current_cell, [current_cell], tilesize)
                                path.reverse()

                        if path:
                            grid.draw_path_line(path, tilesize)
                            pygame.display.update()

                        STATE_SOLVE = True

                    elif STATE_SOLVE:
                        grid.reset_grid(tilesize)
                        pygame.draw.rect(screen, BGCOLOR, (0, 0, WIDTH, HEIGHT))
                        pygame.display.update()
                        STATE_SOLVE = False

                elif button2_rect.collidepoint(mouse_x, mouse_y):
                    state.algorithm = next(state.cycle_algo)
                    grid.algo = state.algorithm
                elif button3_rect.collidepoint(mouse_x, mouse_y):
                    STATE_DONE = True


        pygame.display.flip()
        clock.tick(60)
