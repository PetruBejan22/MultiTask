from tkinter import *
from PIL import ImageTk, Image
import random
from pygame import mixer
import math
import os
import sys
from tkinter import ttk


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

path_images = 'Files/Target/images/'
path_sounds = 'Files/Target/sounds/'


class Target:
    def __init__(self, root):
        self.run = True
        self.refresh_speed = 1000
        mixer.init()
        self.root = root
        self.root.geometry("700x700")
        self.root.minsize(380, 300)
        self.root.title("Target")
        # icon
        icon = resource_path(path_images + "target_icon.ico")
        self.root.iconbitmap(icon)

    # images and menus
    def images_and_menus(self):
        # start again
        start_again_png = resource_path(path_images + "start_again2.png")
        self.start_again_image = ImageTk.PhotoImage(Image.open(start_again_png))

        # Targets
        target1_png = resource_path(path_images + "target1.png")
        self.target1_image = ImageTk.PhotoImage(Image.open(target1_png))
        target2_png = resource_path(path_images + "target2.png")
        self.target2_image = ImageTk.PhotoImage(Image.open(target2_png))
        target3_png = resource_path(path_images + "target3.png")
        self.target3_image = ImageTk.PhotoImage(Image.open(target3_png))
        target4_png = resource_path(path_images + "target4.png")
        self.target4_image = ImageTk.PhotoImage(Image.open(target4_png))
        target5_png = resource_path(path_images + "target5.png")
        self.target5_image = ImageTk.PhotoImage(Image.open(target5_png))

        # create canvas
        self.game = Canvas(self.root, width=700, height=670, bg="#33BAFF", cursor="tcross")
        self.game.pack()

        # menu for Target size
        self.menu_target = ttk.Combobox(self.root,
                                        values=["Target Size 1", "Target Size 2", "Target Size 3", "Target Size 4",
                                                "Target Size 5"], font=("", 14, "bold"), state="readonly", width=11)
        self.menu_target.pack(side=LEFT)
        self.menu_target.current(0)

        # menu for speed target appearance
        self.menu_speed = ttk.Combobox(self.root,
                                       values=["Target Speed 1", "Target Speed 2", "Target Speed 3", "Target Speed 4",
                                               "Target Speed 5"], font=("", 14, "bold"), state="readonly", width=13)
        self.menu_speed.pack(side=RIGHT)
        self.menu_speed.current(0)

    # auto change canvas size with width and height from main screen
    def canvas_size(self, event):
        self.game.config(width=self.root.winfo_width(), height=self.root.winfo_height() - 30)

    # random target
    def random_target(self, target, xy_min):
        try:
            max_width = self.root.winfo_width() - xy_min
            max_height = self.root.winfo_height() - xy_min - 30
            rand_coord = [random.randint(xy_min, max_width), random.randint(xy_min, max_height)]
            self.target_x = rand_coord[0]
            self.target_y = rand_coord[1]
            self.rand_target = self.game.create_image(self.target_x, self.target_y, image=target)
        except:
            pass

    # change speed
    def speed_target(self):
        if self.menu_speed.get() == "Target Speed 1":
            self.refresh_speed = 1000
        if self.menu_speed.get() == "Target Speed 2":
            self.refresh_speed = 800
        if self.menu_speed.get() == "Target Speed 3":
            self.refresh_speed = 600
        if self.menu_speed.get() == "Target Speed 4":
            self.refresh_speed = 400
        if self.menu_speed.get() == "Target Speed 5":
            self.refresh_speed = 200

    # check the size of the target
    def change_target_size(self):
        if self.run:
            try:
                self.game.delete(self.rand_target)
            except:
                pass
            if self.menu_target.get() == "Target Size 1":
                self.random_target(self.target1_image, 30)
            if self.menu_target.get() == "Target Size 2":
                self.random_target(self.target2_image, 45)
            if self.menu_target.get() == "Target Size 3":
                self.random_target(self.target3_image, 60)
            if self.menu_target.get() == "Target Size 4":
                self.random_target(self.target4_image, 75)
            if self.menu_target.get() == "Target Size 5":
                self.random_target(self.target5_image, 90)

            self.speed_target()
        self.root.after(self.refresh_speed, self.change_target_size)

    # reset game
    def start(self):
        self.run = True
        self.game.delete(self.score_text)
        self.game.delete(self.dist_line)
        self.game.delete(self.start_again)

    # check click location
    def check_click_location(self, event):
        if self.run:
            score_numb = math.sqrt((event.x - self.target_x) ** 2 + (event.y - self.target_y) ** 2)
            if self.menu_target.get() == "Target Size 1":
                if score_numb > 25:
                    score_numb = 0
                else:
                    score_numb = round((25 - score_numb) * 4)
            if self.menu_target.get() == "Target Size 2":
                if score_numb > 35.5:
                    score_numb = 0
                else:
                    score_numb = round((35.5 - score_numb) * 2.816)
            if self.menu_target.get() == "Target Size 3":
                if score_numb > 50:
                    score_numb = 0
                else:
                    score_numb = round((50 - score_numb) * 2)
            if self.menu_target.get() == "Target Size 4":
                if score_numb > 62.5:
                    score_numb = 0
                else:
                    score_numb = round((62.5 - score_numb) * 1.6)
            if self.menu_target.get() == "Target Size 5":
                if score_numb > 75:
                    score_numb = 0
                else:
                    score_numb = round((75 - score_numb) * 1.333)

            # draw line (distance)
            self.dist_line = self.game.create_line(self.target_x, self.target_y, event.x, event.y, fill="blue")

            # show score
            self.score_text = self.game.create_text(self.root.winfo_width() / 2, self.root.winfo_height() / 2 - 30,
                                                    text="Score: " + str(score_numb) + "/100",
                                                    font=("", 40), anchor=CENTER)
            self.run = False
            sound = resource_path(path_sounds + "shot.wav")
            mixer.music.load(sound)
            mixer.music.play()
            self.start_again = self.game.create_image(self.root.winfo_width() / 2, self.root.winfo_height() / 2 + 30,
                                                      image=self.start_again_image)
        else:
            self.start()

    # call all function to run the program
    def call_func(self):
        self.images_and_menus() 
        self.change_target_size()
        self.root.bind("<Configure>", self.canvas_size)
        self.game.bind("<Button-1>", self.check_click_location)


# initiate game
if __name__ == '__main__':
    root = Tk()
    path_images = 'images/'
    path_sounds = 'sounds/'
    target = Target(root)
    target.call_func()
    root.mainloop()