import os
import sys

import pygame

from scenes import RenderTmx, FadeScene


class begin_scene:
    def __init__(self, screen, screen_light, alpha, sound_path, sound_voice, sound_pos):
        pygame.init()
        pygame.mixer.init()

        self.screen = screen
        self.screen_light = screen_light
        self.render = RenderTmx(r'resource\begin.tmx')
        self.temp_surface = self.render.surface.copy()
        self.fade = FadeScene(self.render.surface)
        self.is_setting = False
        self.alpha = alpha
        self.sound_path = sound_path
        self.sound_voice = sound_voice
        self.sound_pos = sound_pos
        self.res = [-1, -1, -1, -1, -1]

        # 详解：https://blog.csdn.net/qq_41556318/article/details/86305046
        pygame.mixer.music.set_pos(self.sound_pos)
        pygame.mixer.music.load(self.sound_path)
        pygame.mixer.music.set_volume(self.sound_voice)
        pygame.mixer.music.play(-1)  # -1即循环播放

        surface = pygame.surface.Surface((800, 600))
        self.screen.blit(surface, (0, 0))

    def get_surface(self):
        surface = self.fade.get_back_image()
        self.temp_surface.blit(surface, (0, 0))
        return self.temp_surface

    def run(self):
        scene_exit = False
        clock = pygame.time.Clock()  # 计时器
        while not scene_exit:
            mouse_down = False
            is_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:  # 按下键盘上的键这个事件
                    is_pressed = True
                    pressed_key = event.key
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = True

            if is_pressed:
                if pressed_key == pygame.K_n:
                    sys.exit()
                elif pressed_key == pygame.K_y:
                    scene_exit = True
                elif pressed_key == pygame.K_ESCAPE:
                    self.is_setting = False
                    surface = pygame.surface.Surface((800, 600))
                    self.screen.blit(surface, (0, 0))
                elif pressed_key == pygame.K_x:
                    self.is_setting = True

            if not self.is_setting:
                current_surface = self.get_surface()
                self.screen.blit(current_surface, (0, 0))
                self.screen.blit(self.screen_light, (0, 0))

            if self.is_setting:
                self.screen.blit(pygame.image.load(r'resource/image/setting.png'), (0, 0))
                self.screen.blit(self.screen_light, (0, 0))
                if mouse_down:
                    # print("-----")
                    x, y = pygame.mouse.get_pos()
                    if 400 <= x <= 465 and 270 <= y <= 310:
                        if 0 < self.alpha <= 150:
                            self.alpha -= 10
                            self.screen_light.set_alpha(self.alpha)
                    elif 510 <= x <= 575 and 270 <= y <= 310:
                        # print("+++++")
                        if 0 <= self.alpha < 150:
                            self.alpha += 10
                            self.screen_light.set_alpha(self.alpha)
                    elif 400 <= x <= 465 and 150 <= y <= 180:
                        if self.sound_voice >= 0.9:
                            self.sound_voice += 0.1
                            pygame.mixer.music.set_volume(self.sound_voice)
                    elif 510 <= x <= 575 and 150 <= y <= 180:
                        if self.sound_voice >= 0.1:
                            self.sound_voice -= 0.1
                            pygame.mixer.music.set_volume(self.sound_voice)
                    elif 390 <= x <= 485 and 405 <= y <= 450:
                        pygame.mixer.music.stop()
                        self.sound_path = r'resource/music/张国荣 - 愿你决定.mp3'
                        pygame.mixer.music.load(self.sound_path)
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume())
                        pygame.mixer.music.play(-1)
                    elif 495 <= x <= 600 and 405 <= y <= 450:
                        pygame.mixer.music.stop()
                        self.sound_path = r'resource/music/123.mp3'
                        pygame.mixer.music.load(self.sound_path)
                        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume())
                        pygame.mixer.music.play(-1)


            pygame.display.update()
            self.res[1] = self.alpha
            self.res[2] = self.sound_path
            self.res[3] = pygame.mixer.music.get_volume()
            self.res[4] = pygame.mixer.music.get_pos()
            clock.tick(5)  # 1s循环40次，即刷新页面40次

        return self.res
