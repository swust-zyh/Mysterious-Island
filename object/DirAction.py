# 0下 1左 2上 3右
import os

import pygame


class DirAction:
    def __init__(self, path, prefix, dir_count, image_count, is_loop):
        self.image_index = 0
        self.action_images = []
        self.image_count = image_count
        self.dir = dir_count
        self.is_loop = is_loop

        for i in range(0, dir_count):
            dir_image = []
            for j in range(0, image_count):
                img_path = os.path.join('resource', 'image', path, prefix + str(i) + str(j) + '.png')
                dir_image.append(pygame.image.load(img_path))
            self.action_images.append(dir_image)

    def get_current_image(self, direct):
        # if self.image_index >= self.image_count:
        #     print(self.image_index, self.image_count)
        current_image = self.action_images[direct][self.image_index]
        self.image_index += 1
        if self.image_index >= self.image_count:
            if self.is_loop:
                self.image_index = 0
            else:
                self.image_index -= 1

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