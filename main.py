import random
import tkinter as tk
from pathlib import Path

try:
    from PIL import Image, ImageSequence, ImageTk
except ImportError:
    Image = None
    ImageSequence = None
    ImageTk = None


BASE_DIR = Path(__file__).resolve().parent
EMOJI_DIR = BASE_DIR / "emojis_data"
IDLE_GIF_PATH = EMOJI_DIR / "com_emoji.gif"
HIGH_GIF_PATH = EMOJI_DIR / "no_emoji.gif"
WIN_GIF_PATH = EMOJI_DIR / "win_emoji.gif"
REACTION_DURATION_MS = 1500

secret_number = random.randint(1, 100)
guesses = 0
idle_frames = []
high_frames = []
win_frames = []
current_frames = []
gif_index = 0
animation_job = None
reset_job = None


def load_gif_frames(path):
    if Image is not None and ImageSequence is not None and ImageTk is not None:
        return load_gif_frames_with_pillow(path)
    return load_gif_frames_with_tk(path)


def load_gif_frames_with_pillow(path):
    frames = []

    # Pillow gives us full frames instead of GIF delta slices, which keeps the
    # idle animation from looking warped when it loops.
    with Image.open(path) as gif:
        for frame in ImageSequence.Iterator(gif):
            image = frame.convert("RGBA")
            duration = frame.info.get("duration", gif.info.get("duration", 100))
            frames.append({"image": ImageTk.PhotoImage(image), "duration": max(duration, 20)})

    return frames


def load_gif_frames_with_tk(path):
    frames = []
    index = 0

    while True:
        try:
            image = tk.PhotoImage(file=str(path), format=f"gif -index {index}")
            frames.append({"image": image, "duration": 100})
            index += 1
        except tk.TclError:
            break

    return frames


def get_animation_size(*animations):
    width = 0
    height = 0

    for animation in animations:
        for frame in animation:
            image = frame["image"]
            width = max(width, image.width())
            height = max(height, image.height())

    return width, height


def animate_gif():
    global gif_index, animation_job

    if not current_frames:
        gif_label.config(image="", text="GIF not found")
        animation_job = None
        return

    frame = current_frames[gif_index]
    gif_label.config(image=frame["image"], text="")
    gif_index = (gif_index + 1) % len(current_frames)
    animation_job = window.after(frame["duration"], animate_gif)


def play_frames(frames):
    global current_frames, gif_index, animation_job

    if animation_job is not None:
        window.after_cancel(animation_job)
        animation_job = None

    current_frames = frames
    gif_index = 0

    if current_frames:
        animate_gif()
    else:
        gif_label.config(image="", text="GIF not found")


def show_idle():
    global reset_job

    if reset_job is not None:
        window.after_cancel(reset_job)
        reset_job = None

    play_frames(idle_frames)


def show_no_no():
    global reset_job

    play_frames(high_frames)

    if reset_job is not None:
        window.after_cancel(reset_job)

    reset_job = window.after(REACTION_DURATION_MS, show_idle)


def show_win():
    global reset_job

    if reset_job is not None:
        window.after_cancel(reset_job)
        reset_job = None

    play_frames(win_frames)


def check_guess(event=None):
    global guesses

    value = guess_entry.get()

    try:
        guess = int(value)
    except ValueError:
        result_label.config(text="Wrong input. Try again.")
        guess_entry.delete(0, tk.END)
        show_idle()
        return

    if guess < 1 or guess > 100:
        result_label.config(text="Wrong input. Enter a value from 1-100 only.")
        guess_entry.delete(0, tk.END)
        show_idle()
        return

    guesses += 1

    if guess > secret_number:
        result_label.config(text="You guessed too high.")
        show_no_no()
    elif guess < secret_number:
        result_label.config(text="You guessed too low.")
        show_no_no()
    else:
        result_label.config(
            text=f"You have guessed it!\nYou rolled: {guesses} times!\nSystem rolled: {secret_number}"
        )
        show_win()
        guess_entry.configure(state="disabled")
        guess_button.configure(state="disabled")

    guess_entry.delete(0, tk.END)


def focus_game_window():
    # Briefly mark the window topmost so Windows brings it forward on launch,
    # then return it to normal stacking behavior.
    window.deiconify()
    window.lift()
    window.attributes("-topmost", True)
    guess_entry.focus_force()
    window.after(200, lambda: window.attributes("-topmost", False))


window = tk.Tk()
window.title("Number Guessing Game")

idle_frames = load_gif_frames(IDLE_GIF_PATH)
high_frames = load_gif_frames(HIGH_GIF_PATH)
win_frames = load_gif_frames(WIN_GIF_PATH)
gif_width, gif_height = get_animation_size(idle_frames, high_frames, win_frames)

window_width = max(560, gif_width + 60)
window_height = max(760, gif_height + 260)
window.geometry(f"{window_width}x{window_height}")
window.minsize(window_width, window_height)

title_label = tk.Label(window, text="Guess the Number", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

instruction_label = tk.Label(window, text="Enter a number from 1 to 100")
instruction_label.pack()

guess_entry = tk.Entry(window, font=("Arial", 14))
guess_entry.pack(pady=10)

guess_button = tk.Button(window, text="Submit Guess", command=check_guess)
guess_button.pack()

result_label = tk.Label(window, text="", font=("Arial", 12))
result_label.pack(pady=15)

gif_frame = tk.Frame(window, width=max(gif_width, 1), height=max(gif_height, 1))
gif_frame.pack(pady=10)
gif_frame.pack_propagate(False)

gif_label = tk.Label(gif_frame)
gif_label.pack(expand=True)

show_idle()
guess_entry.bind("<Return>", check_guess)
guess_entry.focus_set()
window.after(150, focus_game_window)

window.mainloop()
