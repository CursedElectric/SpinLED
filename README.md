this is still in wip hell

TODO:
change tap fadeouts to decrease in brightness uniformly, rather than what we got now
universialize a speed modifier so every node has a controllable speed factor (decides how fast the animations play + the duration of the note)

maaaybe combine each note color? idk if thats possible but its a lot of reused code so maybe

The Arduino.txt file needs to be copied and uploaded to your arduino board

TO BUILD PROJECT USE THIS LINE
pyinstaller --noconsole --onefile --add-data "C:\Users\Joshua Foster\AppData\Local\Programs\Python\Python312\Lib\site-packages\CTkColorPicker;CTkColorPicker" --add-data "SpinLED.py;." GUITest2.py