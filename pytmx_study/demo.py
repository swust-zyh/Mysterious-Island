"""
守卫：700x75
"""
import sys
import pygame
from pytmx_study.utils.pytmx_module import TiledRenderer  # 需要从根目录开始 并且包名不能带空格 不然无法识别

pygame.init()

#  申请窗口
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption('Tiled_tmx_render')

render = TiledRenderer(r'resource/map1.tmx')  # 获取图像信息 但是我们加载图片的时候文件相对位置发生了改变的话，就需要修改xml，不然会报错
#  申请放图片的对象
surface = pygame.Surface(render.pixel_size)
render.render_map(surface)  # 画图在图像对象上

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.blit(surface, (0, 0))  # 第二个参数为图片的起始位置

    pygame.display.update()