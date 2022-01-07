from tkinter import *
from tkinter import ttk
from pygame import mixer
import datetime
from datetime import timedelta
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

path_sounds = 'Files/MultiTask_sounds/'


class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.milliseconds_timer = 0  # variable to increase the milliseconds for stopwatch
        self.var_on_off = False      # variable to on/off start_timer
        self.var_timer = False  # variable to on/off timer
        self.milliseconds_for_timer = -900  # total milliseconds to increase

        mixer.init()

    # Function to change label timer for "Timer" from spinbox
    def change_timer_spinbox(self):
        self.hour = (str(self.var_hour.get())).zfill(2)
        self.minute = (str(self.var_minute.get())).zfill(2)
        self.second = (str(self.var_second.get())).zfill(2)
        self.label_timer.config(text="{}:{}:{}".format(self.hour, self.minute, self.second))

    def timer_for_stopwatch(self):
        if self.var_on_off:
            self.start_time = datetime.datetime(2020, 5, 11, 0, 0, 0, 0)  # start the timer from 0, date doesn't matter
            self.time_increase = self.start_time + timedelta(milliseconds=self.milliseconds_timer)  # increase the time
            self.hour_stopwatch = self.time_increase.strftime("%H")  # get only hour
            self.minute_stopwatch = self.time_increase.strftime("%M")  # get only minute
            self.second_stopwatch = self.time_increase.strftime("%S")  # get only second
            self.millisecond_stopwatch = self.time_increase.strftime("%f")  # get only microsecond
            # remove the all "0" from microseconds and leave only two characters
            self.hour_stopwatch = (self.hour_stopwatch.rstrip("0")).ljust(2, "0")
            self.minute_stopwatch = (self.minute_stopwatch.rstrip("0")).ljust(2, "0")
            self.second_stopwatch = (self.second_stopwatch.rstrip("0")).ljust(2, "0")
            self.millisecond_stopwatch = (self.millisecond_stopwatch.rstrip("0")).ljust(1, "0")
            self.label_stopwatch.config(text="{}:{}:{}".format(self.hour_stopwatch, self.minute_stopwatch,
                                                               self.second_stopwatch))
            self.label_stopwatch_milliseconds.config(text="{}".format(self.millisecond_stopwatch))
            self.milliseconds_timer += 100
            self.label_stopwatch_milliseconds.after(100, self.timer_for_stopwatch)

    # start the stopwatch
    def start_for_stopwatch(self):
        self.var_on_off = True
        self.timer_for_stopwatch()
        self.start_stopwatch.config(state=DISABLED)

    # stop the stopwatch
    def stop_for_stopwatch(self):
        self.var_on_off = False
        self.start_stopwatch.config(state=ACTIVE)

    # reset the stopwatch
    def reset_for_stopwatch(self):
        self.var_on_off = True
        self.milliseconds_timer = 0
        self.label_stopwatch.config(text="00:00:00")
        self.label_stopwatch_milliseconds.config(text="0")

    def timer_for_timer(self):
        if self.var_timer:
            self.hour_timer = int(self.spinbox_hour.get())  # get hours from spinbox
            self.minute_timer = int(self.spinbox_minutes.get())  # get minutes from spinbox
            self.second_timer = int(self.spinbox_second.get())  # get seconds from spinbox
            self.set_timer = datetime.datetime(2020, 5, 11, self.hour_timer, self.minute_timer, self.second_timer)
            self.new_time = self.set_timer - timedelta(milliseconds=self.milliseconds_for_timer)  # start counting
            self.total_seconds_timer = self.hour_timer*3600000 + self.minute_timer*60000 + self.second_timer*1000
            if self.total_seconds_timer == self.milliseconds_for_timer:  # stop the timer if gets to 00:00:00
                self.var_timer = False
                if self.var_check_sound.get():
                    try:
                        mixer.music.play(-1)
                    except:
                        pass
                self.milliseconds_for_timer = -1000  # reset the milliseconds
                self.start_timer.config(state=ACTIVE)
                self.spinbox_hour.config(state="readonly")
                self.spinbox_minutes.config(state="readonly")
                self.spinbox_second.config(state="readonly")
            self.hours2 = self.new_time.strftime("%H")  # get the hour
            self.minute2 = self.new_time.strftime("%M")  # get the minute
            self.second2 = self.new_time.strftime("%S")  # get the second
            self.label_timer.config(text="{}:{}:{}".format(self.hours2, self.minute2, self.second2))  # display on the label
            self.milliseconds_for_timer += 100  # increase the milliseconds every loop
            self.label_timer.after(100, self.timer_for_timer)  # loop every 100 milliseconds

    # start the timer
    def start_for_timer(self):
        self.var_timer = True
        self.timer_for_timer()
        self.start_timer.config(state=DISABLED)
        self.spinbox_hour.config(state=DISABLED)
        self.spinbox_minutes.config(state=DISABLED)
        self.spinbox_second.config(state=DISABLED)

    # stop the timer
    def stop_for_timer(self):
        self.var_timer = False
        self.start_timer.config(state=ACTIVE)

    # reset the timer
    def reset_for_timer(self):
        self.hour_timer = int(self.spinbox_hour.get())  # get hours from spinbox
        self.minute_timer = int(self.spinbox_minutes.get())  # get minutes from spinbox
        self.second_timer = int(self.spinbox_second.get())  # get seconds from spinbox
        self.var_timer = False
        self.start_timer.config(state=ACTIVE)
        self.label_timer.config(text="{}:{}:{}".format(str(self.hour_timer).zfill(2), str(self.minute_timer).zfill(2),
                                                  str(self.second_timer).zfill(2)))
        self.milliseconds_for_timer = -900
        self.spinbox_hour.config(state="readonly")
        self.spinbox_minutes.config(state="readonly")
        self.spinbox_second.config(state="readonly")

    # Function to check if check button for sounds is enabled
    def enable_check_sounds(self):
        if self.var_check_sound.get():
            self.frame_playsound = Frame(self.frame_field_stopwatch)
            self.frame_playsound.place(x=100, y=225, width=275, height=25)
            mixer.init()
            self.alarm_sound = resource_path(path_sounds + "alarm_clock.wav")
            mixer.music.load(self.alarm_sound)  # get alarm_clock wav

            Button(self.frame_playsound, text="Test", command=mixer.music.play).place(x=160, y=0, height=20, width=50)  # play
            Button(self.frame_playsound, text="Stop", command=mixer.music.stop).place(x=218, y=0, height=20, width=50)  # stop
        if not self.var_check_sound.get():
            self.frame_playsound.destroy()  # destroy buttons "play" and "stop" if play_sound is unchecked

    # buttons, frames
    def buttons(self):
        self.frame_field_stopwatch = Frame(self.root, width=380, height=500, relief=RAISED)
        self.frame_field_stopwatch.place(x=0, y=0)

        # Label to display "Stopwatch"
        self.label_frame_stopwatch = LabelFrame(self.frame_field_stopwatch, text="Stopwatch", font=("", 15, "bold"),
                                           width=355, height=120)
        self.label_frame_stopwatch.place(x=10, y=5)

        # Label "Stopwatch" timer
        self.label_stopwatch = Label(self.label_frame_stopwatch, text="00:00:00", font=("", 50, "bold"))
        self.label_stopwatch.place(x=27, y=0)
        self.label_stopwatch_milliseconds = Label(self.label_frame_stopwatch, text="0", font=("", 30, "bold"))
        self.label_stopwatch_milliseconds.place(x=297, y=25)

        # Button "Start" for Stopwatch
        self.start_stopwatch = Button(self.frame_field_stopwatch, text="Start", bd=3, font=("", 18, "bold"),
                                 command=self.start_for_stopwatch)
        self.start_stopwatch.place(x=10, y=150, width=90)

        # Button "Stop" for Stopwatch
        self.stop_stopwatch = Button(self.frame_field_stopwatch, text="Stop", bd=3, font=("", 18, "bold"),
                                command=self.stop_for_stopwatch)
        self.stop_stopwatch.place(x=143, y=150, width=90)

        # Button "reset" for Stopwatch
        self.reset_stopwatch = Button(self.frame_field_stopwatch, text="Reset", bd=3, font=("", 18, "bold"),
                                 command=self.reset_for_stopwatch)
        self.reset_stopwatch.place(x=275, y=150, width=90)

        # Label to split between "Stopwatch" and "Timer"
        Label(self.frame_field_stopwatch, bd=1, relief=RAISED).place(x=0, y=220, width=375, height=3)

        # Label to display "Timer"
        self.label_frame_timer = LabelFrame(self.frame_field_stopwatch, text="Timer", font=("", 15, "bold"), width=355,
                                       height=120)
        self.label_frame_timer.place(x=10, y=285)

        # Label "Timer" timer
        self.label_timer = Label(self.label_frame_timer, text="00:00:00", font=("", 50, "bold"))
        self.label_timer.place(x=45, y=0)

        # Button "Start" for Timer
        self.start_timer = Button(self.frame_field_stopwatch, text="Start", bd=3, font=("", 18, "bold"),
                                  command=self.start_for_timer)
        self.start_timer.place(x=10, y=425, width=90)

        # Button "Stop" for Timer
        self.stop_timer = Button(self.frame_field_stopwatch, text="Stop", bd=3, font=("", 18, "bold"),
                                 command=self.stop_for_timer)
        self.stop_timer.place(x=143, y=425, width=90)

        # Button "reset" for Timer
        self.reset_timer = Button(self.frame_field_stopwatch, text="Reset", bd=3, font=("", 18, "bold"),
                                  command=self.reset_for_timer)
        self.reset_timer.place(x=275, y=425, width=90)

        # Spinbox for hours
        self.var_hour = StringVar()
        self.spinbox_hour = Spinbox(self.frame_field_stopwatch, from_=0, to=23, state="readonly", font=("", 20),
                                    textvariable=self.var_hour, command=self.change_timer_spinbox)
        self.spinbox_hour.place(x=70, y=250, width=57)

        # Spinbox for minutes
        self.var_minute = StringVar()
        self.spinbox_minutes = Spinbox(self.frame_field_stopwatch, from_=0, to=59, state="readonly", font=("", 20),
                                       textvariable=self.var_minute, command=self.change_timer_spinbox)
        self.spinbox_minutes.place(x=165, y=250, width=57)

        # Spinbox for seconds
        self.var_second = StringVar()
        self.spinbox_second = Spinbox(self.frame_field_stopwatch, from_=0, to=59, state="readonly", font=("", 20),
                                      textvariable=self.var_second, command=self.change_timer_spinbox)
        self.spinbox_second.place(x=260, y=250, width=57)

        # Check button to play sound when the timer is 00:00:00
        self.var_check_sound = IntVar()
        self.check_sound = Checkbutton(self.frame_field_stopwatch, text="Enable sound", variable=self.var_check_sound,
                                       command=self.enable_check_sounds)
        self.check_sound.place(x=5, y=225)