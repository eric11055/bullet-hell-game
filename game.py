import pygame 
from sys import exit
screen = pygame.display.set_mode((500,500))
pygame.init()

def run_game():
    pygame.init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()