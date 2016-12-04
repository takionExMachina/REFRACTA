# -*- coding: utf-8 -*-

import os
import cv2
import numpy
from equalize_histogram import EqualizeHistogram

def read_images(path):

    #se crea un contador y se inicializa
    count = 0

    #se crea un arreglo para guardar las imagenes y sus etiquetas respectivas
    X, y, c = [], [], []

    #se recorre el directorio entregado como argumento de la funcion
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]

    #se recorren las imagenes
    for image_path in image_paths:
        #se trabaja el string con el directorio para obtener el nombre de la persona
        strings = image_path.split("/", 12)

        #se lee la imagen en escala de grises
        im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        #se equaliza la imagen
        eq = EqualizeHistogram(im)

        """ im instead eq """

        #se cambia el tamaño de la imagen para reducir carga de procesamiento
        im = cv2.resize(im, (200, 200))

        #se agrega la matriz correspondiente a la imagen
        X.append(numpy.asarray(im, dtype = numpy.uint8))

        # Se obtienen el nombre asociado a la imagen
        string_name = strings[5].split('.',1)

        #se agrega la etiqueta de la imagen actual
        y.append(string_name[0])

        #se agrega el numero de imagen para el entrenamiento del modelo
        c.append(count)

        #se actualiza el contador
        count += 1
    #se retorna el arreglo de imagenes y etiquetas
    return [X, y, c]