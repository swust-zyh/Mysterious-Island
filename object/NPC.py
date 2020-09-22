import os

import pygame


class NPC(pygame.sprite.Sprite):  # 括号中加类名实现继承
    def __init__(self, pos_x: int, pos_y: int, width, height, image_count, path, prefix):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image_count = image_count
        self.width = width
        self.height = height
        self.prefix = prefix
        if self.pos_y > 350 and prefix == 'berry':
            self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)  # 人物区域
        else:
            self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

        self.object_images = []
        for i in range(0, self.image_count):
            img_path = os.path.join('resource', 'image', path, prefix + str(i) + '.png')
            image = pygame.image.load(img_path)
            if prefix == 'berry':
                image = pygame.transform.scale(image, (30, 32))
            if prefix == '齿轮':
                image = pygame.transform.scale(image, (50, 52))
            self.object_images.append(image)  # load返回对象类型为surface类型

    def draw(self, surface):  # 窗口变量
        if self.prefix == 'berry':
            surface.blit(self.object_images[self.index], (self.pos_x - 15, self.pos_y - 15))
        else:
            surface.blit(self.object_images[self.index], (self.pos_x - 15, self.pos_y - 25))  # 从tmx的定点为左上角开始绘制所以位置会有少许偏差
        self.index = (self.index + 1) % self.image_count
        # self.pos_x += 2