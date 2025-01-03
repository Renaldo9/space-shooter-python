# TIME IN VIDEO: 2:03:53
import pygame
from os.path import join
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
         super().__init__(groups)
         self.image = pygame.image.load(join('images','player.png')).convert_alpha()
         self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
         self.direction = pygame.Vector2()
         self.speed = 300
         
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print("fire laser")
         
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
 
    
#General Setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280 , 720
# set surface
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
# set title
pygame.display.set_caption("Space Shooter")
running = True

clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
star_surface = pygame.image.load(join('images', 'star.png')).convert_alpha()
for i in range(20):
    Star(all_sprites, star_surface)
player = Player(all_sprites)
    

meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha()
meteor__rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2 , WINDOW_HEIGHT / 2))

laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft = (20 , WINDOW_HEIGHT - 20))


while running:
    dt = clock.tick() / 1000

    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # update
    all_sprites.update(dt)
    
    #draw game
    display_surface.fill('darkgrey') 
    all_sprites.draw(display_surface)
    
    
    pygame.display.update()
    
    
pygame.quit()