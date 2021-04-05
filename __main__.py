# -*- coding: utf-8 -*-

import csv

import pyglet
from pyglet.sprite import Sprite
from pyglet.window import key, FPSDisplay

from GameObject import GameObject, TextBox, ChoiceBox


class MyVM(pyglet.window.Window):  #
    def __init__(self, *args, **kwargs):  # constructor
        super().__init__(*args, **kwargs)  # runs constructor from inherited method
        self.set_location(100, 100)
        self.frame_rate = 1 / 160.0  # number of target fps
        self.background_batch = pyglet.graphics.Batch()
        self.character_batch = pyglet.graphics.Batch()
        self.textbox_batch = pyglet.graphics.Batch()
        self.darkness_batch = pyglet.graphics.Batch()
        self.choice_batch = pyglet.graphics.Batch()  # batches from which graphics are going to be drawn
        self.fps_display = FPSDisplay(self)  # display FPS
        self.fps_display.label.y = self.height - 10
        self.fps_display.label.x = 0
        self.fps_display.label.font_size = 10  # position of FPS counter
        self.story_number = 0  # line number from which story CSV should be read
        self.progress_story = True  # status if story should progress or wait for interaction
        self.characters_table = dict()  # dictionary with all characters
        self.wait_animation = False
        # pyglet.font.add_directory("res/font/")
        # pyglet.font.load('Noto Sans') # set custom font (usefull for windows)

        self.box = TextBox(self.width, "", "", 2, self.textbox_batch)  # Prepares textbox used later
        self.box.set_opacity(0)  # hides textbox since in begining we show "main menu"
        self.choice = ChoiceBox(self.height, self.width, "", "", self.choice_batch)  # Prepares choice boxes
        self.choice.set_opacity(0)  # and hides them
        self.story_board = []  # Creates array for story
        with open("res/story/sb.csv", encoding="utf-8") as fh:  # Puts into array story board
            rd = csv.DictReader(fh, delimiter="|")
            for row in rd:
                self.story_board.append(row)
        del fh

        # creates black box to cover screen when needed
        color = (0, 0, 0, 255)
        self.image_pattern = pyglet.image.SolidColorImagePattern(color=color)
        self.image = self.image_pattern.create_image(self.width, self.height)
        self.darkness = GameObject(0, 0, Sprite(self.image, batch=self.darkness_batch))
        self.darkness.set_opacity(0)

        # creates object with initial main menu background
        self.mmBackground = GameObject(0, 0, "bg/mm.jpg", batch=self.background_batch)

    def on_key_press(self, symbol, modifiers):  # overrides actions on key press
        if symbol == key.NUM_1 or symbol == key._1:  # if number 1
            if self.choice.waiting_choice:  # Checks if its waiting for input
                self.choice.waiting_choice = False  # sets its no longer waiting for input
                self.progress_story = True  # sets flag fro story to progress
                self.story_number = int(self.story_board[self.story_number]["set1"])  # jumps to index of chosen choice
                self.choice.set_opacity(0)  # sets choice boxes as invincible
        if symbol == key.NUM_2 or symbol == key._2:  # if number 2 does the same as 1
            if self.choice.waiting_choice:
                self.choice.waiting_choice = False
                self.progress_story = True
                self.story_number = int(self.story_board[self.story_number]["set2"])
                self.choice.set_opacity(0)
        if symbol == key.SPACE:  # if space
            if not self.choice.waiting_choice and not self.wait_animation:  # check if its not waiting for choice
                if self.box.ready:  # checks if text writing has ended
                    self.box.ready = False  # sets flag for text writing
                    self.story_number += 1  # adds one to story index
                    self.progress_story = True  # sets for story to continue
                else:
                    self.box.skip_write()  # invokes skipping of writing and prints out everything
        if symbol == key.ESCAPE:  # if escape
            pyglet.app.exit()  # quits
        pass

    def on_key_release(self, symbol, modifiers):  # nie używane
        pass

    def on_draw(self):  # how to draw, also sets priority of layers
        self.clear()  # cleans screen
        self.background_batch.draw()  # draws background
        self.character_batch.draw()  # draws characters
        self.textbox_batch.draw()  # draws textbox
        self.choice_batch.draw()  # draws choices box
        self.darkness_batch.draw()  # draws darkness
        self.fps_display.draw()  # draw FPS counter

    def update(self, dt):
        self.update_story()  # runs update_story function
        self.box.update(dt)  # runs text box update with time (so the writing speed is relatively consistent)
        self.darkness.update(dt)  # runs darkness layer update with time (so alpha change is relatively consistent)
        if self.darkness.set_ok:  # is darkness finishes alpha change to desired state allows story to progress
            self.darkness.set_ok = False
            self.progress_story = True
            self.wait_animation = False
        for character in self.characters_table:
            self.characters_table[character].update(dt)  # updates characters animation with time (so it moves smoothly)
            if self.characters_table[character].set_ok:  # if characters animation finishes allows story to progress
                self.characters_table[character].set_ok = False
                self.progress_story = True
                self.wait_animation = False

    def update_story(self):  # story progress
        if self.progress_story:  # check if story should progress
            if self.story_number == -1:  # checks if story number isn't -1
                pyglet.app.exit()  # exists game
            current = self.story_board[self.story_number]  # writes what actions are going to happened
            self.progress_story = False  # sets flag

            if int(current['action']) == 0:  # text action
                self.box.set_opacity(255)  # shows textbox
                self.box.change_speaker(current["person"])  # sets person speaking
                self.box.change_text(current["text"], current["value1"])  # sets text
            elif int(current['action']) == 1:  # choice
                self.choice.set_opacity(255)  # shows choice boxes
                self.choice.change_text(current["value1"], current["value2"])  # sets text in them
            elif int(current['action']) == 2:  # just jump
                self.story_number = int(current["value1"])
                self.progress_story = True
            elif int(current['action']) == 3:  # create character
                self.characters_table[current["person"]] = GameObject(
                    int(current["value2"]), 210, f"char/{current['value1']}", self.character_batch)
                self.story_number += 1
                self.progress_story = True
            elif int(current['action']) == 4:  # move character
                self.characters_table[current["person"]].animate_x(int(current["value1"]))
                self.story_number += 1
                self.wait_animation = True
            elif int(current['action']) == 5:  # remove character
                del self.characters_table[current["person"]]
                self.story_number += 1
                self.progress_story = True
            elif int(current['action']) == 6:  # change background
                self.mmBackground.replace_bg(current['value1'])
                self.story_number += 1
                self.progress_story = True
            elif int(current['action']) == 7:  # screen dimming
                self.story_number += 1
                self.wait_animation = True
                if int(current['value1']) == 0:
                    self.darkness.animate_opacity(0)
                elif int(current['value1']) == 1:
                    self.darkness.animate_opacity(255)
            elif int(current['action']) == 8:  # play sound
                sound = pyglet.resource.media(f"res/sfx/{current['value1']}", streaming=False)
                sound.play()
                self.story_number += 1
                self.progress_story = True
            elif int(current['action']) == 9:  # hide text box
                self.box.set_opacity(0)
                self.story_number += 1
                self.progress_story = True


if __name__ == "__main__":
    window = MyVM(width=1280, height=720, caption="BestVN", resizable=False)  # Creates windows
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()  # runs this ~~trash~~
