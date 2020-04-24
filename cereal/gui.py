import PySimpleGUI as sg

from cereal.helpers import get_serial

# Set theme
sg.theme('Material1')

# Menubar Options
menu = [['Configuration', ['Coming Soon...']]]

# Layout
layout = [[sg.Menu(menu)],
          [sg.Text('Cereal Messages')],
          [sg.Multiline(autoscroll=True, size=(50,10), key='cereal-log'+sg.WRITE_ONLY_KEY, disabled=True)],
          [sg.Text('Serial Monitor')],
          [sg.Multiline(autoscroll=True, size=(50,10), key='serial-log'+sg.WRITE_ONLY_KEY, disabled=True)],
          [sg.In(key='in'), sg.Button('Send')],
          [sg.Text('Set serial port'), sg.Combo(get_serial(), size=(20, 20), key='serial'), sg.Button('Refresh'), sg.Button('Start')],
          [sg.Checkbox('Autoscroll Serial Monitor', key='autoscroll', default=True, enable_events=True)],
          [sg.Button('Clear'), sg.Button('Stop'), sg.Button('Exit')]]

"""
Create application window
"""
window = sg.Window('Cereal', layout, finalize=True)


def clog(message):
    """
    Log to Cereal log

    Stupid implementation with no extra options

    :param message: Message to log
    """
    window['cereal-log'+sg.WRITE_ONLY_KEY].print(message)


def slog(message):
    """
    Log to Serial log

    Stupid implementation with no extra options

    :param message: Message to log
    """
    window['serial-log' + sg.WRITE_ONLY_KEY].print(message)
