import os

import pygame


class Action:
    # 将一个人物的所有的单帧图像放入一个对象中
    def __init__(self, path, prefix, image_count, is_loop):
        self.image_index = 0
        self.action_image = []
        self.image_count = image_count
        self.is_loop = is_loop
        for i in range(0, image_count):
            image_path = os.path.join('resource', 'img', path, prefix + str(i) + '.tga')
            self.action_image.append(pygame.image.load(image_path))

    def get_current_image(self) -> pygame.Surface:
        current_image = self.action_image[self.image_index]
        self.image_index += 1
        if self.image_index >= self.image_count:
            if self.is_loop:
                self.image_index = 0
            else:
                self.image_index = self.image_index - 1

        return current_image

    def is_end(self):
        if self.is_loop:
            return False
        else:
            if self.image_index == self.image_count - 1:
                return True
            else:
                return False

    def reset(self):
        self.image_index = 0