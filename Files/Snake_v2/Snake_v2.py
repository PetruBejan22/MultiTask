from tkinter import *
import random
from pygame import mixer
from PIL import ImageTk, Image
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

path_images = 'Files/Snake_v2/images/'
path_sounds = 'Files/Snake_v2/sounds/'


class Snake_v2:
    def __init__(self, root):
        self.root = root
        mixer.init()
        self.root.title("Snake v2")
        self.root.maxsize(600, 650)
        self.root.minsize(600, 650)
        self.icon = resource_path(path_images + "snakev2_icon.ico")
        self.root.iconbitmap(self.icon)

        def help_snake():
            messagebox.showinfo("Snake v2", "Max Score is 35!\n"
                                         "Every time you make a point, the walls speed and snake's speed is increased")

        # menu bar
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)

        filemenu.add_command(label="About", command=help_snake)

        menubar.add_cascade(label="File", menu=filemenu)

        # coordonates for snake
        self.x1s = 300
        self.y1s = 300

        # coordonates for food
        self.random_food = [random.randint(2, 28), random.randint(2, 28)]
        self.x1f = 20 * self.random_food[0]
        self.y1f = 20 * self.random_food[1]

        # add to snake coordonate
        self.x_plus = 0
        self.y_plus = 0

        # the direction of snake
        self.up = False
        self.down = False
        self.right = False
        self.left = False

        # run the game
        self.run = True

        self.score = 0
        self.lives = 3

        # increase the speed of walls and snake
        self.walls_speed = 0

        # increase wall length
        self.rise = 0
        self.rise_up = True
        self.rise_down = False

        # I don't know what are these
        self.wall1 = 0
        self.wall2 = 0
        self.wall3 = 0
        self.wall4 = 0

        self.xpw = 0
        self.xp = 0

        self.start_ag = 0
        self.game_ov = 0

    def images(self):
        self.game = Canvas(self.root, width=600, height=600)
        self.game.pack()
        # background
        background_png = resource_path(path_images + "snakev2_background.png")
        self.background = ImageTk.PhotoImage(Image.open(background_png))
        self.game.create_image(0, 0, image=self.background)

        # start again
        start_again_png = resource_path(path_images + "start_again.png")
        self.start_again_image = ImageTk.PhotoImage(Image.open(start_again_png))

        # lives
        lives1_png = resource_path(path_images + "lives1.png")
        self.lives1_image = ImageTk.PhotoImage(Image.open(lives1_png))
        lives2_png = resource_path(path_images + "lives2.png")
        self.lives2_image = ImageTk.PhotoImage(Image.open(lives2_png))
        lives3_png = resource_path(path_images + "lives3.png")
        self.lives3_image = ImageTk.PhotoImage(Image.open(lives3_png))
        self.lives3 = self.game.create_image(53, 25, image=self.lives3_image)

        # snake image for up/down/right/left
        snaker_png = resource_path(path_images + "snake_right.png")
        self.snaker_image = ImageTk.PhotoImage(Image.open(snaker_png))
        snakel_png = resource_path(path_images + "snake_left.png")
        self.snakel_image = ImageTk.PhotoImage(Image.open(snakel_png))
        snakeu_png = resource_path(path_images + "snake_up.png")
        self.snakeu_image = ImageTk.PhotoImage(Image.open(snakeu_png))
        snaked_png = resource_path(path_images + "snake_down.png")
        self.snaked_image = ImageTk.PhotoImage(Image.open(snaked_png))

        # snake in game
        self.snake = self.game.create_image(self.x1s, self.y1s, image=self.snaker_image)

        # food image
        food_png = resource_path(path_images + "food.png")
        self.food_image = ImageTk.PhotoImage(Image.open(food_png))
        self.food = self.game.create_image(self.x1f, self.y1f, image=self.food_image)

        # pip image for up/down
        pip_up_png = resource_path(path_images + "pip_up.png")
        self.pip_up = ImageTk.PhotoImage(Image.open(pip_up_png))
        pip_down_png = resource_path(path_images + "pip_down.png")
        self.pip_down = ImageTk.PhotoImage(Image.open(pip_down_png))

        # game over image
        game_over_png = resource_path(path_images + "game_over.png")
        self.game_over = ImageTk.PhotoImage(Image.open(game_over_png))

        self.score_label = Label(self.root, text="Score: " + str(self.score), font=("", 20))
        self.score_label.pack()

        Label(bg='black').place(x=0, y=602, width=600, height=2)

    # snake movement
    def snake_move(self):
        if self.run:
            # new coordonates for snake
            self.x1 = self.x1s + self.x_plus
            self.y1 = self.y1s + self.y_plus

            if self.down:
                self.game.delete(self.snake)
                self.y_plus += 2
                self.snake = self.game.create_image(self.x1, self.y1, image=self.snaked_image)

            if self.right:
                self.game.delete(self.snake)
                self.x_plus += 2
                self.snake = self.game.create_image(self.x1, self.y1, image=self.snaker_image)

            if self.left:
                self.game.delete(self.snake)
                self.x_plus -= 2
                self.snake = self.game.create_image(self.x1, self.y1, image=self.snakel_image)

            if self.up:
                self.game.delete(self.snake)
                self.y_plus -= 2
                self.snake = self.game.create_image(self.x1, self.y1, image=self.snakeu_image)

            # stop snake movement if is max right or min left
            if self.x1 >= 589:
                self.right = False
            elif self.x1 <= 11:
                self.left = False

        self.root.after(36 - self.walls_speed, self.snake_move)

    # collision with food
    def impact_food(self):
        try:
            for x in range(15, 0, -1):
                if (self.x1 + x == self.x1f and self.y1 == self.y1f) or \
                        (self.x1 == self.x1f and self.y1 + x == self.y1f) or \
                        (self.x1 + x == self.x1f and self.y1 + x == self.y1f) or \
                        (self.x1 - x == self.x1f and self.y1 == self.y1f) or \
                        (self.x1 == self.x1f and self.y1 - x == self.y1f) or \
                        (self.x1 - x == self.x1f and self.y1 - x == self.y1f):
                    self.game.delete(self.food)
                    self.random_food = [random.randint(2, 28), random.randint(2, 28)]
                    self.x1f = 20 * self.random_food[0]
                    self.y1f = 20 * self.random_food[1]
                    self.x2f = 20 * (self.random_food[0] + 1)
                    self.y2f = 20 * (self.random_food[1] + 1)
                    self.food = self.game.create_image(self.x1f, self.y1f, image=self.food_image)
                    self.walls_speed += 1
                    self.score += 1
                    self.eat_sound = resource_path(path_sounds + "eat.mp3")
                    mixer.music.load(self.eat_sound)
                    mixer.music.play()
                    if self.score == 35:
                        self.score_label.config(text="Congratulations!!!   Best Score: " + str(self.score))
                        self.run = False
                        self.game_ov = self.game.create_image(300, 300, image=self.game_over)
                        self.start_ag = self.game.create_image(300, 400, image=self.start_again_image)
                    else:
                        self.score_label.config(text="Score: " + str(self.score))
        except:
            pass

    # reset position
    def reset_pos(self):
        self.game.delete(self.snake)
        self.snake = self.game.create_image(300, 300, image=self.snaker_image)
        self.x_plus = 0
        self.y_plus = 0
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.hit_sound = resource_path(path_sounds + "hit.wav")
        mixer.music.load(self.hit_sound)
        mixer.music.play()

        if self.lives == 2:
            self.game.delete(self.lives3)
            self.lives2 = self.game.create_image(39, 25, image=self.lives2_image)
        elif self.lives == 1:
            self.game.delete(self.lives2)
            self.lives1 = self.game.create_image(25, 25, image=self.lives1_image)
        elif self.lives == 0:
            self.game.delete(self.lives1)
            self.run = False
            self.game_ov = self.game.create_image(300, 300, image=self.game_over)
            self.start_ag = self.game.create_image(300, 400, image=self.start_again_image)

    # colission with walls
    def impact_walls(self):
        try:
            # colission with up and down wall
            if self.y1 >= 589 or self.y1 <= 11:
                self.lives -= 1
                self.reset_pos()

            # colission with moving wallls
            for x in range(15, 0, -1):
                # wall 1 up
                if (self.x1 + x == self.x1w and self.y1 <= self.y1w + 115) or \
                        (self.x1 == self.x1w + x and self.y1 <= self.y1w + 115):
                    self.lives -= 1
                    self.reset_pos()
                # wall 1 down
                if (self.x1 + x == self.x1w2 and self.y1 >= self.y1w2 - 115) or \
                        (self.x1 == self.x1w2 + x and self.y1 >= self.y1w2 - 115):
                    self.lives -= 1
                    self.reset_pos()
                # wall 2 up
                if (self.x1 + x == self.x1w3 and self.y1 <= self.y1w3 + 115) or \
                        (self.x1 == self.x1w3 + x and self.y1 <= self.y1w3 + 115):
                    self.lives -= 1
                    self.reset_pos()
                # wall 2 down
                if (self.x1 + x == self.x1w4 and self.y1 >= self.y1w4 - 115) or \
                        (self.x1 == self.x1w4 + x and self.y1 >= self.y1w4 - 115):
                    self.lives -= 1
                    self.reset_pos()
        except:
            pass

    # moving walls
    def walls(self):
        if self.run:
            # wall 1 up
            self.game.delete(self.wall1)
            self.x1w = 600 - self.xp
            self.y1w = -20 + self.rise
            self.wall1 = self.game.create_image(self.x1w, self.y1w, image=self.pip_up)

            # wall 1 down
            self.game.delete(self.wall2)
            self.x1w2 = 600 - self.xp
            self.y1w2 = 620 - self.rise
            self.wall2 = self.game.create_image(self.x1w2, self.y1w2, image=self.pip_down)

            # decrease wall1 x coord
            self.xp += 2

            # start over if x coord is 0
            if self.x1w2 == 0:
                self.xp = 0

            # wall2 up
            self.game.delete(self.wall3)
            self.x1w3 = 900 - self.xpw
            self.y1w3 = 110 - self.rise
            self.wall3 = self.game.create_image(self.x1w3, self.y1w3, image=self.pip_up)

            # wall2 down
            self.game.delete(self.wall4)
            self.x1w4 = 900 - self.xpw
            self.y1w4 = 490 + self.rise
            self.wall4 = self.game.create_image(self.x1w4, self.y1w4, image=self.pip_down)

            # decrease wall2 x coord
            self.xpw += 2

            # start over if x coord is 0
            if self.x1w3 == 0:
                self.xpw = 300

            # increase and decrease walls length
            if self.rise_down:
                self.rise += 2
                if self.y1w == 110:
                    self.rise_down = False
                    self.rise_up = True

            if self.rise_up:
                self.rise -= 2
                if self.y1w == -20:
                    self.rise_up = False
                    self.rise_down = True

            self.impact_walls()
            self.impact_food()
        self.root.after(40 - self.walls_speed, self.walls)

    # start again
    def start_again(self):
        self.run = True
        self.game.delete(self.snake)
        self.game.delete(self.lives1)
        self.game.delete(self.start_ag)
        self.game.delete(self.game_ov)
        self.snake = self.game.create_image(300, 300, image=self.snaker_image)
        self.lives3 = self.game.create_image(53, 25, image=self.lives3_image)
        self.walls_speed = 0
        self.xp = 0
        self.xpw = 0
        self.score = 0
        self.score_label.config(text="Score: " + str(self.score))
        self.lives = 3
        self.x_plus = 0
        self.y_plus = 0
        self.left = False
        self.right = False
        self.up = False
        self.down = False

    # pressed keys actions
    def keys_event(self, event):
        if str(event.keycode) == "37":  # key Left
            self.left = True
            self.up = False
            self.down = False
            self.right = False

        if str(event.keycode) == "39":  # key Right
            self.left = False
            self.right = True
            self.up = False
            self.down = False

        if str(event.keycode) == "38":  # key Up
            self.down = False
            self.up = True
            self.right = False
            self.left = False

        if str(event.keycode) == "40":  # key Down
            self.down = True
            self.up = False
            self.right = False
            self.left = False

        if not self.run:
            if event.keycode:
                self.start_again()

    def run_func(self):
        self.images()
        self.snake_move()
        self.walls()
        self.root.bind("<Key>", self.keys_event)


# start game
if __name__ == '__main__':
    root = Tk()
    path_images = 'images/'
    path_sounds = 'sounds/'
    snake = Snake_v2(root)
    snake.run_func()
    root.mainloop()
