from tkinter import *
from tkinter import messagebox
import random
from pygame import mixer 
from PIL import ImageTk, Image
import os
import sys
from PIL import ImageTk
from random import randint
from playsound import playsound

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

path_images = 'Files/DiceGame/images/'
path_sounds = 'Files/DiceGame/sounds/'


class DiceGame:
	def __init__(self, root):
		self.root = root
		self.root.title('Dice Game')
		self.root.geometry('1000x500')
		self.root.resizable(0, 0)
		mixer.init()

		icon = resource_path(path_images + 'icon.ico')
		self.root.iconbitmap(icon)

		self.player1 = True

		self.score_player1 = 0 		
		self.score_player2 = 0

		self.current_score_p1 = 0
		self.current_score_p2 = 0

		self.dice = [0]		# store dice images

		for num in range(1, 7):
			image = resource_path(path_images + f'dice_{num}.png')
			self.dice.append(ImageTk.PhotoImage(Image.open(image)))

		self.sound = resource_path(f'{path_sounds}dice_roll.wav')			

	# start new game
	def new_game(self):
		# delete last dice rolled and arrow pointed to player 2
		try:
			self.dice_image.place_forget()
			self.player2_arrow.place_forget()
		except:
			pass

		# put dice icon in the middle (the icon has 2 images-left and right)
		self.dice_image_left.place(x=440, y=173)  
		self.dice_image_right.place(x=-2, y=173)		

		# point arrow to player 1
		self.player1 = True
		self.player1_arrow.place(x=463, y=68)		

		# reset scores
		self.current_score_p1 = 0
		self.current_score_p1_label['text'] = '0'
		self.current_score_p2 = 0
		self.current_score_p2_label['text'] = '0'

		self.score_player1 = 0
		self.text_score_player1['text'] = '0'
		self.score_player2 = 0
		self.text_score_player2['text'] = '0'

	# roll dice
	def roll(self):
		rand_number = randint(1, 6)     # get nummber from 1 to 6
		mixer.music.load(self.sound)	# play sound
		mixer.music.play()

		# delete icon and add dice rolled
		try:
			self.dice_image_left.place_forget()
			self.dice_image_right.place_forget()
			self.dice_image.place(x=441, y=173)
		except:
			pass	

		# change image to number rolled dice
		self.dice_image['image'] = self.dice[rand_number]

		# delete current score and move to next player if number rolled was 1
		if rand_number == 1:
			if self.player1:
				self.current_score_p1 = 0
				self.current_score_p1_label['text'] = '0'

				self.player1_arrow.place_forget()
				self.player2_arrow.place(x=0, y=68)
				self.player1 = False
			else:
				self.current_score_p2 = 0
				self.current_score_p2_label['text'] = '0'

				self.player2_arrow.place_forget()
				self.player1_arrow.place(x=463, y=68)

				self.player1 = True

		# sum up current player score		
		else:
			if self.player1:
				self.current_score_p1 += rand_number
				self.current_score_p1_label['text'] = f'{self.current_score_p1}'

				# end game if player's score is above 100
				if self.score_player1 + self.current_score_p1 >= 100:
					score = self.score_player1 + self.current_score_p1
					messagebox.showinfo('Player 1 win!', f'Player 1 score: {score}\nPlayer 2 score: {self.score_player2}')
					self.new_game()
			else:
				self.current_score_p2 += rand_number
				self.current_score_p2_label['text'] = f'{self.current_score_p2}'
				
				# end game if player's score is above 100
				if self.score_player2 + self.current_score_p2 >= 100:
					score = self.score_player2 + self.current_score_p2
					messagebox.showinfo('Player 2 win!', f'Player 2 score: {score}\nPlayer 1 score: {self.score_player1}')
					self.new_game()

	# sum up total score with current score
	def hold(self):
		if self.player1:
			self.score_player1 += self.current_score_p1
			self.text_score_player1['text'] = f'{self.score_player1}'
				
			self.current_score_p1 = 0
			self.current_score_p1_label['text'] = '0'

			self.player1_arrow.place_forget()
			self.player2_arrow.place(x=0, y=68)
			self.player1 = False

		else:
			self.score_player2 += self.current_score_p2
			self.text_score_player2['text'] = f'{self.score_player2}'
				
			self.current_score_p2 = 0
			self.current_score_p2_label['text'] = '0'

			self.player2_arrow.place_forget()
			self.player1_arrow.place(x=463, y=68)
			self.player1 = True					

	def widgets(self):
		global image_arrow_left, new_game_image, hold_image, roll_image, image_arrow_right

		# Frame player 1
		player1_frame = Frame(self.root, bg='#E3E2E2')
		player1_frame.place(x=0, y=0, width=500, height=500)
		player1_text = Label(player1_frame, text='Player 1', font=('', 40), bg='#E3E2E2')
		player1_text.place(x=150, y=50, width=200, height=60)

		self.text_score_player1 = Label(player1_frame, text=self.score_player1, font=('', 50), bg='#E3E2E2', fg='#83C72C')
		self.text_score_player1.place(x=195, y=150, width=110)

		# Frame player 2
		player2_frame = Frame(self.root)
		player2_frame.place(x=500, y=0, width=500, height=500)
		player2_text = Label(player2_frame, text='Player 2', font=('', 40))
		player2_text.place(x=150, y=50, width=200, height=60)

		self.text_score_player2 = Label(player2_frame, text=self.score_player2, font=('', 50), fg='#83C72C')
		self.text_score_player2.place(x=195, y=150, width=110)

		arrow_left = resource_path(path_images + 'arrow_left.png')
		image_arrow_left = ImageTk.PhotoImage(Image.open(arrow_left))
		current_player = Label(player1_frame, image=image_arrow_left, bg='#E3E2E2')
		current_player.place(x=463, y=68)

		new_game_image = resource_path(path_images + 'new_game.png')
		new_game_image = ImageTk.PhotoImage(Image.open(new_game_image))
		new_game_button = Button(self.root, text=' New Game', font=('', 15), bg='#A5F143', activebackground='#A5F143', image=new_game_image, compound=LEFT, command=self.new_game)
		new_game_button.place(x=430, y=15, width=140, height=30)

		roll_image = resource_path(path_images + 'roll.png')
		roll_image = ImageTk.PhotoImage(Image.open(roll_image))
		roll_button = Button(self.root, text=' Roll', font=('', 20, 'bold'), image=roll_image, compound=LEFT, command=self.roll)
		roll_button.place(x=445, y=340, width=110, height=40)

		hold_image = resource_path(path_images + 'hold.png')
		hold_image = ImageTk.PhotoImage(Image.open(hold_image))
		hold_button = Button(self.root, text=' Hold', font=('', 20, 'bold'), image=hold_image, compound=LEFT, command=self.hold)
		hold_button.place(x=445, y=410, width=110, height=40)

		arrow_left = resource_path(path_images + 'arrow_left.png')
		image_arrow_left = ImageTk.PhotoImage(Image.open(arrow_left))

		arrow_right = resource_path(path_images + 'arrow_right.png')
		image_arrow_right = ImageTk.PhotoImage(Image.open(arrow_right))

		self.player1_arrow = Label(player1_frame, image=image_arrow_left, bg='#E3E2E2')
		self.player1_arrow.place(x=463, y=68)

		self.player2_arrow = Label(player2_frame, image=image_arrow_right)

		self.current_score_p1_label = Label(player1_frame, text=self.current_score_p1, font=('', 30), bg='#ED2757', fg='white',)
		self.current_score_p1_label.place(x=210, y=350, width=80, height=80)

		self.current_score_p2_label = Label(player2_frame, text=self.current_score_p2, font=('', 30), bg='#ED2757', fg='white',)
		self.current_score_p2_label.place(x=210, y=350, width=80, height=80)

		# icon dice - 2 images
		dice_start_left = resource_path(path_images + 'dice_start_left.png')
		dice_start_right = resource_path(path_images + 'dice_start_right.png')
		self.dice_start_left = ImageTk.PhotoImage(Image.open(dice_start_left))
		self.dice_start_right = ImageTk.PhotoImage(Image.open(dice_start_right))

		self.dice_image_left = Label(player1_frame, image=self.dice_start_left, bg='#E3E2E2')
		self.dice_image_left.place(x=440, y=173)

		self.dice_image_right = Label(player2_frame, image=self.dice_start_right)
		self.dice_image_right.place(x=-2, y=173)

		# rolled dice image
		self.dice_image = Label(self.root, bg='#E3E2E2')
		self.dice_image.place(x=441, y=173)


# start game
if __name__ == '__main__':
	root = Tk()
	path_images = 'images/'
	path_sounds = 'sounds/'
	dice_game = DiceGame(root)
	dice_game.widgets()
	root.mainloop()