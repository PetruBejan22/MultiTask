from tkinter import *
import random
from pygame import mixer
from PIL import ImageTk, Image
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, worwidgetsks for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

path_images = 'Files/FlappyBird/images/'
path_sounds = 'Files/FlappyBird/sounds/'


class FlappyBird:
    def __init__(self, root):
        self.root = root
        # coordonates for bird
        self.x_bird = 300
        self.y_bird = 300
        self.root.title("Flappy Bird")
        self.root.maxsize(600, 650)
        self.root.minsize(600, 650)

        # icon
        self.icon = resource_path(path_images + "flappybird_icon.ico")
        self.root.iconbitmap(self.icon)
        mixer.init()

        # the direction of bird
        self.up = False

        # run the game
        self.run = True

        # score 
        self.score = 0
        self.best_score = 0
        self.last_score = 0

        self.up_coord = 5
        self.game = Canvas(self.root, width=600, height=598)
        self.game.pack()

        # walls coordonates
        self.xw1 = 0
        self.xw2 = 0
        self.xw3 = 0
        self.xw4 = 0

        # walls
        self.wall1_up = 0
        self.wall1_down = 0
        self.wall2_up = 0
        self.wall2_down = 0
        self.wall3_up = 0
        self.wall3_down = 0
        self.wall4_up = 0
        self.wall4_down = 0
        self.w1_c = -150 + random.randint(0, 300)
        self.w2_c = -150 + random.randint(0, 300)
        self.w3_c = -150 + random.randint(0, 300)
        self.w4_c = -150 + random.randint(0, 300)

    def images(self):
        # background
        background_png = resource_path(path_images + "flappybird_background.png")
        self.background = ImageTk.PhotoImage(Image.open(background_png))
        self.game.create_image(0, 0, image=self.background)
        
        # bird image
        bird_png = resource_path(path_images + "flappybird_png.png")
        self.bird_img = ImageTk.PhotoImage(Image.open(bird_png))

        # bird in game
        self.bird = self.game.create_image(self.x_bird, self.y_bird, image=self.bird_img)

        # pip image for up/down
        pip_up_png = resource_path(path_images + "pip_up.png")
        self.pip_up = ImageTk.PhotoImage(Image.open(pip_up_png))
        pip_down_png = resource_path(path_images + "pip_down.png")
        self.pip_down = ImageTk.PhotoImage(Image.open(pip_down_png))

        # game over image
        game_over_png = resource_path(path_images + "game_over.png")
        self.game_over = ImageTk.PhotoImage(Image.open(game_over_png))

        # start again image
        start_again_png = resource_path(path_images + "start_again.png")
        self.start_again_image = ImageTk.PhotoImage(Image.open(start_again_png))

        self.score_label = Label(self.root, text='Best Score: {}         Score: {}         Last Score: {}'.format(self.best_score, self.score, self.last_score), 
                                font=("", 20))
        self.score_label.place(x=0, y=605)
        Label(bg='black').place(x=0, y=600, width=600, height=2)      

    def bird_move(self):
        if self.up and self.run:
            self.game.delete(self.bird)
            self.y_bird -= (4 * self.up_coord)
            self.up_coord -= 1
            self.bird = self.game.create_image(self.x_bird, self.y_bird, image=self.bird_img)
            if self.up_coord == 0:
                self.up = False
        else:
            self.game.delete(self.bird)
            self.y_bird += 6
            self.bird = self.game.create_image(self.x_bird, self.y_bird, image=self.bird_img)

        self.root.after(50, self.bird_move)    

    def sounds(self, sound):
        mixer.music.load(sound)
        mixer.music.play()

    # game over screen
    def hit_wall(self):
        hit_sound = resource_path(path_sounds + "hit.wav")
        self.run = False
        self.game_ov = self.game.create_image(300, 300, image=self.game_over)
        self.start_ag = self.game.create_image(300, 400, image=self.start_again_image)
        self.sounds(hit_sound)

    # colission with walls
    def impact_walls(self):
        try:
            # colission with up and down wall
            if self.y_bird >= 585 or self.y_bird <= 15:
                self.hit_wall()
            # colission with moving wallls
            for x in range(20, 0, -1):
                # wall 1 up
                if (self.x_bird + x == self.xw1_up or self.x_bird - x == self.xw1_up) and \
                        self.y_bird <= self.yw1_up + 270:
                    self.hit_wall()
                # wall 1 down
                if (self.x_bird + x == self.xw1_down or self.x_bird - x == self.xw1_up) and \
                        self.y_bird >= self.yw1_down - 270:
                    self.hit_wall()
                # wall 2 up
                if (self.x_bird + x == self.xw2_up or self.x_bird - x == self.xw2_up) and \
                        self.y_bird <= self.yw2_up + 270:
                    self.hit_wall()
                # wall 2 down
                if (self.x_bird + x == self.xw2_down or self.x_bird - x == self.xw2_up) and \
                        self.y_bird >= self.yw2_down - 270:
                    self.hit_wall()
                # wall 3 up
                if (self.x_bird + x == self.xw3_up or self.x_bird - x == self.xw3_up) and \
                        self.y_bird <= self.yw3_up + 270:
                    self.hit_wall()
                # wall 3 down
                if (self.x_bird + x == self.xw3_down or self.x_bird - x == self.xw3_up) and \
                        self.y_bird >= self.yw3_down - 270:
                    self.hit_wall()
                # wall 4 up
                if (self.x_bird + x == self.xw4_up or self.x_bird - x == self.xw4_up) and \
                        self.y_bird <= self.yw4_up + 270:
                    self.hit_wall()
                # wall 3 down
                if (self.x_bird + x == self.xw4_down or self.x_bird - x == self.xw4_up) and \
                        self.y_bird >= self.yw4_down - 270:
                    self.hit_wall()
        except:
            pass

    # moving walls
    def walls(self):
        if self.run:
            # wall 1 up
            self.game.delete(self.wall1_up)
            self.xw1_up = 610 - self.xw1
            self.yw1_up = self.w1_c
            self.wall1_up = self.game.create_image(self.xw1_up, self.yw1_up, image=self.pip_up)

            # wall 1 down
            self.game.delete(self.wall1_down)
            self.xw1_down = 610 - self.xw1
            self.yw1_down = 660 + self.w1_c
            self.wall1_down = self.game.create_image(self.xw1_down, self.yw1_down, image=self.pip_down)

            # decrease wall1 x coord
            self.xw1 += 2

            # start over if x coord is 0
            if self.xw1_up + 10 == 0:
                self.xw1 = 0
                self.w1_c = -150 + random.randint(0, 300)

            # wall 2 up
            self.game.delete(self.wall2_up)
            self.xw2_up = 760 - self.xw2
            self.yw2_up = self.w2_c
            self.wall2_up = self.game.create_image(self.xw2_up, self.yw2_up, image=self.pip_up)

            # wall 2 down
            self.game.delete(self.wall2_down)
            self.xw2_down = 760 - self.xw2
            self.yw2_down = 660 + self.w2_c
            self.wall2_down = self.game.create_image(self.xw2_down, self.yw2_down, image=self.pip_down)

            # decrease wall2 x coord
            self.xw2 += 2

            # start over if x coord is 0
            if self.xw2_up + 10 == 0:
                self.xw2 = 150
                self.w2_c = -150 + random.randint(0, 300)

            # wall 3 up
            self.game.delete(self.wall3_up)
            self.xw3_up = 910 - self.xw3
            self.yw3_up = self.w3_c
            self.wall3_up = self.game.create_image(self.xw3_up, self.yw3_up, image=self.pip_up)

            # wall 3 down
            self.game.delete(self.wall3_down)
            self.xw3_down = 910 - self.xw3
            self.yw3_down = 660 + self.w3_c
            self.wall3_down = self.game.create_image(self.xw3_down, self.yw3_down, image=self.pip_down)

            # decrease wall3 x coord
            self.xw3 += 2

            # start over if x coord is 0
            if self.xw3_up + 10 == 0:
                self.xw3 = 300
                self.w3_c = -150 + random.randint(0, 300)

            # wall 4 up
            self.game.delete(self.wall4_up)
            self.xw4_up = 1060 - self.xw4
            self.yw4_up = self.w4_c
            self.wall4_up = self.game.create_image(self.xw4_up, self.yw4_up, image=self.pip_up)

            # wall 4 down
            self.game.delete(self.wall4_down)
            self.xw4_down = 1060 - self.xw4
            self.yw4_down = 660 + self.w4_c
            self.wall4_down = self.game.create_image(self.xw4_down, self.yw4_down, image=self.pip_down)

            # decrease wall4 x coord
            self.xw4 += 2

            # start over if x coord is 0
            if self.xw4_up + 10 == 0:
                self.xw4 = 450
                self.w4_c = -150 + random.randint(0, 300)

            self.update_score()
            self.impact_walls()

        self.root.after(40, self.walls)

    # update score
    def update_score(self):
        if self.x_bird == self.xw1_up or self.x_bird == self.xw2_up or \
                self.x_bird == self.xw3_up or self.x_bird == self.xw4_up:
            self.score += 1
            self.score_label.config(text="Best Score: {}         Score: {}         Last Score: {}".format(self.best_score, self.score, self.last_score))
            self.point_sound = resource_path(path_sounds + "point.wav") 
            self.sounds(self.point_sound)      

    # reset game
    def start_again(self):
        self.run = True
        self.last_score = self.score
        if self.score > self.best_score:
            self.best_score = self.score 
        self.score = 0 
        self.score_label.config(text="Best Score: {}         Score: {}         Last Score: {}".format(self.best_score, self.score, self.last_score))
        self.x_bird = 300
        self.y_bird = 300
        self.xw1 = 0
        self.xw2 = 0
        self.xw3 = 0
        self.xw4 = 0
        self.game.delete(self.game_ov)
        self.game.delete(self.start_ag)

    # pressed keys actions
    def keys_event(self, event):
        if str(event.keycode) == "38":  # key Up
            self.up = True
            self.up_coord = 5
        if not self.run:
            if event.keycode:
                self.start_again()

    def main(self):
        self.images()
        self.walls()
        self.bird_move()
        self.root.bind("<Key>", self.keys_event)


# start game
if __name__ == '__main__':
    root = Tk()
    path_images = 'images/'
    path_sounds = 'sounds/'
    flappy = FlappyBird(root)
    flappy.main()
    root.mainloop()
