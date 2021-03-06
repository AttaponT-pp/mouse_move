import os
import win32api, win32con
import pywintypes
from time import sleep
from random import randint
from tkinter import *
from tkinter import ttk
from qq import *
import base64


def set_icon():
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(img))  # Write to temporary file
    tmp.close()
    root.iconbitmap("tmp.ico")  # Set icon
    os.remove("tmp.ico")  # Remove dying icon


def step_up(position):
    # increase progress bar (10 min)
    progress['value'] += 0.1
    sleep(0.1)
    try:
        position_next = win32api.GetCursorPos()
        if position != position_next:
            # clear progress bar
            progress['value'] = 0
    except pywintypes.error:
        pass


def clear_step():
    # clear progress bar
    progress['value'] = 0
    # get screen size
    x_max = win32api.GetSystemMetrics(0) - 1
    y_max = win32api.GetSystemMetrics(1) - 40
    pos_next = (randint(0, x_max), randint(0, y_max))
    # print('X = {}   Y = {}'.format(pos_next[0], pos_next[1]))
    # set new mouse position
    try:
        win32api.SetCursorPos(pos_next)
        # perform left click
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, pos_next[0], pos_next[1], 0, 0)
        sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, pos_next[0], pos_next[1], 0, 0)
        lbl1.config(text='X = {}   Y = {}'.format(pos_next[0], pos_next[1]))
    except pywintypes.error:
        print('Cannot set new mouse position.')
        pass


def mouse_move():
    # get mouse position
    try:
        pos = win32api.GetCursorPos()
        # print('X = {}   Y = {}'.format(pos[0], pos[1]))
        lbl1.config(text='X = {}   Y = {}'.format(pos[0], pos[1]))
        step_up(pos)
    except pywintypes.error:
        pass
    if progress['value'] > 100:
        clear_step()
    root.after(10, mouse_move)


# create Tkinter
root = Tk()
# change title name
root.title('MOUSE-MOVE')
# set application's icon
# root.iconbitmap('E:\\PythonProject\\MouseMove\\mouse.ico')
set_icon()
# set geometry and fix
root.geometry("250x45")
root.resizable(0, 0)
# add label
lbl1 = Label(root, text='')
lbl1.pack()
# add progress bar
progress = ttk.Progressbar(root, orient=HORIZONTAL, length=200, mode='determinate')
progress.pack()
# call function
mouse_move()
# Set application always on top
# root.wm_attributes("-topmost", 1)
# Hide the apps after launch
root.withdraw()
# update application gui
root.update()
# Reveal the application
root.iconify()
# launch the app
root.mainloop()