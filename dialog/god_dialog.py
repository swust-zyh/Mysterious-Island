import os
import pygame

from dialog import blit_text

class GodDialog:
    def __init__(self, text_num):
        # 1 头像照片
        img_path = os.path.join('resource', 'image', 'magicman', 'dialog.png')
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
            text = "年轻人，也许我能告诉你点什么...\n按y键继续。"
        elif text_num == 2:
            text = "冒险者，成功除了勇气，往往运气是走向成功的第一步。 只有通过运气之神考验的人才能继续寻宝之旅。 你需要先在宝箱中找到开封的宝剑，小心隐身的幽灵哦。 但这并没有结束，" \
               "找到宝剑之后，你需要在四扇大门中找到真正的宝藏之门。 在探索未知的路上，你可能会遇到许多危险，在尝试打开宝藏之门之前，请谨慎！ 记住千万别碰到岛屿上的其他人类，他们将吃掉你，祝你好运~"
        elif text_num == 3:  # 场景2
            text = "幸运的冒险者，你来到了这一关，代表你离成功又进了一步。 在走向成功的道路上，运气虽然重要，但光有运气是走不长远的。 同时也需要拥有面对成功路上所有荆棘的勇气。 "\
                    "注意，千万别碰到勇气之神为了考验寻宝者而留下的地刺，沟壑和宝藏守护者们， 他们会阻止你获得宝藏。 加油，年轻人！\n按y键继续..."
        elif text_num == 4:  # 场景3
            text = "勇敢的冒险者，恭喜你已经通过了宝藏前两关 -- 运气与勇气的考验。 再通过坚持之神的考验你将能获得珍贵的宝藏。 本关卡由于受到坚持之神的重力颠倒，你将会一直向下跌，你需要不断的跳跃， 防止自己落入骷髅大军的虎口，同时本关卡的法师塔的观察范围也极广，如果被他 发现，你将被塔上的法师用来祭天，最后记得绕开蝙蝠守护灵和空中的机关陷阱。 按y键继续..."

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
