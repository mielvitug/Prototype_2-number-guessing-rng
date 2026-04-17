# Number Guessing Game + I mess around and hardcode it as much as possible 

import random # imports the python dependencies
import tkinter as tk # GUI library

# intialize
window = tk.Tk() # creates the main app window
window.title("Number Guessing Game") # Title inside the top of the window
window.geometry("500x700") # Starting size of the window

secret_number = random.randint(1,100)

# function show_guess
def show_guess():
    try: # attempts this code
        guess = int(guess_entry.get())
    except ValueError: # gets the specific error and returns with the statement
        result_label.config(text="Enter a valid number.")
        guess_entry.delete(0, tk.END) # deletes the entry in the box
        return
    
    if guess < 1 or guess > 100:
        result_label.config(text="Enter a number from 1 to 100 only.")
        return

    # if-elif-else block
    if guess > secret_number:
        result_label.config(text="Guess is too high")
    elif guess < secret_number:
        result_label.config(text="Guess is too low")
    else:
        result_label.config(text="You got it!!!")
    guess_entry.delete(0, tk.END)

# title_label
title_label = tk.Label(window, text="Guess the Number", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

# instructions_label
instructions_label = tk.Label(window, text="Enter any number from 1 to 100: ", font=("Arial", 12))
instructions_label.pack()

# guess_entry
guess_entry = tk.Entry(window, font=("Arial", 14))
guess_entry.pack(pady=10)

# guess_button
guess_button = tk.Button(window, text="Submit Guess", command=show_guess)
guess_button.pack(pady=10)

# result_label
result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack(pady=20)

guess_entry.bind("<Return>", show_guess)
window.mainloop() # starts the window