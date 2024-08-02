from settings import *

class Block(pygame.sprite.Sprite):

    def __init__(self, num, row, col, ind):
        super().__init__()
        game_font_60 = pygame.font.Font(None, 60)

        # Initialise attributes
        self.num = num
        self.row = row
        self.col = col
        self.ind = ind

        # Surfs & Rects
        self.surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.surf.get_rect(topleft=(BLOCK_POS[(self.row, self.col)]))
        if self.num != "16":
            self.surf.fill(COLORS["block"])
            self.text_surf = game_font_60.render(str(self.num), True, COLORS["block text"])
        else:
            self.surf.fill(COLORS["bg"])
            self.text_surf = game_font_60.render(str(self.num), True, COLORS["bg"])
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def update_position(self):
        self.rect.topleft = BLOCK_POS[(self.row, self.col)]
        self.text_rect.center = self.rect.center