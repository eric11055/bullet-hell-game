import pygame,sys
from random import randint

width = 900
height = 500
pos = pygame.math.Vector2(width//2,height//2)
pos_offset = pygame.math.Vector2(width//2,height//2)
clock = pygame.time.Clock()
velocity = pygame.math.Vector2(0,0)
acceleration = 2.5
friction = 0.5
metal_tile = pygame.image.load('resources/default/tile_0009.png')

class Target(pygame.sprite.Sprite):
    def __init__(self,group) -> None:
        super().__init__(group)
        self.image = pygame.surface.Surface((10,10))
        self.image.fill((255,0,0))
        self.x = width//2 + 50
        self.y = height//2
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.pos = pygame.math.Vector2(self.x,self.y)


        
    def change_color(self):
        self.image.fill((0,255,0))
        spawn_enemy_bullet(bullets)
        

    def update(self,delta_pos: pygame.math.Vector2):
        self.x -= delta_pos.x
        self.y -= delta_pos.y
        self.rect.x = self.x
        self.rect.y = self.y

        



class Player(pygame.sprite.Sprite):
    def __init__(self,pos,velocity,group):
        super().__init__()
        self.group = group
        self.past_pos = None
        self.image = pygame.image.load('resources/player/player1.png').convert_alpha()
        self.rect = self.image.get_rect(center = (width//2,height//2))
        self.pos = pos
        self.velocity = velocity

    def update(delta_pos):
        pass
        
    def player_controls(self):
        self.past_pos = self.pos.copy()
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

        if self.pos.x > 900:
            self.pos.x = 900
        elif self.pos.x < 0:
            self.pos.x = 0

        if self.pos.y > 500:
            self.pos.y = 500
        elif self.pos.y < 0:
            self.pos.y = 0
        self.group.update(self.pos - self.past_pos)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,velocity,group):
        super().__init__(group)
        self.velocity = velocity
        self.image = pygame.Surface([5, 5])
        self.image.fill((0,0,255))     
        self.rect = self.image.get_rect(center = (x, y))
        self.x = x
        self.y = y
        

    def update(self,delta_pos: pygame.math.Vector2):
        self.x -= delta_pos.x
        self.y -= delta_pos.y

    def move_bullet(self):
        self.x += self.velocity.x
        self.y += self.velocity.y
        self.rect.x = self.x
        self.rect.y = self.y

class Gun(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load('resources/player/gun.png')
        self.rect = self.image.get_rect(center = (pos.x+2.5,pos.y+3))
        self.x,self.y = pos

gun = Gun()

                       

def draw(screen, bullets):
    tile_width = metal_tile.get_width()
    tile_height = metal_tile.get_height()

    screen.fill('black')
    for i in range(width // tile_width + 1):
        for j in range(height // tile_height + 1):
            
            x = i * tile_width - pos.x + pos_offset.x
            y = j * tile_height - pos.y + pos_offset.y
            screen.blit(metal_tile,(x,y))
        
    
        
    screen.blit(target.image,target.rect)
    screen.blit(player1.image,player1.rect)
    screen.blit(gun.image,gun.rect)

    for bullet in bullets:
        pygame.draw.rect(screen, (0,0,255), bullet.rect)

    pygame.display.update()

def spawn_enemy_bullet(bullets):
    target_pos = pygame.math.Vector2(0,0)
    target_pos.x, target_pos.y = player1.pos.x,player1.pos.y
    if target_pos != pygame.math.Vector2(0,0):
        bullet_velocity = (target_pos - target.pos)
        if bullet_velocity.length != 0:
            bullet_velocity = 5 * bullet_velocity.normalize()
            bullet = Bullet(bullet_velocity.x + target.x, bullet_velocity.y + target.y, bullet_velocity,camera_group)
            bullets.append(bullet)

            for index, bullet in enumerate(bullets):
                if bullet.x > height or bullet.x < 0:
                    del bullets[index]
                if bullet.y > width or bullet.y < 0:
                    del bullets[index]                   

def spawn_bullet(bullets):
    mouse_pos = pygame.math.Vector2(0,0)
    mouse_pos.x, mouse_pos.y = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()
    if mouse_pos != pygame.math.Vector2(0,0):
        if mouse_press[0]:
            offset = pygame.math.Vector2(width//2, height//2)
            bullet_velocity = (mouse_pos - offset)
            if bullet_velocity.length != 0:
                bullet_velocity = 5 * bullet_velocity.normalize()
                bullet = Bullet(2 * bullet_velocity.x + width//2, 2 * bullet_velocity.y + height//2+1.5, bullet_velocity,camera_group)
                bullets.append(bullet)

            for index, bullet in enumerate(bullets):
                if bullet.x > height or bullet.x < 0:
                    del bullets[index]
                if bullet.y > width or bullet.y < 0:
                    del bullets[index]
                    

    

def run_game():
    global pos
    global velocity
    global metal_tile
    global player1
    global camera_group
    global target
    global bullets
    
    
    pygame.init()
    bullets = []
    screen = pygame.display.set_mode((width,height))
    camera_group = pygame.sprite.Group()
    player1 = Player(pos,velocity,camera_group)
    metal_tile = pygame.image.load('resources/default/tile_0009.png').convert_alpha()
    target = Target(camera_group)
    run = True

    

    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        
        player1.player_controls()
        spawn_bullet(bullets)
        draw(screen, bullets)
        clock.tick(60)
        for bullet in bullets:
            bullet.move_bullet()
            if target.rect.colliderect(bullet.rect):
                target.change_color()
                bullets.remove(bullet)

        


        
        

if __name__ == '__main__':  
    run_game()