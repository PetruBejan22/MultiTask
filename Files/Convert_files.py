from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox, filedialog
import os
import sys 
from getpass import getuser
import re
from threading import Thread
from subprocess import Popen, PIPE, STDOUT
from tkinterdnd2 import *

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)


class Convert_Files:
	def __init__(self, root):
		self.root = root
		self.files_list = []
		self.output_format_variable = 'mp4'

		self.convert_widgets()
		self.files_listbox.bind("<Button-1>", self.disable_mouse_event_listbox)		# disable left click on listbox

		# drag items from outside
		self.files_listbox.drop_target_register(DND_FILES)
		self.files_listbox.dnd_bind('<<Drop>>', self.drag_items_from_outside)

	# disable mouse event on listbox
	def disable_mouse_event_listbox(self, event):
		return 'break'		

	# Add files
	def add_files(self):
		files = filedialog.askopenfilenames()
		for file in files:
			file_number = self.files_listbox.size()					# get list last number
			self.files_list.append(file)
			name_and_extension = os.path.basename(file)				# get only the filename and extension
			self.files_listbox.insert(END, f'{str(file_number+1)}. {name_and_extension}')

	# drag items from outsite
	def drag_items_from_outside(self, event):
		'''
		If file has space beetwen characters, tkinterdnd2 will add '{' at beggining and '}' at the end
		If file has '{' or '}' and space in name , tkinterdnd2 will add '\' after every word
		If multiple items ar dragged in, the whole thing is a string
		'''
		dragged_files = event.data.replace('\\', '')			# delete special character from name '\'		 
		dragged_files = dragged_files.split()					# split string
		files_list = []
		index = 1
		for item in range(len(dragged_files)):
			file = ' '.join(dragged_files[:index]).strip('{}')	# remove '{' and '}' and group items from list until is a valid path
			if os.path.exists(file):
				files_list.append(file)
				dragged_files = dragged_files[index:]			# remove the valid path from dragged items and continue with next
				index = 1
			else:
				index += 1

		if files_list:
			for file in files_list:
				file_number = self.files_listbox.size()					# get list last number
				self.files_list.append(file)
				name_and_extension = os.path.basename(file)				# get only the filename and extension
				self.files_listbox.insert(END, f'{str(file_number+1)}. {name_and_extension}')			

	# Change output directory
	def change_output_directory(self):
		path = filedialog.askdirectory()
		if path != '':
			self.folder_output_location.set(path + '/')	

	# Open folder location
	def open_folder(self):
		path = self.folder_output_location.get()
		if not os.path.exists(path):
			os.mkdir(path)
		os.startfile(path)

	# toggle output format
	def check_output_option(self, value):
		self.convert_video_values['state'] = DISABLED
		self.convert_audio_values['state'] = DISABLED
		self.custom_output_format['state'] = DISABLED

		if value == 'Video':
			self.convert_video_values['state'] = 'readonly'
			self.output_format_variable = self.convert_video_variable.get()
		elif value == 'Audio':
			self.convert_audio_values['state'] = 'readonly'
			self.output_format_variable = self.convert_audio_variable.get()
		elif value == 'Custom':
			self.custom_output_format['state'] = NORMAL	
			self.output_format_variable = self.custom_output_variable.get()	

		return self.output_format_variable

	# Cancel convert
	def cancel_convert(self):
		self.convert_button['state'] = NORMAL
		self.progress_info_label['text'] = 'Canceled'
		try:		
			os.system(f'start cmd /c taskkill /IM ffmpeg.exe /F')
		except:
			raise Exception('Canceled')	

	# clear list
	def clear_listbox(self):
		self.files_list.clear()
		self.files_listbox.delete(0, END)				

	# Convert files
	def convert_files(self):
		for index, file in enumerate(self.files_list):					# make every file from list with black color
			self.files_listbox.itemconfig(index, fg='black')

		folder_output = self.folder_output_location.get()				# get folder output
		list_size = self.files_listbox.size()							# get list size

		def start_convert():
			for index, file in enumerate(self.files_list):									
				filename = os.path.splitext(os.path.basename(file))[0]							# get only name of the file
				output_format = self.check_output_option(self.output_format_option.get())		# get output format
				new_filename = f'{folder_output}{filename}.{output_format}'						# get new file name 
				ffmpeg_location = resource_path('Files/ffmpeg/ffmpeg.exe')						# ffmpeg location

				self.show_output_info.delete(0.0, END)											# delete output info
				self.progress_info_label['text'] = f'Converting file {index+1} of {list_size}'	

				if not os.path.exists(folder_output):											#  create folder output if not exists
					os.mkdir(folder_output)

				ffmpeg_command = [f'{ffmpeg_location}', '-y', '-i', f'{file}', f'{new_filename}']	# ffmpeg command

				# open command in subprocess and extract info
				with Popen(ffmpeg_command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, bufsize=1, encoding="utf-8", universal_newlines=True) as process:
					self.convert_button['state'] = DISABLED
					total_duration = 100		# file length
					current_time = 100			# current file time

					# iterate through output info and display on screen
					for line in process.stdout:
						self.show_output_info.insert(END, line)
						self.show_output_info.see(END)

						# get file length
						if 'Duration' in line:
							ln = re.findall('[0-9]{2}:[0-9]{2}:[0-9]{2}', line)    
							h, m, s = ln[0].split(':')
							h = int(h) * 3600
							m = int(m) * 60
							total_duration = h + m + int(s)
						
						# get file current time
						if 'time' in line:
							tm = re.findall('[0-9]{2}:[0-9]{2}:[0-9]{2}', line)
							h, m, s = tm[0].split(':')
							h = int(h) * 3600
							m = int(m) * 60
							current_time = h + m + int(s)

						# convert current time and total length into progress (%)
						if total_duration != 0 and current_time != 0 and current_time <= total_duration: 
							progress_percent = round((current_time * 100) / total_duration, 2) 
							self.progress_info_label['text'] = f'Progress file {index+1} of {list_size}:  {progress_percent}%'				

				# change file color into 'green' if it was a succes else into 'red'
				if process.returncode != 0:
					self.files_listbox.itemconfig(index, fg='#FF1616')
				else:
					self.files_listbox.itemconfig(index, fg='#3CD100')

				self.progress_info_label['text'] = 'Finished'
				self.convert_button['state'] = NORMAL				

		Thread(target=start_convert).start()			# start Thread

	def convert_widgets(self):
		### Ouput location
		frame_output_location = LabelFrame(self.root, text='Output location', font=("", 11, 'bold'))
		frame_output_location.place(x=5, y=5, width=367, height=50)

		# select default output location
		username = str(getuser())
		default_output_location = f'C:/Users/{username}/Documents/MultiTask-Convert/'

		self.folder_output_location = StringVar()
		self.folder_output_location.set(default_output_location)
		display_output_location = Label(frame_output_location, textvariable=self.folder_output_location)			# display output folder
		display_output_location.place(x=5, y=5)	

		change_output_folder_button = Button(self.root, text='Change', bd=2, 										# change output folder
											font=("", 10, 'bold'),command=self.change_output_directory)
		change_output_folder_button.place(x=237, y=5, width=60, height=20, bordermode=OUTSIDE)

		open_output_folder_button = Button(self.root, text='Open', font=("", 10, 'bold'), command=self.open_folder)	# open output folder
		open_output_folder_button.place(x=303, y=5, width=60, height=20)

		### Ouput format
		frame_output_format = LabelFrame(self.root, text='Output format', font=("", 11, 'bold'))
		frame_output_format.place(x=5, y=65, width=367, height=90)

		self.output_format_option = StringVar()
		self.output_format_option.set('Video')

		# Select Video output
		Checkbutton(frame_output_format, text='Video:', font=("", 10), variable=self.output_format_option, onvalue='Video', 
					offvalue='Video', command=lambda:self.check_output_option('Video')).place(x=20, y=5)
		convert_video_values = ['mp4', 'mkv', 'wmv',  'avi']
		self.convert_video_variable = StringVar()
		self.convert_video_values = Combobox(frame_output_format, state='readonly', value=convert_video_values, width=5, font=("", 10), 
											textvariable=self.convert_video_variable)
		self.convert_video_values.place(x=90, y=5, height=24)
		self.convert_video_variable.set('mp4')

		# Select Audio output
		Checkbutton(frame_output_format, text='Audio:', font=("", 10), variable=self.output_format_option, onvalue='Audio', 
					offvalue='Audio', command=lambda:self.check_output_option('Audio')).place(x=200, y=5)
		convert_audio_values = ['mp3','flac', 'wav', 'aac', 'm4a']
		self.convert_audio_variable = StringVar()
		self.convert_audio_values = Combobox(frame_output_format, state=DISABLED, value=convert_audio_values, width=5, font=("", 10), 
											textvariable=self.convert_audio_variable)
		self.convert_audio_values.place(x=270, y=5, height=24)
		self.convert_audio_variable.set('mp3')

		# Select custom output
		Checkbutton(frame_output_format, text='Custom output:', font=("", 10), variable=self.output_format_option, onvalue='Custom', 
					offvalue="Custom", command=lambda:self.check_output_option('Custom')).place(x=20, y=35)
		self.custom_output_variable = StringVar()
		self.custom_output_format = Entry(frame_output_format, textvariable=self.custom_output_variable, state=DISABLED, font=("", 10))
		self.custom_output_format.place(x=140, y=38, width=40)

		### add files
		frame_add_files = LabelFrame(self.root, font=("", 11, 'bold'))
		frame_add_files.place(x=5, y=175, width=367, height=150)

		# Add file Button
		add_files_button = Button(self.root, text='Add file(s)', font=("", 10, 'bold'), bd=1, command=self.add_files, width=9)	
		add_files_button.place(x=12, y=164, height=25)

		# Clear list Button
		clear_listbox_button = Button(self.root, text='Clear', font=("", 10, 'bold'), bd=1, command=self.clear_listbox, width=9)	
		clear_listbox_button.place(x=302, y=164, height=25, width=50)
		
		# Scrollbar listbox (vertical)
		scrollbar_listbox_vertical = Scrollbar(frame_add_files)
		scrollbar_listbox_vertical.place(x=345, y=18, height=110)

		# Scrollbar listbox (horizontal)
		scrollbar_listbox_horizontal = Scrollbar(frame_add_files, orient=HORIZONTAL)
		scrollbar_listbox_horizontal.place(x=5, y=128, width=340)

		# Files listbox 
		self.files_listbox = Listbox(frame_add_files, font=("", 11, 'bold'), fg='black', selectbackground='white', highlightthickness=0,	
										 disabledforeground='black', activestyle='none', yscrollcommand=scrollbar_listbox_vertical.set, xscrollcommand=scrollbar_listbox_horizontal.set)
		self.files_listbox.place(x=5, y=18, width=340, height=110)
		scrollbar_listbox_vertical['command'] = self.files_listbox.yview
		scrollbar_listbox_horizontal['command'] = self.files_listbox.xview

		### Convert/ Button
		self.convert_button = Button(self.root, text='Convert', font=('',14,'bold'), bg='#2AE539', command=self.convert_files)
		self.convert_button.place(x=95, y=330, height=30, width=90)	
		# Cancel Button
		Button(self.root, text='Cancel', font=('',14,'bold'), bg='#E75428', command=self.cancel_convert).place(x=190, y=330, height=30, width=90)			 

		### add files
		frame_output_info = LabelFrame(self.root, text='Convert Info', font=("", 11, 'bold'))
		frame_output_info.place(x=5, y=365, width=367, height=110)

		# Scrollbar output info 
		scrollbar_output_info = Scrollbar(frame_output_info)
		scrollbar_output_info.place(x=345, y=0, height=80)
		# Output info Text widget
		self.show_output_info = Text(frame_output_info, font=('', 8), yscrollcommand=scrollbar_output_info.set)
		self.show_output_info.place(x=5, y=0, width=340, height=80)
		scrollbar_output_info['command'] = self.show_output_info.yview

		# Info 
		self.progress_info_label = Label(self.root, text='Status: ...', font=('', 10, 'bold'))
		self.progress_info_label.place(x=3, y=475, height=25)	