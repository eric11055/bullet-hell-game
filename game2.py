import pygame,sys
from random import randint


pos = pygame.math.Vector2(250,250)
clock = pygame.time.Clock()
velocity = pygame.math.Vector2(0,0)
acceleration = 2.5
friction = 0.5
width = 900
height = 500

metal_tile = pygame.image.load('resources/default/tile_0009.png')




class Player(pygame.sprite.Sprite):
    def __init__(self,pos,velocity,group):
        super().__init__(group)
        self.player_image = pygame.image.load('resources/player/player1.png')
        self.player_rect = self.player_image.get_rect(center = pos)
        self.pos = pos
        self.velocity = velocity
        
    def player_controls(self):
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
            self.velocity += input_vector * acceleration
        # apply friction
        self.velocity -= friction * self.velocity
        #update position using velocity
        self.pos += self.velocity
        self.player_rect.x = pos.x
        self.player_rect.y = pos.y

        if self.pos.x > 900:
            self.pos.x = 900
        elif self.pos.x < 0:
            self.pos.x = 0

        if self.pos.y > 500:
            self.pos.y = 500
        elif self.pos.y < 0:
            self.pos.y = 0
        
    


        if self.pos.x > 900:
            self.pos.x = 900
        elif self.pos.x < 0:
            self.pos.x = 0

        if self.pos.y > 500:
            self.pos.y = 500
        elif pos.y < 0:
            self.pos.y = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,velocity):
        self.velocity = velocity
        self.Rect = pygame.Rect(x,y,5,5)

    def move_bullet(self):
        self.Rect.x += self.velocity.x
        self.Rect.y += self.velocity.y
               

def draw(screen, bullets):
    tile_width = metal_tile.get_width()
    tile_height = metal_tile.get_height()

    screen.fill('black')
    for i in range(width // tile_width + 1):
        for j in range(height // tile_height + 1):
            
            x = i * tile_width # 0, tile_width, 2 * tile_width, 3 * tile_widt
            y = j * tile_height
            screen.blit(metal_tile,(x,y))
        
    
        

    screen.blit(player1.player_image,player1.player_rect)

    for bullet in bullets:
        pygame.draw.rect(screen, (0,0,255), bullet.Rect)

    pygame.display.update()


def spawn_bullet(bullets):
    mouse_pos = pygame.math.Vector2(0,0)

    mouse_pos.x, mouse_pos.y = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()
    if mouse_pos != pygame.math.Vector2(0,0):
        if mouse_press[0]:
            bullet_velocity = (mouse_pos - pos)
            if bullet_velocity.length != 0:
                bullet_velocity = 5 * bullet_velocity.normalize()
                bullet = Bullet(bullet_velocity.x + player1.player_rect.centerx, bullet_velocity.y + player1.player_rect.centery, bullet_velocity)
                bullets.append(bullet)



camera_group = pygame.sprite.Group
player1 = Player(pos,velocity,camera_group)
    

    

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
                sys.exit()
                
        camera_group.update()
        camera_group.draw(screen)          
        
        player1.player_controls()
        spawn_bullet(bullets)
        draw(screen, bullets)
        clock.tick(60)
        for bullet in bullets:
            bullet.move_bullet()



        
        

if __name__ == '__main__':  
    run_game()