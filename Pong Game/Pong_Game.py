from settings import *
from sprites  import *
from groups   import *
import json

class Game(pygame.sprite.Sprite):

    def __init__(self):

        # General Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.running = True

        # Sprites
        self.all_sprites    = AllSprites()
        self.paddle_sprites = pygame.sprite.Group()
        self.player         = Player((self.all_sprites, self.paddle_sprites))
        self.ball           = Ball((self.all_sprites), self.paddle_sprites, self.update_score)
        Opponent((self.all_sprites, self.paddle_sprites), self.ball)

        # Score
        try:
            with open(join("score.txt")) as score_file:
                self.score = json.load(score_file)
        except: self.score = {"player" : 0, "opponent" : 0}
        self.game_font_160 = pygame.font.Font(None, 160)

    def display_scores(self):

        # Player Score
        player_score_surf = self.game_font_160.render(str(self.score["player"]), True, COLORS["bg detail"])
        player_score_rect = player_score_surf.get_rect(center = (WINDOW_WIDTH/2 + 100, WINDOW_HEIGHT/2))
        self.display_surface.blit(player_score_surf, player_score_rect)

        # Opponent Score
        opponent_score_surf = self.game_font_160.render(str(self.score["opponent"]), True, COLORS["bg detail"])
        opponent_score_rect = opponent_score_surf.get_rect(center = (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2))
        self.display_surface.blit(opponent_score_surf, opponent_score_rect)

        # Line
        pygame.draw.line(self.display_surface, COLORS["bg detail"], (WINDOW_WIDTH/2, 0), (WINDOW_WIDTH/2, WINDOW_HEIGHT), width=8)

    def update_score(self, side):
        self.score[side] += 1

    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    with open(join("score.txt"), "w") as score_file:
                        json.dump(self.score, score_file)

            # Update
            self.all_sprites.update(dt)

            # Draw
            self.display_surface.fill(COLORS["bg"])
            self.display_scores()
            self.all_sprites.draw()
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()