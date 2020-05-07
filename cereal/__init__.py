"""
   _____                    _
  / ____|                  | |
 | |     ___ _ __ ___  __ _| |
 | |    / _ \ '__/ _ \/ _` | |
 | |___|  __/ | |  __/ (_| | |
  \_____\___|_|  \___|\__,_|_|

        Serial Monitor

Cereal is a basic Python-based serial monitor with a GUI.
Expand it for your own projects!
For example convert Serial to OSC or MIDI!

Created by Ben Saltz
"""

import atexit

import PySimpleGUI as sg

from cereal.gui import slog, clog, window
from cereal.helpers import get_serial
from cereal.task import CerealTask

task = CerealTask()

# Register Exit Handler
atexit.register(task.exit)

clog("Initialized at 9600 baud.")

while True:
    # Get Window Events
    event, values = window.read(timeout=5)

    # Exit
    if event in (None, 'Exit'):
        break

    # Clear Serial Console
    if event == 'Clear':
        window['serial-log'+sg.WRITE_ONLY_KEY].update('')

    # Refresh Device List
    if event == 'Refresh':
        clog('Updating serial device list...')
        window['serial'].update(get_serial())
        clog('Done')

    # Start listening to serial device
    if event == 'Start':
        task.set_device(values.get('serial'))

    # Stop listening to serial device
    if event == 'Stop':
        clog('Stopping...')
        task.stop()
    
    # Send Serial Data
    if event == 'Send':
        if task.device is not None:
            clog("Sent: {}".format(values.get('in')))
            task.device.write(bytes(values.get('in'), encoding='utf8') + b'\r')

    # Toggle autoscroll
    if event == 'autoscroll':
        window['serial-log'+sg.WRITE_ONLY_KEY].update(autoscroll=values.get('autoscroll'))

# Close Window
window.close()

# Teardown
task.exit()

quit()
