from tkinter import Tk, Canvas, Button, Label
from PIL import ImageTk, Image
from random import randrange, sample
from os import path
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception as e:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)

path_images = 'Files/Snake/images/'   


class Snake:
	def __init__(self, root, canvas, right_snake, left_snake):
		self.images()
		self.root = root
		self.game = canvas  

		self.right_snake = right_snake
		self.left_snake = left_snake
		self.up_snake= 0
		self.down_snake = 0

		self.run = True

	def images(self):
		snake_head_up1 = resource_path(path_images + 'snake_head_up.png')
		self.snake_head_up = ImageTk.PhotoImage(Image.open(snake_head_up1))

		snake_head_down1 = resource_path(path_images + 'snake_head_down.png')
		self.snake_head_down = ImageTk.PhotoImage(Image.open(snake_head_down1))

		snake_head_left1 = resource_path(path_images + 'snake_head_left.png')
		self.snake_head_left = ImageTk.PhotoImage(Image.open(snake_head_left1))

		snake_head_right1 = resource_path(path_images + 'snake_head_right.png')
		self.snake_head_right = ImageTk.PhotoImage(Image.open(snake_head_right1))

		snake_tail_down1 = resource_path(path_images + 'snake_tail_down.png')
		self.snake_tail_down = ImageTk.PhotoImage(Image.open(snake_tail_down1))

		snake_tail_up1 = resource_path(path_images + 'snake_tail_up.png')
		self.snake_tail_up = ImageTk.PhotoImage(Image.open(snake_tail_up1))

		snake_tail_right1 = resource_path(path_images + 'snake_tail_right.png')
		self.snake_tail_right = ImageTk.PhotoImage(Image.open(snake_tail_right1))

		snake_tail_left1 = resource_path(path_images + 'snake_tail_left.png')
		self.snake_tail_left = ImageTk.PhotoImage(Image.open(snake_tail_left1))

		snake_corner_NW1 = resource_path(path_images + 'snake_corner_NW.png')
		self.snake_corner_NW = ImageTk.PhotoImage(Image.open(snake_corner_NW1))

		snake_corner_NE1 = resource_path(path_images + 'snake_corner_NE.png')
		self.snake_corner_NE = ImageTk.PhotoImage(Image.open(snake_corner_NE1))

		snake_corner_SW1 = resource_path(path_images + 'snake_corner_SW.png')
		self.snake_corner_SW = ImageTk.PhotoImage(Image.open(snake_corner_SW1))

		snake_corner_SE1 = resource_path(path_images + 'snake_corner_SE.png')
		self.snake_corner_SE = ImageTk.PhotoImage(Image.open(snake_corner_SE1))

		snake_body_horizontal1 = resource_path(path_images + 'snake_body_horizontal.png')
		self.snake_body_horizontal = ImageTk.PhotoImage(Image.open(snake_body_horizontal1))

		snake_body_vertical1 = resource_path(path_images + 'snake_body_vertical.png')
		self.snake_body_vertical = ImageTk.PhotoImage(Image.open(snake_body_vertical1))

	# snake head
	def snake_head(self):
		previous_x_snake = self.x_snake
		previous_y_snake = self.y_snake	

		self.x_snake += self.left_snake + self.right_snake
		self.y_snake += self.up_snake + self.down_snake

		self.snake_length[-1] = [self.x_snake, self.y_snake]  	# snake head

		# game over if snake head hit snake body or hit the walls
		for x in self.snake_length[:-1]:
			if self.snake_length[-1] == x:
				self.run = False
		if self.x_snake <= 10 or self.x_snake >= 590 or self.y_snake <= 10 or self.y_snake >= 590:
			self.run = False	

		# change image based on player input
		image_head=self.snake_head_right
		if self.x_snake > previous_x_snake:
			image_head = self.snake_head_right
		elif self.x_snake < previous_x_snake:
			image_head = self.snake_head_left
		elif self.y_snake > previous_y_snake:
			image_head = self.snake_head_down
		elif self.y_snake < previous_y_snake:
			image_head = self.snake_head_up	
		
		previous_x_snake = self.x_snake
		previous_y_snake = self.y_snake			

		self.game.create_image(self.snake_length[-1][0], self.snake_length[-1][1], image=image_head)

	# Snake tail
	def snake_tail(self):
		snake_tail = self.snake_tail_left		
		if self.snake_length[0][0] < self.snake_length[1][0]:
			snake_tail = self.snake_tail_right
		elif self.snake_length[0][0] > self.snake_length[1][0]:
			snake_tail = self.snake_tail_left
		elif self.snake_length[0][1] > self.snake_length[1][1]:
			snake_tail = self.snake_tail_up
		elif self.snake_length[0][1] < self.snake_length[1][1]:
			snake_tail = self.snake_tail_down	
		
		self.game.create_image(self.snake_length[0][0], self.snake_length[0][1], image=snake_tail)

	# Snake body
	def snake_body(self):
		image_body = self.snake_body_horizontal
		for num, (x, y) in enumerate(self.snake_length[1:-1], 1):
			# Corners clockwise
			if x < self.snake_length[num+1][0] and y < self.snake_length[num-1][1]:     # NW
				image_body = self.snake_corner_NW
			elif x > self.snake_length[num-1][0] and y < self.snake_length[num+1][1]:  # NE
				image_body = self.snake_corner_NE
			elif x > self.snake_length[num+1][0] and y > self.snake_length[num-1][1]:  # SE
				image_body = self.snake_corner_SE
			elif x < self.snake_length[num-1][0] and y > self.snake_length[num+1][1]:  # SW
				image_body = self.snake_corner_SW

			# Corners reverse clockwise
			elif x < self.snake_length[num-1][0] and y < self.snake_length[num+1][1]:     # NW
				image_body = self.snake_corner_NW
			elif x > self.snake_length[num+1][0] and y < self.snake_length[num-1][1]:  # NE
				image_body = self.snake_corner_NE
			elif x > self.snake_length[num-1][0] and y > self.snake_length[num+1][1]:  # SE
				image_body = self.snake_corner_SE
			elif x < self.snake_length[num+1][0] and y > self.snake_length[num-1][1]:  # SW
				image_body = self.snake_corner_SW

			elif x == self.snake_length[num-1][0] and x == self.snake_length[num+1][0]:  # vertical
				image_body = self.snake_body_vertical
			elif y == self.snake_length[num-1][1] and y == self.snake_length[num+1][1]:  # horizontal
				image_body = self.snake_body_horizontal	 			
					
			self.game.create_image(x, y, image=image_body)
	

class Snake_Game:
	def __init__(self, root):
		self.root = root
		self.root.geometry('600x620')
		self.root.resizable(False, False)
		self.root.title('Snake')

		# icon
		self.icon = resource_path(path_images + 'snake_icon.ico')
		self.root.iconbitmap(self.icon)

		self.game = Canvas(self.root, width=600, height=600, bg='white')
		self.game.place(x=-1, y=20)
		self.run = False

		self.snake_speed = 350

		self.game_time = 0

		self.one_player_button = Button(self.root, text='1  Player', font=('', 30, 'bold'), command=self.one_player)
		self.one_player_button.place(x=200, y=250, width=200, height=60)
		self.two_players_button = Button(self.root, text='2  Players', font=('', 30, 'bold'), command=self.two_players)
		self.two_players_button.place(x=200, y=350, width=200, height=60)

		self.menu = Button(self.root, text='Menu', font=('', 20, 'bold'), command=self.return_start)

		game_over1 = resource_path(path_images + 'game_over.png')
		self.game_over_image = ImageTk.PhotoImage(Image.open(game_over1))

		mushroom1 = resource_path(path_images + 'mushroom.png')
		self.mushroom = ImageTk.PhotoImage(Image.open(mushroom1))

		# background
		background1 = resource_path(path_images + 'background_snake.png')
		self.background = ImageTk.PhotoImage(Image.open(background1))

		# Food
		food1 = resource_path(path_images + 'food.png')
		self.food_image = ImageTk.PhotoImage(Image.open(food1))

		wall1 = resource_path(path_images + 'brickwall.png')
		self.wall = ImageTk.PhotoImage(Image.open(wall1))

		wall2 = resource_path(path_images + 'brick-wall.png')
		self.wall2 = ImageTk.PhotoImage(Image.open(wall2))
		self.game_map()
		self.text_game_mode = self.game.create_text(300, 150, text='Select game mode!', font=('', 35, 'bold'))

	# start game
	def start_game(self, event):
		self.run = True

	def one_player(self):
		self.root.bind('<Return>', self.start_game)
		self.game.delete(self.text_game_mode)
		self.game.create_text(250, 115, text='Controls: Player 1\n← - Left\n→ - Right\n↑ - Up\n↓ - Down', font=('20'))
		self.speed_text = self.game.create_text(235, 190, text='Insert - Speed', font=('20'))
		self.game.create_text(300, 310, text='Press <Enter> to start!', font=('', 30, 'bold'))
		self.one_player_mode = True
		self.two_players_mode = False
		self.game_time = 0

		self.player_one = Snake(self.root, self.game, 20, 0)
		self.player_two = Snake(self.root, self.game, 0, -20)

		self.player_one.snake_length = [[70, 70], [90, 70], [90, 70]]
		self.game.create_image(70, 70, image=self.player_one.snake_tail_right)
		self.game.create_image(90, 70, image=self.player_one.snake_body_horizontal)
		self.game.create_image(110, 70, image=self.player_one.snake_head_right)

		self.player_one.x_snake = 90
		self.player_one.y_snake = 70	

		self.player_two.x_snake = 510
		self.player_two.y_snake = 530
		self.player_two.snake_length = [[530, 530], [510, 530], [510, 530]]

		self.root.bind("<Key>", self.key_event)
		self.root.bind('<KeyPress-Insert>', self.snake_fast)    		# Hold Insert to gain speed
		self.root.bind('<KeyRelease-Insert>', self.snake_normal)	  	# Release Insert to get speed back to normal

		self.x_food = randrange(30, 590, 20)
		self.y_food = randrange(30, 590, 20)

		self.x1_mushroom, self.x2_mushroom = sample(list(range(30, 590, 20)), 2)
		self.y1_mushroom, self.y2_mushroom = sample(list(range(30, 590, 20)), 2)

		self.player1_score = 0
		self.player1_score_label  = Label(self.root, text='Player 1 Score : {}'.format(self.player1_score), font=('', 11))
		self.player1_score_label.place(x=5, y=0, height=20)

		self.time_label = Label(self.root, text="", font=('', 11, 'bold'))

		self.player2_score = 0
		self.player2_score_label  = Label(self.root, text='Player 2 Score : {}'.format(self.player2_score), font=('', 11))

		self.one_player_button.place_forget()
		self.two_players_button.place_forget()

	def two_players(self):
		self.one_player()
		self.root.unbind('<KeyPress-Insert>')
		self.root.unbind('<KeyRelease-Insert>')
		self.game.delete(self.speed_text)
		self.game.create_text(370, 485, text='Controls: Player 2\nA - Left\nD - Right\nW - Up\nS - Down', font=('20'))
		self.one_player_mode = False
		self.two_players_mode = True

		self.player2_score_label.place(x=470, y=0, height=20)

		self.random_mushrooms()

		# create Player 2 snake
		self.game.create_image(530, 530, image=self.player_two.snake_tail_left)
		self.game.create_image(510, 530, image=self.player_two.snake_body_horizontal)
		self.game.create_image(490, 530, image=self.player_two.snake_head_left)

	# Food
	def	food(self):
		if self.player_one.x_snake == self.x_food and self.player_one.y_snake == self.y_food:
			self.player_one.snake_length.insert(0, self.player_one.snake_length[0])     #  put snake tail one block behind
			if self.one_player_mode:
				self.player1_score += 1
			else:
				self.player1_score += 3	
				self.mushrooms()
				self.x1_mushroom, self.x2_mushroom = sample(list(range(30, 590, 20)), 2)
				self.y1_mushroom, self.y2_mushroom = sample(list(range(30, 590, 20)), 2)
			self.player1_score_label.config(text='Player 1 Score : {}'.format(self.player1_score))
			self.x_food = randrange(30, 590, 20)
			self.y_food = randrange(30, 590, 20)
			
			
			self.game.create_image(self.x_food, self.y_food, image=self.food_image)	
		elif self.player_two.x_snake == self.x_food and self.player_two.y_snake == self.y_food:
			self.player_two.snake_length.insert(0, self.player_two.snake_length[0])     #  put snake tail one block behind
			self.player2_score += 3
			self.player2_score_label.config(text='Player 2 Score : {}'.format(self.player2_score))
			self.x_food = randrange(30, 590, 20)
			self.y_food = randrange(30, 590, 20)
			self.x1_mushroom, self.x2_mushroom = sample(list(range(30, 590, 20)), 2)
			self.y1_mushroom, self.y2_mushroom = sample(list(range(30, 590, 20)), 2)
			self.mushrooms()
			self.game.create_image(self.x_food, self.y_food, image=self.food_image)
		else:	
			self.game.create_image(self.x_food, self.y_food, image=self.food_image)
			if self.two_players_mode:
				self.mushrooms()	

	# Mushrooms
	def	mushrooms(self):
		if (self.player_one.x_snake == self.x1_mushroom and self.player_one.y_snake == self.y1_mushroom) or\
		   (self.player_one.x_snake == self.x2_mushroom and self.player_one.y_snake == self.y2_mushroom):
			self.x1_mushroom, self.x2_mushroom = sample(list(range(30, 590, 20)), 2)
			self.y1_mushroom, self.y2_mushroom = sample(list(range(30, 590, 20)), 2)
			self.game.create_image(self.x1_mushroom, self.y1_mushroom, image=self.mushroom)
			self.game.create_image(self.x2_mushroom, self.y2_mushroom, image=self.mushroom)
			self.player1_score += 1
			self.player1_score_label.config(text='Player 1 Score : {}'.format(self.player1_score))
		elif(self.player_two.x_snake == self.x1_mushroom and self.player_two.y_snake == self.y1_mushroom) or\
			(self.player_two.x_snake == self.x2_mushroom and self.player_two.y_snake == self.y2_mushroom):
			self.x1_mushroom, self.x2_mushroom = sample(list(range(30, 590, 20)), 2)
			self.y1_mushroom, self.y2_mushroom = sample(list(range(30, 590, 20)), 2)
			self.game.create_image(self.x1_mushroom, self.y1_mushroom, image=self.mushroom)
			self.game.create_image(self.x2_mushroom, self.y2_mushroom, image=self.mushroom)
			self.player2_score += 1
			self.player2_score_label.config(text='Player 2 Score : {}'.format(self.player2_score))
		else:
			if self.two_players_mode:
				self.game.create_image(self.x1_mushroom, self.y1_mushroom, image=self.mushroom)
				self.game.create_image(self.x2_mushroom, self.y2_mushroom, image=self.mushroom)			

	def key_event(self, event):
		if event.keysym == 'Left':
			if self.player_one.right_snake == 0:
				self.player_one.up_snake = self.player_one.down_snake = 0
				self.player_one.left_snake = -20
				
		elif event.keysym == 'Right':
			if self.player_one.left_snake == 0:
				self.player_one.up_snake = self.player_one.down_snake = 0
				self.player_one.right_snake = 20
				
		elif event.keysym == 'Up':
			if self.player_one.down_snake == 0:
				self.player_one.left_snake = self.player_one.right_snake = 0
				self.player_one.up_snake = -20

		elif event.keysym == 'Down':
			if self.player_one.up_snake == 0:
				self.player_one.left_snake = self.player_one.right_snake = 0
				self.player_one.down_snake = 20

		if event.keysym == 'a':
			if self.player_two.right_snake == 0:
				self.player_two.up_snake = self.player_two.down_snake = 0
				self.player_two.left_snake = -20
					
		elif event.keysym == 'd':
			if self.player_two.left_snake == 0:
				self.player_two.up_snake = self.player_two.down_snake = 0
				self.player_two.right_snake = 20
				
		elif event.keysym == 'w':
			if self.player_two.down_snake == 0:
				self.player_two.left_snake = self.player_two.right_snake = 0
				self.player_two.up_snake = -20

		elif event.keysym == 's':
			if self.player_two.up_snake == 0:
				self.player_two.left_snake = self.player_two.right_snake = 0
				self.player_two.down_snake = 20				

	# Squares and walls
	def game_map(self):
		self.game.create_image(400, 400, image=self.background)
		# create squares
		for x in range(20, 600, 20):
			self.game.create_line(x, 20, x, 580, fill='#9ABBBD')
			self.game.create_line(20, x, 580, x, fill='#9ABBBD')

		# create walls					 
		for x in range(11, 610, 20):
			self.game.create_image(x, 10, image=self.wall)
			self.game.create_image(x, 591, image=self.wall)
			self.game.create_image(10, x, image=self.wall)
			self.game.create_image(591, x, image=self.wall)

	# Middle walls collision
	def wall_collision(self):
		player = 0	
		for x in range(210, 410, 20):
			self.game.create_image(x, 110, image=self.wall2)
			self.game.create_image(x, 490, image=self.wall2)
			self.game.create_image(110, x, image=self.wall2)
			self.game.create_image(490, x, image=self.wall2)
			
			if self.player_one.x_snake == x and self.player_one.y_snake == 110 or\
			self.player_one.x_snake == x and self.player_one.y_snake == 490 or\
			self.player_one.x_snake == 110 and self.player_one.y_snake == x or\
			self.player_one.x_snake == 490 and self.player_one.y_snake == x:
				self.run = False
				player = 2
			
			if self.player_two.x_snake == x and self.player_two.y_snake == 110 or\
			self.player_two.x_snake == x and self.player_two.y_snake == 490 or\
			self.player_two.x_snake == 110 and self.player_two.y_snake == x or\
			self.player_two.x_snake == 490 and self.player_two.y_snake == x:
				self.run = False
				player = 1

		return player	

	def food_wall_collision(self):
		for x in range(210, 410, 20):
			if self.x_food == x and self.y_food == 110 or\
			self.x_food == x and self.y_food == 490 or\
			self.x_food == 110 and self.y_food == x or\
			self.x_food == 490 and self.y_food == x:
				self.x_food = randrange(30, 590, 20)
				self.y_food = randrange(30, 590, 20)
				self.food()

	def food_mushroom_collision(self):
		if self.x_food == self.x1_mushroom and self.y_food == self.y1_mushroom or\
		self.x_food == self.x2_mushroom and self.y_food == self.y2_mushroom:
			self.x_food = randrange(30, 590, 20)
			self.y_food = randrange(30, 590, 20)
			self.food()

	def mushroom_wall_collision(self):
		for x in range(210, 410, 20):
			if self.x1_mushroom == x and self.y1_mushroom == 110 or\
			self.x1_mushroom == x and self.y1_mushroom == 490 or\
			self.x1_mushroom == 110 and self.y1_mushroom == x or\
			self.x1_mushroom == 490 and self.y1_mushroom == x:
				self.x1_mushroom = randrange(30, 590, 20)
				self.y1_mushroom = randrange(30, 590, 20)
				self.mushrooms()

			if self.x2_mushroom == x and self.y2_mushroom == 110 or\
			self.x2_mushroom == x and self.y2_mushroom == 490 or\
			self.x2_mushroom == 110 and self.y2_mushroom == x or\
			self.x2_mushroom == 490 and self.y2_mushroom == x:
				self.x2_mushroom = randrange(30, 590, 20)
				self.y2_mushroom = randrange(30, 590, 20)
				self.mushrooms()

	# random mushrooms coordonates
	def random_mushrooms(self):	 
		self.x_m0, self.x_m1, self.x_m2, self.x_m3, self.x_m4, self.x_m5 = sample(list(range(30, 590, 20)), 6) 
		self.x_m6, self.x_m7, self.x_m8, self.x_m9, self.x_m10, self.x_m11 = sample(list(range(30, 590, 20)), 6)
		self.x_m12, self.x_m13, self.x_m14, self.x_m15, self.x_m16, self.x_m16, self.x_m17, self.x_m17 = sample(list(range(30, 590, 20)), 8)
		self.x_m18, self.x_m19, self.x_m20, self.x_m21, self.x_m22, self.x_m23, self.x_m24, self.x_m25 = sample(list(range(30, 590, 20)), 8)

		self.y_m0, self.y_m1, self.y_m2, self.y_m3, self.y_m4, self.y_m5 = sample(list(range(30, 590, 20)), 6)
		self.y_m6, self.y_m7, self.y_m8, self.y_m9, self.y_m10, self.y_m11 = sample(list(range(30, 590, 20)), 6)
		self.y_m12, self.y_m13, self.y_m14, self.y_m15, self.y_m16, self.y_m16, self.y_m17, self.y_m17 = sample(list(range(30, 590, 20)), 8)
		self.y_m18, self.y_m19, self.y_m20, self.y_m21, self.y_m22, self.y_m23, self.y_m24, self.y_m25 = sample(list(range(30, 590, 20)), 8)

		self.mushrooms_list = [[self.x_m0, self.y_m0], [self.x_m1, self.y_m1], [self.x_m2, self.y_m2], [self.x_m3, self.y_m3],
		[self.x_m4, self.y_m4],[self.x_m5, self.y_m5],[self.x_m6, self.y_m6],[self.x_m7, self.y_m7],[self.x_m8, self.y_m8],
		[self.x_m9, self.y_m9],[self.x_m10, self.y_m10],[self.x_m11, self.y_m11],[self.x_m12, self.y_m12],[self.x_m13, self.y_m13],
		[self.x_m14, self.y_m14],[self.x_m15, self.y_m15], [self.x_m16, self.y_m16],[self.x_m17, self.y_m17], [self.x_m18, self.y_m18],
		[self.x_m19, self.y_m19], [self.x_m20, self.y_m20],[self.x_m21, self.y_m21], [self.x_m22, self.y_m22],[self.x_m23, self.y_m23], [self.x_m24, self.y_m24],[self.x_m25, self.y_m25]]

	def event_mushrooms(self):
		for num, (x, y) in enumerate(self.mushrooms_list):
			if x == self.player_one.x_snake and y == self.player_one.y_snake:
				if num % 2 == 0:
					self.player1_score += 1
				else:	
					self.player1_score -= 1
				self.mushrooms_list[num] = [-20, -20]
				self.player1_score_label.config(text='Player 1 Score : {}'.format(self.player1_score))

			elif x == self.player_two.x_snake and y == self.player_two.y_snake:
				if num % 2 == 0:
					self.player2_score += 1
				else:	
					self.player2_score -= 1
				self.mushrooms_list[num] = [-20, -20]
				self.player2_score_label.config(text='Player 2 Score : {}'.format(self.player2_score))
			else:
				self.game.create_image(x, y, image=self.mushroom)					

	def events(self):
		player = 0
		start_event1 = 35 - round(self.game_time)
		if 5 >= start_event1 >= 0:
			self.game.create_text(300, 250, text='"Put your seatbelt!"\n  Event starting in: \n             {}'.format(start_event1), font=("", 25))

		if start_event1 <= 0 and round(self.game_time) <= 50:
			self.time_label.place(x=230, y=0)
			self.time_label.config(text='Event ending in: {}'.format(50-round(self.game_time)))
			self.snake_speed = 100
		else:
			self.snake_speed = 350

		start_event2 = 85 - round(self.game_time)
		if 5 >= start_event2 >= 0:
			self.game.create_text(300, 250, text='"Not all of them are good!"\n        Event starting in: \n                   {}'.format(start_event2), font=("", 25))

		if start_event2 <= 0 and round(self.game_time) <= 110:
			self.time_label.place(x=230, y=0)
			self.time_label.config(text='Event ending in: {}'.format(110-round(self.game_time)))
			self.event_mushrooms()

		if round(self.game_time) >= 35 and round(self.game_time) <= 50:
			pass
		elif round(self.game_time) >= 85 and round(self.game_time) <= 110:
			pass
		elif round(self.game_time) >= 130 and round(self.game_time) <= 160:
			self.time_label.place(x=230, y=0)
			self.time_label.config(text='Game ending in: {}'.format(160-round(self.game_time)))
		elif round(self.game_time) >= 160:
			self.run = False
			self.game_over()
			if self.player1_score > self.player2_score:
				player = 1
			elif self.player2_score > self.player1_score:	
				player = 2
			else:
				player = 'Even'		
		else:	
			self.time_label.config(text='')		
			self.time_label.place_forget()

		return player	

	def game_over(self):
		self.game_ov = self.game.create_image(300, 200, image=self.game_over_image)
		self.menu.place(x=250, y=350)
		self.time_label.config(text='')	
		self.time_label.place_forget()
		self.root.unbind('<Return>')

	def return_start(self):
		self.menu.place_forget()
		self.one_player_button.place(x=200, y=250, width=200, height=60)
		self.two_players_button.place(x=200, y=350, width=200, height=60)
		self.game.delete(self.winner)
		self.text_game_mode = self.game.create_text(300, 150, text='Select game mode!', font=('', 35, 'bold'))
		self.player1_score_label.config(text='')
		self.player2_score_label.config(text='')
		self.game.delete(self.game_ov)		

	def main(self):
		if self.run:
			self.game.delete('all')
			self.game_map()
			# 1 Player
			if self.one_player_mode:
				self.player_one.snake_head()
				self.player_one.snake_tail()
				self.player_one.snake_body()
				self.run = self.player_one.run
				self.food()			
				self.player_one.snake_length[0] = self.player_one.snake_length[1]

				for num, _ in enumerate(self.player_one.snake_length[1:-1], 1):	
					self.player_one.snake_length[num] =  self.player_one.snake_length[num+1]

				if not self.run:
					self.game_over()
					self.winner = self.game.create_text(300, 280, text='Score: {}'.format(self.player1_score), font=('', 30, 'bold'))
	
			# 2 Players
			elif self.two_players_mode:
				# Player 1 initiate
				self.player_one.snake_head()
				self.player_one.snake_tail()
				self.player_one.snake_body()
				run_player1 = self.player_one.run

				# Player 2 initiate
				self.player_two.snake_head()
				self.player_two.snake_tail()
				self.player_two.snake_body()
				run_player2 = self.player_two.run

				self.wall_collision()
				self.food_wall_collision()
				self.food_mushroom_collision()
				self.mushroom_wall_collision()
				
				if not run_player1:
					player = 2
					self.run = False
				elif not run_player2:	
					player = 1
					self.run = False

				if self.wall_collision() != 0:
					player = self.wall_collision() 

				# Player 1 collision with food
				self.food()	
				
				self.player_one.snake_length[0] = self.player_one.snake_length[1]

				for num, _ in enumerate(self.player_one.snake_length[1:-1], 1):	
					self.player_one.snake_length[num] =  self.player_one.snake_length[num+1]

				# collision with himself
				for x, y in self.player_one.snake_length:
					if self.player_two.x_snake == x and self.player_two.y_snake == y:
						self.run = False
						player = 1	

				# Player 2 collision with food
				self.player_two.snake_length[0] = self.player_two.snake_length[1]

				for num, _ in enumerate(self.player_two.snake_length[1:-1], 1):	
					self.player_two.snake_length[num] =  self.player_two.snake_length[num+1]

				# collision with himself
				for x, y in self.player_two.snake_length:
					if self.player_one.x_snake == x and self.player_one.y_snake == y:
						self.run = False
						player = 2

				if self.events() != 0:
					player = self.events() 				

				if not self.run:
					self.game_over()
					self.winner = self.game.create_text(300, 280, text='Player {} wins!'.format(player), font=('', 30, 'bold'))	

				if self.snake_speed == 100:
					self.game_time += 0.1
				else:	
					self.game_time += 0.350	

		self.root.after(self.snake_speed, self.main)

	# Snake speed fast
	def snake_fast(self, event):	
		self.snake_speed = 100

	# Snake speed normal
	def snake_normal(self, event):		
		self.snake_speed = 350											

if __name__ == '__main__':
	root = Tk()
	path_images = 'images/'
	snake = Snake_Game(root)
	snake.main()
	root.mainloop()							
