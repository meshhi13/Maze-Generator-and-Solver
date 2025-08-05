import pygame
import sys
from settings import *
from gamestate import *
from menuitems import MenuItems

def menu_loop(state):
    menu_items = [
        MenuItems("PLAY", False, None),
        MenuItems(f"SIZE: {state.rows}", False, None),
        MenuItems(f"ALGORITHM: {state.algorithm}", False, None),
        MenuItems("QUIT", False, None)
                  ]
    
    while True:
        screen.fill(BGCOLOR)
        
        for i, item in enumerate(menu_items):
            text = FONT.render(item.text, True, COLOR_INACTIVE if item.selected else TEXT_COLOR)
            item.rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + (i-1.5) * 70))
            screen.blit(text, item.rect)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, item in enumerate(menu_items):
                    if item.rect.collidepoint((mouse_x, mouse_y)):
                        item.selected = True
                    else:
                        item.selected = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, item in enumerate(menu_items):
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        if item.rect.collidepoint((mouse_x, mouse_y)):
                            if item.text == "PLAY":
                                return
                            elif item.text.startswith("ALGORITHM:"):
                                state.algorithm = next(state.cycle_algo)
                                item.text = f"ALGORITHM: {state.algorithm}"
                            elif item.text.startswith("SIZE:"):
                                state.rows = next(state.cycle_size)
                                item.text = f"SIZE: {state.rows}"
                                state.cols = state.rows
                            elif item.text == "QUIT":
                                pygame.quit()
                                sys.exit()

        pygame.display.update()
        clock.tick(30)

