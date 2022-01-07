from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox, filedialog
from getpass import getuser
import yt_dlp
from threading import Thread
import os
import sys 
import pyperclip

def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)


class Youtube_Download:
	def __init__(self, root):
		self.root = root
		self.cancel = False
		self.download_status = ''
		self.audio_output = True

	# cancel download
	def cancel_download(self):
		self.cancel = True

		try:		
			os.system(f'start cmd /c taskkill /IM ffmpeg.exe /F')
		except:
			pass

		raise Exception('Canceled')	

	# cancel commands to execute when cancel is pressed
	def cancel_commands(self):
		self.cancel = False
		self.download_status = 'Canceled'
		self.show_download_status.delete(0.0, END)
		self.show_download_status.insert(1.0, 'Canceled\n')
		self.download_button['state'] = NORMAL

		raise Exception('Canceled')		

	# toggle betwen audio and video output
	def toggle_output_format(self, output='Audio'):
		if output == 'Audio':
			self.audio_output = True
			self.audio_download_frame['bd'] = 3
			self.audio_download_frame['bg'] = '#DCDCDC'
			self.toggle_audio_format['state'] = 'readonly'
			self.text_audio_label['bg'] = '#DCDCDC'

			self.video_download_frame['bd'] = 2
			self.video_download_frame['bg'] = '#f0f0f0'
			self.toggle_video_resolution['state'] = DISABLED
			self.text_video_label['bg'] = '#f0f0f0'
		else:
			self.video_download_frame['bd'] = 3
			self.video_download_frame['bg'] = '#DCDCDC'
			self.toggle_video_resolution['state'] = 'readonly'
			self.text_video_label['bg'] = '#DCDCDC'

			self.audio_output = False
			self.audio_download_frame['bd'] = 2
			self.audio_download_frame['bg'] = '#f0f0f0'
			self.toggle_audio_format['state'] = DISABLED
			self.text_audio_label['bg'] = '#f0f0f0'

	# change download folder
	def change_download_directory(self):
		path = filedialog.askdirectory()
		if path == "":
			self.folder_output_location.set(self.folder_output_location.get())
		else:
			self.folder_output_location.set(path + '/')	

	# open folder location
	def open_folder(self):
		path = self.folder_output_location.get()
		if not os.path.exists(path):
			os.mkdir(path)
		os.startfile(path)	

	# audio options
	def audio_download(self):	
		audio_format = self.audio_format_variable.get()
		output_folder = self.folder_output_location.get()

		ydl_opts = {
			'format': 'bestaudio/best',
			'outtmpl': output_folder+'%(title)s.%(ext)s',
			'quiet': True,
			'ignoreerrors': True,
			'postprocessors': [{
								'key': 'FFmpegExtractAudio',
								'preferredcodec': f'{audio_format}',
								'preferredquality': '0',  
							   }]
			}

		return ydl_opts

	# video options
	def video_download(self):
		video_resolution = self.video_resolution_variable.get().split(' ')[0]
		output_folder = self.folder_output_location.get()

		ydl_opts = {
			'format': f'bestvideo[height<={video_resolution}]+bestaudio/best',
			'outtmpl': output_folder+'%(title)s.%(ext)s',
			'quiet': True,
			'ignoreerrors':True,
			'overwrites':True,
			}

		return ydl_opts

	# Download
	def download(self):
		url = self.input_link.get()             # get link
		if self.audio_output:
			ydl_opts = self.audio_download()	# get audio or video options
		else:
			ydl_opts = self.video_download()

		# show status while downloading...
		def my_hook(d):
			if d['status'] == 'finished':
				self.download_status = 'Finished'
				self.show_download_status.delete(1.0, END)
				self.show_download_status.insert(1.0, 'Download complete, now converting...\n')

				if self.cancel:
					self.cancel_commands()

			if d['status'] == 'downloading':
				try:
					file_size = round(d['total_bytes']/(1024**2), 2)	# get file size
					percent = d['_percent_str']							# get file percent downloaded
					try:
						speed = round(d['speed']/(1024**2), 2)			# get file downloading speed
					except:
						speed = d['speed']
					
					file_size = f'Size:    {file_size} MB\n'
					download_speed = f'Speed:    {speed} MB/s\n'
					status = f'Progress:   {percent}\n'
				except:
					self.file_title = 'File Title:    No info\n'				
					self.file_duration = 'File Duration:    No info\n\n'
					file_size = 'Size:    No info\n'
					download_speed = 'Speed:    No info\n'
					status = 'Progress:    No info\n'

				info_status = f'{self.file_title}{self.file_duration}{file_size}{download_speed}{status}'	

				self.show_download_status.delete(1.0, END)
				self.show_download_status.insert(1.0, info_status)			

				if self.cancel:
					self.cancel_commands()

		ffmpeg_location = resource_path('Files/ffmpeg/ffmpeg.exe')

		class MyLogger:
			def debug(self, msg):
				pass

			def warning(self, msg):
				pass

			def error(self, msg):
				pass

		ydl_opts.update({'progress_hooks': [my_hook], 
						'logger': MyLogger(), 
						'ffmpeg_location': ffmpeg_location})

		# start download
		def start_download():
			try:
				with yt_dlp.YoutubeDL(ydl_opts) as ydl:
					self.show_download_status.delete(0.0, END)
					self.show_download_status.insert(1.0, 'Initiating...\n')	
					self.download_status = 'Error'
					self.download_button['state'] = DISABLED
					
					# extract title and duration
					info = ydl.extract_info(url, download=False)
					try:
						self.file_title = f'Title:    {info["title"]}\n'
						self.file_duration = f'Duration:    {info["duration_string"]}\n\n'
					except:
						pass	

					# start download
					ydl.download(url)

					self.cancel = False
					self.download_button['state'] = NORMAL

					if self.download_status == 'Finished':
						self.show_download_status.delete(0.0, END)
						self.show_download_status.insert(1.0, 'Finished\n')
						os.startfile(self.folder_output_location.get())
					elif self.download_status == 'Error':
						self.show_download_status.delete(0.0, END)
						self.show_download_status.insert(1.0, 'Error\n')

			except Exception as e:
				self.show_download_status.delete(0.0, END)
				self.show_download_status.insert(1.0, 'Error\n')
				print('start_download: ', e)

		Thread(target=start_download).start()

	# copy text 
	def copy_text(self):
		try:
			text = self.input_link.selection_get()
			pyperclip.copy(text)
		except:
			pass	

	# paste text
	def paste_text(self):
		# get the cursor index position and paste text 
		self.input_link.select_to(0)
		try:
			text = self.input_link.selection_get()
			text_length = len(text)
		except:
			text_length = 0

		self.input_link.select_clear()	
		self.input_link.insert(text_length, pyperclip.paste())

	# clear input
	def clear_text(self):			
		self.input_link.delete(0, END)			

	# add right click commands 
	def insert_link_commands(self, event):
		menu = Menu(self.root, tearoff = 0)
		menu.add_command(label ="Copy             Ctrl+C", command=self.copy_text)
		menu.add_command(label ="Paste             Ctrl+V", command=self.paste_text)
		menu.add_command(label ="Clear", command=self.clear_text)

		# get cursor position
		try:
			menu.tk_popup(event.x_root, event.y_root)
		finally:
			menu.grab_release()

	# widgets
	def widgets(self):
		### Frame insert link
		frame_insert_link = LabelFrame(self.root, labelanchor='n', text='Insert link (video/playlist/channel)', font=('', 11, 'bold'))
		frame_insert_link.place(x=5, y=10, width=367, height=50)

		self.input_link = Entry(frame_insert_link)
		self.input_link.place(x=5, y=5, width=350)
		self.input_link.bind('<Button-3>', self.insert_link_commands)

		self.audio_widgets()
		self.video_widgets()
		self.output_location()
		self.show_info_widgets()

		self.download_button = Button(self.root, text='Download', bg='#2AE539', font=('',14,'bold'), command=self.download)
		self.download_button.place(x=70, y=270, height=30, width=110)

		self.cancel_button = Button(self.root, text='Cancel', bg='#E75428', font=('',14,'bold'), command=self.cancel_download)
		self.cancel_button.place(x=197, y=270, height=30, width=110)		

	def output_location(self):	
		### Ouput location
		frame_output_location = LabelFrame(self.root, text='Download location', font=("", 11, 'bold'))
		frame_output_location.place(x=5, y=90, width=367, height=50)

		# select default output location
		username = str(getuser())																					
		default_download_location = f'C:/Users/{username}/Downloads/YT-Download/'									# default download folder

		self.folder_output_location = StringVar()
		self.folder_output_location.set(default_download_location)
		display_output_location = Label(frame_output_location, textvariable=self.folder_output_location)			# display output folder
		display_output_location.place(x=5, y=5)	

		change_output_folder_button = Button(self.root, text='Change', bd=2, 										# change output folder
											font=("", 10, 'bold'),command=self.change_download_directory)
		change_output_folder_button.place(x=237, y=90, width=60, height=20, bordermode=OUTSIDE)

		open_output_folder_button = Button(self.root, text='Open', font=("", 10, 'bold'), command=self.open_folder)	# open output folder
		open_output_folder_button.place(x=303, y=90, width=60, height=20)

	### audio widgets
	def audio_widgets(self):
		self.audio_download_frame = LabelFrame(self.root, bd=3, bg='#DCDCDC', font=("", 12, 'bold'))
		self.audio_download_frame.place(x=5, y=175, width=175, height=70)

		# Button to toggle betwen audio/video widgets
		Button(self.root, text='Audio', bd=3, relief=RIDGE, font=("", 12, 'bold'), 
				command=lambda *_:self.toggle_output_format('Audio')).place(x=60, y=165, width=60, height=25)

		self.audio_format_variable = StringVar()
		self.text_audio_label = Label(self.audio_download_frame, text='Format:', bg='#DCDCDC', font=('',11,'bold'))
		self.text_audio_label.place(x=5, y=27)
		format_values = ['Source', 'mp3', 'flac', 'aac', 'm4a',] 
		self.toggle_audio_format = Combobox(self.audio_download_frame, state='readonly', textvariable=self.audio_format_variable, 
								font=("", 10, 'bold'), value=format_values, width=7)
		self.toggle_audio_format.place(x=70, y=27)
		self.toggle_audio_format.current(1)
	
	### video widgets
	def video_widgets(self):
		self.video_download_frame = LabelFrame(self.root, font=("", 12, 'bold'))
		self.video_download_frame.place(x=197, y=175, width=175, height=70)

		# Button to toggle betwen audio/video widgets
		Button(self.root, text='Video + Audio', bd=3, relief=RIDGE, font=("", 12, 'bold'), 
				command=lambda *_:self.toggle_output_format('Video')).place(x=221.5, y=165, width=120, height=25)
		
		self.text_video_label = Label(self.video_download_frame, text='Resolution:', font=('',11,'bold'))
		self.text_video_label.place(x=0, y=27)

		self.video_resolution_variable = StringVar()
		resolution_values = ['4320 (8k)','2160 (4k)', '1440 (2k)', 1080, 720, 480, 360, 240, 144]
		self.toggle_video_resolution = Combobox(self.video_download_frame, font=("", 10, 'bold'), state=DISABLED, value=resolution_values,
									 width=8, textvariable=self.video_resolution_variable)
		self.toggle_video_resolution.place(x=85, y=27)
		self.toggle_video_resolution.current(3)

		self.video_download_frame.bind('<Button-1>', lambda x:self.toggle_output_format(output='Video'))

	# show download info
	def show_info_widgets(self):
		frame_download_status = LabelFrame(self.root, text='Download status', font=("", 12, 'bold'))
		frame_download_status.place(x=5, y=320, width=367, height=170)

		scrollbar_listbox = Scrollbar(frame_download_status)
		scrollbar_listbox.place(x=340, y=5, height=135)
		self.show_download_status = Text(frame_download_status, font=("", 10, 'bold'), spacing3=3 , yscrollcommand=scrollbar_listbox.set)
		self.show_download_status.place(x=5, y=5, width=335, height=135)	
		scrollbar_listbox['command'] = self.show_download_status.yview