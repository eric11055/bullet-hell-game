import pygame 
import math

player = pygame.image.load('resources/player/player1.png')


pos = pygame.math.Vector2(250,250)
    


clock = pygame.time.Clock()

speed = 4

velocity = pygame.math.Vector2(0,0)
acceleration = 2.5
friction = 0.5
width = 900
height = 500

metal_tile = pygame.image.load('resources/default/tile_0009.png')
player = pygame.image.load('resources/player/player1.png')





class Bullet():
    def __init__(self, Rect,x,y,velocity,mx,my):
        self.Rect = Rect
        self.velocity = velocity
        angle = math.atan2(mx,my)
        self.dx = math.sin(angle) * speed
        self.dy = math.cos(angle) * speed
        self.x = x
        self.y = y       

    def move_bullet(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.Rect.x = int(self.x)
        self.Rect.y = int(self.y)
        pass
        

        
                

        


def draw(screen, bullets):
    tile_width = metal_tile.get_width()
    tile_height = metal_tile.get_height()

    screen.fill('black')
    for i in range(width // tile_width + 1):
        for j in range(height // tile_height + 1):
            
            x = i * tile_width # 0, tile_width, 2 * tile_width, 3 * tile_widt
            y = j * tile_height

            screen.blit(metal_tile,(x,y))
    for bullet in bullets:
        pygame.draw.rect(screen, (0,0,255), bullet.Rect)
    
    screen.blit(player,(pos.x,pos.y))
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
    
    mouse_pos = pygame.math.Vector2(0,0)

    mouse_pos.x, mouse_pos.y = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()
    if mouse_pos != pygame.math.Vector2(0,0):
        mouse_pos = mouse_pos.normalize()
        if mouse_press[0]:
            x = pos.x
            y = pos.y
            rect = pygame.Rect(mouse_pos.x + pos.x,mouse_pos.y + pos.y, 5,5)
            bullet_velocity = (mouse_pos - pos) * 1
            bullet = Bullet(rect,bullet_velocity,x,y,mouse_pos.x,mouse_pos.y)
            bullets.append(bullet)


    

    

def run_game():
    global pos
    global velocity

    pygame.init()
    screen = pygame.display.set_mode((width,height))
    run = True

    bullets = []

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()



                
        
        player_controls(bullets)
        draw(screen, bullets)
        clock.tick(60)
        for bullet in bullets:
            bullet.move_bullet()



        
        

if __name__ == '__main__':
    run_game()