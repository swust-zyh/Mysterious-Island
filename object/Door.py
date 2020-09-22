import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, is_jump):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.jump = is_jump
        self.flag1 = False
        self.flag2 = False
        self.flag3 = False
        self.flag4 = False
        self.status1 = False
        self.status2 = False
        self.rect = pygame.Rect(self.pos_x - 30, self.pos_y - 30, 80, 80)