import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)

        self.apple_eaten_sound = pygame.mixer.Sound("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\crunch_sound.wav")
        self.snake_collision = pygame.mixer.Sound("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\snake_collision.mp3")

        self.head_up = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\head_up.png").convert_alpha()
        self.head_down = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\head_down.png").convert_alpha()
        self.head_right = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\head_right.png").convert_alpha()
        self.head_left = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\head_left.png").convert_alpha()

        self.tail_up = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\tail_left.png").convert_alpha()

        self.body_vertical = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\body_horizontal.png").convert_alpha()

        self.body_bl = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\body_bottomleft.png").convert_alpha()
        self.body_br = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\body_bottomright.png").convert_alpha()
        self.body_tl = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\body_topleft.png").convert_alpha()
        self.body_tr = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\body_topright.png").convert_alpha()

    def update_head(self):
        head_dir = self.body[1] - self.body[0]
        if head_dir == Vector2(-1,0) : self.head_graphic = self.head_right
        elif head_dir == Vector2(1,0) : self.head_graphic = self.head_left
        elif head_dir == Vector2(0,1) : self.head_graphic = self.head_up
        elif head_dir == Vector2(0,-1) : self.head_graphic = self.head_down

    def update_tail(self):
        tail_dir = self.body[len(self.body)-1] - self.body[len(self.body)-2]
        if tail_dir == Vector2(1,0) : self.tail_graphic = self.tail_right
        elif tail_dir == Vector2(-1,0) : self.tail_graphic = self.tail_left
        elif tail_dir == Vector2(0,-1) : self.tail_graphic = self.tail_up
        elif tail_dir == Vector2(0,1) : self.tail_graphic = self.tail_down

    def draw_snake(self):
        for index,block in enumerate(self.body):
            self.update_head()
            self.update_tail()
            # Define Rect
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            # Draw head
            if index == 0 : screen.blit(self.head_graphic, block_rect)
            # Draw Tail
            elif index == len(self.body)-1 : screen.blit(self.tail_graphic, block_rect)
            # Draw Body
            else :
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                # Vertical
                if previous_block.x == next_block.x : screen.blit(self.body_vertical, block_rect)
                # Horizontal
                if previous_block.y == next_block.y : screen.blit(self.body_horizontal, block_rect)
                # Corners
                else:
                    if (
                        (previous_block.x == -1 and next_block.y == -1) or
                        (previous_block.y == -1 and next_block.x == -1)
                    ) : screen.blit(self.body_tl,block_rect)
                    elif (
                        (previous_block.x == -1 and next_block.y == 1) or
                        (previous_block.y == 1 and next_block.x == -1)
                    ) : screen.blit(self.body_bl,block_rect)
                    elif (
                        (previous_block.x == 1 and next_block.y == -1) or
                        (previous_block.y == -1 and next_block.x == 1)
                    ) : screen.blit(self.body_tr,block_rect)
                    elif (
                        (previous_block.x == 1 and next_block.y == 1) or
                        (previous_block.y == 1 and next_block.x == 1)
                    ) : screen.blit(self.body_br,block_rect)

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, self.body[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        body_copy = self.body[:]
        body_copy.insert(0, self.body[0] + self.direction)
        self.body = body_copy[:]

class FRUIT:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.apple = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\apple.png")
    
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.apple,fruit_rect)
        # pygame.draw.rect(screen, (183, 111, 122), fruit_rect)

    def randomize_pos(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_apple_eaten()
        self.check_collision()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.display_score()

    def check_apple_eaten(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize_pos()
            self.snake.add_block()
            self.snake.apple_eaten_sound.play()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize_pos()

    def check_collision(self):
        # Collision with border
        if (
            self.snake.body[0].x >= cell_number or
            self.snake.body[0].x < 0 or
            self.snake.body[0].y >= cell_number or
            self.snake.body[0].y < 0
        ):
            self.game_over()
            self.snake.snake_collision.play()
        # Collision with itself
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                self.snake.snake_collision.play()
                self.game_over()

    def game_over(self):
        global game_active
        game_active = False
        self.draw_grass()
        game_over_surf = game_font_100.render("GAME OVER!", True, (56, 74, 12))
        game_over_rect = game_over_surf.get_rect(center = (cell_number * cell_size // 2, (cell_number * cell_size // 2) - 3 * cell_size))
        press_space_surf = game_font_40.render("Press SPACE to Restart", True, (56, 74, 12))
        press_space_rect = press_space_surf.get_rect(center = (cell_number * cell_size // 2, (2 * cell_number * cell_size // 3) - 3 * cell_size))
        screen.blit(game_over_surf,game_over_rect)
        screen.blit(press_space_surf,press_space_rect)
        self.display_score()
        
    def draw_grass(self):
        grass_color_1 = (175, 215, 70)
        grass_color_2 = (167, 209, 61)
        screen.fill(grass_color_1)
        for row in range(cell_number):
            for col in range(cell_number):
                grass_rect = pygame.Rect(
                    col * cell_size,
                    row * cell_size,
                    cell_size,
                    cell_size
                )
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, grass_color_2, grass_rect)

    def display_score(self):
        score_text = f"{len(self.snake.body) - 3:02}"
        score_surf = game_font_36.render(score_text, True, (56, 74, 12))
        score_rect = score_surf.get_rect(topleft=(8, 0))
        screen.blit(score_surf, score_rect)

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

cell_size = 38
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
pygame.display.set_caption("Snake Game")
game_icon = pygame.image.load("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\icon.png").convert_alpha()
pygame.display.set_icon(game_icon)
game_font_36 = pygame.font.Font("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\PoetsenOne-Regular.ttf", 36)
game_font_40 = pygame.font.Font("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\PoetsenOne-Regular.ttf", 40)
game_font_100 = pygame.font.Font("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\PoetsenOne-Regular.ttf", 100)
game_active = True
main_game = MAIN()
bg_music = pygame.mixer.Sound("C:\\Users\\DELL\\Desktop\\Sudev D\\Study Material\\Python\\PyGame\\Snake Game\\Data\\bg_music.mp3")
bg_music.play(loops = -1)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# Main game loop
while True:
    # Event Loop
    for event in pygame.event.get():

        # Quit Game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Update Screen
        if event.type == SCREEN_UPDATE and game_active : main_game.update()

        # Snake Movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction != Vector2(0, 1):
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction != Vector2(0, -1):
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction != Vector2(1, 0):
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and main_game.snake.direction != Vector2(-1, 0):
                main_game.snake.direction = Vector2(1, 0)
        
        # Restart Game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_active:
            game_active = True
            main_game = MAIN()

    # Game Active
    if game_active : main_game.draw_elements()

    # Game Over
    else : main_game.game_over()

    pygame.display.update()
    clock.tick(60)
