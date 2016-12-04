import openface
import cv2
import dlib

def align_images(img):
    # se definen las rutas del predictor
    predictor_path = './models/shape_predictor_68_face_landmarks.dat'

    # modelo para alinear
    align = openface.AlignDlib(predictor_path)

    # se define el detector como caras frontales
    detector = dlib.get_frontal_face_detector()

    #se crea un arreglo con los rostros
    rois = []

    #box = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)

    try:
        # detectar rostros usando dlib
        faces_detected = detector(img)

        for k, d in enumerate(faces_detected):
            # definir el marco del rostro
            bounding_box = align.getLargestFaceBoundingBox(d)

            # alinear el rostro
            roi = align.align(96, img, bounding_box, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

            # se cambia el size de la imagen asociada al roi
            roi = cv2.resize(roi, (96, 96), interpolation=cv2.INTER_CUBIC)

            rois.append(roi)

        return rois
    except:
        pass