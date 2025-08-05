import pygame
import random
import sys
from collections import deque
from settings import *

def game_loop(rows, cols, algo):
    tilesize = WIDTH // cols

    class Cell():
        def __init__(self, x, y):
            self.x = x * tilesize
            self.y = y * tilesize
            
            self.visited = False
            self.current = False
            self.start = False
            self.end = False
            
            self.walls = [True, True, True, True]  # top, right, bottom, left
            self.neighbors = []
            
            self.top = 0
            self.right = 0
            self.bottom = 0
            self.left = 0
            self.next_cell = 0

        def removeWalls(self, next_cell):
            x = int(self.x / tilesize) - int(next_cell.x / tilesize)
            y = int(self.y / tilesize) - int(next_cell.y / tilesize)
            if y == 1:  # top
                self.walls[0] = False
                next_cell.walls[2] = False
            elif x == -1:  # right
                self.walls[1] = False
                next_cell.walls[3] = False
            elif y == -1:  # bottom
                self.walls[2] = False
                next_cell.walls[0] = False
            elif x == 1:  # left
                self.walls[3] = False
                next_cell.walls[1] = False


        def addNeighbors(self):
            if self.top and not self.walls[0] and not self.top.walls[2]:
                self.neighbors.append(self.top)
            if self.right and not self.walls[1] and not self.right.walls[3]:
                self.neighbors.append(self.right)
            if self.bottom and not self.walls[2] and not self.bottom.walls[0]:
                self.neighbors.append(self.bottom)
            if self.left and not self.walls[3] and not self.left.walls[1]:
                self.neighbors.append(self.left)
            
            self.visited = True
                
        def draw(self):
            if self.current:
                pygame.draw.rect(screen, RED, (self.x, self.y, tilesize, tilesize))
            elif self.start:
                pygame.draw.rect(screen, GREEN, (self.x, self.y, tilesize, tilesize))
            elif self.end:
                pygame.draw.rect(screen, RED, (self.x, self.y, tilesize, tilesize))
            elif self.visited:
                pygame.draw.rect(screen, WHITE, (self.x, self.y, tilesize, tilesize))
            
                if self.walls[0]:
                    pygame.draw.line(screen, BLACK, (self.x, self.y), ((self.x + tilesize), self.y), 1)  # top
                if self.walls[1]:
                    pygame.draw.line(screen, BLACK, ((self.x + tilesize), self.y), ((self.x + tilesize), (self.y + tilesize)), 1)  # right
                if self.walls[2]:
                    pygame.draw.line(screen, BLACK, ((self.x + tilesize), (self.y + tilesize)), (self.x, (self.y + tilesize)), 1)  # bottom
                if self.walls[3]:
                    pygame.draw.line(screen, BLACK, (self.x, (self.y + tilesize)), (self.x, self.y), 1)  # left
        
        def checkNeighbors(self):
            if int(self.y / tilesize) - 1 >= 0:
                self.top = grid[int(self.y / tilesize) - 1][int(self.x / tilesize)]
            if int(self.x / tilesize) + 1 <= cols - 1:
                self.right = grid[int(self.y / tilesize)][int(self.x / tilesize) + 1]
            if int(self.y / tilesize) + 1 <= rows - 1:
                self.bottom = grid[int(self.y / tilesize) + 1][int(self.x / tilesize)]
            if int(self.x / tilesize) - 1 >= 0:
                self.left = grid[int(self.y / tilesize)][int(self.x / tilesize) - 1]
            
            if self.top and not self.top.visited:
                self.neighbors.append(self.top)
            if self.right and not self.right.visited:
                self.neighbors.append(self.right)
            if self.bottom and not self.bottom.visited:
                self.neighbors.append(self.bottom)
            if self.left and not self.left.visited:
                self.neighbors.append(self.left)
            
            if self.neighbors:
                self.next_cell = random.choice(self.neighbors)
                return self.next_cell
            return False


    # Initialize grid
    grid = [[Cell(x, y) for x in range(cols)] for y in range(rows)]
    stack = []
    current_cell = grid[0][0]
    done = False
    text_highlight = False
    generated = False
            
    grid[0][0].start = True
    grid[rows - 1][cols - 1].end = True

    def recursive_bfs(current):
        current.addNeighbors()

        for i in current.neighbors:
            print(i.x, i.y)

        

    while not done:
        screen.fill(BGCOLOR)
        text = FONT.render("GENERATING..." if not generated else "SOLVE MAZE", True, COLOR_INACTIVE if (text_highlight and generated) else TEXT_COLOR)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT + 40))
        screen.blit(text, text_rect)

        current_cell.visited = True
        current_cell.current = True

        for row in grid:
            for cell in row:
                cell.draw()

        next_cell = current_cell.checkNeighbors()

        if next_cell:
            current_cell.neighbors = []
            stack.append(current_cell)
            current_cell.removeWalls(next_cell)
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
                        recursive_bfs(current_cell)
        pygame.display.flip()
        clock.tick(60)
