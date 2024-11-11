import pygame, random
from sys import exit
from os.path import join

def display_score():
    current_time = pygame.time.get_ticks() - start_time
    score_surf = test_font.render(f"Score: {str(int(current_time/1000))}", False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return int(current_time/1000)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300: screen.blit(snail_surface,obstacle_rect)
            else: screen.blit(fly_surface,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def display_player_animation():
    global player_surface, player_index
    # Walk animation if player is on floor
    if player_rect.bottom == 300:
        player_index += 0.1
        if player_index >= len(player_walk): player_index=0
        player_surface = player_walk[int(player_index)]
    # Jump animation if player is air bourne
    else:
        player_surface = player_jump

pygame.init()

# Initial Setup / Constants
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font(join("font", "Pixeltype.ttf"), 50)
start_time = 0
game_active = False
score = 0

# Background
sky_surface = pygame.image.load(join("graphics", "Sky.png")).convert_alpha()
ground_surface = pygame.image.load(join("graphics", "Ground.png")).convert_alpha()

# Obstacles
snail_frame_1 = pygame.image.load(join("graphics", "snail", "snail1.png")).convert_alpha()
snail_frame_2 = pygame.image.load(join("graphics", "snail", "snail2.png")).convert_alpha()
snail_frames = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load(join("graphics", "Fly", "Fly1.png")).convert_alpha()
fly_frame_2 = pygame.image.load(join("graphics", "Fly", "Fly2.png")).convert_alpha()
fly_frames = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

# Player
player_walk_1 = pygame.image.load(join("graphics", "player", "player_walk_1.png")).convert_alpha()
player_walk_2 = pygame.image.load(join("graphics", "player", "player_walk_2.png")).convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load(join("graphics", "player", "player_jump.png")).convert_alpha()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom=(80,300))
player_gravity = 0

# Intro Screen
player_stand_surface = pygame.image.load(join("graphics", "player", "player_stand.png")).convert_alpha()
player_stand_surface = pygame.transform.rotozoom(player_stand_surface,0,2)
player_stand_rect = player_stand_surface.get_rect(center=(400,200))

game_name = test_font.render("Pixel Runner", False, (111,196,169))
game_name_rect = game_name.get_rect(center=(400,80))

game_message = test_font.render("Press SPACE to run", False, (111,196,169))
game_message_rect = game_message.get_rect(center=(400,330))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 400)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 100)

# Sound
bg_music = pygame.mixer.Sound(join("audio", "music.wav"))
bg_music.set_volume(0.1)
jump_sound = pygame.mixer.Sound(join("audio", "jump.mp3"))
jump_sound.set_volume(0.3)
bg_music.play(loops = -1)

# Running
while True:
    for event in pygame.event.get():

        # Quit Game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Game Active
        if game_active:

            # Player Jump
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player_rect.bottom==300:
                player_gravity =-20
                jump_sound.play()

            # Obstacle Timer
            if event.type == obstacle_timer:
                if random.randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(random.randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(random.randint(900,1100),210)))
        
            # Snail Animation
            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
            
            # Fly Animation
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index]

        # Game Inactive
        else:
            # Game Over Screen Input
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    # Game Start
    if game_active:

        # Background and Score
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.bottom += player_gravity
        if player_rect.bottom>=300: player_rect.bottom=300
        display_player_animation()
        screen.blit(player_surface, player_rect)

        # Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect,obstacle_rect_list)
        
    # Game Over
    else:
        screen.fill((94,129,162))
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        screen.blit(player_stand_surface,player_stand_rect)
        score_message = test_font.render(f"Your score: {score}",False,(111,196,169))
        score_message_rect = score_message.get_rect(center=(400,330))
        screen.blit(game_name, game_name_rect)

        if score == 0: screen.blit(game_message,game_message_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)