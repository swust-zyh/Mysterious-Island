import pygame


class Treasure(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, have_key: bool):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.key = have_key
        self.status = True
        self.rect = pygame.Rect(self.pos_x - 30, self.pos_y - 30, 50, 50)

    def draw(self, surface):
        if self.status:
            surface.blit(pygame.image.load(r'resource\image\treasure\close.png'), (self.pos_x, self.pos_y))
        else:
            surface.blit(pygame.image.load(r'resource\image\treasure\open.png'), (self.pos_x, self.pos_y))

    def draw_key(self, surface):
        surface.blit(pygame.image.load(r'resource\image\treasure\key.png'), (self.pos_x, self.pos_y))
