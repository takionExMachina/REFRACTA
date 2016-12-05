# -*- coding: utf-8 -*-

import numpy
import cv2
from read_images import read_images
from process_faces import align_images

def RecognizeFaces():
    path_train = './imagenes/data/at/mg/'

    path_img = './imagenes/captured.pgm'

    images = read_images(path_train) # [X, y, c] [imagen, label, contador]

    model = cv2.createLBPHFaceRecognizer()

    # se entrena el modelo con las imagenes del arreglo
    model.train(numpy.asarray(images[0]), numpy.asarray(images[2]))

    img = cv2.imread(path_img, 0)

    rois = align_images(img)

    # se aplica el modelo al roi
    id, con = model.predict(rois[0])

    imagen = images[1][id]

    if con > 80:
        message =  'No hay registro asociado'
    else:
        message =  imagen

    return message
