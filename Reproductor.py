from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pygame
import os

pygame.mixer.init()
#Variables
pausa = False
volumen = 0.5
duracion = 0
TiempoActual = 0
TiempoRestante = 0

#Funciones reproductor
def Play():
    global pausa
    pygame.mixer.music.play()
    if pausa == True:
        pausa = False
def PlayPause():
    global pausa
    if pausa == False:
        pygame.mixer.music.pause()
        pausa = True
    else:
        pygame.mixer.music.unpause()
        pausa = False

def Vol_up():
    global volumen
    if volumen < 1:
        volumen += 0.1
        pygame.mixer.music.set_volume(volumen)

def Vol_down():
    global volumen
    if volumen > 0:
        volumen -= 0.1
        pygame.mixer.music.set_volume(volumen)

def actualizar_tiempo():
    global TiempoRestante, TiempoActual
    actual = pygame.mixer.music.get_pos() / 1000
    if actual >= 0:
        TiempoActual = round(actual)
        min, seg = divmod(int(TiempoActual), 60)
        Time.config(text = f"{min:02d}:{seg:02d}")
        TiempoRestante = max(0, round(duracion - TiempoActual))
        min, seg = divmod(int(TiempoRestante), 60)
        Time2.config(text = f"{min:02d}:{seg:02d}")
        barra.set(TiempoActual)
    v.after(1000, actualizar_tiempo)

#Finciones Menu
def Cargar():
    global duracion
    ruta = filedialog.askopenfilename(filetypes = [("Archivos de audio", "*.mp3")])
    if ruta != "":
        name_music.config(text = f"Reproduciendo:\n{os.path.basename(ruta)}")
        duracion = pygame.mixer.Sound(ruta).get_length()
        min, seg = divmod(int(duracion),60)
        Time2.config(text = f"{min:02d}:{seg:02d}")
        barra.config(to = round(duracion))
    pygame.mixer.music.load(ruta)
    actualizar_tiempo()    

#Ventana principal
v = Tk()
v.title("Reproductor de Música")
v.geometry("1000x600")
v.resizable(False, False)
icon = PhotoImage(file = r"imagenes\Nota musiacal.png")
v.iconphoto(False, icon)

#Menu
Opciones = Menu(v)
v.config(menu = Opciones)
File = Menu(Opciones, tearoff = 0, activebackground = "LIGHT GREY", activeforeground = "#000000")
Opciones.add_cascade(label = "Opcciones", menu = File)
File.add_command(label= "Cargar archivo", command = Cargar)

#Frames
contenedor = Frame(v)
contenedor.pack(side = BOTTOM)

contenedor2 = Frame(v)
contenedor2.pack(side = RIGHT)

contenedor3 = Frame(v)
contenedor3.pack(side = BOTTOM, fill = X, padx = 20)

#Mostrar nombre de la canción
name_music = Label(v, text = "Cargue una canción", font = ("Arial", 20), wraplength = 800, justify = "center")
name_music.pack(side = TOP)

#Boton de play
btn_play = Button(contenedor, command = Play ,text = "▶", font = ("Arial", 20))
btn_play.pack(side = LEFT)

#Boton de pause
btn_pause = Button(contenedor, command = PlayPause ,text = "⏸", font = ("Arial", 20))
btn_pause.pack(side = LEFT)

#Boton volumen +
btn_pause = Button(contenedor2, command = Vol_up, text = "Vol+", font = ("Arial", 20))
btn_pause.pack(side = TOP)

#Boton volumen -
btn_pause = Button(contenedor2, command = Vol_down, text = "Vol-", font = ("Arial", 20))
btn_pause.pack(side = TOP)

#Texto duracion de la canción
Time = Label(contenedor3, text = "00:00", font = ("Arial", 10))
Time.pack(side = LEFT)

#Barra de progreso
barra = ttk.Scale(contenedor3, from_ = 0,to = 100, orient = "horizontal")
barra.pack(side = "right", fill = "x", expand = True, padx = 10)


Time2 = Label(contenedor3, text = "00:00", font = ("Arial", 10))
Time2.pack(side = RIGHT)


v.mainloop()