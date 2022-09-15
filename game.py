import pygame,sys
from random import randint


player = pygame.image.load('resources/player/player1.png')

spawn_pos = pygame.math.Vector2(250,250)
pos = spawn_pos.copy()
clock = pygame.time.Clock()
velocity = pygame.math.Vector2(0,0)
acceleration = 2.5
friction = 0.5
width = 900
height = 500

metal_tile = pygame.image.load('resources/default/tile_0009.png')
player = pygame.image.load('resources/player/player1.png')





class Bullet():
    def __init__(self,x,y,velocity):
        self.velocity = velocity
        self.Rect = pygame.Rect(x,y,5,5)

    def move_bullet(self):
        self.Rect.x += self.velocity.x
        self.Rect.y += self.velocity.y
        

        
            

        


def draw(screen, bullets,tiles):
    tile_width = metal_tile.get_width()
    tile_height = metal_tile.get_height()

    screen.fill('black')
    for i in range(width // tile_width + 1):
        for j in range(height // tile_height + 1):
            
            x = i * tile_width - pos.x + spawn_pos.x # 0, tile_width, 2 * tile_width, 3 * tile_widt
            y = j * tile_height - pos.y + spawn_pos.y
            screen.blit(metal_tile,(x,y))
        
    
        

    screen.blit(player,(spawn_pos.x,spawn_pos.y))

    for bullet in bullets:
        pygame.draw.rect(screen, (0,0,255), bullet.Rect)

    pygame.display.update()



def player_controls(bullets):
    global pos
    global velocity
    

    key = pygame.key.get_pressed()
    # update the velocity vector using acceleration
    input_vector = pygame.math.Vector2(0,0)
    if key[pygame.K_w]:
        input_vector.y -= 1
    if key[pygame.K_a]:
        input_vector.x -= 1
    if key[pygame.K_s]:
        input_vector.y += 1
    if key[pygame.K_d]:
        input_vector.x += 1
    if input_vector != pygame.math.Vector2(0,0):
        input_vector = input_vector.normalize()
        velocity += input_vector * acceleration
    # apply friction
    velocity -= friction * velocity
    #update position using velocity
    pos += velocity

    if pos.x > 900:
        pos.x = 900
    elif pos.x < 0:
        pos.x = 0

    if pos.y > 500:
        pos.y = 500
    elif pos.y < 0:
        pos.y = 0

        
    
    mouse_pos = pygame.math.Vector2(0,0)

    mouse_pos.x, mouse_pos.y = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()
    if mouse_pos != pygame.math.Vector2(0,0):
        if mouse_press[0]:
            bullet_velocity = (mouse_pos - spawn_pos)
            if bullet_velocity.length != 0:
                bullet_velocity = 5 * bullet_velocity.normalize()
                bullet = Bullet(bullet_velocity.x + spawn_pos.x, bullet_velocity.y + spawn_pos.y, bullet_velocity)
                bullets.append(bullet)


    

    

def run_game():
    global pos
    global velocity
    tiles = []
    pygame.init()

    
    screen = pygame.display.set_mode((width,height))
    run = True

    bullets = []

    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()



                
        
        player_controls(bullets)
        draw(screen, bullets,tiles)
        clock.tick(60)
        for bullet in bullets:
            bullet.move_bullet()



        
        

if __name__ == '__main__':
    
    run_game()