"""
Oliver Giczi, 7B
Programm zum Herunterladen von Youtube-Videos


geändert:
- Benutzer kann nun auswählen, wo Datei gespeichert wird
- bei Schließen des Programmes wird thumbnail-Datei gelöscht
- nun kann man die Datei auch in .mp3 Format speichern
- Auswahl der Auflösung bei Video (360p und 720p) // geplant war auch 480p und 1080p, funktioniert aber nicht
- Logging (Datum, Dateiname, Speicherort und Dateigröße)
"""


# FF: vorher pytube3 installieren (pip3)


from tkinter import *                       # Importieren der benötigten Bibliotheken
from tkinter import simpledialog, filedialog
from pytube import YouTube
import urllib.request
from PIL import Image
import os
from datetime import date

old_dir = os.getcwd()

def btSuchenClick():
    global thumbnail, yt

    yt = YouTube(tLink.get())           # Eingabe in YT-Link umwandeln

    thumbnail_url = yt.thumbnail_url
    
    urllib.request.urlretrieve(thumbnail_url, "thumbnail.gif")     # Thumbnail des Videos herunterladen

    imageFile = "thumbnail.gif"
    im = Image.open(imageFile)
    im = im.resize((200, 200), Image.ANTIALIAS)
    im.save("thumbnail.gif")
    thumbnail = PhotoImage(file = "thumbnail.gif")
    canv.create_image(50, 50, image = thumbnail, anchor = CENTER)       # Thumbnail des Videos zeigen


def btDownloadClick():  # Video herunterladen;
    global data_format
    data_format = options.get()

    if data_format == ".mp3 (Audio)":       # wenn der Benutzer .mp3 Datei haben möchte;
        video = yt.streams.filter(only_audio=True).first()

        if not os.path.exists(video.title + ".mp3"):

            video.download()
            os.rename(video.title + ".mp4", video.title + ".mp3")


    if "360p" in data_format:            # wenn der Benutzer .mp4 Datei haben möchte; 360p
        video = yt.streams.get_by_resolution("360p")
        video.download()

    if "720p" in data_format:               # 720p
        video = yt.streams.get_by_resolution("720p")
        video.download()

    saveData(video)

def btSaveLocClick():      # Benuter wählt Ordner aus, wo er Datei speichern möchte
    os.chdir(str(filedialog.askdirectory()))


def saveData(video):    # die Daten werden in einer csv-Datei gespeichert
    titel = video.title

    datum = date.today()
    datum = datum.strftime("%d/%m/%Y")

    save_loc = os.getcwd()

    if ".mp3" in data_format:
        file_stats = os.stat(titel + ".mp3")

    else:
        file_stats = os.stat(titel + ".mp4")

    data_size = str(round(file_stats.st_size / (1024 * 1024), 2)) + " MB"

    log_name = "youtube_log.csv"

    if not os.path.exists(log_name):
        f = open(log_name, "w")
        worte = ["Titel", "Datum", "Speicherort", "Dateigröße"]
        for wort in worte:
            f.write(wort + ";")

        f.write("\n")

        f.close()

    f = open(log_name, "a")


    daten = [titel, datum, save_loc, data_size]

    for datei in daten:
        f.write(datei + ";")

    f.write("\n")
    f.close()



    f = open(log_name)
    lines = []
    for line in f:
        lines.append(line)

    f.close()

    new_lines = []

    for line in lines:
        if line not in new_lines:
            new_lines.append(line)

    f = open(log_name, "w")

    for line in new_lines:
        f.write(line)




win = Tk()		# Hauptfenster


win.title("Youtube-Downloader")		# Fenstertitel

bgColor = "#E0F1F7"     # Hintergrundfarbe 1
bgColor1 = "#809fff"    # Hintergrundfarbe 2

win.geometry("600x500")		# Größe des Fensters

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

lbAuthor = Label(win, text = "Copyright © Giczi Oliver 2020")
lbAuthor.place(relx = 0.5, rely = 0.94, anchor = CENTER)

win.mainloop()

os.chdir(old_dir)
os.remove("thumbnail.gif")
