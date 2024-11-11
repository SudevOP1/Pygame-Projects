import pygame
from os.path import join
from random import randint, uniform
from math import sin as sin
from math import pi as pi

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

# Classes
class Player(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)

        # Images
        self.image = pygame.image.load(join("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Movement
        self.direction = pygame.math.Vector2(1, 1)
        self.speed = 500
        self.can_move = True

        # Death
        self.is_dead = False
        self.spawn_meteor = True

        # Laser Cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 150

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration: self.can_shoot = True

    def update(self, dt):
        if self.can_move:

            # Movement
            keys = pygame.key.get_pressed()
            if self.rect.right  >= WINDOW_WIDTH : self.rect.right  = WINDOW_WIDTH
            if self.rect.left   <= 0            : self.rect.left   = 0
            if self.rect.bottom >= WINDOW_HEIGHT: self.rect.bottom = WINDOW_HEIGHT
            if self.rect.top    <= 0            : self.rect.top    = 0
            self.direction.x = int(keys[pygame.K_d])-int(keys[pygame.K_a])
            self.direction.y = int(keys[pygame.K_s])-int(keys[pygame.K_w])
            self.direction = self.direction.normalize() if self.direction else self.direction
            self.rect.center += self.direction * self.speed * dt

            # Laser
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.can_shoot:
                Laser(laser_image, self.rect.midtop, (all_sprites, laser_sprites))
                self.can_shoot = False
                self.laser_shoot_time = pygame.time.get_ticks()
                laser_sound.play()
            self.laser_timer()

class Star(pygame.sprite.Sprite):

    def __init__(self, groups, star_image):
        super().__init__(groups)
        self.image = star_image
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
        self.can_move = True

class Laser(pygame.sprite.Sprite):

    def __init__(self, laser_image, pos, groups):
        super().__init__(groups)
        self.image = laser_image
        self.rect = self.image.get_frect(midbottom = pos)
        self.speed = 1000
        self.can_move = True
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        if self.can_move:
            self.rect.y -= self.speed * dt
            if self.rect.bottom < 0: self.kill()

class Meteor(pygame.sprite.Sprite):

    def __init__(self, meteor_image, groups):
        super().__init__(groups)
        self.og_image = self.image = meteor_image
        self.rect = self.image.get_frect(midbottom = (randint(0, WINDOW_WIDTH), -10))
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.can_move = True
        # Rotation
        self.rotation_speed = uniform(-100, -50) or uniform(50, 100)
        self.rotation = 0

    def update(self, dt):
        if self.can_move:
            
            # Movement
            self.rect.x += self.direction.x * self.speed * dt
            self.rect.y += self.direction.y * self.speed * dt

            # Rotation
            self.rotation += self.rotation_speed * dt
            self.image = pygame.transform.rotozoom(self.og_image, self.rotation, 1)
            self.rect = self.image.get_frect(center = self.rect.center)
        
            # Kill
            if self.rect.top > WINDOW_HEIGHT: self.kill()

class Explosion(pygame.sprite.Sprite):

    def __init__(self, pos, frames, groups):
        super().__init__(groups)
        self.frames       = frames
        self.frame_index  = 0
        self.image        = self.frames[int(self.frame_index)]
        self.rect         = self.image.get_frect(center = pos)
        self.can_move     = True
        
    def update(self, dt):
        if self.can_move:
            self.frame_index += 40 * dt
            if self.frame_index <  len(self.frames): self.image = self.frames[int(self.frame_index)]
            if self.frame_index >= len(self.frames): self.kill()


# Functions
def display_score(last_restart_time):

    # Score Text
    score = str((pygame.time.get_ticks() - last_restart_time) // 1000)
    score_surf = game_font_40.render(score, True, "white")
    score_rect = score_surf.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT-50))
    display_surface.blit(score_surf, score_rect)

    # Design around Text
    pygame.draw.line(display_surface, "white", start_pos=score_rect.topleft + pygame.Vector2(-10, -10),  end_pos=score_rect.topright + pygame.Vector2(10, -10) , width=3)
    pygame.draw.line(display_surface, "white", start_pos=score_rect.topright + pygame.Vector2(10, -10),  end_pos=score_rect.bottomright + pygame.Vector2(10, 0), width=3)
    pygame.draw.line(display_surface, "white", start_pos=score_rect.bottomright + pygame.Vector2(10, 0), end_pos=score_rect.bottomleft + pygame.Vector2(-10, 0), width=3)
    pygame.draw.line(display_surface, "white", start_pos=score_rect.bottomleft + pygame.Vector2(-10, 0), end_pos=score_rect.topleft + pygame.Vector2(-10, -10) , width=3)

def check_laser_meteor_collision():
    for laser in laser_sprites:
        collided_meteors = pygame.sprite.spritecollide(sprite=laser, group=meteor_sprites, dokill=True, collided=pygame.sprite.collide_mask)
        if collided_meteors:
            explosion_sound.play()
            laser.kill()
            for meteor in collided_meteors: Explosion(meteor.rect.center, explosion_images, all_sprites)

def check_player_meteor_collision():
    global game_menu, game_menu_start_time
    collided_meteors = pygame.sprite.spritecollide(sprite=player, group=meteor_sprites, dokill=False, collided=pygame.sprite.collide_mask)
    if collided_meteors:
        for sprite in all_sprites: sprite.can_move = False
        for meteor in collided_meteors: player.is_dead = True
        if player.is_dead:
            game_menu = True
            game_menu_start_time = pygame.time.get_ticks()


# General setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
running      = True
spawn_meteor = False
initial_score = 0

# Load files
bg_music         = pygame.mixer.Sound(join("audio", "game_music.wav"))
laser_sound      = pygame.mixer.Sound(join("audio", "laser.wav"))
explosion_sound  = pygame.mixer.Sound(join("audio", "explosion.wav"))
game_font_40     = pygame.font.Font("Oxanium-Bold.ttf", 40)
game_font_50     = pygame.font.Font("Oxanium-Bold.ttf", 50)
game_font_90     = pygame.font.Font("Oxanium-Bold.ttf", 90)
star_image       = pygame.image.load(join("images", "star.png")).convert_alpha()
laser_image      = pygame.image.load(join("images", "laser.png")).convert_alpha()
meteor_image     = pygame.image.load(join("images", "meteor.png")).convert_alpha()
explosion_images = [
    pygame.transform.rotozoom(
        pygame.image.load(join("images", "explosion", str(i) + ".png")).convert_alpha(),
        0,
        2 
    )
    for i in range(21)
]
bg_music.set_volume(0.4)
bg_music.play(loops=-1)
laser_sound.set_volume(0.5)
explosion_sound.set_volume(0.5)

# Sprites Setup
all_sprites    = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites  = pygame.sprite.Group()
star_sprites   = pygame.sprite.Group()
player         = Player(all_sprites)
for i in range(30): Star((all_sprites, star_sprites), star_image)

# Meteor Custom Event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 100)

# Game Menu Setup
game_menu  = True
reset_done = False
game_menu_start_time  = 0
oscillation_time      = 0
last_restart_time     = 0
game_title_text_surf  = game_font_90.render("MONSTER SHOOTER", True, "white")
press_space_text_surf = game_font_50.render("Press SPACE to Start", True, "white")
game_title_text_rect  = game_title_text_surf .get_frect(midtop    = ((WINDOW_WIDTH/2), 130))
press_space_text_rect = press_space_text_surf.get_frect(midbottom = ((WINDOW_WIDTH/2), (WINDOW_HEIGHT) - 10))
game_menu_player_image_surf = pygame.transform.rotozoom(player.image, 0, 1.5)
game_menu_player_image_rect = game_menu_player_image_surf.get_frect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))


# Run
while running:
    dt = clock.tick(60) / 1000

    # Game Menu
    if game_menu:
        oscillation_time += dt

        # Wait for 500 ms
        if pygame.time.get_ticks() - game_menu_start_time < 1000:
            current_time = pygame.time.get_ticks()
            score = str(int(current_time // 1000))
            display_score(last_restart_time)
            continue
        
        # Kill player, meteor, laser sprites
        if not reset_done:
            score = 0
            player.spawn_meteor = True
            meteor_sprites.empty()
            laser_sprites.empty()
            for sprite in meteor_sprites: sprite.kill()
            for sprite in all_sprites:
                if isinstance(sprite, (Player, Laser, Meteor, Explosion)):
                    sprite.kill()
            reset_done = True

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == meteor_event: Meteor(meteor_image, meteor_sprites)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_menu = False
                last_restart_time = current_time
                player = Player(all_sprites)

        # Update variables and sprites
        game_menu_player_image_rect.center = ((WINDOW_WIDTH/2), (WINDOW_HEIGHT/2))
        game_menu_player_image_rect.centery += 50*sin(3*pi*oscillation_time)
        meteor_sprites.update(dt)

        # Draw game menu
        display_surface.fill("#3a2e3f")
        meteor_sprites.draw(display_surface)
        display_surface.blit(game_menu_player_image_surf, game_menu_player_image_rect)
        display_surface.blit(game_title_text_surf , game_title_text_rect )
        display_surface.blit(press_space_text_surf, press_space_text_rect)
        pygame.display.update()

    # Game Playing
    if not game_menu:
        if reset_done: reset_done = False
        current_time = pygame.time.get_ticks()

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == meteor_event and player.spawn_meteor: Meteor(meteor_image, (all_sprites, meteor_sprites))

        # Update
        all_sprites.update(dt)
        check_laser_meteor_collision()
        check_player_meteor_collision()
        score = str(int(current_time // 1000))

        # Draw the game
        display_surface.fill("#3a2e3f")
        all_sprites.draw(display_surface)
        display_score(last_restart_time)
        pygame.display.update()

pygame.quit()