import os
import traceback
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from typing import List, Dict

from api import WeatherApi
from places import Places

""" Settings"""
HEIGHT = 873
WIDTH = 999
TITLE = 'Maciej Marcinkowski - Weather GUI'
PLACES_LIST_FILE = '../assets/city_list.txt'
BG_IMG_FILE = '../assets/bg.png'
ICONS_DIR = '../assets/icons'

""" Handlers """
temp_widgets = []


def on_error(*args):
    traceback.print_stack()
    messagebox.showerror("Error", args[1])


def on_listbox_update(data):
    place_listbox.delete(0, END)
    place_listbox.insert(END, *data)


def on_place_select(event):
    input_field.delete(0, END)
    input_field.insert(0, place_listbox.get(ANCHOR))


def on_input_change(event):
    user_input = input_field.get()

    # No user input, set base data
    if not user_input:
        on_listbox_update(loaded_places)
        return

    filtered_data = []
    for item in loaded_places:
        if user_input.lower() in str(item).lower():
            filtered_data.append(item)

    on_listbox_update(filtered_data)


def on_button_click():
    for widget in temp_widgets:
        widget.destroy()

    user_input = input_field.get()
    selected_item = place_listbox.get(ACTIVE)
    if not input_field.get() or user_input != selected_item:
        raise Exception('Wybierz miasto')

    found_id = None
    for place in loaded_places:
        if str(place) == selected_item:
            found_id = place.api_id

    if not found_id:
        raise Exception('Cos poszlo nie tak :( - brak ID miasta')

    forecast = WeatherApi.get_weather(found_id)
    if len(forecast) < 3:
        raise Exception('API nie zwrocilo pogody dla najblizszych 3 dni, wybierz inne miasto')

    for day in forecast:
        day_frame = LabelFrame(output_frame, text=f'{day.forecast_date}', bg='#ffffff', font=40)
        day_frame.pack(expand=True, fill=BOTH, side=LEFT)

        day_image = loaded_icons['default.png']
        for icon_name, tk_image in loaded_icons.items():
            if icon_name == day.icon_path:
                day_image = tk_image

        Label(day_frame, image=day_image, bg='#ffffff')\
            .pack(expand=True, fill=BOTH)

        Label(day_frame, text=f'{day.weather}', bg='#ffffff', font=20)\
            .pack(expand=True, fill=X)

        Label(day_frame, text=f'Minimalna temperatura: {day.min_temp}°C', bg='#ffffff', font=20)\
            .pack(expand=True, fill=X)

        Label(day_frame, text=f'Maxymalna temperatura: {day.max_temp}°C', bg='#ffffff', font=20)\
            .pack(expand=True, fill=X)

        temp_widgets.append(day_frame)


""" Data """
loaded_places = Places().load_all(PLACES_LIST_FILE)

""" Drawing """
# Root setup
root = tk.Tk()
root.maxsize(WIDTH, HEIGHT)
root.minsize(WIDTH, HEIGHT)
root.title(TITLE)
root.tk.call('wm', 'iconphoto', root.w, PhotoImage(file=BG_IMG_FILE))
root.report_callback_exception = on_error

# Load all icons
loaded_icons: Dict[str, PhotoImage] = {}
files = os.listdir(ICONS_DIR)
for f in files:
    full_path = f'{ICONS_DIR}\\{f}'
    tk_photo = PhotoImage(file=full_path)
    loaded_icons.update({f: tk_photo})

# Background image
bg_img = PhotoImage(file=BG_IMG_FILE)
bg = Label(root, image=bg_img)
bg.image = bg_img
bg.place(x=0, y=0, relwidth=1, relheight=1)

# Input Frame
input_frame = Frame(root, highlightthickness=2)
input_frame.place(relx=.5, rely=.1, relwidth=.5, relheight=.05, anchor=N)
input_frame.config(highlightbackground="#b6fcec", highlightcolor="#b6fcec")

input_label = Label(input_frame, text='Podaj miasto:', font=20)
input_label.pack(side=LEFT)

input_field = Entry(input_frame, font=50)
input_field.pack(expand=YES, fill=X)
input_field.bind("<KeyRelease>", on_input_change)

# Select City Listbox
place_listbox = Listbox(root)
place_listbox.place(relx=.3, rely=.18, relheight=.2, relwidth=.45)
place_listbox.bind("<<ListboxSelect>>", on_place_select)
# Scrollbar for Listbox
scrollbar = Scrollbar(place_listbox)
scrollbar.pack(side=RIGHT, fill=Y)
# Assign scrollbar
place_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=place_listbox.yview)

on_listbox_update(loaded_places)

show_button = Button(root, font=40, text=f'Zobacz pogode', command=on_button_click)
show_button.place(relx=.45, rely=.45, relheight=.03, relwidth=.15)

# Output Frame
output_frame = Frame(root, highlightthickness=2)
output_frame.place(relx=.5, rely=.5, relwidth=.85, relheight=.45, anchor=N)
output_frame.config(highlightbackground="#b6fcec", highlightcolor="#b6fcec")

# Run
root.mainloop()
