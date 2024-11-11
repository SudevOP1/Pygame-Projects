from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from random import randint, choice
from os.path import join

class Game:

    def __init__(self):

        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Survivor')
        self.clock     = pygame.time.Clock()
        self.running   = True
        self.main_menu = True

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # gun timer
        self.can_shoot = True
        self.shoot_time = 0 
        self.gun_cooldown = 100

        # enemy timer 
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 300)
        self.spawn_positions = []
        
        # audio
        self.music_toggle = True
        self.sound_toggle = True
        self.shoot_sound = pygame.mixer.Sound(join("..", 'audio', 'shoot.wav'))
        self.shoot_sound.set_volume(0.2)
        self.impact_sound = pygame.mixer.Sound(join('..', 'audio', 'impact.ogg'))
        self.music = pygame.mixer.Sound(join('..', 'audio', 'music.wav'))
        self.music.set_volume(0.5)
        self.music.play(loops = -1)

        # setup
        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_surf  = pygame.image.load(join('..', "images", "gun", "bullet.png")).convert_alpha()
        self.bg_image     = pygame.image.load(join('..', "images", "bg.png")).convert_alpha()
        self.game_font_40 = pygame.font.Font (join('..', "data"  , "karmatic_arcade.ttf"), size=40)

        folders = list(walk(join('..', "images", "enemies")))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join('..', "images", "enemies", folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key = lambda name: int(name.split(".")[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(
                self.bullet_surf,
                pos,
                self.gun.player_direction,
                (self.all_sprites, self.bullet_sprites)
            )
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.gun_cooldown : self.can_shoot = True

    def setup(self):
        map = load_pygame(join('..', 'data', 'maps', 'world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE,y * TILE_SIZE), image, self.all_sprites)
        
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    bullet,
                    self.enemy_sprites,
                    False,
                    pygame.sprite.collide_mask
                )
                if collision_sprites:
                    self.impact_sound.play()
                    for sprite in collision_sprites:
                        sprite.destroy()
                    bullet.kill()

    def player_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            # kill enemy and bullet sprites
            for sprite in self.bullet_sprites: sprite.kill()
            for sprite in self.enemy_sprites : sprite.kill()
            # reset player pos to spawn
            for obj in load_pygame(join('..', 'data', 'maps', 'world.tmx')).get_layer_by_name('Entities'):
                if obj.name == 'Player':
                    self.player.rect = self.player.image.get_frect(center = (obj.x,obj.y))
                    self.player.hitbox_rect = self.player.rect.inflate(-60, -90)
            # set main_menu to true
            self.main_menu = True

    def display_main_menu(self):
        # Play button text
        self.play_text_surf     = self.game_font_40.render("Play", antialias=True, color="white")
        self.play_text_rect     = self.play_text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 60))
        self.play_text_bg_rect  = pygame.Surface((self.play_text_rect.right-self.play_text_rect.left, self.play_text_rect.bottom-self.play_text_rect.top)).get_frect(center=self.play_text_rect.center)
        # Quit button text
        self.quit_text_surf     = self.game_font_40.render("Quit", antialias=True, color="white")
        self.quit_text_rect     = self.quit_text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 20))
        self.quit_text_bg_rect  = pygame.Surface((self.quit_text_rect.right-self.quit_text_rect.left, self.quit_text_rect.bottom-self.quit_text_rect.top)).get_frect(center=self.quit_text_rect.center)
        # Music button text
        music_button_text       = "Music: ON" if self.music_toggle else "Music: OFF"
        self.music_text_surf    = self.game_font_40.render(music_button_text, antialias=True, color="white")
        self.music_text_rect    = self.music_text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 60))
        self.music_text_bg_rect = pygame.Surface((self.music_text_rect.right-self.music_text_rect.left, self.music_text_rect.bottom-self.music_text_rect.top)).get_frect(center=self.music_text_rect.center)
        # Sound button text
        # Bg
        self.display_surface.blit(self.bg_image, (0, 0))
        # Draw play button
        pygame.draw.rect(
            self.display_surface, 
            (0, 0, 0),
            self.play_text_rect.inflate(30, 20),
            border_radius=10
        )
        pygame.draw.line(self.display_surface, "white", self.play_text_rect.topleft     + pygame.Vector2(-15,-10), self.play_text_rect.topright   + pygame.Vector2( 15,-10), width=5)
        pygame.draw.line(self.display_surface, "white", self.play_text_rect.bottomright + pygame.Vector2( 15, 10), self.play_text_rect.topright   + pygame.Vector2( 15,-10), width=5)
        pygame.draw.line(self.display_surface, "white", self.play_text_rect.bottomright + pygame.Vector2( 15, 10), self.play_text_rect.bottomleft + pygame.Vector2(-15, 10), width=5)
        pygame.draw.line(self.display_surface, "white", self.play_text_rect.topleft     + pygame.Vector2(-15,-10), self.play_text_rect.bottomleft + pygame.Vector2(-15, 10), width=5)
        # Draw quit button
        pygame.draw.rect(
            self.display_surface, 
            (0, 0, 0),
            self.quit_text_rect.inflate(30, 20),
            border_radius=10
        )
        pygame.draw.line(self.display_surface, "white", self.quit_text_rect.topleft     + pygame.Vector2(-15,-10), self.quit_text_rect.topright   + pygame.Vector2( 15,-10), width=5)
        pygame.draw.line(self.display_surface, "white", self.quit_text_rect.bottomright + pygame.Vector2( 15, 10), self.quit_text_rect.topright   + pygame.Vector2( 15,-10), width=5)
        pygame.draw.line(self.display_surface, "white", self.quit_text_rect.bottomright + pygame.Vector2( 15, 10), self.quit_text_rect.bottomleft + pygame.Vector2(-15, 10), width=5)
        pygame.draw.line(self.display_surface, "white", self.quit_text_rect.topleft     + pygame.Vector2(-15,-10), self.quit_text_rect.bottomleft + pygame.Vector2(-15, 10), width=5)
        # Draw quit button
        pygame.draw.rect(
            self.display_surface, 
            (0, 0, 0),
            self.quit_text_rect.inflate(30, 20),
            border_radius=10
        )
        pygame.draw.line(self.display_surface, "white", self.music_text_rect.topleft     + pygame.Vector2(-15,-10), self.music_text_rect.topright   + pygame.Vector2( 15,-10), width=5)
        pygame.draw.line(self.display_surface, "white", self.music_text_rect.bottomright + pygame.Vector2( 15, 10), self.music_text_rect.topright   + pygame.Vector2( 15,-10), width=5)
        pygame.draw.line(self.display_surface, "white", self.music_text_rect.bottomright + pygame.Vector2( 15, 10), self.music_text_rect.bottomleft + pygame.Vector2(-15, 10), width=5)
        pygame.draw.line(self.display_surface, "white", self.music_text_rect.topleft     + pygame.Vector2(-15,-10), self.music_text_rect.bottomleft + pygame.Vector2(-15, 10), width=5)
        # Draw buttons texts
        self.display_surface.blit(self.play_text_surf , self.play_text_rect)
        self.display_surface.blit(self.quit_text_surf , self.quit_text_rect)
        # self.display_surface.blit(self.music_text_surf, self.music_text_rect)


    def run(self):

        while self.running:
            # dt 
            dt = self.clock.tick() / 1000

            # event loop 
            for event in pygame.event.get():
                if   event.type == pygame.QUIT: self.running = False
                elif self.main_menu and event.type == pygame.MOUSEBUTTONDOWN and self.quit_text_bg_rect.collidepoint(pygame.mouse.get_pos()): self.running = False
                elif self.main_menu and event.type == pygame.MOUSEBUTTONDOWN and self.play_text_bg_rect.collidepoint(pygame.mouse.get_pos()): self.main_menu = False
                elif event.type == self.enemy_event:
                    Enemy(
                        choice(self.spawn_positions),
                        choice(list(self.enemy_frames.values())),
                        (self.all_sprites, self.enemy_sprites),
                        self.player, self.collision_sprites
                    )

            if self.main_menu: self.display_main_menu()
            else:
                # update
                self.gun_timer()
                self.input()
                self.all_sprites.update(dt)
                self.bullet_collision()
                self.player_collision()
                # draw
                self.display_surface.fill('black')
                self.all_sprites.draw(self.player.rect.center)

            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()