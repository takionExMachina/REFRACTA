import logging as logging

logging.basicConfig(level=logging.DEBUG)


import base64
import cv2
import numpy
from process_faces import align_images
from read_images import read_images
from mssql import queryPerson
from mssql import imageId
from spyne import  Application, rpc, ServiceBase, Unicode
from spyne import Iterable
from spyne.protocol.soap  import Soap11
from spyne.server.wsgi  import WsgiApplication


def RecognizeFaces():
    path_train = './imagenes/data/at/mg/'

    path_img = './imagenes/captured.pgm'

    images = read_images(path_train) # [X, y, c] [imagen, label, contador]

    #model = cv2.createLBPHFaceRecognizer(4, 2, 7, 7, 20.0)
    model = cv2.createLBPHFaceRecognizer(radius=4, neighbors=6,grid_x=5, grid_y=5, threshold=80)

    # se entrena el modelo con las imagenes del arreglo
    model.train(numpy.asarray(images[0]), numpy.asarray(images[2]))

    img = cv2.imread(path_img, 0)

    roi = img  #align_images(img)

    # se aplica el modelo al roi
    id, con = model.predict(roi)

    imagen = images[1][id]

    if con > 80:
        message =  None
    else:
        message =  imagen

    return message

class HelloWorldService(ServiceBase):
    @rpc(Unicode,_returns=Iterable(Unicode))
    def say_hello(ctx,name):

        fh = open("./imagenes/captured.pgm","wb")
        fh.write(base64.b64decode(name))
        fh.close()

        image = RecognizeFaces()

        if image is None:
            return None
        else:
            rut = str(imageId(image))

            if rut is None:
                return 'No hay registros asociados a la persona'
            else:
                return  queryPerson(str(rut))

application = Application([HelloWorldService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8001, wsgi_app)
    server.serve_forever()
