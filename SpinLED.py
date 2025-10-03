import serial
import numpy as np
import time
import threading
import random
import socket
import re
import math
from pynput import mouse
from pynput import keyboard
import matplotlib.pyplot as plt
import configparser
import customtkinter

config = configparser.ConfigParser()

# Serial settings
serial_port = "COM4"  # Replace with the correct COM port
baud_rate = 576000

# customizable
beat_color = (200, 200, 200) #RGB format
scratch_color = (255,127,80) #why the fuck is this blue
red_tap = (255, 0, 255) #RGB
blue_tap = (100, 255, 50) #RGB
left_spin_color = (100, 255, 50) #RGB
right_spin_color = (255, 255, 200) #RGB
beat_color_bool = "True"
beat_boost = 20 #for only. tells how much to increase brightness on beat by. Also ignores maxbrightness
saturation_boost = 2 #does this work?
strip_length =  598 #how many LEDs are on the strip
spin_animation_speed = 1 #how many pixels each frame jumps
max_brightness = 100 #max brightness for everything on the strip
dampening_factor = 0.9 #mm damp. this might not work
tap_size = 299 #LEGACY. still controls some effects. do not make higher than striplength / 2
tapsizemodifier = 1 #tap size
tap_speed = 1 #how fast tap reaches full lenght
match_size = 50
brightmod = (255/max_brightness)
delay = 1


#non-customizable
overlay_lock = threading.Lock()
brightfactor = max_brightness / 255 #
left_spin_color = (left_spin_color[0]*brightfactor, left_spin_color[1]*brightfactor, left_spin_color[2]*brightfactor) #equally dampens rgb of spin effect to ensure it is under the maxbrightness
right_spin_color = (right_spin_color[0]*brightfactor, right_spin_color[1]*brightfactor, right_spin_color[2]*brightfactor)   

#initializing values
update_serial = True ##used so when user inputs another com port the connection is killed and remade
last_sent_time = time.time()
y_values = 0
coordinates = 0
effects_to_remove = []
server_status = "string"
port_status = "string"
previous_colors = [(0, 0, 0)] * strip_length 
overlay_colors = [(0, 0, 0)] * strip_length  
livetime = time.time
start_time = 1
active_effects = []
current_time = 1
sync_frame = ([4, 3, 2, 1]) # for syncing with ESP32
spinning_l = False
spinning_r = False
colors = [[0,0,0] for _ in range(strip_length)]
# Track the last time we updated the smoothed colors
last_update_time = time.time()
last_smooth_colors = []  # Stores the last smoothed colors
m = 0
t = 0
osc_damp = 1 #dampen rate for parabola
osc_freq = 20 #oscillation frequency for parabola
data = ""
data_prev = "a"
notes = []
temp_spin_l_color = [[0,0,0] for _ in range(strip_length)]
temp_spin_r_color = [[0,0,0] for _ in range(strip_length)]
prevright = (0, 0, 0)
prevleft = (0, 0, 0)
temp_hold_blue_color = [[0,0,0] for _ in range(strip_length)]
temp_hold_red_color = [[0,0,0] for _ in range(strip_length)]
match_index = (strip_length / 9) 
s_down = True #for scratches. makes effect bounce
s = 1
v = time.time()
n = 0#for counting time AFTER blue hold has ended (fade out effect)
u = 0#for counting time AFTER red hold has ended (fade out effect)
spinright = time.time()
spinleft = time.time()
red_match_timer = 100000
blue_match_timer = 100000
strip_length
spinstart = time.time()
beathold = False
frequency = 1
holdstart = False
tempb = 0.2 #for holds to store decreasing value on fade out effect
tempr = 0.2 
match_rand = int(strip_length / 9)
firstnotes = []

#calcing random scratch colors
scratch_min = (min(255, int((scratch_color[0] / 10) * 6)), 
               min(255, int((scratch_color[1] / 10) * 6)), 
               min(255, int((scratch_color[2] / 10) * 6))) 

scratch_max = (min(255, int((scratch_color[0] / 10) * 12)), 
               min(255, int((scratch_color[1] / 10) * 12)), 
               min(255, int((scratch_color[2] / 10) * 12)))

def update_colors():
    global red_tap, blue_tap, left_spin_color, right_spin_color, scratch_color, beat_color, beat_boost, spin_animation_speed, max_brightness, tapsizemodifier, tap_speed, brightmod, delay, beat_color_bool
    config.read('config.ini')
    customvalue = (int(config.get('Other Effects', 'Custom', fallback=1)))
    red_tap = (int(config.get('Red Tap', f'B{customvalue}', fallback=100)), int(config.get('Red Tap', f'G{customvalue}', fallback=100)), int(config.get('Red Tap', f'R{customvalue}', fallback=100)))
    blue_tap = (int(config.get('Blue Tap', f'B{customvalue}', fallback=100)), int(config.get('Blue Tap', f'G{customvalue}', fallback=100)), int(config.get('Blue Tap', f'R{customvalue}', fallback=100)))
    left_spin_color = (int(config.get('Left Spin', f'B{customvalue}', fallback=100)), int(config.get('Left Spin', f'G{customvalue}', fallback=100)), int(config.get('Left Spin', f'R{customvalue}', fallback=100)))
    right_spin_color = (int(config.get('Right Spin', f'B{customvalue}', fallback=100)), int(config.get('Right Spin', f'G{customvalue}', fallback=100)), int(config.get('Right Spin', f'R{customvalue}', fallback=100)))
    scratch_color = (int(config.get('Scratch', f'B{customvalue}', fallback=100)), int(config.get('Scratch', f'G{customvalue}', fallback=100)), int(config.get('Scratch', f'R{customvalue}', fallback=100)))
    beat_color = int(config.get('Beat', f'B{customvalue}', fallback=100)), int(config.get('Beat', f'G{customvalue}', fallback=100)), int(config.get('Beat', f'R{customvalue}', fallback=100))
    beat_boost = float(config.get('Other Effects', 'Beat Boost', fallback = 20))
    spin_animation_speed = float(config.get('Other Effects', 'Spin Animation Speed', fallback = 20)) / 20
    max_brightness = float(config.get('Other Effects', 'Max Brightness' , fallback = 200))
    tapsizemodifier = int(config.get('Other Effects', 'Tap Size Modifier' , fallback = 1)) / 50
    tap_speed = float(config.get('Other Effects', 'Tap Speed' , fallback = 50))
    tap_speed = max(1, abs(tap_speed - 100) / 5) #inverting tap speed here. 100 is the max tap_speed number. change when changing tap_speeds max
    delay = float(config.get('Other Effects', 'Delay' , fallback = 0)) / 8
    beat_color_bool = (config.get('Options', 'beat color', fallback = "True"))
    if left_spin_color != prevleft:
        for i in range(0 , int(strip_length)): #checking for effect range (effect_var does not go over striplength here)

            #brightness multiplier
            mod = strip_length - i
            mod = (mod / strip_length) 
            mod = max(0, (255 * mod) - i)

            r, g, b = left_spin_color

            r = max(0, r - mod)
            g = max(0, g - mod)
            b = max(0, b - mod)
    if right_spin_color != prevright:
        for i in range(0 , int(strip_length)): #checking for effect range (effect_var does not go over striplength here)

            #brightness multiplier
            mod = strip_length - i
            mod = (mod / strip_length) 
            mod = max(0, (255 * mod) - i)

            r, g, b = left_spin_color

            r = max(0, r - mod)
            g = max(0, g - mod)
            b = max(0, b - mod)
        


def on_press(key):
    global blue_match_timer, red_match_timer, spinning_l, spinning_r, scratch, start_spintime, current_value, loop, start_time, livetime, match_rand
    try:
        if key.char == '1':  # Check if '1' is pressed
            index = 300
            index = random.randint(index - match_rand, index + match_rand)
            active_effects.append({
                "start_index": index,
                "start_time": time.time(),
                "effect_id": 5,
                "effect_var": 0
                })
            blue_match_timer = time.time()
            print("match hit")
        if key.char == '2':  # Check if '1' is pressed
            var = 1
            index = 300
            index = random.randint(index - match_rand, index + match_rand)
            active_effects.append({
                "start_index": index,
                "start_time": time.time(),
                "effect_id": 6,
                "effect_var": var
                })
            red_match_timer = time.time()
            print("match hit")
        if key.char == '3':  # Check if '1' is pressed
            active_effects.append({
                "start_index": 300,
                "start_time": time.time(),
                "effect_id": 3,
                "effect_var": tap_speed #osc_freq
                })
            print("tap hit")
        if key.char == '4':  # Check if '1' is pressed
            active_effects.append({
                "start_index": 300,
                "start_time": time.time(),
                "effect_id": 4,
                "effect_var": tap_speed #osc_freq
                })
            print("tap hit")
        if key.char == '5':  # Check if '1' is pressed
            active_effects.append({
                "start_index": strip_length,
                "start_time": time.time(),
                "effect_id": 1,
                "effect_var": 1
                })
            print("spin hit")
            remove_note("SpinLeftStart")
            scratch = False
            loop = False #for ease out
        if key.char == '6':  # Check if '1' is pressed
            active_effects.append({
                "start_index": strip_length,
                "start_time": time.time(),
                "effect_id": 2,
                "effect_var": 1
            })
            remove_note("SpinRightStart")
            scratch = False
            loop = False #for ease out
        if key.char == '7':  # Check if '1' is pressed
            active_effects.append({
                "start_index": 300,
                "start_time": time.time(),
                "effect_id": 8,
                "effect_var": tap_size
            })
            print("hold hit")
            remove_note("SpinRightStart")
            scratch = False
            loop = False #for ease out
        if key.char == '8':
            start_time = livetime() + 0.5
            int(start_time)

    except AttributeError:
        print(f"Special key {key} pressed")



listener = keyboard.Listener(
    on_press=on_press)
listener.start()



def port_connect():
    global data, firstnotes, server_status
    host = '127.0.0.1'  # Same as C# server
    port = 8008        # Same port as C# server
    server_connected = False
    while True:
        try:
            # Create a socket and connect to the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            client_socket.connect((host, port))
            server_status = f"Connected on port {port} through local ip {host}!"
            server_connected = True

            break
        except ConnectionRefusedError:
            print("No server found. Retrying Connection")
            server_status = "No server found. Retrying Connection"
            server_connected = False
            time.sleep(1)
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying Connection")
            server_status = f"Unexpected error: {e}. Retrying Connection"
            server_connected = False
            time.sleep(1)
    while server_connected:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            current_time = str(time.time())
            firstnotes.append(data + f" time {current_time}")
        except ConnectionResetError:
            server_status = ("Server disconnected.")
            server_connected = False
            break

def delaysend():
    global data, delay, firstnotes
    for note in firstnotes:
        current_time = time.time() #timer
        notetimer = re.search(r"time (\d+\.\d+)", note) #find notes time
        notetimer = float(notetimer.group(1)) #float that shit
        if notetimer + delay <= current_time: #check if note should be processed
            add_note(note)
            firstnotes.remove(note) #remove note from temp list
            print("note trigger")



def add_note(note):
    global notes
    notes.append(note)

def remove_note(name):
    global notes
    notes = [note for note in notes if not note.startswith(name)]


def apply_overlay(main):
    """Combine the main colors with the overlay buffer."""
    with overlay_lock:
        # Merge overlay effects with main colors
        combined_colors = [
            overlay if overlay != (0, 0, 0) else smoothed_colors
            for overlay, smoothed_colors in zip(overlay_colors, main)
        ]
    return combined_colors

def on_beat():
    global start_time, beathold
    """Handle key press events."""
    if any("DrumStart" in note for note in notes):
        for note in notes:
            if "DrumStart" and "Beatholdtrue" in note:
                beathold = True
                print("bveathold!")
        start_time = livetime() + 0.5
        int(start_time)
        remove_note("DrumStart")

def beat_end():
    global start_time, beathold
    if any("DrumEnd" in note for note in notes):
        start_time = livetime() + 0.5
        int(start_time)
        beathold = False
        print("beat ended!")
        remove_note("DrumEnd")

def on_hold():
    global holdstart
    if any("Blue HoldStart" in note for note in notes):
        for note in notes:
            if "Blue HoldStart" and "Holdtrue" in note:
                holdstart = True
                match = re.search(r"Blue HoldStart \((-?\d+)\)", note)
                try:
                    index = int((int(match.group(1)) + 4) * match_index)
                except:
                    index = 0

                active_effects.append({
                    "start_index": index,
                    "start_time": time.time(),
                    "effect_id": 8,
                    "effect_var": 0,
                    "xvalue": 0,
                    "yvalue": 0,
                    "end" : False
                    })
                remove_note("Blue HoldStart")

            elif "Blue HoldStart" in note:
                match = re.search(r"Blue HoldStart \((-?\d+)\)", note)
                try:
                    index = int((int(match.group(1)) + 4) * match_index)
                except:
                    index = 0

                active_effects.append({
                    "start_index": index,
                    "start_time": time.time(),
                    "effect_id": 8,
                    "effect_var": 0,
                    "xvalue": 0,
                    "yvalue": 0,
                    "end" : False
                    })
                remove_note("Blue HoldStart")

    if any("Red HoldStart" in note for note in notes):
        for note in notes:
            if "Red HoldStart" and "Holdtrue" in note:
                holdstart = True
                match = re.search(r"Red HoldStart \((-?\d+)\)", note)
                try:
                    index = int((int(match.group(1)) + 4) * match_index)
                except:
                    index = 0

                active_effects.append({
                    "start_index": index,
                    "start_time": time.time(),
                    "effect_id": 9,
                    "effect_var": 0,
                    "xvalue": 0,
                    "yvalue": 0,
                    "end" : False
                    })
                remove_note("Red HoldStart")

            elif "Red HoldStart" in note:
                match = re.search(r"Red HoldStart \((-?\d+)\)", note)
                try:
                    index = int((int(match.group(1)) + 4) * match_index)
                except:
                    index = 0

                active_effects.append({
                    "start_index": index,
                    "start_time": time.time(),
                    "effect_id": 9,
                    "effect_var": 0,
                    "xvalue": 0,
                    "yvalue": 0,
                    "end" : False
                })
                remove_note("Red HoldStart")

def on_sectioncontinuationorend():
    global holdstart
    if any("SectionContinuationOrEnd" in note for note in notes):
        for note in notes:
            if "SectionContinuationOrEnd" and "Holdtrue" in note:
                return
            else:
                print("ending hold")
                holdstart = False



def on_release():
    global start_time
    if "IsDrum" in notes:
        start_time = time.time()

def on_scratch():
    global scratch
    if any("ScratchStart" in note for note in notes):
        active_effects.append({
            "start_index": 0,
            "start_time": 0,
            "effect_id": 7
            })
        scratch = True
        remove_note("ScratchStart")

def on_continue():
    if any("SectionContinuationOrEnd" in note for note in notes):
        for note in notes:
            if "SectionContinuationOrEnd" in note:
                remove_note("SectionContinuationOrEnd")
    if any("Blue HoldStart" in note for note in notes):
        for note in notes:
            if "Blue HoldStart" in note:
                remove_note("Blue HoldStart")
    if any("Red HoldStart" in note for note in notes):
        for note in notes:
            if "Red HoldStart" in note:
                remove_note("Red HoldStart")       
    if any("Red Match" in note for note in notes):
        for note in notes:
            if "Red Match" in note:
                remove_note("Red Match")   
    if any("Blue Match" in note for note in notes):
        for note in notes:
            if "Blue Match" in note:
                remove_note("Blue Match")         

def on_match():
    global scratch, blue_match_timer, red_match_timer, active_effects, match_rand
    if any("Blue Match" in note for note in notes):
        var = 1
        for note in notes:
            if "Blue Match" in note:
                    match = re.search(r"Blue Match \((-?\d+)\)", note)
                    try:
                        index = (int(match.group(1)) + 4)
                        index = random.randint(index - match_rand, index + match_rand)
                        for effect in active_effects:
                            if effect["start_index"] ==  index and effect["effect_id"] == 5 or effect["start_index"] == index and effect["effect_id"] == 6:
                                var = effect["effect_var"] + 1
                                active_effects.remove(effect)
                    except:
                        index = 0

                    active_effects.append({
                        "start_index": index,
                        "start_time": time.time(),
                        "effect_id": 5,
                        "effect_var": var
                        })
                    remove_note("Blue Match")
                    scratch = False
                    blue_match_timer = time.time()
    if any("Red Match" in note for note in notes):
        for note in notes:
            if "Red Match" in note:
                var = 1
                match = re.search(r"Red Match \((-?\d+)\)", note)
                try:
                    index = (int(match.group(1)) + 4)
                    index = random.randint(index - match_rand, index + match_rand)
                    for effect in active_effects:
                        if effect["start_index"] ==  index and effect["effect_id"] == 5 or effect["start_index"] == index and effect["effect_id"] == 6:
                            var = effect["effect_var"] + 1
                            active_effects.remove(effect)
                except:
                    index = 0

                active_effects.append({
                    "start_index": index,
                    "start_time": time.time(),
                    "effect_id": 6,
                    "effect_var": var
                    })
                remove_note("Red Match")
                scratch = False
                red_match_timer = time.time()



def spin_start():
    global spinning_l, spinning_r, effects_to_remove, scratch, current_value, start_spintime, loop, active_effects
    if any("SpinLeftStart" in note for note in notes):
        active_effects.append({
            "start_index": strip_length,
            "start_time": time.time(),
            "effect_id": 1,
            "effect_var": ease_out(spinstart, strip_length, t)
            })
        remove_note("SpinLeftStart")
        current_value = ease_out(spinstart, strip_length, t)
        start_spintime = time.time() #for ease out
        scratch = False
        loop = False #for ease out

        #setting matches to 0
        for effect in active_effects:
            if effect["effect_id"] == 3 or effect["effect_id"] == 4:
                effects_to_remove.append(effect)

    if any("SpinRightStart" in note for note in notes):
        active_effects.append({
            "start_index": strip_length,
            "start_time": time.time(),
            "effect_id": 2,
            "effect_var": ease_out(spinstart, strip_length, t)
        })
        remove_note("SpinRightStart")
        current_value = ease_out(spinstart, strip_length, t)
        start_spintime = time.time() #for ease out
        scratch = False

        #setting matches to 0
        for effect in active_effects:
            if effect["effect_id"] == 3 or effect["effect_id"] == 4:
                effects_to_remove.append(effect)

        return

def tap_start():
    global active_effects, strip_length, scratch, osc_freq
    if any("Blue Tap" in note for note in notes):
        for note in notes:
            if "Blue Tap" in note:
                # Add the new effect with its start index and start time
                match = re.search(r"Blue Tap \((-?\d+)\)", note)
                remove_note("Blue Tap")
            try:
                index = int((int(match.group(1)) + 4) * match_index)
                index = int(index)
            except:
                index = 0
            index = random.randint(index - 40, index + 40)
            active_effects.append({
                "start_index": index,
                "start_time": time.time(),
                "effect_id": 3,
                "effect_var": tap_speed #osc_freq
                })
            scratch = False
    if any("Red Tap" in note for note in notes):
        for note in notes:
            if "Red Tap" in note:
                # Add the new effect with its start index and start time
                match = re.search(r"Red Tap \((-?\d+)\)", note)
                remove_note("Red Tap")
            try:
                index = int((int(match.group(1)) + 4) * match_index)
                index = int(index)
            except:
                index = 0
            index = random.randint(index - 40, index + 40)
            active_effects.append({
                "start_index": index,
                "start_time": time.time(),
                "effect_id": 4,
                "effect_var": tap_speed #osc_freq 
                })
            scratch = False


def sine_wave(x, amplitude, frequency, phase=0):
    return amplitude * np.sin(2 * np.pi * frequency * x + phase)


def oscillating_parabola(x, osc_damp, osc_freq):
    normalized_x = x / tap_size  # Normalize x to the range [-50, 50]. this determines the range of the tap
    unscaled = (1 - normalized_x**2) * np.exp(-osc_damp * np.abs(normalized_x)) * np.cos(osc_freq * normalized_x)
    return 127 * unscaled  # Scale to make max value 255

def get_y_coords_for_index(i):
    # Ensure i is within the valid range
    if 0 <= i < len(coordinates):
        x, y = coordinates[i]  
        return y
    else:
        raise ValueError(f"i is out of range{i}")

    


def beats():
    global colors, start_time, beat_color_bool, beat_color
    live = livetime()
    int(live)
    time_diff = max(start_time - live, 0)
    if beat_color_bool == "True":
        for i in range(strip_length):
            index = i
            r, g, b = beat_color[2], beat_color[1], beat_color[0]
            x, y ,z = colors[i][2], colors[i][1], colors[i][0]
            
            r = ((r / 255) * beat_boost)
            g = ((g / 255) * beat_boost)
            b = ((b / 255) * beat_boost)
            r = min(max(int(x + r * time_diff), x), 255)
            g = min(max(int(y + g * time_diff), y), 255)
            b = min(max(int(z + b * time_diff), z), 255)

            colors[index] = (r, g, b)
    elif beathold == True:

            for i in range(strip_length):
                
                index = i
                r, g, b = colors[i][2], colors[i][1], colors[i][0]

                r = r + (255 / beat_boost)
                g = g + (255 / beat_boost)
                b = b + (255 / beat_boost)

                colors[index] = (r, g, b)
    else: 
        for i in range(strip_length):
            index = i
            r, g, b = colors[i][2], colors[i][1], colors[i][0]

            # Apply the same increase to all color components
            r = min(max(int(r + beat_boost * time_diff), r), 255)
            g = min(max(int(g + beat_boost * time_diff), g), 255)
            b = min(max(int(b + beat_boost * time_diff), b), 255)

            colors[index] = (r, g, b)

    return colors

def ease_out(spinstart, strip_length, t):
    value = strip_length - (strip_length - spinstart) * math.exp(-spin_animation_speed * t)
    value = math.ceil(value) #first value controls speed, 2nd controls difference in speed of start of animation compared to the end
    if value < strip_length * 2:
        #print(value)
        return value

def send_colors(colors, ser):
    #try:
        with overlay_lock:  # Ensure exclusive access to the serial port
            try:
                # Send the sync frame first
                ser.write(sync_frame)
                
                # Send the LED data
                data = bytearray(np.clip(np.array(colors), 0, max_brightness).astype(np.uint8).flatten()[:(strip_length * 3)])

                ser.write(data)
                
                #print(f"Sync frame sent: {len(sync_frame)} bytes, LED data sent: {len(data)} bytes")
            except Exception as e:
                print(f"Error sending data: {e}")

def update_effects(): 
    global active_effects, effects_to_remove, overlay_colors, overlay_lock, tempb, tempr, tapsizemodifier, strip_length, match_size, tap_dur ,brightmod, temp_hold_blue_color,temp_hold_red_color, blue_match, red_match, spinning_l,tap_speed, spinning_r, loop, m , q, u, n, t, s, d, e, f, v, osc_freq, effects_to_remove, colors, spinright, spinleft, previous_colors, s_down, scratch, blue_match_timer, red_match_timer, current_value, x_values, y_values, coordinates, holdstart, y_values, coordinates, effects_to_remove, previous_colors
    brightmod = (255/max( 1, max_brightness))
    active_effects.sort(key=lambda effect: effect["effect_id"])
    current_time = time.time()
    blue_match = False
    red_match = False
    with overlay_lock:
        # Reset overlay colors
        overlay_colors = [(0, 0, 0)] * strip_length
        for effect in active_effects:
            elapsed_time = current_time - effect["start_time"]
            start_index = int(effect["start_index"])
            if effect["effect_id"] == 1 or effect["effect_id"] == 2:
                active_effects.sort(key=lambda effect: effect["start_time"])
                if effect["effect_id"] == 1:  # LEFT SPIN
                        elapsed_spintime = current_time - effect["start_time"]#timer for ease_out
                        t = elapsed_spintime #for ease_out
                        effect["effect_var"] = math.ceil(ease_out(0, strip_length * 2, t)) #calculating effect range(goes up to double of striplength)

                        if  effect["effect_var"] < strip_length:

                            for i in range(0 , int(effect["effect_var"])): #checking for effect range (effect_var does not go over striplength here)

                                #brightness multiplier
                                mod = effect["effect_var"] - i
                                mod = (mod / effect["effect_var"]) 
                                mod = max(0, (255 * mod) - i)

                                r, g, b = left_spin_color

                                r = max(0, (r - mod) / brightmod)
                                g = max(0, (g - mod) / brightmod)
                                b = max(0, (b - mod) / brightmod)

                                temp_spin_l_color[i] = (r, g, b)
                                colors[i] = (r, g, b)
                                #save temp colors for second part of animation
                        
                        if effect["effect_var"] >= strip_length: #for when spin is fading out
                            
                            effect["start_index"] = effect["start_index"] + (spin_animation_speed * 10) #animation speed for fadeout
                            
                            for i in range(0 , strip_length):
                                
                                index = int(effect["start_index"] - strip_length + i) # creating an index to move colors to. should be between 0 and striplength
                                if 0 <= index < strip_length: #double checking its between 0 and strip length

                                    r, g, b = temp_spin_l_color[i][0], temp_spin_l_color[i][1], temp_spin_l_color[i][2] #getting colors for i

                                    colors[index] = (r, g, b) #applying colors to newly generated index
                            if effect["start_index"] > strip_length * 2: #remove effect
                                effects_to_remove.append(effect)


                if effect["effect_id"] == 2: #RIGHT SPIN
                        
                        elapsed_spintime = current_time - effect["start_time"]#timer for ease_out
                        t = elapsed_spintime #for ease_out
                        effect["effect_var"] = math.ceil(ease_out(0, strip_length * 2, t)) #calculating effect range(goes up to double of striplength)

                        if  effect["effect_var"] < strip_length:

                            for i in range(0 , int(effect["effect_var"])): #checking for effect range (effect_var does not go over striplength here)

                                x, y, z = colors[i][0], colors[i][1], colors[i][2] #get colors from

                                #brightness multiplier
                                mod = effect["effect_var"] - i
                                mod = (mod / effect["effect_var"]) 
                                mod = max(0, (255 * mod) - i)

                                r, g, b = right_spin_color

                                r = max(0, (r - mod) / brightmod)
                                g = max(0, (g - mod) / brightmod)
                                b = max(0, (b - mod) / brightmod)

                                temp_spin_r_color[i] = (r, g, b)
                                colors[i] = (r, g, b)
                                #save temp colors for second part of animation

                        if effect["effect_var"] >= strip_length: #for when spin is fading out
                            
                            effect["start_index"] = effect["start_index"] + (spin_animation_speed * 10) #animation speed for fadeout
                            
                            for i in range(0 , strip_length):
                                
                                index = int(effect["start_index"] - strip_length + i) # creating an index to move colors to. should be between 0 and striplength
                                if 0 <= index < strip_length: #double checking its between 0 and strip length

                                    r, g, b = temp_spin_r_color[i][0], temp_spin_r_color[i][1], temp_spin_r_color[i][2] #getting colors for i

                                    colors[index] = (r, g, b) #applying colors to newly generated index
                            if effect["start_index"] > strip_length * 2: #remove effect
                                effects_to_remove.append(effect)
                                

            if effect["effect_id"] == 5: #blue match
                size_mod = int(match_size * tapsizemodifier)
                print(size_mod)
                if effect["start_time"] - current_time + (tap_speed / 5) > 0:
                    for i in range(effect["start_index"] - size_mod , effect["start_index"] + size_mod ): #10 is size of match. this and other 10 to control size 
                        x, y, z = colors[i][0], colors[i][1], colors[i][2]
                        r, g, b = blue_tap

                        wawa =  (effect["start_time"] - current_time) + (tap_speed / 5)

                        bright = abs(abs(effect["start_index"] - i) / size_mod -1) / brightmod
                        r = max(x, wawa * (x + (r * (bright ** 2))))
                        g = max(y, wawa * (y + (g * (bright ** 2))))
                        b = max(z, wawa * (z + (b * (bright ** 2))))


                        colors[i] = (r, g, b)
                if effect["start_time"] - (tap_speed / 5) <= 0:
                        effects_to_remove.append(effect)


            if effect["effect_id"] == 6: #red match
                size_mod = int(match_size * tapsizemodifier)
                if effect["start_time"] - current_time + (tap_speed / 5) > 0:
                    for i in range(effect["start_index"] - size_mod, effect["start_index"] + size_mod): #10 is size of match. this and other 10 to control size 
                        x, y, z = colors[i][0], colors[i][1], colors[i][2]
                        r, g, b = red_tap

                        wawa =  (effect["start_time"] - current_time) + (tap_speed / 5)

                        bright = abs(abs(effect["start_index"] - i) / size_mod -1) / brightmod #change 10 here to control size of match. the number at the end is diving brightness (ie 3 / maxbrightness) 
                        
                        r = max(x, wawa * (x + (r * (bright ** 2))))
                        g = max(y, wawa * (y + (g * (bright ** 2))))
                        b = max(z, wawa * (z + (b * (bright ** 2))))


                        colors[i] = (r, g, b)
                if effect["start_time"] - current_time + (tap_speed / 5) <= 0:
                        
                        effects_to_remove.append(effect)


            if effect["effect_id"] == 3:  # BLUE TAP
                #made inverse mechanic that starts at 1 when fade out is trigger and ends at zero. wait
                fade_out_duration = (tap_speed / 5) / 1/2  # the same duration as your condition
                #logic for sine wave 
                osc_freq = effect["effect_var"]
                effect["effect_var"] = effect["effect_var"] / tap_speed
                x_values = np.arange(-tap_size, tap_size, 1) #size of tap
                y_values = [oscillating_parabola(x, osc_damp, osc_freq) for x in x_values]
                coordinates = [(int(x), int(oscillating_parabola(x, osc_damp, osc_freq))+ 127) for x in x_values]
                if current_time - effect["start_time"] <= ((tap_speed / 5) * 1/2):
                    for i in range(max(0, start_index - tap_size), min(strip_length, start_index + tap_size)):
                        
                        #getting old colors
                        x, y, z = colors[i][0], colors[i][1], colors [i][2]

                        #logic for the main tap brightness
                        iterate = i - start_index + tap_size
                        brightness = get_y_coords_for_index(iterate)
                        r, g, b = blue_tap
                        r, g, b = [int(c * brightness / 255) for c in blue_tap]
                        r = max(x, x +(r ** 1 - abs((i - start_index) / tapsizemodifier))/ brightmod) #the number controls the size of the tap. lower == bigger
                        g = max(y, y +(g ** 1 - abs((i - start_index) / tapsizemodifier))/ brightmod)
                        b = max(z, z +(b ** 1 - abs((i - start_index) / tapsizemodifier))/ brightmod)
                        
                        colors[i] = (r, g, b)
                elif current_time - effect["start_time"] <= (tap_speed / 5) * 2:
                    inverse = elapsed_time - fade_out_duration
                    inverse = max(0.0, 1.0 - (inverse / fade_out_duration))
                    factor = -1/2 * (math.cos(inverse * math.pi)) + 1/2
                    print(factor)
                    for i in range(max(0, start_index - tap_size), min(strip_length, start_index + tap_size)):
                        #getting old colors
                        x, y, z = colors[i][0], colors[i][1], colors [i][2]
                        r, g, b = blue_tap
                        iterate = i - start_index + tap_size
                        brightness = get_y_coords_for_index(iterate)
                        #logic for fadeout effect
                        r, g, b = [int(c * brightness / 255) for c in blue_tap]
                        r = max(x, x +(r ** factor - abs((i - start_index) / tapsizemodifier))/ brightmod) #the number controls the size of the tap. lower == bigger
                        g = max(y, y +(g ** factor - abs((i - start_index) / tapsizemodifier))/ brightmod)
                        b = max(z, z +(b ** factor - abs((i - start_index) / tapsizemodifier))/ brightmod)
                        #send colors to array
                        colors[i] = (r, g, b)

                elif current_time - effect["start_time"] <= (tap_speed / 5) * 3:
                    print("removed")
                    effects_to_remove.append(effect)

            if effect["effect_id"] == 4:  # Red TAP
                #made inverse mechanic that starts at 1 when fade out is trigger and ends at zero. wait
                fade_out_duration = (tap_speed / 5) / 1/2  # the same duration as your condition
                #logic for sine wave 
                osc_freq = effect["effect_var"]
                effect["effect_var"] = effect["effect_var"] / tap_speed
                x_values = np.arange(-tap_size, tap_size, 1) #size of tap
                y_values = [oscillating_parabola(x, osc_damp, osc_freq) for x in x_values]
                coordinates = [(int(x), int(oscillating_parabola(x, osc_damp, osc_freq))+ 127) for x in x_values]
                if current_time - effect["start_time"] <= ((tap_speed / 5) * 1/2):
                    for i in range(max(0, start_index - tap_size), min(strip_length, start_index + tap_size)):
                        
                        #getting old colors
                        x, y, z = colors[i][0], colors[i][1], colors [i][2]

                        #logic for the main tap brightness
                        iterate = i - start_index + tap_size
                        brightness = get_y_coords_for_index(iterate)
                        r, g, b = red_tap
                        r, g, b = [int(c * brightness / 255) for c in red_tap]
                        r = max(x, x +(r ** 1 - abs((i - start_index) / tapsizemodifier))/ brightmod) #the number controls the size of the tap. lower == bigger
                        g = max(y, y +(g ** 1 - abs((i - start_index) / tapsizemodifier))/ brightmod)
                        b = max(z, z +(b ** 1 - abs((i - start_index) / tapsizemodifier))/ brightmod)
                        
                        colors[i] = (r, g, b)
                elif current_time - effect["start_time"] <= (tap_speed / 5) * 2:
                    inverse = elapsed_time - fade_out_duration
                    inverse = max(0.0, 1.0 - (inverse / fade_out_duration))
                    factor = -1/2 * (math.cos(inverse * math.pi)) + 1/2
                    print(factor)
                    for i in range(max(0, start_index - tap_size), min(strip_length, start_index + tap_size)):
                        #getting old colors
                        x, y, z = colors[i][0], colors[i][1], colors [i][2]
                        r, g, b = red_tap
                        iterate = i - start_index + tap_size
                        brightness = get_y_coords_for_index(iterate)
                        #logic for fadeout effect
                        r, g, b = [int(c * brightness / 255) for c in red_tap]
                        r = max(x, x +(r ** factor - abs((i - start_index) / tapsizemodifier))/ brightmod) #the number controls the size of the tap. lower == bigger
                        g = max(y, y +(g ** factor - abs((i - start_index) / tapsizemodifier))/ brightmod)
                        b = max(z, z +(b ** factor - abs((i - start_index) / tapsizemodifier))/ brightmod)
                        #send colors to array
                        colors[i] = (r, g, b)

                elif current_time - effect["start_time"] <= (tap_speed / 5) * 3:
                    print("removed")
                    effects_to_remove.append(effect)
            
            if effect["effect_id"] == 8:  # Blue Hold
                
                inverse = 1 - (n - current_time) 
                frequency = 10
                x_values = np.arange(effect["effect_var"], (effect["effect_var"] + tap_size), 1)
                #print(x_values)
                effect["xvalue"] = np.concatenate([x_values, x_values[::-1]])
                effect["effect_var"] = effect["effect_var"] + 5
                amplitude = 127  # Example amplitude
                frequency = 0.04  # Example frequency
                effect["yvalue"] = sine_wave(effect["xvalue"], amplitude, frequency)
                iterate = 0

                if holdstart == True and effect["end"] == False:
                    tempb = min(tempb * 2, 1)
                    for i in range(max(0, start_index - tap_size), min(strip_length, start_index + tap_size)):
                        
                        #capture old colors
                        x, y, z = colors[i][0], colors[i][1], colors [i][2]

                        #logic for the main tap brightness
                        brightness = effect["yvalue"][iterate]
                        brightness = (brightness + 127) * tempb
                        iterate = iterate + 1

                        r, g, b = blue_tap
                        r = max(x, x +((r / 255) * brightness))
                        g = max(y, y +((g / 255) * brightness))
                        b = max(z, z +((b / 255) * brightness))

                        r, g, b = [int(c * brightness / 255) for c in blue_tap]
                        r = max(x, x + (r - abs((i - start_index) * tapsizemodifier)) / brightmod)  #the number controls the size of the tap. lower == bigger
                        g = max(y, y + (g - abs((i - start_index) * tapsizemodifier)) / brightmod) 
                        b = max(z, z + (b - abs((i - start_index) * tapsizemodifier)) / brightmod) 
                        
                        #send colors to array
                        temp_hold_blue_color[i] = (r, g, b)
                        colors[i] = (r, g, b)

                        effect["start_time"] = time.time() #for counting time AFTER note has ended (fade out effect)
                if holdstart == False or effect["end"] == True:
                    tempb = tempb * 1.5
                    for i in range(max(0, start_index - tap_size), min(strip_length, start_index + tap_size)):
                        r, g, b = temp_hold_blue_color[i][0], temp_hold_blue_color[i][1], temp_hold_blue_color[i][2]
                        index = i
                        x, y, z = colors[i][0], colors[i][1], colors [i][2]
                        
                        #logic for the main tap brightness
                        brightness = effect["yvalue"][iterate]
                        brightness = (brightness + 127)
                        iterate = iterate + 1

                        r, g, b = blue_tap
                        r = (r / 255) * brightness
                        g = (g / 255) * brightness
                        b = (b / 255) * brightness

                        r, g, b = [int(c * brightness / 255) for c in blue_tap]
                        r = r - abs((i - start_index) * tapsizemodifier) #the number controls the size of the tap. lower == bigger
                        g = g - abs((i - start_index) * tapsizemodifier)
                        b = b - abs((i - start_index) * tapsizemodifier)
                        
                        #send colors to array
                        r = max(x, x + ((r / tempb)) / brightmod)
                        g = max(y, y + ((g / tempb)) / brightmod)
                        b = max(z, z + ((b / tempb)) / brightmod)

                        temp_hold_blue_color[i] = (r, g, b)

                        colors[i] = (r, g, b)
                        effect["end"] = True
                    
                if current_time - effect["start_time"] >= 1:
                    tempb = 0.2
                    effects_to_remove.append(effect)
                    temp_hold_blue_color = [[0,0,0] for _ in range(strip_length)]

                
            if effect["effect_id"] == 9:  # Red Hold
                inverse = 1 - (n - current_time) 
                frequency = 10
                x_values = np.arange(effect["effect_var"], (effect["effect_var"] + tap_size), 1)
                #print(x_values)
                effect["xvalue"] = np.concatenate([x_values, x_values[::-1]]) 
                effect["effect_var"] = effect["effect_var"] + 5
                amplitude = 127  # Example amplitude
                frequency = 0.04  # Example frequency
                effect["yvalue"] = sine_wave(effect["xvalue"], amplitude, frequency) 
                iterate = 0

                if holdstart == True and effect["end"] == False:
                    tempr = min(tempr * 2, 1)
                    for i in range(max(0, start_index - tap_size), min(strip_length, start_index + tap_size)):
                        
                        #capture old colors
                        x, y, z = colors[i][0], colors[i][1], colors [i][2]

                        #logic for the main tap brightness
                        brightness = effect["yvalue"][iterate]
                        
                        brightness = (brightness + 127) * tempr
                        iterate = iterate + 1

                        r, g, b = red_tap
                        r = max(x, x +((r / 255) * brightness))
                        g = max(y, y +((g / 255) * brightness))
                        b = max(z, z +((b / 255) * brightness))

                        r, g, b = [int(c * brightness / 255) for c in red_tap]
                        r = max(x, x + (r - abs((i - start_index) * tapsizemodifier)) / brightmod)  #the number controls the size of the tap. lower == bigger
                        g = max(y, y + (g - abs((i - start_index) * tapsizemodifier)) / brightmod)
                        b = max(z, z + (b - abs((i - start_index) * tapsizemodifier)) / brightmod)
                        
                        #send colors to array

                        #compare old colors against new colors
                        if x >= r:
                            r = x
                        if y >= g:
                            g = y
                        if z >= b:
                            b = z
                        temp_hold_red_color[i] = (r, g, b)
                        colors[i] = (r, g, b)

                        effect["start_time"] = time.time() #for counting time AFTER note has ended (fade out effect)
                if holdstart == False or effect["end"] == True:
                    tempr = tempr * 1.5
                    for i in range(max(0, start_index - tap_size), min(strip_length, start_index + tap_size)):
                        r, g, b = temp_hold_red_color[i][0], temp_hold_red_color[i][1], temp_hold_red_color[i][2]
                        index = i
                        x, y, z = colors[i][0], colors[i][1], colors [i][2]
                        
                        #logic for the main tap brightness
                        brightness = effect["yvalue"][iterate]
                        brightness = (brightness + 127)
                        iterate = iterate + 1

                        r, g, b = red_tap
                        r = (r / 255) * brightness
                        g = (g / 255) * brightness
                        b = (b / 255) * brightness

                        r, g, b = [int(c * brightness / 255) for c in red_tap]
                        r = r - abs((i - start_index) * tapsizemodifier) #the number controls the size of the tap. lower == bigger
                        g = g - abs((i - start_index) * tapsizemodifier)
                        b = b - abs((i - start_index) * tapsizemodifier)
                        
                        #send colors to array
                        r = max(x, x + ((r / tempb)) / brightmod)
                        g = max(y, y + ((g / tempb)) / brightmod)
                        b = max(z, z + ((b / tempb)) / brightmod)

                        temp_hold_red_color[i] = (r, g, b)

                        colors[i] = (r, g, b)
                        effect["end"] = True
                        
                    
                if current_time - effect["start_time"] >= 1:
                    effects_to_remove.append(effect)
                    temp_hold_red_color = [[0,0,0] for _ in range(strip_length)]
                    tempr = 0.2

            if any(any(string in note for string in ["Blue Tap", "Red Tap", "Blue Match", "Red Match", "SectionContinuationOrEnd", "SpinLeftStart", "SpinRightStart"]) for note in notes):
                    for effect in active_effects:
                        if effect["effect_id"] == 7:
                            effects_to_remove.append(effect)
                            #print("removing effect 7")
                            break


            if effect["effect_id"] == 7 and scratch == True: #SCRATCH
                for i in range(start_index, strip_length):
                    r, g, b = colors[i][0], colors[i][1], colors[i][2]
                    d, e, f = scratch_min[0], scratch_min[1], scratch_min[2]
                    j, k, l = scratch_max[0], scratch_max[1], scratch_max[2]
                    x, y, z =  (random.randint(d, j), random.randint(e, k), random.randint(f, l))
                    r = r + x
                    g = g + y
                    b = b + z
                    colors[i] = r, g, b
                colors = colors[-s:] + colors[:-s]
                if s_down == True:
                    s = s - 6
                    if s <= -24:
                        s_down = False
                    break
                else:
                    s = s + 6
                    if s >= 24:
                        s_down = True
                    break 
            if effect["effect_id"] == 7 and scratch == False:
                effects_to_remove.append(effect)
    for effect in effects_to_remove:
        try:
            ##print(f"effect being removed{effect}")
            active_effects.remove(effect)
        except: 
            print("effect not found")
    return colors


def mouse_light_effect(start_index, effect_id):
    """Start a light effect at a given LED index with a unique effect ID."""
    global active_effects
    effect_id = 1
    # Add a new effect with its start time, index, and ID
    active_effects.append({
        "start_time": livetime(),
        "start_index": start_index,
        "effect_id": effect_id
    })


def start_main_loop(): # Open the serial connection
    global y_values, coordinates, effects_to_remove, previous_colors, update_serial, colors, port_status, ser
    with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
        #last_sent_time = time.time()
        t1 = threading.Thread(None, port_connect)
        t1.start()
        print("fag")
        while True:
            if update_serial:
                try:
                    print("port status changed")
                    ser.close()
                    ser = serial.Serial(serial_port, baud_rate, timeout=1)
                    port_status = f"Serial port {serial_port} connected!"
                    update_serial = False
                except serial.SerialException as e:
                    port_status = f"failed to communicate with port {serial_port} becasue: {e}"
                    time.sleep(1)
            else:
                if not t1.is_alive():
                    t1 = threading.Thread(None, port_connect)
                    t1.start()
                    print("restarting t1")
                last_sent_time = time.time()
                colors = [[0,0,0] for _ in range(strip_length)]
                # Measure start time
                #start_time = time.time()
                #if data != data_prev:

                #for tap effect
                x_values = np.arange(-tap_size, tap_size, 1) #size of tap
                y_values = [oscillating_parabola(x, osc_damp, osc_freq) for x in x_values]
                coordinates = [(int(x), int(oscillating_parabola(x, osc_damp, osc_freq))+ 127) for x in x_values]

                effects_to_remove = [] # reset effects to remove
                
                delaysend()
                on_match()
                update_colors()
                spin_start()
                tap_start()
                on_scratch()
                on_beat()
                on_hold()
                beat_end()
                on_release()
                on_sectioncontinuationorend()
                on_continue()
                previous_colors = colors
                update_effects()
                beats()
                send_colors(colors, ser)



            #time.sleep(0.1)
            # print(f"removed effects{effects_to_remove}")
            
            ##print(smoothed_colors[:2])

            # Measure execution time
            # execution_time = time.time() - start_time
            # #print(f"Loop executed in {execution_time:.6f} seconds")
            # execution_time = timeit.timeit("get_screen_colors()", globals=globals(), number=100)
            # #print(f"on_spin executed in {execution_time / 100:.6f} seconds per run (average)")