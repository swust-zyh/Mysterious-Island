import random
import sys
import time

import pygame
import pytmx

from dialog.Door_dialog import DoorDialog
from dialog.god_dialog import GodDialog
from object.Door import Door
from object.Invisible_obstacle import InvisibleObstacle
from object.NPC import NPC
from object.Gamer import Gamer
from object.InteractiveMoveNPC import InteractiveMoveNPC
from object.Treasure import Treasure
from scenes import RenderTmx, FadeScene


class Scene1:
    def __init__(self, screen, screen_light, alpha, sound_path, sound_voice, sound_pos, *objects):
        pygame.init()
        pygame.mixer.init()

        # print(alpha)
        self.screen = screen
        self.render = RenderTmx(r'resource/map1.tmx')
        self.temp_surface = self.render.surface.copy()  # 临时surface用于人物自主移动
        self.objects = objects  # 后面要用就要用私有变量，不然后面的类方法将用不了该变量
        # 对象层
        self.guard_group = pygame.sprite.Group()
        self.monster_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.door_group = pygame.sprite.Group()
        self.invisible_group = pygame.sprite.Group()
        self.restart_dialog = pygame.image.load(r'resource/image/regame.png')
        self.is_regame = False
        self.init_object_group()
        self.fade = FadeScene(self.render.surface)
        self.dialog = GodDialog(1)
        self.door = Door(0, 0, False)
        self.door_dialog1 = DoorDialog(1)
        self.door_dialog2 = DoorDialog(2)
        self.door_dialog3 = DoorDialog(3)
        self.door_dialog4 = DoorDialog(4)
        self.screen_light = screen_light
        self.flag = True
        self.scene_exit = False
        self.is_setting = False
        self.alpha = alpha
        self.invisible = InvisibleObstacle(10, 10)
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
                if group.name == '守卫':
                    for obj in group:
                        guard = NPC(obj.x, obj.y, obj.width, obj.height, 2, 'guard', 'guard')
                        self.guard_group.add(guard)

                if group.name == 'gamer':
                    for obj in group:
                        self.gamer = Gamer(obj.x, obj.y, 10, 10, True, 4, 2)

                if group.name == '怪兽':
                    for obj in group:
                        if int(obj.name) % 2:
                            monster = InteractiveMoveNPC(obj.x, obj.y, 'monsters', '红野人', False, 50, 2)
                            self.monster_group.add(monster)
                        else:
                            monster = InteractiveMoveNPC(obj.x, obj.y, 'monsters', '蓝野人', False, 40, 1)
                            self.monster_group.add(monster)

                if group.name == '宝箱':
                    cnt = 0
                    mask = random.randint(1, 5)
                    for obj in group:
                        cnt += 1
                        if cnt == mask:
                            box = Treasure(obj.x, obj.y, False)
                        else:
                            box = Treasure(obj.x, obj.y, True)
                        self.box_group.add(box)

                if group.name == '门':
                    cnt = 0
                    mask = random.randint(1, 4)
                    for obj in group:
                        cnt += 1
                        if cnt == mask:
                            door = Door(obj.x, obj.y, True)
                        else:
                            door = Door(obj.x, obj.y, False)
                        self.door_group.add(door)

                if group.name == '神秘人':
                    for obj in group:
                        self.god = InteractiveMoveNPC(obj.x, obj.y, 'magicman', 'god', True, 45, 1)

                if group.name == '障碍':
                    for obj in group:
                        if obj.name == 'invisible':
                            invisible = InvisibleObstacle(obj.x, obj.y)
                            self.invisible_group.add(invisible)
                        else:
                            obstacle = pygame.sprite.Sprite()
                            obstacle.rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            self.obstacle_group.add(obstacle)

    def get_current_surface(self):
        surface = self.fade.get_back_image()
        self.temp_surface.blit(surface, (0, 0))
        # 覆盖的思想
        self.temp_surface.blit(self.render.surface, (0, 0))
        for it in self.objects:
            it.draw(self.temp_surface)
        for guard in self.guard_group:  # 从tmx的定点为左上角开始绘制所以位置会有少许偏差
            guard.draw(self.temp_surface)
        for box in self.box_group:
            box.draw(self.temp_surface)
        for monster in self.monster_group:
            monster.draw(self.temp_surface)

        # 开宝箱
        collide_box = pygame.sprite.spritecollide(self.gamer, self.box_group, False)
        if len(collide_box) > 0:
            for box in collide_box:
                box.status = False
            if not self.gamer.key and box.key:
                box.draw_key(self.temp_surface)
                self.gamer.key = True

        self.gamer.draw(self.temp_surface)

        # 碰撞隐形障碍
        collide_invisible = pygame.sprite.spritecollide(self.gamer, self.invisible_group, False)
        if len(collide_invisible) > 0:
            for invisible in collide_invisible:
                if not invisible.flag:
                    invisible.draw(self.temp_surface)
                    self.invisible = invisible
                if not invisible.status:
                    self.gamer.hp -= 20
                    invisible.status = True
        else:
            self.invisible.flag = True

        # 进门
        collide_door = pygame.sprite.spritecollide(self.gamer, self.door_group, False)
        if len(collide_door) > 0:
            for door in collide_door:
                if self.gamer.key and door.jump:
                    self.scene_exit = True
                elif self.gamer.key and not door.jump:
                    if door.status1:
                        self.temp_surface.blit(self.door_dialog4.surface, (0, 0))
                        if not door.flag1:
                            self.gamer.hp -= 20
                            door.flag1 = True
                    else:
                        self.temp_surface.blit(self.door_dialog2.surface, (0, 0))
                        if not door.flag3:
                            self.gamer.hp -= 20
                            door.flag3 = True
                        self.door = door
                elif not self.gamer.key:
                    if door.status2:
                        self.temp_surface.blit(self.door_dialog3.surface, (0, 0))
                        if not door.flag2:
                            self.gamer.hp -= 20
                            door.flag2 = True
                    else:
                        self.temp_surface.blit(self.door_dialog1.surface, (0, 0))
                        if not door.flag4:
                            self.gamer.hp -= 20
                            door.flag4 = True
                        self.door = door
        else:
            if self.door.pos_x != 0:
                if self.gamer.key:
                    self.door.status1 = True
                else:
                    self.door.status2 = True

            # print(self.door.status2, "+++++++")

        self.god.draw(self.temp_surface)

        pygame.draw.rect(self.temp_surface, pygame.Color(240, 65, 85),
                         # pygame.draw模块详解：https://www.cnblogs.com/leonyoung/archive/2012/07/01/2572205.html
                         pygame.Rect(self.gamer.pos_x - 10, self.gamer.pos_y - 20, self.gamer.hp / 2, 5))

        if self.is_regame:
            self.temp_surface.blit(self.restart_dialog, (100, 30))

        # 开始提示
        if self.flag:
            self.temp_surface.blit(self.dialog.surface, (0, 0))

        return self.temp_surface

    def run(self):
        clock = pygame.time.Clock()  # 计时器
        while not self.scene_exit:
            # print(self.gamer.hp)
            mouse_down = False
            pressed_key = 0
            if self.gamer.hp <= 0:
                self.is_regame = True

            is_pressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:  # 按下键盘上的键这个事件
                    is_pressed = True
                    pressed_key = event.key
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = True

            if self.is_regame:
                if mouse_down:
                    x, y = pygame.mouse.get_pos()
                    if 240 <= x <= 570 and 170 <= y <= 215:
                        sys.exit()
                    elif 240 <= x <= 570 and 290 <= y <= 330:
                        self.res[0] = -2
                        return self.res

            # 碰撞怪兽
            collide_monster = pygame.sprite.spritecollide(self.gamer, self.monster_group, False)
            if len(collide_monster) > 0:
                self.is_regame = True

            if is_pressed:
                self.gamer.key_move(pressed_key, self.obstacle_group)
                if pressed_key == pygame.K_y:
                    self.flag = False
                elif pressed_key == pygame.K_ESCAPE:
                    self.is_setting = False
                    surface = pygame.surface.Surface((800, 600))
                    self.screen.blit(surface, (0, 0))
                elif pressed_key == pygame.K_x:
                    self.is_setting = True

            self.god.collide(self.gamer)

            if not self.is_setting:
                current_surface = self.get_current_surface()
                self.screen.blit(current_surface, (0, 0))
                self.screen.blit(self.screen_light, (0, 0))

            # print(mouse_down)
            # print(self.alpha)

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
