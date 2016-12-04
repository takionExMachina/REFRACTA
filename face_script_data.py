#-*- coding: UTF-8 -*-
import cv2
import openface
import dlib
import ftplib


"""
    Esta funcion se encarga de obtener los frames desde la camara y recortar el rostro,
    para luego guardar las imagenes con el nombre de la person como estiqueta

    @params None
    @returns None
"""
def generate():
    #se definen las rutas del predictor
    predictor_path =  './models/shape_predictor_68_face_landmarks.dat'

    #se define el detector como caras frontales
    detector = dlib.get_frontal_face_detector()

    #se define el predictor o modelo predictor
    predictor = dlib.shape_predictor(predictor_path)

    #modelo para alinear
    align = openface.AlignDlib(predictor_path)

    camera = cv2.VideoCapture(0)

    count = 0

    name = None

    option = 'Y'

    while(True):
        try:
            ret, frame = camera.read()

            #se transforma la lectura de la camara a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            box = cv2.resize(gray, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_CUBIC)

            #detectar rostros usando dlib
            faces_detected = detector(box)

            for k,d in enumerate(faces_detected):
                shape = predictor(box, d)
                roi_raw = gray[d.left():d.right(),d.top():d.bottom()]

                #definir el marco del rostro
                bounding_box = align.getLargestFaceBoundingBox(box)

                #alinear el rostro
                roi = align.align(96, box, bounding_box, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

                #se muestra la region de interes
                cv2.imshow("ROI", roi)

                #cv2.imwrite('./data/at/mg/%s.pgm' % str(count), f)
                count += 1

            #se muestra la captura de la camara
            cv2.imshow("camera", frame)

            #si se presiona la tecla c se captura el rostro
            if cv2.waitKey(100/12) & 0xff == ord("c"):

                #si no hay nombre registrado para la captura se solicita uno
                if name is None:
                    name = raw_input("Ingrese el nombre: ")
                else:
                    option = str.upper(raw_input("Es la misma persona? (Y)es (N)o: "))

                #se escribe el archivo
                cv2.imwrite('./imagenes/data/at/mg/' + str(name) + '_' + '%s.pgm' % str(count), roi)
                print "imagen guardada"

            if cv2.waitKey(100/12) & 0xff == ord("q"):
                break
        except:
            pass
    #se libera el recurso
    camera.release()

    #se cierran las ventanas
    cv2.destroyAllWindows()

if __name__ == "__main__":
    generate()
