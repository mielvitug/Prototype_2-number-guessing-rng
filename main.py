# Number Guessing Game + I mess around

import random  # imports the python dependencies
import tkinter as tk  # GUI library
from pathlib import Path

try:
    # Pillow helps decode GIFs into full frames so they don't appear distorted.
    from PIL import Image, ImageSequence, ImageTk
except ImportError:
    Image = None
    ImageSequence = None
    ImageTk = None

# initialize
window = tk.Tk()  # creates the main app window
window.title("Number Guessing Game ")  # Title inside the top of the window
window.geometry("560x860")  # Starting size of the window
window.minsize(520, 800)

BASE_DIR = Path(__file__).resolve().parent
IDLE_GIF_PATH = BASE_DIR / "emojis_data" / "com_emoji.gif"
WRONG_GIF_PATH = BASE_DIR / "emojis_data" / "no_emoji.gif"
WIN_GIF_PATH = BASE_DIR / "emojis_data" / "win_emoji.gif"
CRI_EMOJI_PATH = BASE_DIR / "emojis_data" / "cri_emoji.jpg"
GIF_SCALE = 0.7

RESULT_NORMAL_FONT = ("Arial", 20)
RESULT_BOLD_FONT = ("Arial", 20, "bold")
WINDOW_BG_TOP = "#170022"
WINDOW_BG_BOTTOM = "#05010d"
PANEL_BG = "#12061f"
PANEL_BORDER = "#8f3dff"
TEXT_PRIMARY = "#f7eeff"
TEXT_SECONDARY = "#d4b7ff"
ACCENT_PINK = "#ff4fd8"
ENTRY_BG = "#1d0a2f"
ENTRY_BORDER = "#9a4dff"
BUTTON_BG = "#2f0e4d"
BUTTON_ACTIVE_BG = "#4d1581"
GIF_PANEL_BG = "#09020f"
PANEL_RADIUS = 42
PANEL_REL_WIDTH = 0.90
PANEL_REL_HEIGHT = 0.94
CONTENT_REL_WIDTH = 0.82
CONTENT_REL_HEIGHT = 0.86

# Each list stores every frame for one animation.
wrong_frames = []
current_frames = []
idle_frames = []
win_frames = []

# reset_job stores the "go back to idle" timer so we can cancel it cleanly.
gif_index = 0
reset_job = None
guesses = 0
secret_number = random.randint(1, 100)


def show_guess(event=None):
    global guesses, reset_job

    try:  # attempts this code
        guess = int(guess_entry.get())
    except ValueError:  # gets the specific error and returns with the statement
        set_result_message("Enter a valid number.")
        guess_entry.delete(0, tk.END)  # deletes the entry in the box
        return

    if guess < 1 or guess > 100:
        set_result_message("Enter a number from 1 to 100 only.")
        guess_entry.delete(0, tk.END)
        return

    guesses += 1

    # Switch both the message and the active animation based on the guess.
    if guess > secret_number:
        set_result_message(f"Guess is too high. Attempts: {guesses}", bold_phrase="too high")
        play_animation(wrong_frames)

        if reset_job is not None:
            window.after_cancel(reset_job)

        reset_job = window.after(1500, show_idle)
    elif guess < secret_number:
        set_result_message(f"Guess is too low. Attempts: {guesses}", bold_phrase="too low")
        play_animation(wrong_frames)

        if reset_job is not None:
            window.after_cancel(reset_job)

        reset_job = window.after(1500, show_idle)
    else:
        set_result_message(f"You got it!!! Attempts: {guesses}")
        show_win()

    guess_entry.delete(0, tk.END)


def show_idle():
    global reset_job

    # If a return-to-idle timer is already waiting, clear it before showing idle.
    if reset_job is not None:
        window.after_cancel(reset_job)
        reset_job = None

    play_animation(idle_frames)


def show_win():
    global reset_job

    # Winning should cancel any pending wrong-answer timer so the win GIF stays on.
    if reset_job is not None:
        window.after_cancel(reset_job)
        reset_job = None

    play_animation(win_frames)


def set_result_message(message, bold_phrase=None):
    # A Text widget lets us style only part of the sentence.
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    result_text.insert("1.0", message)
    result_text.tag_add("center", "1.0", "end")

    if bold_phrase:
        start = message.find(bold_phrase)
        if start != -1:
            end = start + len(bold_phrase)
            result_text.tag_add("bold", f"1.{start}", f"1.{end}")

    result_text.config(state="disabled")


def hex_to_rgb(color):
    color = color.lstrip("#")
    return tuple(int(color[index:index + 2], 16) for index in (0, 2, 4))


def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def draw_rounded_panel(canvas, x1, y1, x2, y2, radius, fill, outline, border_width, tags):
    radius = max(1, int(radius))
    radius = min(radius, int((x2 - x1) / 2), int((y2 - y1) / 2))

    # Fill shapes
    canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=fill, outline="", tags=tags)
    canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=fill, outline="", tags=tags)
    canvas.create_oval(x1, y1, x1 + radius * 2, y1 + radius * 2, fill=fill, outline="", tags=tags)
    canvas.create_oval(x2 - radius * 2, y1, x2, y1 + radius * 2, fill=fill, outline="", tags=tags)
    canvas.create_oval(x1, y2 - radius * 2, x1 + radius * 2, y2, fill=fill, outline="", tags=tags)
    canvas.create_oval(x2 - radius * 2, y2 - radius * 2, x2, y2, fill=fill, outline="", tags=tags)

    # Border lines
    canvas.create_line(x1 + radius, y1, x2 - radius, y1, fill=outline, width=border_width, tags=tags)
    canvas.create_line(x1 + radius, y2, x2 - radius, y2, fill=outline, width=border_width, tags=tags)
    canvas.create_line(x1, y1 + radius, x1, y2 - radius, fill=outline, width=border_width, tags=tags)
    canvas.create_line(x2, y1 + radius, x2, y2 - radius, fill=outline, width=border_width, tags=tags)

    # Rounded border corners
    canvas.create_arc(
        x1, y1, x1 + radius * 2, y1 + radius * 2,
        start=90, extent=90, style=tk.ARC, outline=outline, width=border_width, tags=tags
    )
    canvas.create_arc(
        x2 - radius * 2, y1, x2, y1 + radius * 2,
        start=0, extent=90, style=tk.ARC, outline=outline, width=border_width, tags=tags
    )
    canvas.create_arc(
        x1, y2 - radius * 2, x1 + radius * 2, y2,
        start=180, extent=90, style=tk.ARC, outline=outline, width=border_width, tags=tags
    )
    canvas.create_arc(
        x2 - radius * 2, y2 - radius * 2, x2, y2,
        start=270, extent=90, style=tk.ARC, outline=outline, width=border_width, tags=tags
    )


def draw_gradient_background(event=None):
    width = background_canvas.winfo_width()
    height = background_canvas.winfo_height()

    if width <= 0 or height <= 0:
        return

    top_rgb = hex_to_rgb(WINDOW_BG_TOP)
    bottom_rgb = hex_to_rgb(WINDOW_BG_BOTTOM)

    background_canvas.delete("gradient")
    background_canvas.delete("glow")
    background_canvas.delete("panel")

    for y in range(height):
        ratio = y / max(height - 1, 1)
        color = tuple(
            int(top_rgb[index] + (bottom_rgb[index] - top_rgb[index]) * ratio)
            for index in range(3)
        )
        background_canvas.create_line(0, y, width, y, fill=rgb_to_hex(color), tags="gradient")

    # Neon glows to push the cyberpunk look without covering the controls.
    background_canvas.create_oval(-120, -80, 260, 260, fill="#32074d", outline="", tags="glow")
    background_canvas.create_oval(width - 260, height - 340, width + 120, height + 60, fill="#10153d", outline="", tags="glow")

    panel_width = width * PANEL_REL_WIDTH
    panel_height = height * PANEL_REL_HEIGHT
    x1 = (width - panel_width) / 2
    y1 = (height - panel_height) / 2
    x2 = x1 + panel_width
    y2 = y1 + panel_height

    draw_rounded_panel(
        background_canvas,
        x1,
        y1,
        x2,
        y2,
        PANEL_RADIUS,
        fill=PANEL_BG,
        outline=PANEL_BORDER,
        border_width=2,
        tags="panel",
    )


def load_gif_frames(path):
    if Image is not None and ImageSequence is not None and ImageTk is not None:
        return load_gif_frames_with_pillow(path)
    return load_gif_frames_with_tk(path)


def load_gif_frames_with_pillow(path):
    frames = []

    # Pillow gives us fully rendered frames, which avoids the warped/delta-frame
    # look some optimized GIFs get with plain tk.PhotoImage frame loading.
    with Image.open(path) as gif:
        for frame in ImageSequence.Iterator(gif):
            image = frame.copy().convert("RGBA")

            if GIF_SCALE != 1.0:
                width = max(1, int(image.width * GIF_SCALE))
                height = max(1, int(image.height * GIF_SCALE))
                image = image.resize((width, height), Image.LANCZOS)

            frames.append(ImageTk.PhotoImage(image))

    return frames


def load_gif_frames_with_tk(path):
    frames = []
    index = 0

    # Fallback loader when Pillow is unavailable.
    while True:
        try:
            frame = tk.PhotoImage(file=str(path), format=f"gif -index {index}")
            frames.append(frame)
            index += 1
        except tk.TclError:
            break

    return frames


def animate_gif():
    global gif_index

    if current_frames:
        # Show the current frame, then move to the next one in a loop.
        gif_label.config(image=current_frames[gif_index])
        gif_label.image = current_frames[gif_index]

        gif_index = (gif_index + 1) % len(current_frames)

        window.after(100, animate_gif)


def play_animation(frames):
    global current_frames, gif_index

    # Changing current_frames tells animate_gif which GIF to loop next.
    current_frames = frames
    gif_index = 0


window.configure(bg=WINDOW_BG_BOTTOM)

background_canvas = tk.Canvas(window, highlightthickness=0, bd=0)
background_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
background_canvas.bind("<Configure>", draw_gradient_background)

content_frame = tk.Frame(
    window,
    bg=PANEL_BG,
    bd=0,
    padx=28,
    pady=24,
)
content_frame.place(
    relx=0.5,
    rely=0.5,
    anchor="center",
    relwidth=CONTENT_REL_WIDTH,
    relheight=CONTENT_REL_HEIGHT,
)

cry_image = None
if Image is not None and ImageTk is not None and CRI_EMOJI_PATH.exists():
    cry_image_source = Image.open(CRI_EMOJI_PATH).convert("RGBA")
    cry_image_source.thumbnail((28, 28), Image.LANCZOS)
    cry_image = ImageTk.PhotoImage(cry_image_source)

eyebrow_frame = tk.Frame(content_frame, bg=PANEL_BG)
eyebrow_frame.pack(pady=(2, 14))

eyebrow_label_left = tk.Label(
    eyebrow_frame,
    text="GUESS THE NUMBER ",
    font=("Consolas", 11, "bold"),
    bg=PANEL_BG,
    fg=ACCENT_PINK,
)
eyebrow_label_left.pack(side="left")

if cry_image is not None:
    eyebrow_emoji_label = tk.Label(
        eyebrow_frame,
        image=cry_image,
        bg=PANEL_BG,
        bd=0,
    )
    eyebrow_emoji_label.image = cry_image
else:
    eyebrow_emoji_label = tk.Label(
        eyebrow_frame,
        text=" CRI ",
        font=("Consolas", 11, "bold"),
        bg=PANEL_BG,
        fg=TEXT_PRIMARY,
    )
eyebrow_emoji_label.pack(side="left")

eyebrow_label_right = tk.Label(
    eyebrow_frame,
    text=" TWIN",
    font=("Consolas", 11, "bold"),
    bg=PANEL_BG,
    fg=ACCENT_PINK,
)
eyebrow_label_right.pack(side="left")

# title_label
title_label = tk.Label(
    content_frame,
    text="Guess The Number",
    font=("Bahnschrift", 28, "bold"),
    bg=PANEL_BG,
    fg=TEXT_PRIMARY,
)
title_label.pack(pady=(0, 12))

# instructions_label
instructions_label = tk.Label(
    content_frame,
    text="Tap into the system. Enter a number from 1 to 100.",
    font=("Segoe UI", 12),
    bg=PANEL_BG,
    fg=TEXT_SECONDARY,
)
instructions_label.pack(pady=(0, 18))

entry_frame = tk.Frame(content_frame, bg=ENTRY_BORDER, padx=1, pady=1)
entry_frame.pack(pady=(0, 14))

# guess_entry
guess_entry = tk.Entry(
    entry_frame,
    font=("Consolas", 15),
    width=18,
    justify="center",
    relief="flat",
    bd=0,
    bg=ENTRY_BG,
    fg=TEXT_PRIMARY,
    insertbackground=ACCENT_PINK,
)
guess_entry.pack(ipady=8, ipadx=10)

# guess_button
guess_button = tk.Button(
    content_frame,
    text="Submit Guess",
    command=show_guess,
    font=("Consolas", 11, "bold"),
    relief="flat",
    bd=0,
    padx=18,
    pady=10,
    bg=BUTTON_BG,
    fg=TEXT_PRIMARY,
    activebackground=BUTTON_ACTIVE_BG,
    activeforeground=TEXT_PRIMARY,
    cursor="hand2",
)
guess_button.pack(pady=(0, 18))

# result_text
result_text = tk.Text(
    content_frame,
    width=30,
    height=2,
    font=RESULT_NORMAL_FONT,
    borderwidth=0,
    highlightthickness=0,
    bg=PANEL_BG,
    fg=TEXT_PRIMARY,
    wrap="word",
)
result_text.tag_configure("center", justify="center")
result_text.tag_configure("bold", font=RESULT_BOLD_FONT)
result_text.config(state="disabled")
result_text.pack(pady=(0, 18))

guess_entry.bind("<Return>", show_guess)

gif_frame = tk.Frame(
    content_frame,
    bg=GIF_PANEL_BG,
    highlightbackground=PANEL_BORDER,
    highlightthickness=1,
    padx=12,
    pady=12,
)
gif_frame.pack(pady=(6, 0))

gif_label = tk.Label(gif_frame, bg=GIF_PANEL_BG)
gif_label.pack()

# Load the idle, wrong-answer, and win animations before the loop starts.
idle_frames = load_gif_frames(IDLE_GIF_PATH)
wrong_frames = load_gif_frames(WRONG_GIF_PATH)
win_frames = load_gif_frames(WIN_GIF_PATH)

if idle_frames:
    show_idle()
    animate_gif()
else:
    gif_label.config(text="GIF not found", fg=TEXT_PRIMARY, bg=GIF_PANEL_BG)

window.after(10, draw_gradient_background)
guess_entry.focus_set()
window.mainloop()  # starts the window
