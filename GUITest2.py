from tkinter import *
import configparser
import customtkinter
import customtkinter as ctk
from CTkColorPicker import *
from customtkinter import CTk, CTkOptionMenu, CTkLabel
from PIL import ImageColor
import re

config = configparser.ConfigParser()
config.read('config.ini')
root = ctk.CTk()
customnumbervalue = customtkinter.StringVar(value="Custom 1")  # set initial value
##INITIALZING VALUES
default_categories = ['Red Tap', 'Blue Tap', 'Left Spin', 'Right Spin', 'Scratch', 'Beat']
default_rgb = {'R1': '100', 'G1': '100', 'B1': '100', 'R2': '100', 'G2': '100', 'B2': '100', 'R3': '100', 'G3': '100', 'B3': '100', 'R4': '100', 'G4': '100', 'B4': '100', 'R5': '100', 'G5': '100', 'B5': '100'}


customnumbervalue = 1

for category in default_categories:
    if category not in config:
        config[category] = default_rgb

if 'Other Effects' not in config:
    config['Other Effects'] = {}
if 'Custom' not in config['Other Effects']:
    config['Other Effects']['Custom'] = '1'
if 'beat boost' not in config['Other Effects']:
    config['Other Effects']['beat boost'] = '50'
if 'Spin Animation Speed' not in config['Other Effects']:
    config['Other Effects']['Spin Animation Speed'] = '50'
if 'Max Brightness' not in config['Other Effects']:
    config['Other Effects']['Max Brightness'] = '50'
if 'Tap Size Modifier' not in config['Other Effects']:
    config['Other Effects']['Tap Size Modifier'] = '1'
if 'Tap Speed' not in config['Other Effects']:
    config['Other Effects']['Tap Speed'] = '2'
if 'Brightness Modifier' not in config['Other Effects']:
    config['Other Effects']['Brightness Modifier'] = '3'
if 'Delay' not in config['Other Effects']:
    config['Other Effects']['Delay'] = '0'
if 'Spin Animation Speed' in config['Other Effects']:
    config['Other Effects']['Spin Animation Speed'] = '50'
with open('config.ini', 'w') as configfile:
    config.write(configfile)
##


def get_config_value(section, key, default='100'):
    return float(config.get(section, key, fallback=default))


rgbs = {
    category: [DoubleVar(value=get_config_value(category, key)) for key in ('R', 'G', 'B')]
    for category in default_categories
}

##SEARCHING VALUES FOR SLIDERS
beat_boost = DoubleVar(value=get_config_value('Other Effects', 'Beat Boost'))
spin_animation_speed = DoubleVar(value=get_config_value('Other Effects', 'Spin Animation Speed'))
max_brightness = DoubleVar(value=get_config_value('Other Effects', 'Max Brightness'))
tapsizemodifier = DoubleVar(value=get_config_value('Other Effects', 'Tap Size Modifier'))
tap_speed = DoubleVar(value=get_config_value('Other Effects', 'Tap Speed'))
brightmod = DoubleVar(value=get_config_value('Other Effects', 'Brightness Modifier'))
delay = DoubleVar(value=get_config_value('Other Effects', 'Delay'))
##



customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


#STARTING ROOT
ctk.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("900x800")  # Increased size to accommodate new slider
root.title("SpinLED")
##


def write_color_to_config(note, value):
    global customnumbervalue
    print(customnumbervalue)
    config.set(note, f"r{customnumbervalue}", str(value[0]))
    config.set(note, f"g{customnumbervalue}", str(value[1]))
    config.set(note, f"b{customnumbervalue}", str(value[2]))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print(f"Updated {note} to {value}")

def open_color_picker(button, note):
    pick_color = AskColor() # open the color picker
    color = pick_color.get() # get the color string

    button.configure(fg_color=color)
    color = ImageColor.getcolor(color, "RGB")
    write_color_to_config(note, color)
root = ctk.CTk()

def read_color_in_config(category):
    print(config.get(category, f'r{customnumbervalue}'),config.get(category, f'g{customnumbervalue}'),config.get(category, f'b{customnumbervalue}'))
    r = int(config.get(category,f'r{customnumbervalue}'))
    g = int(config.get(category, f'g{customnumbervalue}'))
    b = int(config.get(category,f'b{customnumbervalue}'))

    color = "#{0:02x}{1:02x}{2:02x}".format((r),(g),(b))
    return (color)

## THIS IS FOR CUSTOMS OPTION MENU

def optionmenu_callback(choice):
    global customnumbervalue
    choice = ''.join(filter(str.isdigit, str(choice)))
    customnumbervalue = choice
    if str(choice) == 'rpy_var0':
        customnumbervalue = 1
        choice = 1
    print("optionmenu dropdown clicked:", choice)

    for label, button in buttons.items():
        r = int(config.get(label, f'r{choice}'))
        g = int(config.get(label, f'g{choice}'))
        b = int(config.get(label, f'b{choice}'))

        color = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        button.configure(fg_color=color)

    print(r, g, b)
    return (color)





combobox = customtkinter.CTkOptionMenu(master=root,
                                        values=["Custom 1", "Custom 2", "Custom 3", "Custom 4", "Custom 5"],
                                        command=optionmenu_callback)
combobox.grid(pady = 20, padx = 20)

##NOTES COLORS
buttons = {}  # Dictionary to store all buttons by label

red_tap_button = ctk.CTkButton(
    master=root, text="Red Tap", text_color="black",
    fg_color=read_color_in_config('Red Tap'),
    command=lambda: open_color_picker(red_tap_button, 'Red Tap')
)
red_tap_button.grid(row = 2, pady = 20, padx = 20)
buttons['Red Tap'] = red_tap_button

blue_tap_button = ctk.CTkButton(
    master=root, text="Blue Tap", text_color="black",
    fg_color=read_color_in_config('Blue Tap'),
    command=lambda: open_color_picker(blue_tap_button, 'Blue Tap')
)
blue_tap_button.grid(row = 4, pady = 20, padx = 20)
buttons['Blue Tap'] = blue_tap_button

left_spin_button = ctk.CTkButton(
    master=root, text="Left Spin", text_color="black",
    fg_color=read_color_in_config('Left Spin'),
    command=lambda: open_color_picker(left_spin_button, 'Left Spin')
)
left_spin_button.grid(row = 6, pady = 20, padx = 20)
buttons['Left Spin'] = left_spin_button

right_spin_button = ctk.CTkButton(
    master=root, text="Right Spin", text_color="black",
    fg_color=read_color_in_config('Right Spin'),
    command=lambda: open_color_picker(right_spin_button, 'Right Spin')
)
right_spin_button.grid(row = 8, pady = 20, padx = 20)
buttons['Right Spin'] = right_spin_button

scratch_button = ctk.CTkButton(
    master=root, text="Scratch", text_color="black",
    fg_color=read_color_in_config('Scratch'),
    command=lambda: open_color_picker(scratch_button, 'Scratch')
)
scratch_button.grid(row = 10, pady = 20, padx = 20)
buttons['Scratch'] = scratch_button

beat_button = ctk.CTkButton(
    master=root, text="Beat", text_color="black",
    fg_color=read_color_in_config('Beat'),
    command=lambda: open_color_picker(beat_button, 'Beat')
)
beat_button.grid(row = 12, pady = 20, padx = 20)
buttons['Beat'] = beat_button
##

def storevalue(category, spot, value):
    config.set(category, spot, str(value))
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print(f"Updated {category} {spot} to {value}")


def update_slider(name, value):
    value_labels[name].configure(text=f"{name}: {float(value):.1f}")
    storevalue('Other Effects', f'{name}', value)


brightmod_slider = ctk.CTkSlider(
    master=root,
    from_=1,
    to=10,
    variable=brightmod,
    command=lambda value: (storevalue('Other Effects', 'brightness modifier', value), (update_slider("Brightness Modifier", value))),
    width=200)
brightmod_slider.grid(column=1, row = 1, columnspan=len(default_categories), sticky=N)

brightmod_value_label = ctk.CTkLabel(
    root, text = f"brightness modifier: {config.get('Other Effects', 'brightness modifier')}")
brightmod_value_label.grid(column=1, row=0, sticky=SW)


tap_speed_slider = ctk.CTkSlider(
    master=root,
    from_=10,
    to=100,
    variable=tap_speed,
    command=lambda value: (storevalue('Other Effects', 'Tap Speed', value), (update_slider("Tap Speed", value))),
    width=200)
tap_speed_slider.grid(column=1, row = 3, sticky=N)

tap_speed_value_label = ctk.CTkLabel(
    root, text = f"Tap Speed: {config.get('Other Effects', 'Tap Speed')}")
tap_speed_value_label.grid(column=1, row=2, sticky=SW)


tap_size_modifier_slider = ctk.CTkSlider(
    master=root,
    from_=1,
    to=100,
    variable=tapsizemodifier,
    command=lambda value: (storevalue('Other Effects', 'Tap Size Modifier', value), (update_slider("Tap Size Modifier", value))),
    width=200)
tap_size_modifier_slider.grid(column=1, row = 5, sticky=N)

tap_size_value_label = ctk.CTkLabel(
    root, text = f"Tap Size Modifier: {config.get('Other Effects', 'Tap Size Modifier')}")
tap_size_value_label.grid(column=1, row=4, sticky=SW)


beat_boost_slider = ctk.CTkSlider(
    master=root,
    from_=1,
    to=10,
    variable=beat_boost,
    command=lambda value: (storevalue('Other Effects', 'Beat Boost', value), (update_slider("Beat Boost", value))),
    width=200)
beat_boost_slider.grid(column=1, row = 7, sticky=N)

beat_boost_value_label = ctk.CTkLabel(
    root, text = f"Beat Boost: {config.get('Other Effects', 'Beat Boost')}")
beat_boost_value_label.grid(column=1, row=6, sticky=SW)


spin_animation_speed_slider = ctk.CTkSlider(
    master=root,
    from_=1,
    to=100,
    variable=spin_animation_speed,
    command=lambda value: (storevalue('Other Effects', 'Spin Animation Speed', value), (update_slider("Spin Animation Speed", value))),
    width=200)
spin_animation_speed_slider.grid(column=1, row = 9, sticky=N)

spin_animation_speed_value_label = ctk.CTkLabel(
    root, text = f"Spin Animation Speed: {config.get('Other Effects', 'Spin Animation Speed')}")
spin_animation_speed_value_label.grid(column=1, row=8, sticky=SW)


max_brightness_slider = ctk.CTkSlider(
    master=root,
    from_=0,
    to=255,
    variable=max_brightness,
    command=lambda value: (storevalue('Other Effects', 'Max Brightness', value), (update_slider("Max Brightness", value))),
    width=200)
max_brightness_slider.grid(column=1, row = 11, sticky=N)

max_brightness_value_label = ctk.CTkLabel(
    root, text = f"Max Brightness: {config.get('Other Effects', 'Max Brightness')}")
max_brightness_value_label.grid(column=1, row=10, sticky=SW)


delay_slider = ctk.CTkSlider(
    master=root,
    from_=-10,
    to=10,
    variable=delay,
    command=lambda value: (storevalue('Other Effects', 'Delay', value), (update_slider("Delay", value))),
    width=200)
delay_slider.grid(column=1, row = 13, sticky=N)

delay_value_label = ctk.CTkLabel(
    root, text = f"Delay: {config.get('Other Effects', 'Delay')}")
delay_value_label.grid(column=1, row=12, sticky=SW)

value_labels = {
    "Brightness Modifier": brightmod_value_label,
    "Tap Speed": tap_speed_value_label,
    "Tap Size Modifier": tap_size_value_label,
    'Beat Boost': beat_boost_value_label,
    'Spin Animation Speed': spin_animation_speed_value_label,
    'Max Brightness': max_brightness_value_label,
    'Delay': delay_value_label
}




optionmenu_callback(1)
root.mainloop()