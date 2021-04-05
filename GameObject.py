from math import ceil, floor

import pyglet
from pyglet.sprite import Sprite


class GameObject:
    def __init__(self, posx, posy, image, batch=None):
        self.in_opacity = False
        self.x_target = posx
        self.batch = batch
        self.begin = 255
        self.opacity_target = 255
        self.set_ok = False
        self.waiting = False
        if isinstance(image, str):
            self.sprite = Sprite(pyglet.image.load(f"res/{image}"), batch=self.batch)
        else:
            self.sprite = image
        self.sprite.x = posx
        self.sprite.y = posy
        self.opacity = self.sprite.opacity

    def draw(self):
        self.sprite.draw()

    def replace_bg(self, image):
        self.sprite = Sprite(pyglet.image.load(f"res/bg/{image}"), batch=self.batch)

    def update(self, dt):

        if not self.sprite.x == self.x_target:
            if ceil(self.sprite.x) < self.x_target:
                self.sprite.x += 150 * dt
            if ceil(self.sprite.x) == self.x_target or floor(self.sprite.x) == self.x_target:
                self.sprite.x = self.x_target
                self.set_ok = True
            if floor(self.sprite.x) > self.x_target:
                self.sprite.x -= 150 * dt

        if not self.sprite.opacity == self.opacity_target:
            if ceil(self.sprite.opacity) < self.opacity_target:
                self.sprite.opacity += 150 * dt
            if ceil(self.sprite.opacity) == self.opacity_target or floor(self.sprite.opacity) == self.opacity_target:
                self.sprite.opacity = self.opacity_target
                self.set_ok = True
            if floor(self.sprite.opacity) > self.opacity_target:
                self.sprite.opacity -= 150 * dt

    def set_opacity(self, opacity=255):
        self.sprite.opacity = opacity
        self.opacity_target = opacity

    def animate_opacity(self, opacity=255):
        self.begin = self.sprite.opacity
        self.opacity_target = opacity
        self.set_ok = False

    def animate_x(self, x):
        self.begin = self.sprite.x
        self.x_target = x
        self.set_ok = False


class TextBox:
    def __init__(self, window_width, speaker, text, speed, batch):
        width = int(round(window_width - 20))
        height = int(round(210))
        x = 10
        y = 10
        self.ready = False
        self.text_length = len(text)
        self.printed = 0
        self.counter = 0
        self.speed = speed
        self.in_text = text
        messagebox = pyglet.graphics.OrderedGroup(0)
        cheracterbox = pyglet.graphics.OrderedGroup(1)
        texts = pyglet.graphics.OrderedGroup(2)

        color = (133, 172, 173, 200)
        self.image_pattern = pyglet.image.SolidColorImagePattern(color=color)
        self.image = self.image_pattern.create_image(width, height)
        self.text_box = GameObject(x, y, Sprite(self.image, batch=batch, group=messagebox))

        color = (128, 191, 255, 255)
        self.image_pattern = pyglet.image.SolidColorImagePattern(color=color)
        self.image = self.image_pattern.create_image(200, 30)
        self.character_box = GameObject(x + 10, y + height - 20, Sprite(self.image, batch=batch, group=cheracterbox))

        self.character = pyglet.text.Label(" GameObject", x=x + 15, y=y + height - 10, width=200, batch=batch,
                                           group=texts, font_name="Noto Sans")
        self.text = pyglet.text.HTMLLabel("", x=x + 10, y=y + height - 40, height=height - 20, width=width - 10,
                                          multiline=True, batch=batch, group=texts)


    def update(self, dt):
        self.update_text(dt)

    def update_text(self, dt):
        if self.counter == self.speed:
            self.counter = 0
            if not self.printed >= self.text_length:
                if self.in_text[self.printed] == "<":
                    while not self.in_text[self.printed] == ">":
                        self.printed += 1
                        self.text.text = self.in_text[:self.printed + 1]
                    self.printed += 1
                try:
                    if not self.in_text[self.printed] == "<":
                        self.printed += 1
                        self.text.text = self.in_text[:self.printed]
                except IndexError:
                    pass
            else:
                self.ready = True
        else:
            self.counter += 1

    def change_text(self, text, speed=None):
        if not speed is None:
            self.speed = int(speed)
        self.in_text = text
        self.text_length = len(text)
        self.printed = 0
        self.counter = 0

    def change_speaker(self, character):
        self.character.text = character

    def skip_write(self):
        self.printed = self.text_length
        self.text.text = self.in_text

    def set_opacity(self, opacity=255):
        self.text_box.set_opacity(opacity)
        self.character_box.set_opacity(opacity)
        if opacity == 0:
            self.character.text = ""
            self.text.text = ""
            self.text_length = len("")
            self.printed = 0
            self.counter = 0


class ChoiceBox():
    def __init__(self, window_height, window_width, choice1, choice2, batch):
        x = 300
        y = window_height - 200
        width = int(round(window_width - 300 - x))
        height = int(round(100))
        color = (16, 129, 146, 230)
        self.waiting_choice = False
        background = pyglet.graphics.OrderedGroup(0)
        text = pyglet.graphics.OrderedGroup(1)
        self.image_pattern = pyglet.image.SolidColorImagePattern(color=color)
        self.image = self.image_pattern.create_image(width=width, height=height)
        self.choice1_box = GameObject(x, y, Sprite(self.image, batch=batch, group=background))
        self.choice2_box = GameObject(x, y - 200, Sprite(self.image, batch=batch, group=background))

        self.choice1 = pyglet.text.Label(choice1, x=x + (width / 2), y=y + (height / 2), height=height, width=width,
                                         batch=batch, group=text, anchor_y="center", anchor_x='center', font_size=34,
                                         multiline=True, font_name="Noto Sans", bold=False)

        self.choice2 = pyglet.text.Label(choice2, x=x + (width / 2), y=y + (height / 2) - 200, height=height,
                                         width=width, batch=batch, group=text, anchor_y="center", anchor_x='center',
                                         font_size=34, font_name="Noto Sans", multiline=True, bold=False)

    def update(self, dt):
        pass

    def set_opacity(self, opacity=255):
        self.choice1_box.set_opacity(opacity)
        self.choice2_box.set_opacity(opacity)
        if opacity == 0:
            self.choice1.text = ""
            self.choice2.text = ""

    def change_text(self, text1, text2):
        self.choice1.text = text1
        self.choice2.text = text2
        self.waiting_choice = True
