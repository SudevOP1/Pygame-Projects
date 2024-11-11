from settings import *
from sprites  import *

class Game:

    def __init__(self):

        # General Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Slide Puzzle")
        self.clock = pygame.time.Clock()
        self.game_font_30 = pygame.font.Font(None, 40)

        # Variables
        self.running = True
        self.started = False
        self.win     = False
        self.start_time      = 0
        self.elapsed_time    = 0
        self.last_reset_time = 0
        self.best_time = self.load_best_time()
        
        # Sprites
        self.setup_blocks()

    def draw_blocks(self):
        for block in self.blocks:
            self.display_surface.blit(block.surf, block.rect)
            self.display_surface.blit(block.text_surf, block.text_rect)

    def setup_blocks(self):
        self.blocks = []
        nums = [i for i in range(1, 16)]
        for row in range(1, 5):
            for col in range(1, 5):
                if not (row == 4 and col == 4):
                    num = choice(nums)
                    index = (row-1)*4 + (col-1)
                    self.blocks.append(Block(num, row, col, index))
                    nums.remove(num)
        self.invis_block = Block(num='16', row=4, col=4, ind=15)
        self.blocks.append(self.invis_block)

    def move_block(self, direction):
        if not self.win:    
        
            # Move up
            if direction == "up" and self.invis_block.row < 4:
                moving_block = next(block for block in self.blocks if (block.row == self.invis_block.row + 1 and block.col == self.invis_block.col))
                moving_block.row -= 1
                self.invis_block.row += 1
                moving_block.update_position()
                self.invis_block.update_position()
            
            # Move down
            elif direction == "down" and self.invis_block.row > 1:
                moving_block = next(block for block in self.blocks if (block.row == self.invis_block.row - 1 and block.col == self.invis_block.col))
                moving_block.row += 1
                self.invis_block.row -= 1
                moving_block.update_position()
                self.invis_block.update_position()
            
            # Move right
            elif direction == "right" and self.invis_block.col > 1:
                moving_block = next(block for block in self.blocks if (block.col == self.invis_block.col - 1 and block.row == self.invis_block.row))
                moving_block.col += 1
                self.invis_block.col -= 1
                moving_block.update_position()
                self.invis_block.update_position()
            
            # Move left
            elif direction == "left" and self.invis_block.col < 4:
                moving_block = next(block for block in self.blocks if (block.col == self.invis_block.col + 1 and block.row == self.invis_block.row))
                moving_block.col -= 1
                self.invis_block.col += 1
                moving_block.update_position()
                self.invis_block.update_position()

    def move_block_using_mouse(self, pos):
        # Check if click is on a block
        clicked_block = next((block for block in self.blocks if block.rect.collidepoint(pos)), None)
        # Move the block
        if clicked_block:
            if((clicked_block.row == self.invis_block.row and abs(clicked_block.col - self.invis_block.col) == 1) or
               (clicked_block.col == self.invis_block.col and abs(clicked_block.row - self.invis_block.row) == 1)):
                if   clicked_block.row == self.invis_block.row and clicked_block.col == self.invis_block.col - 1: self.move_block("right")
                elif clicked_block.row == self.invis_block.row and clicked_block.col == self.invis_block.col + 1: self.move_block("left")
                elif clicked_block.col == self.invis_block.col and clicked_block.row == self.invis_block.row - 1: self.move_block("down")
                elif clicked_block.col == self.invis_block.col and clicked_block.row == self.invis_block.row + 1: self.move_block("up")

    def display_time_and_buttons(self):

        # Calculate time
        if not self.win:
            current_time = pygame.time.get_ticks()
            total_seconds = int((current_time-self.last_reset_time)/1000)
            minutes = int(total_seconds / 60)
            seconds = total_seconds % 60
            self.time = f"{minutes:02}:{seconds:02}"
        else:
            self.time = f"{int(self.elapsed_time/60):02}:{int(self.elapsed_time%60):02}"

        # Time Surfs & Rects
        time_text_surf = self.game_font_30.render(f"Time: {self.time}", True, COLORS["text"])
        time_bg_surf   = pygame.Surface(pygame.Vector2(200,self.game_font_30.get_height()+20))
        time_bg_rect   = time_bg_surf.get_frect(bottomright = pygame.Vector2(WINDOW_WIDTH-20,WINDOW_HEIGHT-20))
        time_text_rect = time_text_surf.get_frect(center = time_bg_rect.center)
        time_bg_surf.fill(COLORS["text bg"])

        # New Game Button Surfs & Rects
        new_game_text_surf    = self.game_font_30.render("New Game", True, COLORS["text"])
        new_game_bg_surf      = time_bg_surf.copy()
        self.new_game_bg_rect = new_game_bg_surf.get_frect(bottomright = time_bg_rect.topright-pygame.Vector2(0,20))
        new_game_text_rect    = new_game_text_surf.get_frect(center = self.new_game_bg_rect.center)
        new_game_bg_surf.fill(COLORS["text bg"])

        # Solve Button Surfs & Rects
        solve_text_surf = self.game_font_30.render("Solve", True, COLORS["text"])
        solve_bg_surf   = new_game_bg_surf.copy()
        self.solve_bg_rect   = solve_bg_surf.get_frect(bottomright = self.new_game_bg_rect.topright-pygame.Vector2(0,20))
        solve_text_rect = solve_text_surf.get_frect(center = self.solve_bg_rect.center)
        solve_bg_surf.fill(COLORS["text bg"])

        # Display time and buttons
        self.display_surface.blit(time_bg_surf, time_bg_rect)
        self.display_surface.blit(time_text_surf, time_text_rect)
        self.display_surface.blit(new_game_bg_surf, self.new_game_bg_rect)
        self.display_surface.blit(new_game_text_surf, new_game_text_rect)
        self.display_surface.blit(solve_bg_surf, self.solve_bg_rect)
        self.display_surface.blit(solve_text_surf, solve_text_rect)

    def new_game(self):
        self.win = False

        # Reset Blocks
        self.setup_blocks()

        # Reset Time
        self.last_reset_time = pygame.time.get_ticks()

    def check_win(self):
        for block in self.blocks:
            num = int(block.num)
            if num != 16:
                if (
                    block.row != int((num-1)/4 + 1) or
                    block.col != int((num-1)%4 + 1)
                ):
                    return False
        if self.time < self.best_time:
            self.save_best_time()
        return True

    def solve(self):
        for block in self.blocks:
            num = int(block.num)
            block.row = int((num-1)/4) + 1
            block.col =     (num-1)%4  + 1
            block.update_position()

        self.invis_block.row = 4
        self.invis_block.col = 4
        self.invis_block.update_position()

    def display_best_time(self):

        # Best time Surfs & Rects
        best_time_text_surf = self.game_font_30.render(f"Best Time: {self.best_time}", True, COLORS["text"])
        best_time_text_rect = best_time_text_surf.get_frect()
        best_time_bg_surf   = pygame.Surface(pygame.Vector2(best_time_text_rect.right-best_time_text_rect.left+20,best_time_text_rect.bottom-best_time_text_rect.top+20))
        best_time_bg_rect   = best_time_bg_surf.get_frect(topright = pygame.Vector2(WINDOW_WIDTH-20,20))
        best_time_text_rect.center = best_time_bg_rect.center
        best_time_bg_surf.fill(COLORS["text bg"])

        # Display best time
        self.display_surface.blit(best_time_bg_surf, best_time_bg_rect)
        self.display_surface.blit(best_time_text_surf, best_time_text_rect)

    def load_best_time(self):
        try:
            with open("data.txt") as data_file: return json.load(data_file)
        except:
            return "--:--"

    def save_best_time(self):
        with open("data.txt", "w") as data_file: json.dump(self.best_time, data_file)

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            # Event Loop
            for event in pygame.event.get():

                # Quit
                if event.type == pygame.QUIT:
                    self.running = False

                # Move block using keyboard
                if event.type == pygame.KEYDOWN:
                    if not self.win and event.key == pygame.K_UP   : self.move_block("up")
                    if not self.win and event.key == pygame.K_DOWN : self.move_block("down")
                    if not self.win and event.key == pygame.K_LEFT : self.move_block("left")
                    if not self.win and event.key == pygame.K_RIGHT: self.move_block("right")

                # Move block using mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.move_block_using_mouse(mouse_pos)

                # New Game and Solve Buttons
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.new_game_bg_rect.collidepoint(mouse_pos): self.new_game()
                    if self.solve_bg_rect.collidepoint(mouse_pos): self.solve()

            # Draw
            self.display_surface.fill(COLORS["bg"])
            self.draw_blocks()
            self.display_time_and_buttons()
            self.display_best_time()
            self.win = self.check_win()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()