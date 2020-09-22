import pygame

from object.DirAction import DirAction


class SceneGamer:
    def __init__(self, pos_x, pos_y, rect_width, rect_height, is_loop, dir_count, image_count):
        self.walk = DirAction('gamer', 'gamer', dir_count, image_count, is_loop)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.dir = 3
        self.jump = False
        self.jump_count = 0
        self.a = 1
        self.key = False
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.rect_width, self.rect_height)  # 游戏中角色脚下的圆圈

    def reset_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.rect_width, self.rect_height)  # 游戏中角色脚下的圆圈

    def key_move(self, pressed_key):
        if pressed_key == pygame.K_UP:
            self.jump = True

    def collide(self, obstacle_group):
        pos_x = self.pos_x  # 判断障碍物相撞
        pos_y = self.pos_y

        self.rect = pygame.Rect(pos_x, pos_y, self.rect_width, self.rect_height)
        collide_list = pygame.sprite.spritecollide(self, obstacle_group, False)  # 返回值为列表

        if len(collide_list) > 0:
            self.rect = pygame.Rect(self.pos_x, self.pos_y, self.rect_width, self.rect_height)
            return
        else:
            self.pos_x = pos_x
            self.pos_y = pos_y

    def draw(self, surface):
        image = self.walk.get_current_image(self.dir)
        surface.blit(image, (self.pos_x, self.pos_y))