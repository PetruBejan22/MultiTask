from tkinter import *
import pygame
from math import sqrt
import pygame_menu
import time
import sys
import os
from random import choice

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

path_images = 'Files/Hangman/images/'

class Hangman(pygame_menu.menu.Menu):
	def __init__(self, screen, word, menu):
		self.screen = screen
		self.word = word
		self.menu = menu
		self.run = True
		self.exit_game = False
		self.clock = pygame.time.Clock()
		self.alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		self.font = pygame.font.SysFont('TimesNewRoman', 50, bold=True)
		self.mouse_pos = (0,0)
		self.mouse_on = True		
		self.count = 0
		self.guessed = ' '
		self.not_guessed = ''
		self.count_bad_letters = 0
		self.end_game = False
		self.mouse_pos2 = (0,0)

		background1 = resource_path(path_images + 'background_hangman.png')
		self.background = pygame.image.load(background1)
		you_lose1 = resource_path(path_images + 'you_lose.png')
		self.you_lose = pygame.image.load(you_lose1)
		you_win1 = resource_path(path_images + 'you_win.png')
		self.you_win = pygame.image.load(you_win1)

		self.hangman_images = []
		# load images
		for file in range(7):
			fil = resource_path(path_images + f'hangman{file}.png')
			self.hangman_images.append(pygame.image.load(fil))

	def check_letter(self, screen, font):
		count_good_letters = 0
		for let in self.guessed:
			for number, lett in enumerate(self.word):
				if let == lett:
					count_good_letters += 1
					text = font.render(let, True, ('#1D2CAF'))
				else:
					text = font.render('_', True, ('#1D2CAF'))
				screen.blit(text, (300 + number * 50, 150))
			if self.count == len(self.word):
				self.count = 0

		# end game if bad letters reached 6 or the word was guessed
		if self.count_bad_letters == 6 or count_good_letters == len(self.word):
			if self.count_bad_letters == 6:
				screen.blit(self.you_lose, (310, 250))
				word = font.render(f'Word:   {self.word}', True, ('#1D2CAF'))
				screen.blit(word, (310, 50))		
			else:	
				screen.blit(self.you_win, (310, 250))	

			self.mouse_on = False
			self.end_game = True
			self.not_guessed = ''	
			text = font.render('Play again?', True, ('#3F80D8'))
			screen.blit(text, (390, 350))
			pygame.draw.rect(screen, ('#5FC227'), (400, 420, 80, 50))
			pygame.draw.rect(screen, ('#C63A1B'), (550, 420, 80, 50))
			yes = font.render('Yes', True, ('#F5E5E2'))
			no = font.render('No', True, ('#F5E5E2'))
			screen.blit(yes, (405, 415))
			screen.blit(no, (560, 415))
  
			if (self.mouse_pos2[0] >= 400 and self.mouse_pos2[0] <= 480) and\
			(self.mouse_pos2[1] >= 420 and self.mouse_pos2[1] <= 470):
				self.run = False
			if (self.mouse_pos2[0] >= 550 and self.mouse_pos2[0] <= 630) and\
			(self.mouse_pos2[1] >= 420 and self.mouse_pos2[1] <= 470):
				self.exit_game = True
		else:				
			font = pygame.font.SysFont('TimesNewRoman', 40, bold=True)
			wrong_letters = font.render(f'Bad letters: {self.not_guessed}', True, ('#1D2CAF'))
			screen.blit(wrong_letters, (50, 400))		

	# draw letters on screen
	def draw_letters(self, screen, alphabet, font, mouse_pos):
		# X axis
		for num, x in enumerate(range(110, 910, 65)):
			# Y axis
			for y in range(550, 750, 100):
				# first row with letters from A-M and second row from N-Z 
				if y > 550:
					letter = alphabet[num + 13]
				else:
					letter = alphabet[num]

				# draw circles
				pygame.draw.circle(screen, ('#A0A0A0'), (x, y), 30)

				# center letter inside circles
				text = font.render(letter, True, ('#1D2CAF'))
				text_x, text_y, *_ = text.get_rect(center=(x, y))
				screen.blit(text, (text_x, text_y))

				# get circle radius and then check is mouse was clicked inside circle
				coord = sqrt((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2)

				if coord <= 30:
					self.alphabet = alphabet.replace(letter, " ")  # change clicked letter with " "
					self.mouse_pos = (0, 0)  # reset mouse coord

					if letter in self.word:
						self.count += self.word.count(letter) 
						self.guessed += letter	
					elif letter == " ":
						pass
					else:
						self.not_guessed += letter + " "
						self.count_bad_letters += 1									

	def main(self):
		while self.run:
			self.screen.blit(self.background, (0,0))    # background
			self.screen.blit(self.hangman_images[self.count_bad_letters], (50, 100))

			self.check_letter(self.screen, self.font)

			self.clock.tick(30)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.run = False
					self.exit_game = True
					break
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.mouse_on:
						self.mouse_pos = pygame.mouse.get_pos()	   # mouse coord
					if self.end_game:	
						self.mouse_pos2 = pygame.mouse.get_pos()

			self.draw_letters(self.screen, self.alphabet, self.font, self.mouse_pos)

			pygame.display.update()
			if self.exit_game:
				self.run = False
				pygame.display.quit()

# initialize game and menu
def initialize_game():
	global screen, word, mode, player_input
	pygame.init()

	screen = pygame.display.set_mode((1000, 700))
	pygame.display.set_caption('Hangman')

	icon = pygame.image.load(resource_path(path_images + 'hangman_png.png'))
	pygame.display.set_icon(icon)

	image_hangman = resource_path(path_images + 'hangman_png.png')
	
	menu = pygame_menu.Menu('Menu', 1000, 700, theme=pygame_menu.themes.THEME_BLUE)    # init menu

	english_words =['ANIMAL', 'PICTURE', 'MOTHER', 'FATHER', 'EARTH', 'SENTENCE', 'BEFORE', 'ABOUT', 'NUMBER', 'SOUND', 'PEOPLE', 'COUNTRY', 'ANSWER', 'BETWEEN', 'SCHOOL', 'PLANT', 'FARM', 'SCIENCE', 'MOUNTAIN', 'CHILDREN', 'SECOND', 'YOUNG', 'FAMILY', 'COMPLETE', 'QUESTION', 'FIRE', 'ROCK', 'STREET', 'NOTHING', 'ISLAND', 'POSSIBLE', 'GAME', 'LANGUAGE', 'DISTANT', 'PAINT', 'LANGUAGE', 'AMONG', 'POWER', 'MACHINE', 'CORRECT', 'BEAUTY', 'GREEN', 'FINAL', 'FRONT', 'DEVELOP', 'OCEAN', 'STRONG', 'SPECIAL', 'MIND', 'SPACE', 'REMEMBER', 'HUNDRED', 'INTEREST', 'TABLE', 'PATTERN', 'MONEY', 'VOICE', 'GOVERN']
	cuvinte_romana = ['METEO', 'TRADUCERE', 'LIBERTATE', 'HOROSCOP', 'SPORT', 'FURTUNA', 'REALITATE', 'ELEFANT', 'HOTEL', 'TRACTOR', 'ZIAR', 'CALCULATOR', 'COMISAR', 'MUZICA', 'AUTOTURISM', 'HARTA', 'FOTBAL', 'RADIO', 'RESTAURANT', 'RULOTA', 'CANAPEA', 'CUTREMUR', 'LAPTOP', 'CASA', 'CEAS', 'MASINA', 'REMORCA', 'SIMPATIE', 'TEREN', 'AVARIAT', 'PLACERE', 'TASTATURA', 'ANTIVIRUS', 'DRUJBA', 'CALENDAR', 'MOBILA', 'BILIARD', 'COLINDA', 'PISICA', 'PORUMBEL', 'ROCHIE', 'OPERA', 'PLATFORMA', 'TATUAJ', 'TELEFON', 'TAXI', 'TESTARE', 'VREME', 'APARTAMENT', 'COCOS', 'GHICITOR', 'PAT', 'SIMULATOR', 'TELEGRAF', 'CAZARE']	
	
	alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' 		
	alphabet_list = [x for x in alphabet]		# valid chars for user input

	word = 'HANGMAN'
	mode = 'player input'

	def input_word(value):
		global word
		word = value.upper()

	# change mode
	def set_mode(value, mode_value):
		global mode, player_input
		mode = mode_value
		if mode == 'player input':
			player_input.show()
		else:
			player_input.hide()	
	
	# select word
	def play_button():
		global word, mode, screen
		if mode == 'auto română':
			word = choice(cuvinte_romana)
		elif mode == 'auto english':
			word = choice(english_words)

		hangman = Hangman(screen, word, menu)
		hangman.main()

	# add menu commands
	menu.add.image(image_hangman, scale=(0.6, 0.6), scale_smooth=True)	
	menu.add.selector('Select Mode: ', [('Player Input', 'player input'), ('Auto(română)', 'auto română'), ('Auto(english)', 'auto english')], onchange=set_mode)
	player_input = menu.add.text_input('Add Word: ', maxchar=14, valid_chars=alphabet_list, onchange=input_word)
	menu.add.button('Play', play_button)
	menu.add.button('Exit', pygame.display.quit)
	menu.mainloop(screen)
	

if __name__ == '__main__':
	path_images = 'images/'
	initialize_game()