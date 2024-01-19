from tkinter import *                      
from tkinter import filedialog
from pytube import YouTube
import urllib.request
from PIL import Image
import os, re

old_dir = os.getcwd()

def btSuchenClick():
    global thumbnail, yt
    # Eingabe in YT-Link umwandeln
    yt = YouTube(tLink.get())           

    # Thumbnail des Videos herunterladen und zeigen; wird nach dem Schließen des Programmes automatisch gelöscht (unten)
    thumbnail_url = yt.thumbnail_url
    
    urllib.request.urlretrieve(thumbnail_url, "thumbnail.gif")     

    imageFile = "thumbnail.gif"
    im = Image.open(imageFile)
    im = im.resize((200, 200), Image.ANTIALIAS)
    im.save("thumbnail.gif")
    thumbnail = PhotoImage(file = "thumbnail.gif")
    canv.create_image(50, 50, image = thumbnail, anchor = CENTER)

def btDownloadClick():
    global data_format
    data_format = options.get()

    if data_format == ".mp3 (Audio)":       
        video = yt.streams.filter(only_audio=True).first()
        video.download()
        # einfachste lösung, da es in pytube nicht möglich ist, direkt als mp3 herunterzuladen
        os.rename(video.title + ".mp4", video.title + ".mp3")

    else:
        res = re.search(r"\d{3}p", data_format)
        video = yt.streams.get_by_resolution(res.group())
        video.download()

# Benutzer wählt Ordner aus, wo Datei gespeichert werden sollte
def btSaveLocClick():      
    os.chdir(str(filedialog.askdirectory()))

win = Tk()		
win.title("Youtube-Downloader")		

# Hintergrundfarbe 1
bgColor = "#E0F1F7"    
# Hintergrundfarbe 2 
bgColor1 = "#809fff"    
# Größe des Fensters
win.geometry("600x500")		

win.configure(background = bgColor)

lbTitel = Label(win, text = "Youtube - Downloader", bg = "orange", width = 50, font = "Helvetica 18 bold")
lbTitel.place(relx = 0.5, rely = 0.05, anchor = CENTER)

lbLink = Label(win, text = "Video-Link", bg = bgColor1, width = 50, font = "Helvetica 10 bold")
lbLink.place(relx = 0.5, rely = 0.14, anchor = CENTER)

tLink = Entry(win, width = 80)
tLink.place(relx = 0.5, rely = 0.2, anchor = CENTER)
tLink.insert(END,"https://www.youtube.com/watch?v=LXb3EKWsInQ")

btSuchen = Button(win, text = "Suchen", command = btSuchenClick)
btSuchen.configure(height = 2, width = 20)
btSuchen.place(relx = 0.5, rely = 0.3, anchor = CENTER)

canv = Canvas(win, width = 100, height = 100, bg = "white")
canv.place(relx = 0.2, rely = 0.35, anchor = CENTER)

lbLine = Label(win, text = ("="*100), bg = bgColor, font = "Helvetica 15")
lbLine.place(relx = 0.5, rely = 0.5, anchor = CENTER)

options = StringVar(win)
options.set("Datei-Format auswählen")
tab = (" " * 10)
omFormat = OptionMenu(win, options, ".mp3 (Audio)", ".mp4 (Video; 360p)", tab + "(Video, 720p)")
omFormat.place(relx = 0.5, rely = 0.55, width = 200, anchor = CENTER)

btSaveLoc = Button(win, text = "Wo soll die Datei gespeichert werden?", command = btSaveLocClick)
btSaveLoc.configure(height = 1, width = 40)
btSaveLoc.place(relx = 0.5, rely = 0.62, anchor = CENTER)

lbLine = Label(win, text = ("="*100), bg = bgColor, font = "Helvetica 15")
lbLine.place(relx = 0.5, rely = 0.7, anchor = CENTER)

btDownload = Button(win, text = "Herunterladen", command = btDownloadClick)
btDownload.configure(height = 3, width = 50)
btDownload.place(relx = 0.5, rely = 0.8, anchor = CENTER)

lbAuthor = Label(win, text = "Oliver Giczi")
lbAuthor.place(relx = 0.5, rely = 0.94, anchor = CENTER)

win.mainloop()

os.chdir(old_dir)
path = "thumbnail.gif"
if os.path.isfile(path):
    os.remove("thumbnail.gif")