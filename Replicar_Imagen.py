import numpy as np
from io import BytesIO
import requests
import matplotlib
from matplotlib import pyplot as plt
from PIL import Image
import random as rd
import math

prob_cruce = 0.8
prob_mutacion = 0.2
n_generaciones = 100

url = "https://rfbi.com.au/wp-content/uploads/Stay-Active-web-icon-100px-x-100px-300x300.jpg"
rta = requests.get(url)
imagen = Image.open(BytesIO(rta.content))

imgArrayOriginal = np.array(imagen)
print(imgArrayOriginal.shape)
plt.imshow(imgArrayOriginal)
plt.show()

imgAleatoria=np.array(imagen)
for i in range(len(imgAleatoria)):
  for j in range(len(imgAleatoria[0])):
   for ij in range(3):
    imgAleatoria[i][j][ij]=rd.randint(0, 255)

plt.title("Imagen Aleatoria")
print(imgAleatoria.shape)
plt.imshow(imgAleatoria)
plt.show()

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
        if rd.random() < prob_mutacion:
            cromosoma[i] = rd.randint(0, 255)
    return cromosoma

def cruce(cromosoma, cromosomaObjetivo):
    if rd.random() < prob_cruce:
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

for generacion in range(n_generaciones):
  print("Imagen Aleatoria Generacion: ", generacion +1)
  for i in range(len(imgAleatoria)):
        for j in range(len(imgAleatoria[0])):
            imgAleatoria[i][j] = cruce(imgAleatoria[i][j], imgArrayOriginal[i][j])
            #imgAleatoria[i][j] = mutacion(imgAleatoria[i][j])
            #aptitud = calcular_aptitud(imgAleatoria[i][j], imgArrayOriginal[i][j])
            #if(aptitud > 0.05):
            #   imgAleatoria[i][j] = mutacion(imgAleatoria[i][j])

    
    #print(imgAleatoria[800][500])
    #print(imgAleatoria[800][500][1])
    #plt.title("Imagen Aleatoria Generacion: ", generacion +1)
  plt.title(f"Imagen generación {generacion +1}")
  plt.imshow(imgAleatoria)
  plt.show()
    