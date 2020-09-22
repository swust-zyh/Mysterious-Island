import os
import pygame

from dialog import blit_text

class DoorDialog:
    def __init__(self, text_num):
        # 1 头像照片
        img_path = os.path.join('resource', 'image', 'door.png')
        header = pygame.image.load(img_path)
        header_w = header.get_width()
        header_h = header.get_height()
        # # 头像缩小一半 参数：(原图像，(size))
        # header = pygame.transform.scale(temp_header, (header_w, header_h))
        # 2 对话框图片
        dialog_path = os.path.join('resource', 'image', 'dialoguebox.png')
        dialog = pygame.image.load(dialog_path)
        dialog_w = dialog.get_width()
        dialog_h = dialog.get_height()
        # # 缩小一半
        # dialog = pygame.transform.scale(temp_dialog, (dialog_w, dialog_h))
        # 3 绘制汉字
        font_path = os.path.join('resource', 'font', '迷你简粗宋.TTF')
        # 根据字体文件创建一个字体（Font）对象 font相当于是一个字体
        font = pygame.font.Font(font_path, 18)  # font类详解：https://blog.csdn.net/qq_41556318/article/details/86303502
        if text_num == 1:
            text = "只有开封的宝剑才能打开通往宝藏的大门，你将受到神的制裁，生命值减20...\n禁忌之门从此封印直到你找到开封的宝剑..."
        elif text_num == 2:
            text = "很不幸，神并没有眷顾你，你将受到神的制裁，生命值减20...\n禁忌之门破碎..."
        elif text_num == 3:
            text = "禁忌之门已封印..."
        elif text_num == 4:
            text = "禁忌之门已破碎..."

        """
        遇空格换行
        参数：
        1. surface
        2. 文本
        3. 文本显示的左上角位置
        4. 字体
        """
        blit_text(dialog, text, (130, 10), font)

        # 4 生成surface并绘制
        h = header_h
        w = dialog_w
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)  # 黑图片  fill
        # 5 设置关键色，形成透明图片
        # self.surface.set_colorkey((0, 0, 0))  # pygame.SRCALPHA
        # 6 把头像 对话框绘制上去
        self.surface.blit(dialog, (0, 0))
        self.surface.blit(header, (0, 0))
