from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
import getpass
import PIL.ImageGrab
import time
import os
import sys
from pygame import mixer
import keyboard

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

path_sounds = 'Files/MultiTask_sounds/'


class Screenshot:
	def __init__(self, root):
		self.root = root
		mixer.init()

	# Save screenshot to selected folder
	def take_screenshot(self):
		path = self.location_save.get()   # MultiTask Screenshot folder
		try:
			if not os.path.exists(path):
				os.mkdir(path)
		except:
			messagebox.showerror('Error', 'Invalid path')
			try:
				self.root.after_cancel(self.start_timer)
			except:
				pass	
		else:
			current_time_folder = time.strftime("%d-%m-%Y")  
			date_folder = path + '/' + current_time_folder   # Folder with the current date
			if not os.path.exists(date_folder):
				os.mkdir(date_folder)

			current_time_file = time.strftime("%H;%M;%S")  # file name = current time
			format_image = self.format_save.get()   # get extension
			location_name_file_save = date_folder + '/' + "{}{}".format(current_time_file, format_image)
			screenshot = PIL.ImageGrab.grab()
			screenshot.save(location_name_file_save)	

			if self.var_sound.get():
				self.sound = resource_path(path_sounds + 'camera_sound.mp3')
				mixer.music.load(self.sound)
				mixer.music.play()		

	# change folder location
	def change_location(self):
		self.location_save.config(state='normal')

		new_location = filedialog.askdirectory()
		if new_location:
			self.location_save.delete(0, END)
			self.location_save.insert(0, new_location)

		self.location_save.config(state='disabled')

	# start taking screenshots
	def start_screenshot_timer(self):
		try:
			if self.run:
				try:
					self.root.after_cancel(self.start_timer)
				except:
					pass

				time = int(self.screenshot_value.get())
				if self.screenshot_time.get() == 'seconds':
					time *= 1000
				elif self.screenshot_time.get() == 'minutes':
					time *= 60_000
				elif self.screenshot_time.get() == 'hours':
					time *= 3_600_600		

				self.take_screenshot()
				self.start_timer = self.root.after(time, self.start_screenshot_timer)
		except Exception as e:
			print('start_screenshot_timer: ***', e)		

	# start screenshot timer
	def enable_screenshot_timer(self):
		self.run = True	
		self.start_screenshot_timer()
		self.enable_screenshot_timer_button.config(state='disabled')
		self.cancel_screenshot_timer_button.config(state='normal')	

	def cancel_screenshot_timer(self):
		self.root.after_cancel(self.start_timer)
		self.run = False
		self.enable_screenshot_timer_button.config(state='normal')
		self.cancel_screenshot_timer_button.config(state='disabled')		

	# open the folder location
	def open_folder(self):
		try:
			path = self.location_save.get()
			os.startfile(path)
		except:
			messagebox.showerror('Error', 'Folder path not found')				

	# widgets
	def widgets(self):
		username = str(getpass.getuser())
		default_location = 'C:/Users/{}/Pictures/MultiTask_Screenshot'.format(username)
		keyboard.add_hotkey('print_screen', self.take_screenshot)  # take screnshot even if program has focus or not

		self.take_screenshot_button = Button(self.root, text='Take Screenshot', bg='#2AE539', activebackground='#2AE539', font=("", 14, 'bold'), command=self.take_screenshot)
		self.take_screenshot_button.place(x=105, y=30, width=170)

		Label(self.root, text='(Shortcut:                               key)').place(x=104, y=70)
		Label(self.root, text='Print_Screen', font=('', 10, 'italic', 'bold')).place(x=163, y=70)

		self.options_frame = LabelFrame(self.root, text='Options', font=("", 12, 'bold'))
		self.options_frame.place(x=5, y=100, width=367)

		Label(self.options_frame, text='Location:', font=("", 10, 'bold')).grid(row=0, column=0, pady=15)	

		self.location_save = Entry(self.options_frame, font=("", 10), width=32)
		self.location_save.grid(row=0, column=1, pady=15)
		self.location_save.insert(0, default_location)
		self.location_save.config(state='disabled')

		self.change_location_button = Button(self.options_frame, text='Change', font=("", 10, 'bold'), command=self.change_location)
		self.change_location_button.grid(row=0, column=2, pady=10, padx=5)

		Label(self.options_frame, text='Format:', font=("", 10, 'bold')).grid(row=1, column=0, sticky=W, pady=10)
		self.format_save = ttk.Combobox(self.options_frame, value=('.png', '.jpeg'), state='readonly', width=10, font=("", 10, 'bold'))
		self.format_save.grid(row=1, column=1, sticky=W, pady=10)
		self.format_save.current(0)

		Label(self.options_frame, text='Sound:', font=("", 10, 'bold')).grid(row=2, column=0, sticky=W, pady=10)
		self.var_sound = IntVar()
		self.sound = Checkbutton(self.options_frame, variable=self.var_sound)
		self.sound.grid(row=2, column=1, sticky=W, pady=10)

		self.auto_screenshot_frame = LabelFrame(self.root, text='Auto Screenshot', font=("", 12, 'bold'), width=300, height=200)
		self.auto_screenshot_frame.place(x=5, y=280, width=366)

		Label(self.auto_screenshot_frame, text='Take screenshot every:', font=("", 10, 'bold')).grid(row=0, column=0, sticky=W, pady=20)
		self.screenshot_value = ttk.Combobox(self.auto_screenshot_frame, state='readonly', width=8, font=("", 10, 'bold'))
		self.screenshot_value.grid(row=0, column=1, sticky=W, pady=10, padx=10)
		self.screenshot_value.config(value=('1', '2', '5', '10', '15', '20', '30', '45', '60'))
		self.screenshot_value.current(0)
		self.screenshot_value.bind("<<ComboboxSelected>>", lambda _: self.start_screenshot_timer())

		self.screenshot_time = ttk.Combobox(self.auto_screenshot_frame, value=('seconds', 'minutes', 'hours'), state='readonly', width=8, font=("", 10, 'bold'))
		self.screenshot_time.grid(row=0, column=2, sticky=E, pady=10)
		self.screenshot_time.current(0)
		self.screenshot_time.bind("<<ComboboxSelected>>", lambda _: self.start_screenshot_timer())

		self.enable_screenshot_timer_button = Button(self.auto_screenshot_frame, text='Enable', font=('', 14, 'bold'), command=self.enable_screenshot_timer, bg='#2AE539', activebackground='#2AE539')
		self.enable_screenshot_timer_button.grid(row=1, column=0, columnspan=2, padx=30, pady=10)

		self.cancel_screenshot_timer_button = Button(self.auto_screenshot_frame, text='Cancel', font=('', 14, 'bold'), command=self.cancel_screenshot_timer, bg='#F36C75', state='disabled', activebackground='#F36C75')
		self.cancel_screenshot_timer_button.grid(row=1, column=1, columnspan=2, padx=30, pady=10)

		Button(self.root, text = 'Open folder location', font=('', 13), command=self.open_folder).place(x=5, y=430)
		Label(self.root, text='Note: You can take screenshots even if the program is minimized').place(x=5, y=470)
