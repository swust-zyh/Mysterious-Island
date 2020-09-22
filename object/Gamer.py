import pygame

from object.DirAction import DirAction


class Gamer:
    def __init__(self, pos_x, pos_y, rect_width, rect_height, is_loop, dir_count, image_count):
        self.walk = DirAction('gamer', 'gamer', dir_count, image_count, is_loop)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.hp = 100
        self.dir = 0
        self.key = False
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.rect_width, self.rect_height)  # 游戏中角色脚下的圆圈

    def reset_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.rect_width, self.rect_height)  # 游戏中角色脚下的圆圈

    def draw(self, surface):
        image = self.walk.get_current_image(self.dir)
        surface.blit(image, (self.pos_x, self.pos_y))

    def key_move(self, pressed_key, obstacle_group):
        pos_x = self.pos_x  # 判断障碍物相撞
        pos_y = self.pos_y
        if pressed_key == pygame.K_UP:
            self.dir = 2
            pos_y -= 10
        elif pressed_key == pygame.K_DOWN:
            self.dir = 0
            pos_y += 10
        elif pressed_key == pygame.K_LEFT:
            self.dir = 1
            pos_x -= 10
        elif pressed_key == pygame.K_RIGHT:
            self.dir = 3
            pos_x += 10
        else:
            return

        self.rect = pygame.Rect(pos_x, pos_y, self.rect_width, self.rect_height)
        collide_list = pygame.sprite.spritecollide(self, obstacle_group, False)  # 返回值为列表

        if len(collide_list) > 0:
            self.rect = pygame.Rect(self.pos_x, self.pos_y, self.rect_width, self.rect_height)
            return
        else:
            return self.__move__()

    # 0 下 1 左  2 上 3 右
    def __move__(self):
        x = 0
        y = 0
        if self.dir == 2:
            y = -10
        elif self.dir == 0:
            y = 10
        elif self.dir == 1:
            x = -10
        else:
            x = 10

        self.pos_y += y
        self.pos_x += x
        return [x, y]