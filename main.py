import tkinter
from tkinter import *
import math
import json
from datetime import datetime
import pygame

# ---------------------------- CONSTANTS ------------------------------- #

FONT_NAME = "Courier"
reps = 0
timer = None
color_options = [
    {"default": {"bg": "#f7f5dd", "work": "#9bdeac", "short": "#e2979c", "long": "#e7305b"}},
    {"dark_mode": {"bg": "#3f3939", "work": "#bcbcbc", "short": "#74666d", "long": "#a4b885"}},
    {"d_faves": {"bg": "#601ba2", "work": "#35ea4D", "short": "#9fd329", "long": "#d9d2e9"}},
    {"desert": {"bg": "#d8a300", "work": "#ef8552", "short": "#6aa84f", "long": "#9fc5e8"}}
]

default = color_options[0]["default"]
dark_mode = color_options[1]["dark_mode"]
d_faves = color_options[2]["d_faves"]
desert = color_options[3]["desert"]
selected_theme = {}
color_mode = [default, dark_mode, d_faves, desert]

short_timer_settings = {"work": 0.5, "short": 0.5, "long": 0.5}
long_timer_settings = {"work": 0.5, "short": 0.5, "long": 0.5}

# ---------------------------- CHANGE COLOR THEME ------------------------------- #

index = 0


def change_colors():
    global index, selected_theme
    if index <= 2:
        index += 1
    else:
        index = 0
    selected_theme = color_mode[index]
    window.config(bg=selected_theme["bg"])
    canvas.config(bg=selected_theme["bg"])
    title_text.config(fg=selected_theme["work"], bg=selected_theme["bg"])
    start_button.config(highlightbackground=selected_theme["bg"])
    reset_button.config(highlightbackground=selected_theme["bg"])
    check_mark.config(fg=selected_theme["work"], bg=selected_theme["bg"])
    color_change.config(highlightbackground=selected_theme["bg"])


# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    global timer
    global reps
    reps = 0
    title_text.config(text="Timer")
    canvas.itemconfig(timer_text, text="00:00")
    window.after_cancel(timer)


# ---------------------------- TIMER MECHANISMS ------------------------------- #

def start_timer():
    global reps
    work_sec = 5
    short_break_sec = 5
    long_break_sec = 5
    reps += 1

    if reps % 8 == 0:
        title_text.config(text="Long Break", fg=selected_theme["long"])
        canvas.itemconfig(tomato, image=splat_pic)
        count_down(long_break_sec)
    elif reps % 2 == 0:
        save_session_stamp()
        title_text.config(text="Short Break", fg=selected_theme["short"])
        canvas.itemconfig(tomato, image=splat_pic)
        count_down(short_break_sec)
    else:
        canvas.itemconfig(tomato, image=tomato_pic)
        title_text.config(text="Work, Bitch!", fg=selected_theme["work"])
        count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    count_min = math.floor(count / 60)
    if count_min < 10:
        count_min = f"0{count_min}"
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        global reps
        num_sessions = math.floor(reps / 2)
        checkmark = "✓"
        checks = ""
        if reps % 2 != 0:
            start_timer()
        else:
            if num_sessions % 3 == 0:
                title_text.config(text="Last session before a long break.\nYou got this!\nPress start when you're "
                                       "ready.", fg=selected_theme["long"])
            elif num_sessions % 4 == 0:
                title_text.config(text="Get back to it.\nPress start when you're ready.", fg=selected_theme["long"])
            else:

                title_text.config(text="Press start when you're ready.", fg=selected_theme["long"])
        for n in range(num_sessions):
            checks += checkmark
            check_mark.config(text=f"Sessions:\n {checks}")


# ---------------------------- SAVE SESSION DATA ------------------------------- #

def save_session_stamp():
    global reps
    num_sessions = math.floor(reps / 2)
    date = datetime.now()
    today = date.strftime("%y-%m-%d")
    current_time = date.strftime("%H:%M")
    session_key = f"Session {num_sessions}"
    session_value = current_time
    day_start_entry = {
        today: {
            session_key: session_value
        }
    }
    single_entry = {session_key: session_value}

    try:
        with open("venv/study_data.json", "r") as study_data_file:
            data = json.load(study_data_file)

    except FileNotFoundError:
        with open("venv/study_data.json", "w") as study_data_file:
            json.dump(day_start_entry, study_data_file, indent=4)
    else:
        if today not in data:
            data.update(day_start_entry)
        today_data = data[today]
        today_data.update(single_entry)
        with open("venv/study_data.json", "w") as study_data_file:
            json.dump(data, study_data_file, indent=4)


# ---------------------------- SOUNDS FUNCTIONS------------------------------- #
pygame.mixer.init()

def work_end():

# ---------------------------- UI SETUP ------------------------------- #

selected_theme = default
window = Tk()
window.title("My Pomodoro")
window.config(padx=100, pady=50, bg=selected_theme["bg"])
# window.maxsize(width=650, height=450)


# title_frame = tkinter.Frame(window, bg=selected_theme["bg"], height=10, width=50)
title_text = Label(text="Timer", font=(FONT_NAME, 50), fg=selected_theme["work"], bg=selected_theme["bg"])
title_text.grid(row=0, column=1, sticky=EW)

# content_frame = tkinter.Frame(window)
canvas = Canvas(width=200, height=224, bg=selected_theme["bg"], highlightthickness=0)
tomato_pic = PhotoImage(file="tomato.png")
splat_pic = PhotoImage(file="splat.png")
tomato = canvas.create_image(100, 112, image=tomato_pic)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightbackground=selected_theme["bg"], command=start_timer)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", highlightbackground=selected_theme["bg"], command=reset_timer)
reset_button.grid(column=2, row=2)

check_mark = Label(text="Sessions:", fg=selected_theme["work"], bg=selected_theme["bg"], font=(FONT_NAME, 18, "bold"))
check_mark.grid(column=0, row=4)

color_change = Button(text="Color Theme", highlightbackground=selected_theme["bg"], command=change_colors)
color_change.grid(column=2, row=4)

# short_timer = Button(text="25min Timer", highlightbackground=selected_theme["bg"], command=partial(start_timer, short_timer_settings))
# short_timer.grid(column=0, row=4)

# long_timer = Button(text="50min Timer", highlightbackground=selected_theme["bg"], command=partial(start_timer, long_timer_settings))
# long_timer.grid(column=1, row=4)

window.mainloop()
