"""
实现代码复用
"""
import enum

import pygame
from pytmx_study.utils.pytmx_module import TiledRenderer


class RenderTmx:
    def __init__(self, path):
        self.tmx_path = path
        self.tiled = TiledRenderer(self.tmx_path)  # 得到图片信息
        self.surface = pygame.Surface(self.tiled.pixel_size)  # 申请渲染图片的对象
        self.tiled.render_map(self.surface)  # 画图 surface类


# 详解：https://www.cnblogs.com/-beyond/p/9777329.html
class SceneStatus(enum.IntEnum):  # 枚举类不能用来初始化实例，其实就相当于一个数组（key值不能相同）
    """
    场景的状态
    """
    In = 1  # 渐入
    Normal = 2  # 正常
    Out = 3  # 渐出


class FadeScene:
    def __init__(self, back_image: pygame.image):
        """
        渐变场景构造函数，back_image是整个背景
        """
        self.back_image = back_image
        self.alpha = 0
        self.status = SceneStatus.In

    def set_status(self, status: SceneStatus):
        """
        设置渐变场景的状态值
        :param status: 状态值
        """
        self.status = status
        if status == SceneStatus.In:
            self.alpha = 0
        if status == SceneStatus.Normal:
            self.alpha = 255
        if status == SceneStatus.Out:
            self.alpha = 0

    def get_out(self):
        if self.status == SceneStatus.Out and self.alpha == 255:
            return True
        else:
            return False

    def get_back_image(self):
        temp_surface = self.back_image
        if self.status == SceneStatus.Normal:
            return temp_surface
        elif self.status == SceneStatus.In:
            temp_surface.set_alpha(self.alpha)
            black_surface = pygame.Surface((800, 600))  # black_surface.fill((0, 0, 0))
            black_surface.blit(temp_surface, (0, 0))  # 参数二为位置信息
            self.alpha += 50
            if self.alpha >= 255:
                self.alpha = 0
                self.status = SceneStatus.Normal
            return black_surface
        elif self.status == SceneStatus.Out:
            temp_surface.set_alpha(255 - self.alpha)
            black_surface = pygame.Surface((800, 600))  # black_surface.fill((0, 0, 0))
            black_surface.blit(temp_surface, (0, 0))  # 参数二为位置信息
            self.alpha += 20
            if self.alpha >= 255:
                self.alpha = 255
            return black_surface
