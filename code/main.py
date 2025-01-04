from os import kill
import pygame
from os.path import join
from random import randint, uniform


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images','player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2()
        self.speed = 500
         
        #timer cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        # mask
        self.mask = pygame.mask.from_surface(self.image)
        
 
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
         
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot == True:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()

        self.laser_timer()

                     
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
 
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, dt):
        self.rect.centery -= 900 * dt
        if self.rect.bottom < 0:
            self.kill()
        
class Meteor(pygame.sprite.Sprite):
    def __init__(self,surf, pos, groups):
        super().__init__(groups)
        self.original_surface = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.life_time = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400,500)
        self.mask = pygame.mask.from_surface(self.image)
        self.rotation_speed = randint(40,80)
        self.rotation = 0
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt 
        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surface, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        explosion_sound.play()
    
    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def reset_game():
    # Clear all sprites
    all_sprites.empty()
    meteor_sprites.empty()
    laser_sprites.empty()

    # Recreate stars and player
    for i in range(20):
        Star(all_sprites, star_surface)
    global player
    player = Player(all_sprites)

    # Reset game variables (e.g., score)
    global start_time
    start_time = pygame.time.get_ticks()
        
def collisions():
    global game_paused
    
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        explosion_sound.play()
        AnimatedExplosion(explosion_frames, player.rect.center, all_sprites)
        game_paused = True
        
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    text_surf = font.render(str(current_time), True, (240,240,240))
    text_rect = text_surf.get_frect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (240,240,240), text_rect.inflate(20, 12).move(0, -8), 5, 10)

def show_menu():
    global menu_displayed
    if not menu_displayed:
        # Render menu background
        menu_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        menu_surf.set_alpha(200)
        menu_surf.fill((0, 0, 0))
        display_surface.blit(menu_surf, (0, 0))

        # Render options
        font_size = 50
        menu_font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), font_size)
        reset_text = menu_font.render("Press R to Reset", True, (255, 255, 255))
        quit_text = menu_font.render("Press Q to Quit", True, (255, 255, 255))

        reset_rect = reset_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - font_size))
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + font_size))

        display_surface.blit(reset_text, reset_rect)
        display_surface.blit(quit_text, quit_rect)
        pygame.display.update()

        menu_displayed = True  # Mark menu as displayed

def handle_menu_input():
    global running, game_paused, menu_displayed

    # Handle events to reset or quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reset the game
                reset_game()
                game_paused = False
                menu_displayed = False  # Reset menu display flag
            elif event.key == pygame.K_q:  # Quit the game
                running = False
    
#General Setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280 , 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
running = True
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
game_paused = False
menu_displayed = False

# import
meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()
star_surface = pygame.image.load(join('images', 'star.png')).convert_alpha()
explosion_frames = [ pygame.image.load((join('images', 'explosion', f'{i}.png'))).convert_alpha() for i in range(21) ]
laser_sound = pygame.mixer.Sound(join('audio','laser.wav'))
laser_sound.set_volume(0.2)
explosion_sound = pygame.mixer.Sound(join('audio','explosion.wav'))
explosion_sound.set_volume(0.2)


game_music = pygame.mixer.Sound(join('audio','game_music.wav'))
game_music.set_volume(0.2)
game_music.play(loops=-1)


# load sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
font = pygame.font.Font(join('images','Oxanium-Bold.ttf'), 40)

for i in range(20):
    Star(all_sprites, star_surface)
player = Player(all_sprites)
    

# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)


while running:
    dt = clock.tick() / 1000
    
    if game_paused:
        show_menu()
        handle_menu_input()
        continue
    
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event and not game_paused:
            x,y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor (meteor_surf, (x, y), (all_sprites, meteor_sprites))
            
    # update
    all_sprites.update(dt)
    collisions()
    
    
    
    
    
    #draw game
    display_surface.fill('#3a2e3f') 
    display_score()

    all_sprites.draw(display_surface)
    
    
    
    
    
    pygame.display.update()
    
    
pygame.quit()