"""
随着人物的移动进行场景移动
"""
import os
import sys

import pygame

from scenes.scene1 import Scene1

from scenes.begin_scene import begin_scene
from scenes.scene2 import Scene2
from scenes.scene3 import Scene3

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((800, 600), pygame.SRCALPHA)
    screen_light = pygame.surface.Surface((800, 600))
    screen_light.set_alpha(0)
    icon = pygame.image.load(r'./resource/image/icon.ico')  # 图片要先加载才能设置
    pygame.display.set_icon(icon)  # 设置favicon
    pygame.display.set_caption('Mysterious Island')
    surface = pygame.image.load(r'resource/image/start.png')
    surface = pygame.transform.scale(surface, (800, 600))
    help_surface = pygame.image.load(r'resource/image/help.png')
    end_surface = pygame.image.load(r'resource/image/end.png')
    setting_surface = pygame.image.load(r'resource/image/setting.png')
    alpha = 0
    sound_pos = 0
    sound_voice = 1

    # 详解：https://blog.csdn.net/qq_41556318/article/details/86305046
    sound_path = os.path.join('resource', 'music', '123.mp3')
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)  # -1即循环播放

    i = 0
    while i <= 5:
        # print(i)
        if i == 0:
            scene_exit = False
            is_surface = True
            is_help = False
            is_setting = False
            while not scene_exit:
                mouse_down = False
                pressed_key = 0
                for event in pygame.event.get():  # 获取鼠标点击事件 键盘操作事件没法 返回列表
                    if event.type == pygame.QUIT:  # pygame.QUIT其实就是鼠标点击叉号这个指令
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:  # 鼠标点击事件获取 看右键是否可以？
                        mouse_down = True
                    if event.type == pygame.KEYDOWN:
                        pressed_key = event.key
                        if pressed_key == pygame.K_ESCAPE:
                            is_surface = True
                            is_help = False
                            is_setting = False

                if is_setting and mouse_down:
                    x, y = pygame.mouse.get_pos()
                    if 400 <= x <= 465 and 270 <= y <= 310:
                        if 0 < alpha <= 150:
                            alpha -= 10
                            screen_light.set_alpha(alpha)
                    elif 510 <= x <= 575 and 270 <= y <= 310:
                        # print("+++++")
                        if 0 <= alpha < 150:
                            alpha += 10
                            screen_light.set_alpha(alpha)
                    elif 400 <= x <= 465 and 150 <= y <= 180:
                        if sound_voice <= 0.9:
                            sound_voice += 0.1
                            pygame.mixer.music.set_volume(sound_voice)  # pygame.mixer.music.get_volume这个函数会为浮点数（小数点应该有后16位），py加减会产生精度误差，所以不能直接写
                    elif 510 <= x <= 575 and 150 <= y <= 180:
                        # print(pygame.mixer.music.get_volume())
                        if sound_voice >= 0.1:
                            sound_voice -= 0.1
                            pygame.mixer.music.set_volume(sound_voice)
                    elif 390 <= x <= 485 and 405 <= y <= 450:
                        # print(pygame.mixer.music.get_volume())
                        pygame.mixer.music.stop()
                        sound_path = r'resource/music/张国荣 - 愿你决定.mp3'
                        pygame.mixer.music.load(sound_path)
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume())
                        pygame.mixer.music.play(-1)
                    elif 495 <= x <= 600 and 405 <= y <= 450:
                        pygame.mixer.music.stop()
                        sound_path = r'resource/music/123.mp3'
                        pygame.mixer.music.load(sound_path)
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume())
                        pygame.mixer.music.play(-1)

                elif mouse_down:
                    x, y = pygame.mouse.get_pos()  # 获取当前鼠标相对于窗口的笛卡尔坐标
                    # start
                    if 195 <= x <= 600 and 210 <= y <= 260:
                        # print("+++")
                        scene_exit = True
                    # quit
                    if 195 <= x <= 600 and 310 <= y <= 360:
                        sys.exit()
                    # help
                    if 30 <= x <= 140 and 540 <= y <= 570:
                        # print("+++")
                        is_help = True
                        is_surface = False
                        is_setting = False
                    # setting
                    if 195 <= x <= 600 and 420 <= y <= 480:
                        is_setting = True
                        is_surface = False
                        is_help = False

                if is_surface:
                    screen.blit(surface, (0, 0))  # 第一个参数为图片，第二个参数为相对窗口的笛卡尔坐标系的相对坐标
                elif is_help:
                    screen.blit(help_surface, (0, 0))
                else:
                    screen.blit(setting_surface, (0, 0))

                screen.blit(screen_light, (0, 0))
                pygame.display.update()
            i += 1

        elif i == 1:
            sound_pos = pygame.mixer.music.get_pos()
            begin = begin_scene(screen, screen_light, alpha, sound_path, sound_voice, sound_pos)
            res = begin.run()
            alpha = res[1]
            sound_path = res[2]
            sound_voice = res[3]
            sound_pos = res[4]
            i += 1

        # print(alpha)

        elif i == 2:
            scene1 = Scene1(screen, screen_light, alpha, sound_path, sound_voice, sound_pos)
            res = scene1.run()
            alpha = res[1]
            sound_path = res[2]
            sound_voice = res[3]
            sound_pos = res[4]
            if res[0] == -2:
                # print("+++++++")
                i = 0
            else:
                i += 1

        elif i == 3:
            scene2 = Scene2(screen, screen_light, alpha, sound_path, sound_voice, sound_pos)
            res = scene2.run()
            alpha = res[1]
            sound_path = res[2]
            sound_voice = res[3]
            sound_pos = res[4]
            if res[0] == -2:
                # print("+++++++")
                i = 0
            else:
                i += 1

        elif i == 4:
            scene3 = Scene3(screen, screen_light, alpha, sound_path, sound_voice, sound_pos)
            res = scene3.run()
            alpha = res[1]
            sound_path = res[2]
            sound_voice = res[3]
            sound_pos = res[4]
            if res[0] == -2:
                # print("+++++++")
                i = 0
            else:
                i += 1

        elif i == 5:
            pygame.mixer.music.stop()
            while True:
                for event in pygame.event.get():  # 获取鼠标点击事件 键盘操作事件没法 返回列表
                    if event.type == pygame.QUIT:  # pygame.QUIT其实就是鼠标点击叉号这个指令
                        sys.exit()

                screen.blit(end_surface, (0, 0))  # 第一个参数为图片，第二个参数为相对窗口的笛卡尔坐标系的相对坐标
                screen.blit(screen_light, (0, 0))
                pygame.display.update()
                i += 1