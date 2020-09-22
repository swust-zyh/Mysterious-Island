import pygame

from dialog.god_dialog import GodDialog
from object.DirAction import DirAction


class InteractiveMoveNPC(pygame.sprite.Sprite):

    def __init__(self, x, y, path, prefix, have_dialog: bool, max_step_count, direct):  # 0为上下，1为左右
        """
        初始化函数
        :param x: 全局x坐标
        :param y: 全局y坐标
        """
        pygame.sprite.Sprite.__init__(self)  # 调用基类构造函数
        self.walk = DirAction(path, prefix, 4, 2, True)
        self.width = 10
        self.height = 10
        self.speed = 2  # x、y方向同一速度
        self.dir = direct  # 方向
        self.step_count = 0  # 记步
        self.max_step_count = max_step_count
        self.have_dialog = have_dialog
        self.pos_x = x
        self.pos_y = y
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.stop = False
        self.dialog = GodDialog(2)  # 对话框  解耦

    def draw(self, surface):
        """
        绘制函数
        :param surface: 背景
        :param x: 窗口x坐标
        :param y: 窗口y坐标
        :return:
        """
        image = self.walk.get_current_image(self.dir)
        if self.stop and self.have_dialog:
            surface.blit(self.dialog.surface, (0, 0))
        surface.blit(image, (self.pos_x, self.pos_y))
        self.__move__()

    def __move__(self):
        if self.stop:
            return
        self.step_count += 1
        if self.dir == 0:
            self.pos_x += self.speed
        elif self.dir == 1:
            self.pos_x -= self.speed
        elif self.dir == 2:
            self.pos_y -= self.speed
        elif self.dir == 3:
            self.pos_y += self.speed

        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

        if self.step_count == self.max_step_count:
            self.step_count = 0
            if self.dir == 0:
                self.dir = 1
            elif self.dir == 1:
                self.dir = 0
            elif self.dir == 2:
                self.dir = 3
            elif self.dir == 3:
                self.dir = 2

    def collide(self, actor):
        if pygame.sprite.collide_rect(self, actor):
            self.stop = True
        else:
            self.stop = False
