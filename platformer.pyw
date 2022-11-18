import platform, os
import win10toast
running = True

from plyer import notification
def push(title, message):
    plt = platform.system()
    if plt == "Darwin":
        command = '''
        osascript -e 'display notification "{message}" with title "{title}"'
        '''
    elif plt == "Linux":
        command = f'''
        notify-send "{title}" "{message}"
        '''
    elif plt == "Windows":
        notification.notify(
        app_name='GD Platformer Mod',
        title=title,
        message=message)
        return
    else:
        return
    os.system(command)

# change keyboard layout
import py_win_keyboard_layout
py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)

if not os.path.exists('config.txt'):
    print('config.txt does not exist! im creating it')
    push('creating config', 'config.txt does not exist! im creating it')
    with open('config.txt', 'a') as f:
        f.write('smoothing_iterations 20\nfps 240\n#smooting_iterations default is 10 and this value changes the way the movement smoothing works\n#the default fps is 60 and increasing this will make the program run faster allowing you to use higher fps in gd but this is at the cost of cpu usage')
        f.close()
    smooth_iter_c = 10
    loop_sleep = 0.0001
    fps = 60
else:
    try:
        with open('config.txt', 'r') as f:
            settings = f.readlines()
            splitted = settings[0].split(' ')
            splitted2 = settings[1].split(' ')
        smooth_iter_c = int(splitted[1])
        fps = int(splitted2[1])
    except:
        print('something is wrong in your config,\nill reset it rq')
        push('wrong config!', 'something is wrong in your config,\nill reset it rq')
        with open('config.txt', 'w+') as f:
            f.truncate(0)
            f.write('smoothing_iterations 20\nfps 240\n#smooting_iterations default is 10 and this value changes the way the movement smoothing works\n#the default fps is 60 and increasing this will make the program run faster allowing you to use higher fps in gd but this is at the cost of cpu usage')
            f.close()
        smooth_iter_c = 10
        loop_sleep = 0.0001
        fps = 60

import keyboard as k
import time
from sys import exit as sysexit
import time
from pygdmod.pygdmod import *
from requests import get as requestsget
import tkinter as tk
from tkinter import ttk
import _thread
import webbrowser
from pygame import time as clockt
from tkinter import ttk

#Gui
toggled = 0
toggled2 = 0

def main(useless1,useless2):
    global window
    global slider
    global speedhacklbl
    def changestate():
        global toggled
        global xpos
        if toggled == 1:
            toggled = 0
        else:  
            xpos = modloader.getXpos(1)
            toggled = 1

    def changestate2():
        global toggled2
        global xposp1, xposp2
        if toggled2 == 1:
            toggled2 = 0
        else:  
            xposp1 = modloader.getXpos(1)
            xposp2 = modloader.getXpos(2)
            toggled2 = 1

    def reloadsettings():
        global smooth_iter_c
        global loop_sleep
        global fps
        with open('config.txt', 'r') as f:
            settings = f.readlines()
            splitted = settings[0].split(' ')
            splitted2 = settings[1].split(' ')
        smooth_iter_c = int(splitted[1])
        fps = int(splitted2[1])
        push('Setting Synced', 'Setting Synced From config.txt')
        smoothing_iterations_label.config(text="Smoothing iterations: " + str(smooth_iter_c))
        FPSlabel.config(text="FPS: " + str(fps))

    def GitHubRepoOpen():
        webbrowser.open_new("https://github.com/TrollinDude/Platformer-Mode")

    window = tk.Tk()
    window.geometry('320x200')
    window.minsize(320,200)
    window.resizable(True, True)
    window.title('GD Platformer Mod')

    C1 = tk.Checkbutton(window, text = "Toggle Platformer Mode", command=changestate)
    C1.place(relx=.0, rely=0, anchor = "nw")

    C2 = tk.Checkbutton(window, text = "Toggle 2p Mode", command=changestate2)
    C2.place(relx=.0, rely=0, y = 22, anchor = "nw")

    ReSyncset = tk.Button(window, text="Reload config.txt", command=reloadsettings)
    ReSyncset.place(relx = 1, x =-2, y = 2, anchor="ne")

    smoothing_iterations_label = tk.Label(window, text="Smoothing iterations: " + str(smooth_iter_c), justify = "right", font=("Arial", 9))
    smoothing_iterations_label.place(relx = 1, x =-2, y = 33, anchor="ne")

    FPSlabel = tk.Label(window, text="FPS: " + str(fps), justify = "right", font=("Arial", 9))
    FPSlabel.place(relx = 1, x =-2, y = 50, anchor="ne")

    controlsInf = tk.Label(window, text="Controls:\nD -> P1 Move forward.\nA -> P1 Move back.\nRight -> P2 Move forward.\nLeft -> P2 Move back.\nZ -> Set chekpoint.\nX -> Remove chekpoint.", justify = "left", font=("Arial", 10))
    controlsInf.place(relx=.0, rely=0, y = 48, anchor = "nw")

    credits = tk.Label(window, text="Edited by user666\nOriginal by TrollinDude\nUsed gd.py by nekitdev", justify = "right", font=("Arial", 10))
    credits.place(relx = 1, x =-2, rely=1, y = 1, anchor = "se")

    GitHubRepoOpen = tk.Button(window, text="Github", command = GitHubRepoOpen)
    GitHubRepoOpen.place(relx=.0, rely=1, height=22, anchor="sw")

    def close_window():
        global running
        running = False 

    window.protocol("WM_DELETE_WINDOW", close_window)

    window.mainloop()

#end of gui

current_ver = 4

loop_init = False
xpos = 0
xposp1 = 0
xposp2 = 0
once = 1
once1 = 1
Clock = clockt.Clock()
try:
    modloader = GeometryDashModloader()
except:
    print("geometry dash not found")
    push('Geometry Dash not found', 'Geometry Dash not found, pls start the game first!')
    input()
    sysexit()
step = 0
prev_time = time.time()
checkpoints = [1]
nocheckpoint = 1
was_pressed_d = False
was_pressed_a = False
was_pressed_d1 = False
was_pressed_a1 = False
was_pressed_d2 = False
was_pressed_a2 = False

_thread.start_new_thread(main, (1,1))
speedhackval = 1

import gd.memory
# process name, can be changed for different executable names, I guess
PROCESS_NAME = "GDPS-2.2-by-user666"  # no need for ".exe"
# create gd.py memory object, without loading it (loaded when running)
memory = gd.memory.get_memory(PROCESS_NAME, load=True)

while 1:
    speedhack = modloader.getSpeedhack()

    '''
    Controls check
    '''
    if k.is_pressed("d") or k.is_pressed("right") and not isDead and toggled2 == 0:
        xpos += step * dt * 60 * speedhack
        was_pressed_d = True
        smooth_iter = smooth_iter_c
        memory.player_unfreeze()
        memory.player_unlock_jump_rotation()
    elif was_pressed_d:
        try:
            xpos += smooth_iter * dt * 60 * speedhack / smooth_iter
        except:
            was_pressed_d = False
        smooth_iter -= 1
        if smooth_iter == 1:
            was_pressed_d = False

    if k.is_pressed("a") or k.is_pressed("left") and not isDead and toggled2 == 0:
        xpos -= step * dt * 60 * speedhack
        was_pressed_a = True
        smooth_iter = smooth_iter_c
        memory.player_unfreeze()
        memory.player_unlock_jump_rotation()
    elif was_pressed_a:
        try:
            xpos -= smooth_iter * dt * 60 * speedhack / smooth_iter
        except:
            was_pressed_a = False
        smooth_iter -= 1
        if smooth_iter == 1:
            was_pressed_a = False


    if k.is_pressed("d") and not isDead and toggled2 == 1:
        xposp1 += step * dt * 60 * speedhack
        was_pressed_d1 = True
        smooth_iter1 = smooth_iter_c
        memory.player_unfreeze()
        memory.player_unlock_jump_rotation()
    elif was_pressed_d1 and toggled2 == 1:
        try:
            xposp1 += smooth_iter1 * dt * 60 * speedhack / smooth_iter1
        except:
            was_pressed_d1 = False
        smooth_iter1 -= 1
        if smooth_iter1 == 1:
            was_pressed_d1 = False

    if k.is_pressed("a") and not isDead and toggled2 == 1:
        xposp1 -= step * dt * 60 * speedhack
        was_pressed_a1 = True
        smooth_iter1 = smooth_iter_c
        memory.player_unfreeze()
        memory.player_unlock_jump_rotation()
    elif was_pressed_a1 and toggled2 == 1:
        try:
            xposp1 -= smooth_iter1 * dt * 60 * speedhack / smooth_iter1
        except:
            was_pressed_a1 = False
        smooth_iter1 -= 1
        if smooth_iter1 == 1:
            was_pressed_a1 = False

    if k.is_pressed("right") and not isDead and toggled2 == 1:
        xposp2 += step * dt * 60 * speedhack
        was_pressed_d2 = True
        smooth_iter2 = smooth_iter_c
        memory.player_unfreeze()
        memory.player_unlock_jump_rotation()
    elif was_pressed_d2 and toggled2 == 1:
        try:
            xposp2 += smooth_iter2 * dt * 60 * speedhack / smooth_iter2
        except:
            was_pressed_d2 = False
        smooth_iter2 -= 1
        if smooth_iter2 == 1:
            was_pressed_d2 = False

    if k.is_pressed("left") and not isDead and toggled2 == 1:
        xposp2 -= step * dt * 60 * speedhack
        was_pressed_a2 = True
        smooth_iter2 = smooth_iter_c
        memory.player_unfreeze()
        memory.player_unlock_jump_rotation()
    elif was_pressed_a2 and toggled2 == 1:
        try:
            xposp2 -= smooth_iter2 * dt * 60 * speedhack / smooth_iter2
        except:
            was_pressed_a2 = False
        smooth_iter2 -= 1
        if smooth_iter2 == 1:
            was_pressed_a2 = False

    now = time.time()
    dt = now - prev_time
    prev_time = now

    if modloader.isInEndscreen():
        checkpoints = []
        xpos = 1

    isDead = modloader.isDead()
    val6 = modloader.getPlayerSpeed()
    xposval = modloader.getXpos() # player 1 by default

    if xposval == 0:
        xpos = 1
        checkpoints = []

    #make it work in practice
    try:   
        if k.is_pressed("z") and once1 == 1 and modloader.isInPracticeMode():
            checkpoints.append([xpos, xposp1, xposp2])
            nocheckpoint = 0
            once1 = 0
        if k.is_pressed("z") == False and once1 == 0 and modloader.isInPracticeMode():
            once1 = 1

        if k.is_pressed("x") and once == 1 and modloader.isInPracticeMode():
            checkpoints.pop()
            once = 0
        if k.is_pressed("x") == False and once == 0 and modloader.isInPracticeMode():
            once = 1
    except:
        nocheckpoint = 1

    #respawning on check points
    if not isDead and toggled == 1 and toggled2 == 0:
        modloader.setXpos(pos=xpos, player='both') # set xpos of both players
    if isDead and toggled == 1 and toggled2 == 0:
        try:
            xpos = checkpoints[-1][0]
        except:
            ()
        if nocheckpoint == 1:
            xpos = 1

    if not isDead and toggled == 1 and toggled2 == 1:
        modloader.setXpos(pos=xposp1, player=1)
        modloader.setXpos(pos=xposp2, player=2)
    if isDead and toggled == 1 and toggled2 == 1:
        try:
            xposp1 = checkpoints[-1][1]
            xposp2 = checkpoints[-1][2]
        except:
            ()
        if nocheckpoint == 1:
            xposp1 = 1
            xposp2 = 1

    if xpos <= 0:
        xpos = 0
        xposp1 = 0
        xposp2 = 0

    if val6 == 0.699999988079071:
        step = 4.186001
    elif val6 == 0.8999999761581421:
        step = 5.193001747
    elif val6 == 1.100000023841858:
        step = 6.457002163
    elif val6 == 1.2999999523162842:
        step = 7.800002098
    elif val6 == 1.600000023841858:
        step = 9.600003242
    else:
        step = 4.186001

    if loop_init == False:
        modloader.setSpeedHack(1)
    if memory.gamemode.value == 4 and toggled == 1 and was_pressed_d == 0 and was_pressed_a == 0 and was_pressed_d1 == 0 and was_pressed_a1 == 0:
        memory.player_freeze()
    if toggled == 1 and was_pressed_d == 0 and was_pressed_a == 0 and was_pressed_d1 == 0 and was_pressed_a1 == 0:
        memory.player_lock_jump_rotation()
    if memory.is_in_level == True:
        xpos = 0
        xposp1 = 0
        xposp2 = 0


    if running == False:
        sysexit()

    loop_init = True
    Clock.tick(fps)