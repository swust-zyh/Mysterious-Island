import pygame

class InvisibleObstacle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.status = False
        self.flag = False
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 30, 30)

    def draw(self, surface):
        surface.blit(pygame.image.load(r'resource\image\obstacle\invisible.png'), (self.pos_x, self.pos_y))