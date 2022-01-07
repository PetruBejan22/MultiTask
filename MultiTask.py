from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Notebook, Style
from PIL import ImageTk, Image
import os
import sys
from threading import Thread
from webbrowser import open as webbrowser_open
from tkinterdnd2 import *


from Files import Info
from Files.Random_generator_numbers import Random_Generator_Numbers
from Files.Shutdown import Shutdown
from Files.Stopwatch import Stopwatch
from Files.Target.Target import Target
from Files.FlappyBird.FlappyBird import FlappyBird
from Files.Snake.Snake import Snake_Game
from Files.Snake_v2.Snake_v2 import Snake_v2
from Files.Screenshot import Screenshot
from Files.Hangman import Hangman
from Files.yt_download import Youtube_Download
from Files.Convert_files import Convert_Files
from Files.DiceGame.DiceGame import DiceGame


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

path_images = 'Files/MultiTask_images/'
path_sounds = 'Files/MultiTask_sounds/'
images = []

# load images
def load_image(image):
    file = resource_path(path_images + image)
    file = ImageTk.PhotoImage(Image.open(file))
    images.append(file)
    return images[-1] 

# About page from menu     
def about_page(root):
    root_about = Toplevel(root)
    root_about.title('About')
    root_about.maxsize(250, 120)
    root_about.minsize(250, 120)
    root_about.iconphoto(False, load_image('multitask_image.png'))
    label_site = Label(root_about, text='petrubejan.epizy.com', justify=LEFT, cursor='hand2', font=("", 13, "bold", "italic", "underline"))
    label_site.pack(side=TOP)
    label_site.bind("<Button-1>", lambda _: webbrowser_open('petrubejan.epizy.com'))
                
    label_about = Label(root_about, text=Info.info, anchor='w', justify=LEFT, pady=5, padx=25, font=('', 10))
    label_about.pack(fill='both', side=LEFT, expand=TRUE)
# Menu
def menu_multitask(root):          
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)

    filemenu.add_command(label="Patch History", command=patch_history)
    filemenu.add_separator()
    filemenu.add_command(label="About", command=lambda:about_page(root))
    menubar.add_cascade(label="Help", menu=filemenu)
    root.config(menu=menubar)

# Games
def games_tab():
    # flappy bird start
    def flappy_bird_game():
        root = Toplevel()
        flappy_bird = FlappyBird(root)
        flappy_bird.run_func()

    # target game start
    def target_game():
        root = Toplevel()
        target = Target(root)
        target.call_func()

    # snake game start
    def snake_game():
        root = Toplevel()
        snake = Snake_Game(root)
        snake.main()    

    # snake game start
    def snake_v2_game():
        root = Toplevel()
        snake_v2 = Snake_v2(root)
        snake_v2.run_func()

    def hangman_game():   
        Thread(target=Hangman.initialize_game).start()

    # dice game 
    def dice_game():
        root = Toplevel()
        dice_game = DiceGame(root)
        dice_game.widgets()           
 
    button_flappy_bird = Button(frame_games, command=flappy_bird_game,image=load_image('flappybird_image.png'))  # Flappy Bird
    button_flappy_bird.place(x=0, y=0, width=190, height=167)

    # Snake
    button_snake = Button(frame_games, command=snake_game, image=load_image('snake_image.png'))  # Snake
    button_snake.place(x=190, y=0, width=190, height=167)

    # Hangman
    button_hangman = Button(frame_games, command=hangman_game, image=load_image('hangman_image.png'))
    button_hangman.place(x=0, y=167, width=190, height=167)

    # Snake v2
    button_snake_v2 = Button(frame_games, command=snake_v2_game, image=load_image('snake_v2_image.png'))  # Snake v2
    button_snake_v2.place(x=190, y=167, width=190, height=167)

    # Target
    button_target = Button(frame_games, command=target_game, image=load_image('target_image.png'))  # Target
    button_target.place(x=0, y=334, width=190, height=167)

    # Dice
    button_dice_game = Button(frame_games, command=dice_game, image=load_image('dice_game_image.png'))  # Dice Game
    button_dice_game.place(x=190, y=334, width=190, height=167)

# Shutdown
def shutdown_tab():
    shut = Shutdown(frame_shutdown)
    shut.buttons()  

# Stopwatch
def stopwatch_tab():
    stop_watch = Stopwatch(frame_stopwatch)
    stop_watch.buttons()    

def yt_download_tab():
    yt_download = Youtube_Download(frame_yt_download)
    yt_download.widgets()

def convert_files_tab():
    convert_files = Convert_Files(frame_convert_files)
    #convert_files.convert_widgets()

def screenshot_tab():
    screenshot = Screenshot(frame_screenshot)
    screenshot.widgets()    

# Random generator button
def random_generator_tab(root):
    rand_numbers = Random_Generator_Numbers(frame_random_generator)
    rand_numbers.buttons()

def tabs_multitask(root):
    global frame_games, frame_shutdown, frame_stopwatch, frame_yt_download
    global frame_convert_files, frame_screenshot, frame_random_generator

    # Style for tabs
    style = Style()
    if sys.platform == "win32":
        style.theme_use('winnative')
    style.configure('lefttab.TNotebook', tabposition='wn')
    style.configure('.', font=('Courier New','15','bold'), width=13)
    style.map('.', background=[('selected', '#8E96F1'), ('active', '#BFE8E0')])

    # Tabs
    tabs = Notebook(root, style='lefttab.TNotebook')

    # Tab for games
    frame_games = Frame(tabs, width=380, height=500)
    tabs.add(frame_games, text='Games')
    games_tab()

    # Tab for shutdown
    frame_shutdown = Frame(tabs, width=380, height=500)
    tabs.add(frame_shutdown, text='Shutdown')
    shutdown_tab()

    # Tab for stopwatch
    frame_stopwatch = Frame(tabs, width=380, height=500)
    tabs.add(frame_stopwatch, text='Stopwatch')
    stopwatch_tab()

    # Tab for yt-download
    frame_yt_download = Frame(tabs, width=380, height=500)
    tabs.add(frame_yt_download, text='YT-Download')
    yt_download_tab()

    # Tab for yt-download
    frame_convert_files = Frame(tabs, width=380, height=500)
    tabs.add(frame_convert_files, text='Convert files')
    convert_files_tab()

    # Tab for Screenshot
    frame_screenshot = Frame(tabs, width=380, height=500)
    tabs.add(frame_screenshot, text='Screenshot')
    screenshot_tab()

    # Tab for random generator
    frame_random_generator = Frame(tabs, width=380, height=500)
    tabs.add(frame_random_generator, text='Random')
    random_generator_tab(root)

    tabs.grid(row=0, column=0, sticky="nw")

# Patch History
def patch_history():
     messagebox.showinfo("Patch History", Info.patch_history)
   
def main():
    root = Tk()
    root.title("MultiTask")
    root.geometry("550x500")
    root.maxsize(550, 500)
    root.minsize(550, 500)

    # icon
    icon = resource_path(path_images + 'multitask_icon.ico')
    root.iconbitmap(icon)

    tabs_multitask(root)
    menu_multitask(root)
    
     # Line to separate the two columns
    Label(root, bd=2, height=500, relief=RAISED).place(x=168, width=2)
    root.mainloop()

if __name__ == '__main__':
    main() 