import sys

import pygame
from pytmx import pytmx

from dialog.god_dialog import GodDialog
from object.Door import Door
from object.InteractiveMoveNPC import InteractiveMoveNPC
from object.NPC import NPC
from object.SceneGamer import SceneGamer
from scenes import RenderTmx, FadeScene


class Scene2:
    def __init__(self, screen, screen_light, alpha, sound_path, sound_voice, sound_pos):
        self.flag = True
        self.is_y = False
        self.screen = screen
        self.screen_light = screen_light
        self.is_setting = False
        self.alpha = alpha
        self.render = RenderTmx(r'resource/map2.tmx')
        self.temp_surface = self.render.surface.copy()
        self.fade = FadeScene(self.render.surface)
        self.thorn_group = pygame.sprite.Group()
        self.steps_group = pygame.sprite.Group()
        self.gully_group = pygame.sprite.Group()
        self.can_walk_group = pygame.sprite.Group()
        self.scene_exit = False
        self.mask = False
        self.t = 10
        self.init_object_group()
        self.dialog = GodDialog(3)
        self.is_regame = False
        self.restart_dialog = pygame.image.load(r'resource/image/regame.png')
        self.sound_path = sound_path
        self.sound_voice = sound_voice
        self.sound_pos = sound_pos
        self.res = [-1, -1, -1, -1, -1]

        # 详解：https://blog.csdn.net/qq_41556318/article/details/86305046
        pygame.mixer.music.set_pos(self.sound_pos)
        pygame.mixer.music.load(self.sound_path)
        pygame.mixer.music.set_volume(self.sound_voice)
        pygame.mixer.music.play(-1)  # -1即循环播放

    def init_object_group(self):
        for group in self.render.tiled.tmx_data.objectgroups:  # 得到图片信息
            if isinstance(group, pytmx.TiledObjectGroup):  # isinstance函数: runoob.com/python/python-func-isinstance.html
                if group.name == 'gamer':
                    for obj in group:
                        self.gamer = SceneGamer(obj.x, obj.y, 10, 10, True, 4, 2)

                if group.name == '地刺':
                    for obj in group:
                        thorn = NPC(obj.x, obj.y, obj.width, obj.height, 1, "", "berry")
                        self.thorn_group.add(thorn)

                if group.name == '传送门':
                    for obj in group:
                        self.door = Door(obj.x, obj.y, True)

                if group.name == '怪兽':
                    for obj in group:
                        if obj.name == '褐色':
                            self.monster1 = InteractiveMoveNPC(obj.x, obj.y, '2_monsters', 'player', False, 50, 0)
                        if obj.name == '绿色':
                            self.monster2 = InteractiveMoveNPC(obj.x, obj.y, '2_monsters', 'innman', False, 20, 1)

                if group.name == '台阶':
                    for obj in group:
                        step = pygame.sprite.Sprite()
                        step.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.steps_group.add(step)

                if group.name == '沟壑':
                    for obj in group:
                        # print(obj.x, obj.y)
                        gully = pygame.sprite.Sprite()
                        gully.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.gully_group.add(gully)

                if group.name == '可走层':
                    for obj in group:
                        can_walk = pygame.sprite.Sprite()
                        can_walk.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.can_walk_group.add(can_walk)


    def get_current_surface(self):
        # print(len(self.thorn_group))
        surface = self.fade.get_back_image()
        self.temp_surface.blit(surface, (0, 0))
        for thorn in self.thorn_group:
            thorn.draw(self.temp_surface)
        self.monster1.draw(self.temp_surface)
        self.monster2.draw(self.temp_surface)
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
            # print(self.gamer.pos_x, self.gamer.pos_y)
            if self.gamer.pos_y > 400:
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

            # 检测可走路段 只能掉到190
            collide_can_walk = pygame.sprite.spritecollide(self.gamer, self.can_walk_group, False)
            if len(collide_can_walk) == 0 and not self.gamer.jump:
                self.gamer.pos_y += 30

            # 掉进沟壑里
            collide_gully = pygame.sprite.spritecollide(self.gamer, self.gully_group, False)
            # print(len(collide_gully), len(self.gully_group))
            # print(self.gamer.pos_x, self.gamer.pos_y)
            if len(collide_gully) > 0:
                self.gamer.pos_y += 40
                self.gamer.pos_x -= 10

            # 碰撞地刺
            collide_obstacle = pygame.sprite.spritecollide(self.gamer, self.thorn_group, False)
            if len(collide_obstacle) > 0:
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

            # 碰npc
            collide_npc1 = pygame.sprite.collide_rect(self.gamer, self.monster1)
            collide_npc2 = pygame.sprite.collide_rect(self.gamer, self.monster2)
            if collide_npc1 or collide_npc2:
                self.is_regame = True


            # 通关
            collide_door = pygame.sprite.collide_rect(self.gamer, self.door)
            if collide_door:
                self.scene_exit = True

            if is_pressed:
                self.gamer.key_move(pressed_key)
                if pressed_key == pygame.K_y:
                    self.flag = False
                elif pressed_key == pygame.K_ESCAPE:
                    self.is_setting = False
                    surface = pygame.surface.Surface((800, 600))
                    self.screen.blit(surface, (0, 0))
                elif pressed_key == pygame.K_x:
                    self.is_setting = True

            if self.is_regame:
                self.gamer.pos_x -= 10
                if mouse_down:
                    x, y = pygame.mouse.get_pos()
                    if 240 <= x <= 570 and 170 <= y <= 215:
                        sys.exit()
                    elif 240 <= x <= 570 and 290 <= y <= 330:
                        self.res[0] = -2
                        return self.res

            if not self.flag:
                if self.gamer.pos_x >= 750:
                    self.gamer.pos_x = 750
                    self.gamer.rect = pygame.Rect(self.gamer.pos_x, self.gamer.pos_y, self.gamer.rect_width, self.gamer.rect_height)
                else:
                    self.gamer.pos_x += 10
                    self.gamer.rect = pygame.Rect(self.gamer.pos_x, self.gamer.pos_y, self.gamer.rect_width, self.gamer.rect_height)

            if self.gamer.jump:
                if self.t >= -10:
                    self.gamer.a = 1  # 前半段减速上跳
                    if self.t < 0:
                        self.gamer.a = -1  # 后半段加速下落
                    self.gamer.pos_y -= 0.5 * self.gamer.a * (self.t ** 2)  # 匀加速直线运动的位移公式

                    if self.gamer.pos_y < 0:
                        self.gamer.pos_y = 0  # 防止跳出边界
                    self.t -= 5
                else:
                    self.gamer.jump = False
                    self.t = 10

            if not self.is_setting:
                current_surface = self.get_current_surface()
                self.screen.blit(current_surface, (0, 0))
                self.screen.blit(self.screen_light, (0, 0))

            if self.is_setting:
                if self.gamer.pos_x != 0:
                    self.gamer.pos_x -= 10
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
