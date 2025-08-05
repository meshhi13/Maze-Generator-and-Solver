import pygame
from settings import *

class Cell():
    def __init__(self, x, y, tilesize):
        self.x = x * tilesize
        self.y = y * tilesize
        
        self.visited = False
        self.current = False
        self.start = False
        self.end = False
        self.searched = False
        self.path = False
        
        self.walls = [True, True, True, True]  # top, right, bottom, left
        self.neighbors = []
        
        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0
        self.next_cell = 0

    def removeWalls(self, next_cell, tilesize):
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


    def addNeighbors(self, tilesize):
        if self.top and not self.walls[0] and not self.top.walls[2] and not self.top.searched:
            self.neighbors.append(self.top)
        if self.right and not self.walls[1] and not self.right.walls[3] and not self.right.searched:
            self.neighbors.append(self.right)
        if self.bottom and not self.walls[2] and not self.bottom.walls[0] and not self.bottom.searched:
            self.neighbors.append(self.bottom)
        if self.left and not self.walls[3] and not self.left.walls[1] and not self.left.searched:
            self.neighbors.append(self.left)
            
    def draw(self, tilesize):
        if self.start or self.path:
            pygame.draw.rect(screen, GREEN, (self.x, self.y, tilesize, tilesize))
        elif self.searched:
            pygame.draw.rect(screen, SEARCHED, (self.x, self.y, tilesize, tilesize))
        elif self.current:
            pygame.draw.rect(screen, CURRENT, (self.x, self.y, tilesize, tilesize))
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

class Grid():
    def __init__(self, rows, cols):
        self.grid = [[Cell(x, y, WIDTH // rows) for x in range(cols)] for y in range(rows)]
    
    def checkNeighbors(self, current_cell, tilesize, rows, cols):
        if int(current_cell.y / tilesize) - 1 >= 0:
            current_cell.top = self.grid[int(current_cell.y / tilesize) - 1][int(current_cell.x / tilesize)]
        if int(current_cell.x / tilesize) + 1 <= cols - 1:
            current_cell.right = self.grid[int(current_cell.y / tilesize)][int(current_cell.x / tilesize) + 1]
        if int(current_cell.y / tilesize) + 1 <= rows - 1:
            current_cell.bottom = self.grid[int(current_cell.y / tilesize) + 1][int(current_cell.x / tilesize)]
        if int(current_cell.x / tilesize) - 1 >= 0:
            current_cell.left = self.grid[int(current_cell.y / tilesize)][int(current_cell.x / tilesize) - 1]
        
        if current_cell.top and not current_cell.top.visited:
            current_cell.neighbors.append(current_cell.top)
        if current_cell.right and not current_cell.right.visited:
            current_cell.neighbors.append(current_cell.right)
        if current_cell.bottom and not current_cell.bottom.visited:
            current_cell.neighbors.append(current_cell.bottom)
        if current_cell.left and not current_cell.left.visited:
            current_cell.neighbors.append(current_cell.left)
        
        if current_cell.neighbors:
            current_cell.next_cell = random.choice(current_cell.neighbors)
            return current_cell.next_cell
        
        return False
