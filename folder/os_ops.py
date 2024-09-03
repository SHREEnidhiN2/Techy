import os
import subprocess as sp

paths = {
    'notepad': "C:\Windows\\notepad",
    'calculator': "C:\\Windows\\System32\\calc.exe"
}


def open_notepad():
    sp.Popen(['start', '/max', paths['notepad']], shell=True)


def open_cmd():
    sp.Popen(['start', '/max', 'cmd.exe'], shell=True)


def open_camera():
    # Example command to start the camera application in full screen if supported
    sp.Popen(['start', '/max', 'microsoft.windows.camera:'], shell=True)


def open_calculator():
    sp.Popen(['start', '/max', paths['calculator']], shell=True)
