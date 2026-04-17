# Number Guessing Game + I mess around and hardcode it as much as possible 

import random # imports the python dependencies
import tkinter as tk # GUI library

window = tk.Tk() # creates the main app window
window.title("Number Guessing Game") # Title inside the top of the window
window.geometry("500x700") # Starting size of the window

def show_guess():
    guess = guess_entry.get()
    result_label.config(text=f"You typed: {guess}")

title_label = tk.Label(window, text="Guess the Number", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

instruction_label = tk.Label(window, text="Enter a number from 1 to 100", font=("Arial", 12))
instruction_label.pack()

guess_entry = tk.Entry(window, font=("Arial", 14))
guess_entry.pack(pady=10)

guess_button = tk.Button(window, text="Submit Guess", command=show_guess)
guess_button.pack(pady=10)

result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack(pady=20)

window.mainloop() # starts the window