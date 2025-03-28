import numpy as np
from io import BytesIO
import requests
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image as IM
import random as rd
import math
from tkinter import *
from tkinter import ttk


ventana = Tk()
#prob_cruce = 0.8
#prob_mutacion = 0.2
#n_generaciones = 100
imgArrayOriginal = np.array(None)
imgAleatoria = np.array(None)
url = StringVar()
prob_cruce = IntVar()
prob_mutacion = IntVar()
n_generaciones = IntVar()
imagen = None

url.set("https://rfbi.com.au/wp-content/uploads/Stay-Active-web-icon-100px-x-100px-300x300.jpg")
prob_cruce.set(80)
prob_mutacion.set(3)
n_generaciones.set(10)
imagen_objetivo = None
imagen_aleatoria = None
imagen_resultado = None



main_frame = Frame(ventana)
my_Canvas = Canvas(main_frame)
Canvas_frame = ttk.LabelFrame(my_Canvas, padding="20 10 10 40")
Result_frame = ttk.LabelFrame(Canvas_frame, padding="20 10 20 10")


def leer_imagen():
    #url = "https://rfbi.com.au/wp-content/uploads/Stay-Active-web-icon-100px-x-100px-300x300.jpg"
    rta = requests.get(url.get())
    global imagen 
    imagen = IM.open(BytesIO(rta.content))
    global imgArrayOriginal 
    imgArrayOriginal = np.array(imagen)

    print(imgArrayOriginal.shape)
    #plt.imshow(imgArrayOriginal)
    #plt.show()
    plt.clf()

    for widget in Result_frame.winfo_children():
        widget.destroy()
    
    imagen_objetivo = plt.figure(figsize=(3, 3))
    plt.imshow(imgArrayOriginal)
    canvas_imgOriginal = FigureCanvasTkAgg(imagen_objetivo, master=Result_frame)
    canvas_imgOriginal.draw()
    canvas_imgOriginal.get_tk_widget().grid(column=0, row=1, columnspan=10, rowspan=10, pady=(5,0), padx=2, sticky=(W, E))

def generar_imagen_aleatoria():
    global imgAleatoria
    imgAleatoria =np.array(imagen)
    for i in range(len(imgAleatoria)):
        for j in range(len(imgAleatoria[0])):
            for ij in range(3):
                imgAleatoria[i][j][ij]=rd.randint(0, 255)
    
    #print(imgAleatoria.shape)
    #plt.imshow(imgAleatoria)
    #plt.show()
    imagen_aleatoria = plt.figure(figsize=(3, 3))
    plt.title("Imagen Aleatoria")
    plt.imshow(imgAleatoria)
    canvas_imgAleatoria = FigureCanvasTkAgg(imagen_aleatoria, master=Result_frame)
    canvas_imgAleatoria.draw()
    canvas_imgAleatoria.get_tk_widget().grid(column=0, row=14, columnspan=10, rowspan=10, pady=(5,0), padx=2, sticky=(W, E))

def calcular_aptitud(cromosoma, cromosomaObjetivo):

    aptitud = 0
    for i in range(len(cromosoma)):
        aptitud = aptitud + (math.pow(abs(cromosomaObjetivo[i] - cromosoma[i]),2))
    aptitud = aptitud/len(cromosoma)
    return (1/(aptitud+1))
    #aptitud_R = abs(float(cromosomaObjetivo[0]) - float(cromosoma[0]))
    #aptitud_G = abs(float(cromosomaObjetivo[1]) - float(cromosoma[1]))
    #aptitud_B = abs(float(cromosomaObjetivo[2]) - float(cromosoma[2]))
    #aptitud = 1/(1+((math.pow(aptitud_R, 2) + math.pow(aptitud_G, 2) + math.pow(aptitud_B, 2)) / 3))
    #return aptitud

def mutacion(cromosoma):
    for i in range(len(cromosoma)):
        if rd.random() < float(prob_mutacion.get()/100):
            cromosoma[i] = rd.randint(0, 255)
    return cromosoma

def cruce(cromosoma, cromosomaObjetivo):
    if rd.random() < float(prob_cruce.get()/100):
        punto_cruce = rd.randint(1, len(cromosoma)-1)
        #punto_cruce = 1
        cromosoma_mutado = mutacion(cromosoma)
        #cromosoma_mutado = np.concatenate((cromosoma_mutado[:punto_cruce], cromosoma[punto_cruce:]))

        cromosoma_mutado = np.concatenate((cromosomaObjetivo[:punto_cruce], cromosoma_mutado[punto_cruce:]))

        nuevo_cromosoma_1 = np.concatenate((cromosoma_mutado[:punto_cruce], cromosoma[punto_cruce:]))
        nuevo_cromosoma_2 = np.concatenate((cromosoma[:punto_cruce], cromosoma_mutado[punto_cruce:]))
        #nuevo_cromosoma_1 = np.concatenate((cromosoma_mutado[:punto_cruce], cromosomaObjetivo[punto_cruce:]))
        #nuevo_cromosoma_2 = np.concatenate((cromosomaObjetivo[:punto_cruce], cromosoma_mutado[punto_cruce:]))

        # Mutación opcional de los nuevos cromosomas
        nuevo_cromosoma_1 = mutacion(nuevo_cromosoma_1)
        nuevo_cromosoma_2 = mutacion(nuevo_cromosoma_2)

        aptitud_cromosoma_1 = calcular_aptitud(nuevo_cromosoma_1, cromosomaObjetivo)
        aptitud_cromosoma_2 = calcular_aptitud(nuevo_cromosoma_2, cromosomaObjetivo)
        aptitud_cromosoma = calcular_aptitud(cromosoma, cromosomaObjetivo)

        if aptitud_cromosoma_1 > aptitud_cromosoma_2 and aptitud_cromosoma_1 > aptitud_cromosoma:
            return nuevo_cromosoma_1
        elif aptitud_cromosoma_2 > aptitud_cromosoma and aptitud_cromosoma_2 > aptitud_cromosoma_1:
            return nuevo_cromosoma_2
        else:
            return cromosoma
    return cromosoma

def igualar_imagen():
    for generacion in range(n_generaciones.get()):
        print("Imagen Aleatoria Generacion: ", generacion +1)
        for i in range(len(imgAleatoria)):
            for j in range(len(imgAleatoria[0])):
                imgAleatoria[i][j] = cruce(imgAleatoria[i][j], imgArrayOriginal[i][j])
        
        #plt.imshow(imgAleatoria)
        #plt.show()
        imagen_resultado = plt.figure(figsize=(3, 3))
        plt.title(f"Imagen generación {generacion +1}")
        plt.imshow(imgAleatoria)
    canvas_imgAleatoria = FigureCanvasTkAgg(imagen_resultado, master=Result_frame)
    canvas_imgAleatoria.draw()
    canvas_imgAleatoria.get_tk_widget().grid(column=0, row=24, columnspan=10, rowspan=10, pady=(5,0), padx=2, sticky=(W, E))

def Interface_Grafica():
    main_frame.pack(fill=BOTH, expand=1)
    
    ventana.columnconfigure(0, weight=1)
    ventana.rowconfigure(0, weight=1)

    my_Canvas.pack(side=LEFT, expand=1, fill=BOTH, pady=(10, 30))

    my_Scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_Canvas.yview)
    my_Scrollbar.pack(side=RIGHT, fill=Y)

    my_Canvas.configure(yscrollcommand=my_Scrollbar.set)
    my_Canvas.bind('<Configure>', lambda e: my_Canvas.configure(scrollregion= my_Canvas.bbox("all")))
    Canvas_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    my_Canvas.create_window((0,0), window=Canvas_frame, anchor="nw")
    #Canva Resultado
    s = ttk.Style()
    s.configure('My.TFrame', background='#c6c6c6', color='black')

    #Canvas_Frame
    ttk.Label(Canvas_frame, text="URL: "). grid(column=0, row=0, sticky=(E), pady=(30, 0))
    url_Entry = ttk.Entry(Canvas_frame, width=30, textvariable=url)
    url_Entry.grid(column=1, row=0, pady=(30, 0))
    url_Entry.focus()
    ttk.Label(Canvas_frame, text="Probabilidad de Cruce: "). grid(column=0, row=1, sticky=(E), pady=(10, 0))
    cruce_Entry = ttk.Entry(Canvas_frame, width=30, textvariable=prob_cruce)
    cruce_Entry.grid(column=1, row=1, pady=(10, 0))
    ttk.Label(Canvas_frame, text="Probabilidad de Mutacion: "). grid(column=0, row=2, sticky=(E), pady=(10, 0))
    cruce_Entry = ttk.Entry(Canvas_frame, width=30, textvariable=prob_mutacion)
    cruce_Entry.grid(column=1, row=2, pady=(10, 0))
    ttk.Label(Canvas_frame, text="Generaciones: "). grid(column=0, row=3, sticky=(E), pady=(10, 0))
    generaciones_Entry = ttk.Entry(Canvas_frame, width=30, textvariable=n_generaciones)
    generaciones_Entry.grid(column=1, row=3, pady=(10, 0))
    ttk.Label(Canvas_frame, text="______________________________________________________________________________"). grid(column=0, row=4, columnspan=10, sticky=(E), pady=(10, 0))

    ttk.Button(Canvas_frame, text="Leer Imagen", padding="0 5 0 5", command=leer_imagen).grid(column=0, row=5, columnspan=2, pady=(5,0), padx=2, sticky=(W, E))
    ttk.Button(Canvas_frame, text="Generar Imagen Aleatoria", padding="0 5 0 5", command=generar_imagen_aleatoria).grid(column=0, row=6, columnspan=2, pady=(5,0), padx=2, sticky=(W, E))
    ttk.Button(Canvas_frame, text="Iniciar Algoritmo Genetico", padding="0 5 0 5", command=igualar_imagen).grid(column=0, row=7, columnspan=2, pady=(5,0), padx=2, sticky=(W, E))

    #ttk.Button(main_frame, text="Limpiar", width=15, padding="0 5 0 5", command=LimpiarInformarcion).grid(column=3, row=11, columnspan=2, pady=(5,0), padx=2, sticky=(W, E))
    #ttk.Label(main_frame, text="______________________________________________________________________________"). grid(column=0, row=12, columnspan=10, sticky=(E), pady=(0, 0))
    
    Result_frame.grid(column=0, row=8, columnspan=20, rowspan=50, sticky=(N, W, E, S))
    ventana.mainloop()

def main():
    ventana.geometry("400x700")
    ventana.minsize(400,700)
    ventana.maxsize(400,800)
    ventana.title("Generador de Imagenes")
    Interface_Grafica()

if __name__ == "__main__":
    main()