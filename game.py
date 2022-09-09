import pygame 
from sys import exit

screen = pygame.display.set_mode((500,500))
pygame.init()

player = pygame.image.load('resources/player/player1.png')

        
x = 250
y = 250


clock = pygame.time.Clock()

speed = 4




def run_game():
    global x
    global y
    
    pygame.init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            

        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            y -= speed
        if key[pygame.K_a]:
            x -= speed
        if key[pygame.K_s]:
            y += speed
        if key[pygame.K_d]:
            x += speed

        screen.fill('black')
        screen.blit(player,(x,y))

        

        pygame.display.update()
        clock.tick(60)