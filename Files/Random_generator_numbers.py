from tkinter import *
import random
from tkinter import messagebox

class Random_Generator_Numbers:
    def __init__(self, frame_content):
        self.frame_content = frame_content

    def clear_button_unchecked(self):
        if self.var_clear_action.get() == 0:
            self.clear()

    def clear(self):
        self.text_results.delete(1.0, END)
        self.count = 0

    # Function "Generate" button
    def generate(self):
        try:
            self.list_of_numbers = range(int(self.spin_min.get()), (int(self.spin_max.get()) + 1))  # range numbers
            self.random_numbers = random.sample(self.list_of_numbers, int(self.numbers.get()))
            self.random_numbers1 = str(self.random_numbers).replace("[", "")  # delete "[" and "]"
            self.random_numbers1 = str(self.random_numbers1).replace("]", "")
            self.sorted_numbers = sorted(self.random_numbers)
            self.sorted_numbers = str(self.sorted_numbers).replace("[", "")  # delete "[" and "]" for sorted numbers
            self.sorted_numbers = str(self.sorted_numbers).replace("]", "")
            self.reverse_numbers = sorted(self.random_numbers, reverse=True)  # delete "[" and "]" for sorted numbers
            self.reverse_numbers = str(self.reverse_numbers).replace("[", "")
            self.reverse_numbers = str(self.reverse_numbers).replace("]", "")

            if self.var_clear_action.get():  # Function to check if "One line numbers" is checked
                self.clear()
                if self.var_sort.get():
                    self.text_results.insert(END, self.sorted_numbers)
                elif self.var_reverse.get():
                    self.text_results.insert(END, self.reverse_numbers)
                else:
                    self.text_results.insert(END, self.random_numbers1)
            else:
                if self.var_sort.get():
                    self.count += 1
                    self.text_results.insert(END, str(self.count) + ".   " + self.sorted_numbers + "\n")
                elif self.var_reverse.get():
                    self.count += 1
                    self.text_results.insert(END, str(self.count) + ".   " + self.reverse_numbers + "\n")
                else:
                    self.count += 1
                    self.text_results.insert(END, str(self.count) + ".   " + self.random_numbers1 + "\n")
        except:
            messagebox.showerror("Error", "Invalid input")

    def sorted_select(self):  # Function to uncheck reverse_numbers
        self.reverse_numbers_button.deselect()

    def reverse_select(self):  # Function to uncheck sorted_numbers
        self.sorted_numbers_button.deselect()

    def change_font_text(self, x):  # Function to change font size of text field
        self.text_results.config(font=("", self.var_font_scale.get()))

    def buttons(self):
        # Frame context for numbers
        self.frame_context_numbers = Frame(self.frame_content, width=380, height=500, relief=RAISED)
        self.frame_context_numbers.place(x=0, y=0)

        # result counting
        self.count = 0

        # Frame for text and scrollbar
        self.frame_scroll = Frame(self.frame_context_numbers, bd=0, width=360, height=250, relief=RAISED)
        self.frame_scroll.place(x=5, y=205)

        # Label and spinbox for "Min"
        self.spin_min = Spinbox(self.frame_context_numbers, from_=1, to=1000, width=5, font=("", 15))
        self.spin_min.place(x=30, y=40)
        self.label_from = Label(self.frame_context_numbers, text="Min", font=("", 15))
        self.label_from.place(x=50, y=5)

        # Label and spinbox for "Max"
        self.spin_max = Spinbox(self.frame_context_numbers, from_=1, to=1000, width=5, font=("", 15))
        self.spin_max.place(x=150, y=40)
        self.label_from = Label(self.frame_context_numbers, text="Max", font=("", 15))
        self.label_from.place(x=167, y=5)

        # Label and spinbox for "Numbers"
        self.numbers = Spinbox(self.frame_context_numbers, from_=1, to=1000, width=5, font=("", 15,))
        self.numbers.place(x=270, y=40)
        self.label_from = Label(self.frame_context_numbers, text="Numbers", font=("", 15))
        self.label_from.place(x=265, y=5)

        # Button "Generate"
        button_generate = Button(self.frame_context_numbers, bg="#7BEA63", text="Generate", width=9,
                                 font=("", 20, "bold"), bd=2, height=1, command=self.generate)
        button_generate.place(x=200, y=100)

        # Check button for sorted numbers
        self.var_sort = IntVar()
        self.sorted_numbers_button = Checkbutton(self.frame_context_numbers, text="Sort numbers", font=("", 13),
                                                 variable=self.var_sort, command=self.sorted_select)
        self.sorted_numbers_button.place(x=5, y=110)

        # Check button for reverse sorted numbers
        self.var_reverse = IntVar()
        self.reverse_numbers_button = Checkbutton(self.frame_context_numbers, text="Reverse numbers", font=("", 13),
                                                  variable=self.var_reverse, command=self.reverse_select)
        self.reverse_numbers_button.place(x=5, y=140)

        # One line of numbers button
        self.var_clear_action = IntVar()
        clear_button_action = Checkbutton(self.frame_context_numbers, text="One line of numbers", font=("", 13),
                                          variable=self.var_clear_action, command=self.clear_button_unchecked)
        clear_button_action.place(x=5, y=80)

        # Font scale
        self.var_font_scale = IntVar()
        font_scale = Scale(self.frame_context_numbers, from_=5, to=150, width=15, orient=HORIZONTAL,
                           variable=self.var_font_scale, length=150, command=self.change_font_text)
        font_scale.place(x=100, y=160)

        # Font text scale button
        font_text = Label(self.frame_context_numbers, text="Font size", font=("", 13, "bold"))
        font_text.place(x=5, y=175)

        # Text window
        self.text_results = Text(self.frame_scroll, bd=2, font=("", 13))
        self.text_results.place(x=2, y=130, anchor=W, width=340, height=255)

        # Scrollbar text
        self.scrollbar_text = Scrollbar(self.frame_scroll, command=self.text_results.yview)
        self.scrollbar_text.place(x=358, y=0, anchor=NE, height=255)
        self.text_results.config(yscrollcommand=self.scrollbar_text.set)

        # Clear Button
        clear_button = Button(self.frame_context_numbers, text="Clear", font=("", 13), command=self.clear)
        clear_button.place(x=3, y=460)