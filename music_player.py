from tkinter import *
from tkinter.ttk import Progressbar
import pygame
import os
import eyed3
from tkinter import filedialog


root = Tk()
root.title("Music Player")
root.geometry("1000x400+200+200")
pygame.init()
pygame.mixer.init()
track = StringVar()
status = StringVar()

trackframe = LabelFrame(root, text="Song Track", font = ("times new roman", 15, "bold"), bg = "grey", fg = "white", bd = 5, relief = GROOVE)
trackframe.place(x = 0, y = 0, width = 600, height = 100)
songtrack = Label(trackframe, textvariable = track, width = 20, font = ('times new roman',24,'bold'), bg = 'grey', fg = 'gold').grid(row = 0, column = 0, padx = 1, pady = 5)
trackstatus = Label(trackframe, textvariable = status, font = ("times new roman", 24, "bold"), bg = "grey", fg = "gold").grid(row = 0, column = 0, padx = 10, pady = 5)
buttonframe = LabelFrame(root, text = "Control Panel", font =("times new roman",15,"bold"), bg = "grey", fg = "white", bd = 5, relief  = GROOVE)
buttonframe.place(x = 0, y = 100, width = 600, height = 100)
songsframe = LabelFrame(root, text = "Song Playlist", font = ("times new roman", 15, "bold"), bg = "grey", fg = "white", bd = 5, relief = GROOVE)
songsframe.place(x = 600, y = 0, width = 400, height = 200)
scrol_y = Scrollbar(songsframe, orient = VERTICAL)
playlist = Listbox(songsframe, yscrollcommand = scrol_y.set, selectbackground = "gold", selectmode = SINGLE, font = ("times new roman", 12, "bold"), bg = "silver", fg = "navyblue", bd = 5, relief = GROOVE)
scrol_y.pack(side = RIGHT, fill = Y)
scrol_y.config(command = playlist.yview)
playlist.pack(fill = BOTH)

def directory():
    os.chdir(filedialog.askdirectory())
    songtracks = os.listdir()
    for track in songtracks:
        playlist.insert(END, track)


progres = LabelFrame(root, text = "Progress", font = ("times new roman", 15, "bold"), bg = "grey", fg = "white", bd = 5, relief = GROOVE)
progres.place(x = 0, y = 200, width = 1000, height = 200)

menu = Menu(root, bg = "grey", fg = "gold")
new_item = Menu(menu)
new_item.add_command(label = "SELECT FOLDER", command = directory)
new_item.add_command(label = "QUIT", command = quit)
menu.add_cascade(label = "File", menu = new_item)
root.config(menu = menu)
        


def playsong():
    global dur
    global o_t
    global val
    temp = playlist.get(ACTIVE)
    status.set(temp + "Playing")
    pygame.mixer.music.load(playlist.get(ACTIVE))
    pygame.mixer.music.play()
    dur = eyed3.load(playlist.get(ACTIVE)).info.time_secs
    bar.config(maximum = dur)
    mins = dur // 60
    dur = dur % 60
    hours = mins // 60
    mins = mins % 60
    o_t = str(int(hours))+" : "+str(int(mins))+" : "+str(int(dur))
    l = Label(progres, bg = "grey", font = ("times new roman", 16, "bold"))
    l.configure(text = " / " + o_t)
    l.place(x = 500, y = 50)
    val = 1


def stopsong():
    status.set("Stopped")
    pygame.mixer.music.stop()


def pausesong():
    status.set("Paused")
    pygame.mixer.music.pause()

def unpausesong():
    status.set("Resumed")
    pygame.mixer.music.unpause()
    
sec = 0

def tick():
    global dur
    global sec
    bar['value'] = sec
    sec = pygame.mixer.music.get_pos()//1000 + 1
    try:
        val == 1
        timer += 1
    except NameError:
        pass
    try:
        x = int(vol.get())
        pygame.mixer.music.set_volume(x/10)
    except:
        pass
    mins = sec // 60
    sec1 = sec % 60
    hours = mins // 60
    mins = mins % 60
    t = str(hours)+" : "+str(mins)+" : "+str(sec1)
    lbl.configure(text = t)
    bar.after(1000, tick)

vol_count = IntVar()
vol_count.set(10)

vol = Spinbox(buttonframe, from_ = 0, to = 10, font = ("times new roman",16,"bold"), bg = "grey", fg = "gold", bd = 5, width = 5, textvariable = vol_count)
vol.grid(row = 0, column = 6)

vol_lbl = Label(buttonframe, text = "Volume  ",bg = "grey",fg = "gold", font = ("times new roman",10,"bold"))
vol_lbl.grid(row = 0,column = 4)

pausebtn = Button(buttonframe, text = "Pause", command = pausesong, width = 6, height = 1,font = ("times new roman",16,"bold"), fg = "navyblue", bg = "gold").grid(row = 0,column = 1,padx = 10,pady = 5)
unpausebtn = Button(buttonframe, text = "Resume", command = unpausesong, width = 6, height = 1,font = ("times new roman",16,"bold"), fg = "navyblue", bg = "gold").grid(row = 0,column = 2,padx = 10,pady = 5)
stopbtn = Button(buttonframe, text = "Stop", command = stopsong, width = 6, height = 1,font = ("times new roman",16,"bold"), fg = "navyblue", bg = "gold").grid(row = 0,column = 3,padx = 10,pady = 5)
playbtn = Button(buttonframe, text = "Play", command = playsong, width = 6, height = 1,font = ("times new roman",16,"bold"), fg = "navyblue", bg = "gold").grid(row = 0,column = 0,padx = 10,pady = 5)

bar = Progressbar(progres, length = 850)
bar.place(x = 55, y = 100)
lbl = Label(progres, bg = "grey", font = ("times new roman", 16, "bold"))
lbl.place(x = 400, y = 50)
tick()


root.mainloop()
