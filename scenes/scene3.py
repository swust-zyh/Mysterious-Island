import sys

import pygame
from pytmx import pytmx

from dialog.god_dialog import GodDialog
from object.Door import Door
from object.InteractiveMoveNPC import InteractiveMoveNPC
from object.NPC import NPC
from object.SceneGamer import SceneGamer
from scenes import RenderTmx, FadeScene


class Scene3:
    def __init__(self, screen, screen_light, alpha, sound_path, sound_voice, sound_pos):
        self.flag = True
        self.screen = screen
        self.screen_light = screen_light
        self.scene_exit = False
        self.is_setting = False
        self.alpha = alpha
        self.render = RenderTmx(r'resource/map3.tmx')
        self.temp_surface = self.render.surface.copy()
        self.fade = FadeScene(self.render.surface)
        self.birds_group = pygame.sprite.Group()
        self.steps_group = pygame.sprite.Group()
        self.pagoda_group = pygame.sprite.Group()
        self.gear_group = pygame.sprite.Group()
        self.can_walk_group = pygame.sprite.Group()
        self.thorn_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.scene_exit = False
        self.mask = False
        self.t = 10
        self.init_object_group()
        self.dialog = GodDialog(4)
        self.is_regame = False
        self.restart_dialog = pygame.image.load(r'resource/image/regame.png')

        self.sound_path = sound_path
        self.sound_voice = sound_voice
        self.sound_pos = sound_pos
        self.res = [-1, -1, -1, -1, -1]

        # 详解：https://blog.csdn.net/qq_41556318/article/details/86305046
        pygame.mixer.music.set_pos(self.sound_pos / 1000)
        pygame.mixer.music.load(self.sound_path)
        pygame.mixer.music.set_volume(self.sound_voice)
        pygame.mixer.music.play(-1)  # -1即循环播放

    def init_object_group(self):
        for group in self.render.tiled.tmx_data.objectgroups:  # 得到图片信息
            if isinstance(group, pytmx.TiledObjectGroup):  # isinstance函数: runoob.com/python/python-func-isinstance.html
                if group.name == 'gamer':
                    for obj in group:
                        self.gamer = SceneGamer(obj.x, obj.y, 10, 10, True, 4, 2)

                if group.name == '瞭望塔':
                    for obj in group:
                        pagoda = pygame.sprite.Sprite()
                        pagoda.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.pagoda_group.add(pagoda)

                if group.name == '传送门':
                    for obj in group:
                        self.door = Door(obj.x, obj.y, True)

                if group.name == '飞鸟':
                    for obj in group:
                        bird = InteractiveMoveNPC(obj.x, obj.y, 'birds', 'devil', False, 50, 0)
                        self.birds_group.add(bird)

                if group.name == '齿轮':
                    for obj in group:
                        gear = NPC(obj.x, obj.y, obj.width, obj.height, 1, "", "齿轮")
                        self.gear_group.add(gear)

                if group.name == '台阶':
                    for obj in group:
                        step = pygame.sprite.Sprite()
                        step.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.steps_group.add(step)

                if group.name == '可走层':
                    for obj in group:
                        can_walk = pygame.sprite.Sprite()
                        can_walk.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.can_walk_group.add(can_walk)

                if group.name == '地刺':
                    for obj in group:
                        thorn = NPC(obj.x, obj.y, obj.width, obj.height, 1, "", "berry")
                        self.thorn_group.add(thorn)

                if group.name == '骷髅大军':
                    for obj in group:
                        obstacle = pygame.sprite.Sprite()
                        obstacle.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.obstacle_group.add(obstacle)


    def get_current_surface(self):
        # print(len(self.thorn_group))
        # print(len(self.thorn_group))
        surface = self.fade.get_back_image()
        self.temp_surface.blit(surface, (0, 0))
        for gear in self.gear_group:
            gear.draw(self.temp_surface)
        for bird in self.birds_group:
            bird.draw(self.temp_surface)
        for thorn in self.thorn_group:
            thorn.draw(self.temp_surface)
        self.gamer.draw(self.temp_surface)
        # 开始提示
        if self.flag:
            self.temp_surface.blit(self.dialog.surface, (0, 0))
        if self.is_regame:
            self.temp_surface.blit(self.restart_dialog, (100, 30))
        return self.temp_surface

    def run(self):
        clock = pygame.time.Clock()  # 计时器
        while not self.scene_exit:
            mouse_down = False
            if self.flag:
                self.temp_surface.blit(self.dialog.surface, (0, 0))

            # print(self.gamer.pos_x, self.gamer.pos_y)
            if self.gamer.pos_y > 385:
                self.is_regame = True
            # print(self.gamer.pos_x)
            is_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:  # 按下键盘上的键这个事件
                    is_pressed = True
                    pressed_key = event.key
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = True

            self.gamer.collide(self.obstacle_group)

            if self.is_regame:
                self.gamer.pos_x -= 10
                self.gamer.pos_y -= 10
                if mouse_down:
                    x, y = pygame.mouse.get_pos()
                    if 240 <= x <= 570 and 170 <= y <= 215:
                        sys.exit()
                    elif 240 <= x <= 570 and 290 <= y <= 330:
                        self.res[0] = -2
                        return self.res

            # 碰撞齿轮
            collide_gear = pygame.sprite.spritecollide(self.gamer, self.gear_group, False)
            collide_obstacle = pygame.sprite.spritecollide(self.gamer, self.obstacle_group, False)
            collide_birds = pygame.sprite.spritecollide(self.gamer, self.birds_group, False)
            collide_thorn = pygame.sprite.spritecollide(self.gamer, self.thorn_group, False)
            collide_pagoda = pygame.sprite.spritecollide(self.gamer, self.pagoda_group, False)
            if len(collide_gear) > 0 or len(collide_obstacle) > 0 or len(collide_birds) or len(collide_thorn) or len(collide_pagoda):
                self.is_regame = True

            # 上台阶
            # print(len(self.steps_group))
            # for it in self.steps_group:
            #     print(it.rect, "+++", self.gamer.rect)
            collide_steps = pygame.sprite.spritecollide(self.gamer, self.steps_group, False)
            if len(collide_steps) > 0:
                self.gamer.jump = False
                self.t = 10
                self.gamer.a = 1


            # 通关
            collide_door = pygame.sprite.collide_rect(self.gamer, self.door)
            if collide_door:
                self.scene_exit = True

            if is_pressed:
                if not self.flag:
                    if pressed_key == pygame.K_UP:
                        self.gamer.pos_y -= 20
                elif pressed_key == pygame.K_y:
                    self.flag = False

            if is_pressed:
                if pressed_key == pygame.K_ESCAPE:
                    self.is_setting = False
                    surface = pygame.surface.Surface((800, 600))
                    self.screen.blit(surface, (0, 0))
                elif pressed_key == pygame.K_x:
                    # print("++++++++")
                    self.is_setting = True

            if not self.flag:
                if self.gamer.pos_x >= 750:
                    self.gamer.pos_x = 750
                    self.gamer.rect = pygame.Rect(self.gamer.pos_x, self.gamer.pos_y, self.gamer.rect_width, self.gamer.rect_height)
                else:
                    self.gamer.pos_x += 10
                    self.gamer.rect = pygame.Rect(self.gamer.pos_x, self.gamer.pos_y, self.gamer.rect_width, self.gamer.rect_height)
                self.gamer.pos_y += 10


            if not self.is_setting:
                current_surface = self.get_current_surface()
                self.screen.blit(current_surface, (0, 0))
                self.screen.blit(self.screen_light, (0, 0))

            if self.is_setting:
                if self.gamer.pos_x != 0:
                    self.gamer.pos_x -= 10
                if not self.flag:
                    self.gamer.pos_y -= 10
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
