# Number Guessing Game + I mess around and hardcode it as much as possible 

import random # imports the python dependencies
import tkinter as tk # GUI library
from pathlib import Path

# intialize
window = tk.Tk() # creates the main app window
window.title("Number Guessing Game") # Title inside the top of the window
window.geometry("500x700") # Starting size of the window

BASE_DIR = PATH(__file__).resolve().parent
IDLE_GIF_PATH = BASE_DIR / "emojis_data" / "com_emoji.gif"

gif_index = 0

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
    
    guesses += 1

    # if-elif-else block
    if guess > secret_number:
        result_label.config(text=f"Guess is too high. Attempts: {guesses}")
    elif guess < secret_number:
        result_label.config(text=f"Guess is too low. Attempts: {guesses}")
    else:
        result_label.config(text=f"You got it!!! Attempts: {guesses}")

    guess_entry.delete(0, tk.END)

def load_gif_frames(path):
    frames = []
    index = 0

    while True:
        try:
            frame = tk.PhotoImage(file=str(path), format=f"gif -index {index}")
            frames.append(frame)
            index += 1
        except tk.TclError:
            break
    return frames

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

gif_label = tk.Label(window)
gif_label.pack(pady=20)

idle_frames = load_gif_frames(IDLE_GIF_PATH)

if idle_frames:
    gif_label.config(image=idle_frames[0])
    gif_label.image = idle_frames[0]
else: 
    gif_label.config(text="GIF not found")

window.mainloop() # starts the window=