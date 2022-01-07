from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import datetime
from datetime import timedelta
import os
import sys
from PIL import ImageTk, Image

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

path_images = 'Files/MultiTask_images/'    

class Shutdown:
    def __init__(self, root):
        self.root = root
        self.run = False

    # Function for showing time
    def show_time(self):
        self.time1 = datetime.datetime.now().strftime("%H:%M:%S   %d-%b-%Y")
        self.label_show_time.config(text=self.time1)
        self.label_show_time.after(100, self.show_time)

    # Function to run o first button
    def first_button_set(self):
        self.year = int(datetime.datetime.now().strftime("%Y"))
        self.month = int(datetime.datetime.now().strftime("%m"))
        self.month_name = datetime.datetime.now().strftime("%b")
        self.day = int(datetime.datetime.now().strftime("%d"))
        self.hours = int(self.var_hour.get())
        self.minutes = int(self.var_minute.get())
        self.seconds = int(self.var_second.get())
        self.current_time = datetime.datetime.now()
        self.set_time = datetime.datetime(self.year, self.month, self.day, self.hours, self.minutes, self.seconds)
        self.show_only_time = datetime.time(self.hours, self.minutes, self.seconds)
        self.time_remaining = self.set_time - self.current_time
        self.time_in_seconds = int(self.time_remaining.total_seconds())

        # Execute windows command
        if self.set_time > self.current_time:
            os.system("shutdown -a")
            if self.menu_combobox.get() == "Shutdown":
                self.run = True
                os.system("shutdown /s /t {}".format(self.time_in_seconds))
                self.commands_to_run()
            elif self.menu_combobox.get() == "Restart":
                self.run = True
                os.system("shutdown /r /t {}".format(self.time_in_seconds))
                self.commands_to_run()
        else:
            messagebox.showerror("Input error", "You can't set the time in past")

    # Function to change the label irl for remaining time
    def time_shutdown_after(self):
        if self.run:
            self.year = int(datetime.datetime.now().strftime("%Y"))
            self.month = int(datetime.datetime.now().strftime("%m"))
            self.month_name = datetime.datetime.now().strftime("%b")
            self.day = int(datetime.datetime.now().strftime("%d"))
            self.hours = int(self.var_hour.get())
            self.minutes = int(self.var_minute.get())
            self.seconds = int(self.var_second.get())
            self.current_time = datetime.datetime.now()
            self.set_time = datetime.datetime(self.year, self.month, self.day, self.hours, self.minutes, self.seconds)
            self.show_only_time = datetime.time(self.hours, self.minutes, self.seconds)
            self.time_remaining = self.set_time - self.current_time
            self.time_in_seconds = int(self.time_remaining.total_seconds())
            self.days1 = self.time_in_seconds // 86400
            self.hours1 = (self.time_in_seconds - self.days1 * 86400) // 3600
            self.minutes1 = (self.time_in_seconds - self.days1 * 86400 - self.hours1 * 3600) // 60
            self.seconds1 = self.time_in_seconds - self.days1 * 86400 - self.hours1 * 3600 - self.minutes1 * 60
            self.label_shutdown_after.config(text="  {}:{}:{}                         ".format(str(self.hours1).zfill(2),
                                             str(self.minutes1).zfill(2), str(self.seconds1).zfill(2)))
            self.label_shutdown_after.after(100, self.time_shutdown_after)

    # Commands to run when first set button is pressed
    def commands_to_run(self):
        # Change label text and display messagebox
        self.days1 = self.time_in_seconds // 86400
        self.hours1 = (self.time_in_seconds - self.days1 * 86400) // 3600
        self.minutes1 = (self.time_in_seconds - self.days1 * 86400 - self.hours1 * 3600) // 60
        self.seconds1 = self.time_in_seconds - self.days1 * 86400 - self.hours1 * 3600 - self.minutes1 * 60
        messagebox.showinfo("{} enabled".format(self.menu_combobox.get()),  # message info about shutdown time
                            "Your computer will {} at: {}"
                            "\nRemaining time:  {}:{}:{}".format(self.menu_combobox.get(), self.show_only_time,
                                                                 str(self.hours1).zfill(2),
                                                                 str(self.minutes1).zfill(2),
                                                                 str(self.seconds1).zfill(2)))
        self.label_shutdown_at.config(text="{}     {}-{}-{}".format(self.show_only_time, str(self.day), self.month_name,
                                                                    str(self.year)))
        self.menu_combobox.config(state=DISABLED)  # disable  menu Combobox
        self.scale_hour.config(state=DISABLED)  # disable scale for hour
        self.scale_minute.config(state=DISABLED)  # disable scale for minute
        self.scale_second.config(state=DISABLED)  # disable scale for second
        self.entry_hour.config(state=DISABLED)  # disable entry for hour
        self.entry_minute.config(state=DISABLED)  # disable entry for minute
        self.entry_second.config(state=DISABLED)  # disable entry for second
        self.set_button_shutdown1.config(state=DISABLED)  # disable first button set
        self.set_button_shutdown2.config(state=DISABLED)  # disable second button set
        self.time_shutdown_after()  # show time ramaining irl

    # Function to run on the second button
    def second_button_set(self):
        # Getting imput from user entry
        try:
            self.hours3 = int(self.entry_hour.get())
            self.minutes3 = int(self.entry_minute.get())
            self.seconds3 = int(self.entry_second.get())

            self.current_time = datetime.datetime.now()
            self.set_time2 = self.current_time + datetime.timedelta(hours=self.hours3, minutes=self.minutes3,
                                                                    seconds=self.seconds3)
            self.time_remaining = self.set_time2 - self.current_time
            self.time_in_seconds = int(self.time_remaining.total_seconds())

            if self.set_time2 > self.current_time:
                os.system("shutdown -a")
                if self.menu_combobox.get() == "Shutdown":
                    self.run = True
                    os.system("shutdown /s /t {}".format(self.time_in_seconds))
                    self.commands_to_run_button2()
                elif self.menu_combobox.get() == "Restart":
                    self.run = True
                    os.system("shutdown /r /t {}".format(self.time_in_seconds))
                    self.commands_to_run_button2()
        except:
            messagebox.showerror("Error", "Invalid input, only numbers are acceptable")

    # Label to change time ramaining irl
    def time_shutdown_after_button2(self):
        if self.run:
            self.current_time = datetime.datetime.now()
            self.time_remaining = self.set_time2 - self.current_time
            self.time_in_seconds = int(self.time_remaining.total_seconds())
            self.days2 = self.time_in_seconds // 86400
            self.hours2 = (self.time_in_seconds - self.days2 * 86400) // 3600
            self.minutes2 = (self.time_in_seconds - self.days2 * 86400 - self.hours2 * 3600) // 60
            self.seconds2 = self.time_in_seconds - self.days2 * 86400 - self.hours2 * 3600 - self.minutes2 * 60
            self.label_shutdown_after.config(text="{} days and  {}:{}:{}    ".format(self.days2, str(self.hours2).zfill(2),
                                             str(self.minutes2).zfill(2), str(self.seconds2).zfill(2)))
            self.label_shutdown_after.after(100, self.time_shutdown_after_button2)

    # Function to change text label of displaying the set time and show messagebox
    def commands_to_run_button2(self):
        self.year = self.set_time2.strftime("%Y")
        self.month = self.set_time2.strftime("%b")
        self.day = self.set_time2.strftime("%d")
        self.hour = self.set_time2.strftime("%H")
        self.minute = self.set_time2.strftime("%M")
        self.second = self.set_time2.strftime("%S")
        self.days1 = self.time_in_seconds // 86400
        self.hours1 = (self.time_in_seconds - self.days1 * 86400) // 3600
        self.minutes1 = (self.time_in_seconds - self.days1 * 86400 - self.hours1 * 3600) // 60
        self.seconds1 = self.time_in_seconds - self.days1 * 86400 - self.hours1 * 3600 - self.minutes1 * 60
        messagebox.showinfo("{} enabled".format(self.menu_combobox.get()),
                                 "Your computer will {} at:  {}:{}:{}   {}-{}-{}"
                                 "\nRemaining time:  {} days and  {}:{}:{}".format(self.menu_combobox.get(), self.hour,
                                                                                   self.minute, self.second, self.day,
                                                                                   self.month, self.year, self.days1,
                                                                                   str(self.hours1).zfill(2),
                                                                                   str(self.minutes1).zfill(2),
                                                                                   str(self.seconds1).zfill(2)))
        self.label_shutdown_at.config(text="{}:{}:{}   {}-{}-{}".format(self.hour, self.minute, self.second, self.day,
                                                                        self.month, self.year))
        self.menu_combobox.config(state=DISABLED)  # disable  menu Combobox
        self.scale_hour.config(state=DISABLED)  # disable scale for hour
        self.scale_minute.config(state=DISABLED)  # disable scale for minute
        self.scale_second.config(state=DISABLED)  # disable scale for second
        self.entry_hour.config(state=DISABLED)  # disable entry for hour
        self.entry_minute.config(state=DISABLED)  # disable entry for minute
        self.entry_second.config(state=DISABLED)  # disable entry for second
        self.set_button_shutdown1.config(state=DISABLED)  # disable first button set
        self.set_button_shutdown2.config(state=DISABLED)  # disable second button set
        self.time_shutdown_after_button2()  # command to change remaining time irl

    # Cancel button function
    def cancel_button(self):
        self.run = False
        os.system("shutdown -a")
        self.menu_combobox.config(state="readonly")  # disable  menu Combobox
        self.scale_hour.config(state=NORMAL)  # disable scale for hour
        self.scale_minute.config(state=NORMAL)  # disable scale for minute
        self.scale_second.config(state=NORMAL)  # disable scale for second
        self.entry_hour.config(state=NORMAL)  # disable entry for hour
        self.entry_minute.config(state=NORMAL)  # disable entry for minute
        self.entry_second.config(state=NORMAL)  # disable entry for second
        self.set_button_shutdown1.config(state=NORMAL)  # disable first button set
        self.set_button_shutdown2.config(state=NORMAL)  # disable second button set
        self.label_shutdown_at.config(text="")
        self.label_shutdown_after.config(text="")

    def update_time_shutdown(self, s):
        self.shutdown_timer.config(text="{}:{}:{}".format(self.var_hour.get().zfill(2), self.var_minute.get().zfill(2),
                                   self.var_second.get().zfill(2)))

    # Combobox for Shutdown/Restart/Log off/Hibernate
    def change_labels(self, x):
        if self.menu_combobox.get() == "Shutdown":
            self.label1.config(text="Shutdown after: ")
            self.label2.config(text="Shutdown after: ")
            self.label3.config(text="Shutdown after: ")
            self.label4.config(text="Shutdown at: ")
            self.label5.config(text="Shutdown after: ")
        elif self.menu_combobox.get() == "Restart":
            self.label1.config(text="Restart after: ")
            self.label2.config(text="Restart after: ")
            self.label3.config(text="Restart after: ")
            self.label4.config(text="Restart at: ")
            self.label5.config(text="Restart after: ")

    # Buttons,frames and labels
    def buttons(self):
        # Frame field shutdown
        self.frame_field_shutdown = Frame(self.root, width=380, height=500, relief=RAISED)
        self.frame_field_shutdown.place(x=0, y=0)

        # Label for showing time
        self.label_show_time = Label(self.frame_field_shutdown, bd=1, font=("", 14, "bold"))
        self.label_show_time.place(x=120, y=0)

        # Label for showing the shutdown time
        self.shutdown_timer = Label(self.frame_field_shutdown, text="00:00:00", font=('', 16, "bold"))
        self.shutdown_timer.place(x=145, y=150, width=130, height=40)

        # Button for set timer
        self.set_image1 = resource_path(path_images + "confirm_button.png")
        self.set_image = ImageTk.PhotoImage(Image.open(self.set_image1))
        self.set_button_shutdown1 = Button(self.frame_field_shutdown, image=self.set_image,
                                           command=self.first_button_set)
        self.set_button_shutdown1.place(x=297, y=64, height=70, width=70)

        # Button 2 for set timer
        self.set_button_shutdown2 = Button(self.frame_field_shutdown, image=self.set_image,
                                           command=self.second_button_set)
        self.set_button_shutdown2.place(x=297, y=220, height=70, width=70)

        # Button for cancel
        self.cancel_image1 = resource_path(path_images + "cancel_button.png")
        self.cancel_image = ImageTk.PhotoImage(Image.open(self.cancel_image1))
        self.cancel_button = Button(self.frame_field_shutdown, text="Cancel", image=self.cancel_image, compound="left",
                                    font=("", 23, "bold"), fg="red", activeforeground="red", command=self.cancel_button)
        self.cancel_button.place(x=105, y=317, width=165, height=65)

        # Labels for Hour, Minute and Seconds
        Label(self.frame_field_shutdown, text="H: ", font=("", 12, "bold")).place(x=100, y=48)
        Label(self.frame_field_shutdown, text="M: ", font=("", 12, "bold")).place(x=100, y=88)
        Label(self.frame_field_shutdown, text="S: ", font=("", 12, "bold")).place(x=100, y=127)

        # Current time label
        self.current_time = Label(self.frame_field_shutdown, text="Current time:", font=("", 12))
        self.current_time.place(x=5, y=1)

        # Label shutdown and hours/minutes/seconds
        Label(self.frame_field_shutdown, bd=1, relief=RAISED).place(x=0, y=185, height=5,
                                                                    width=377)  # Line label separator
        Label(self.frame_field_shutdown, bd=1, relief=RAISED).place(x=0, y=390, height=5,
                                                                    width=377)  # Line2 label separator

        self.label1 = Label(self.frame_field_shutdown, text="Shutdown after:", font=("", 14))
        self.label1.place(x=5, y=200)
        self.label2 = Label(self.frame_field_shutdown, text="Shutdown after:", font=("", 14))
        self.label2.place(x=5, y=240)
        self.label3 = Label(self.frame_field_shutdown, text="Shutdown after:", font=("", 14))
        self.label3.place(x=5, y=280)

        # Labels to show when the pc will shutdown
        self.label4 = Label(self.frame_field_shutdown, text="Shutdown at: ", font=("", 14))
        self.label4.place(x=5, y=408)
        self.label5 = Label(self.frame_field_shutdown, text="Remaining time: ", font=("", 14))
        self.label5.place(x=5, y=452)
        self.label_shutdown_at = Label(self.frame_field_shutdown, font=("", 14))
        self.label_shutdown_at.place(x=150, y=408)
        self.label_shutdown_after = Label(self.frame_field_shutdown, font=("", 14))
        self.label_shutdown_after.place(x=150, y=452)

        self.menu_combobox = ttk.Combobox(self.frame_field_shutdown, values=["Shutdown", "Restart"],
                                          font=("", 11), state="readonly")
        self.menu_combobox.place(x=0, y=90, width=95)
        self.menu_combobox.current(0)
        self.menu_combobox.bind("<<ComboboxSelected>>", self.change_labels)

        # Labels
        Label(self.frame_field_shutdown, font=("", 14), text="hours").place(x=200, y=200)
        Label(self.frame_field_shutdown, font=("", 14), text="minutes").place(x=200, y=240)
        Label(self.frame_field_shutdown, font=("", 14), text="seconds").place(x=200, y=280)

        # Entry for hour/minute/second
        self.var_hour_entry = StringVar()
        self.entry_hour = Entry(self.frame_field_shutdown, font=("", 15), textvariable=self.var_hour_entry,
                                justify=CENTER)
        self.entry_hour.place(x=140, y=203, width=60, height=25)

        self.var_minute_entry = StringVar()
        self.entry_minute = Entry(self.frame_field_shutdown, font=("", 15), textvariable=self.var_minute_entry,
                                  justify=CENTER)
        self.entry_minute.place(x=140, y=243, width=60, height=25)

        self.var_second_entry = StringVar()
        self.entry_second = Entry(self.frame_field_shutdown, font=("", 15), textvariable=self.var_second_entry,
                                  justify=CENTER)
        self.entry_second.place(x=140, y=283, width=60, height=25)

        # Scale for setting hour
        self.var_hour = StringVar()
        self.scale_hour = Scale(self.frame_field_shutdown, from_=0, to=23, orient=HORIZONTAL,
                                command=self.update_time_shutdown, variable=self.var_hour)
        self.scale_hour.place(x=130, y=30, width=160)

        # Scale for setting minute
        self.var_minute = StringVar()
        self.scale_minute = Scale(self.frame_field_shutdown, from_=0, to=59, orient=HORIZONTAL,
                                  command=self.update_time_shutdown, variable=self.var_minute)
        self.scale_minute.place(x=130, y=70, width=160)

        # Scale for setting seccond
        self.var_second = StringVar()
        self.scale_second = Scale(self.frame_field_shutdown, from_=0, to=59, orient=HORIZONTAL,
                                  command=self.update_time_shutdown, variable=self.var_second)
        self.scale_second.place(x=130, y=110, width=160)

        # Default user input time ("0")
        self.entry_hour.insert(0, "0")
        self.entry_minute.insert(0, "0")
        self.entry_second.insert(0, "0")

        self.show_time()
