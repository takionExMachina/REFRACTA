from clientGUI import *

def clienRefracta():
    import cv2


    camera = cv2.VideoCapture(0)

    haar = './models/haarcascade_frontalface_default.xml'

    classifier = cv2.CascadeClassifier(haar)

    count = 0

    while True:
        try:
            count += 1
            _, frame = camera.read()
            if count % 5:
                frame = cv2.resize(frame, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_LINEAR)
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces = classifier.detectMultiScale(gray,1.2, 5)

                r = 0
                g = 255
                b = 0

                roi = None

                if faces is not None:
                    for x, y, w, h in faces:
                        roi = gray[x:x+w,y:y+h]

                        save = cv2.imwrite('./data/captured.pgm', roi)

                        if save:
                            message = sendFace()

                            if message != 'No hay registros asociados a la persona':
                                r = 255
                                g = 0
                                b = 0
                            else:
                                r = 0
                                g = 255
                                b = 0

                        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (b, g, r), 3)
                frame = cv2.cvtColor(frame,cv2.COLOR_RGB2RGBA)
                show_frame(frame)
        except:
            pass



def sendFace():
    from zeep import Client
    import base64

    face_recog = Client('http://localhost:8000/?wsdl')

    with open('./data/captured.pgm', 'rb') as image:
        string = base64.b64encode(image.read())

    result = face_recog.service.say_hello(string)

    response = ''

    for i in result:
        response += i

    return response


if __name__ == '__main__':
    clienRefracta()