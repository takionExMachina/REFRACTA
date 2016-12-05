
import cv2
import Tkinter as tk
import Image, ImageTk

info = 'INFORMACION PERSONA: '
rut = 'Rut: '
nombres = 'Nombres: '
apellidos = 'Apellidos: '
descripcion = 'Descripcion: '
fecha_registro = 'Fecha Registro: '
fecha_caducidad = 'Fecha Caducidad: '
recinto = 'Recinto: '
direccion = 'Direccion: '
comuna = 'Comuna: '
provincia = 'Provincia: '
region = 'Region: '

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("REFRACTA Client")
window.config(background="#000000")

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Label frame
labelFrame = tk.Frame(window, width=400, height=200)
labelFrame.grid(row=0,column=1)

lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)

labelTitle = tk.Label(labelFrame)
labelTitle.grid(row=0, column=0)
labelTitle.configure(text=info)

labelRut = tk.Label(labelFrame)
labelRut.grid(row=1, column=0)
labelRut.configure(text=rut)

labelNombres = tk.Label(labelFrame)
labelNombres.grid(row=3, column=0)
labelNombres.configure(text=nombres)

labelApellidos = tk.Label(labelFrame)
labelApellidos.grid(row=4, column=0)
labelApellidos.configure(text=apellidos)

labelDescripcion = tk.Label(labelFrame)
labelDescripcion.grid(row=5, column=0)
labelDescripcion.configure(text=descripcion)

labelFechaRegistro = tk.Label(labelFrame)
labelFechaRegistro.grid(row=6, column=0)
labelFechaRegistro.configure(text=fecha_registro)

labelFechaCaducidad = tk.Label(labelFrame)
labelFechaCaducidad.grid(row=7, column=0)
labelFechaCaducidad.configure(text=fecha_caducidad)

labelRecinto = tk.Label(labelFrame)
labelRecinto.grid(row=8, column=0)
labelRecinto.configure(text=recinto)

labelDireccion = tk.Label(labelFrame)
labelDireccion.grid(row=9, column=0)
labelDireccion.configure(text=direccion)

labelComuna = tk.Label(labelFrame)
labelComuna.grid(row=10, column=0)
labelComuna.configure(text=comuna)

labelProvincia = tk.Label(labelFrame)
labelProvincia.grid(row=11, column=0)
labelProvincia.configure(text=provincia)

labelRegion = tk.Label(labelFrame)
labelRegion.grid(row=12, column=0)
labelRegion.configure(text=region)

#Capture video frames
cap = cv2.VideoCapture(0)

haar = './models/haarcascade_frontalface_default.xml'

classifier = cv2.CascadeClassifier(haar)

def sendFace():
    from zeep import Client
    import base64

    face_recog = Client('http://localhost:8001/?wsdl')

    with open('./data/captured.pgm', 'rb') as image:
        string = base64.b64encode(image.read())

    result = face_recog.service.say_hello(string)

    response = ''

    for i in result:
        response += i

    return response

def messageProcess(message):
    returned = []
    message = message.split(' ')

    rut = message[1]
    nombres = message[3] + ' ' + message[4]
    apellidos = message[6] + ' ' + message[7]

    descripcion = ''

    for i in range(message.index('descripcion:') + 1 ,message.index('fecha:')):
        descripcion +=  message[i] + " "


    fecha_registro = message[message.index('fecha:') + 1]
    fecha_caducidad = message[message.index('caduca:') + 1]
    recinto = message[message.index('recinto:') + 1]

    direccion = ''

    for d in range(message.index('direccion:') + 1, message.index('comuna:')):
        direccion += message[d] + " "

    comuna = message[message.index('comuna:') + 1]
    provincia = message[message.index('provincia:') + 1]

    region = ''

    for r in range(message.index('region:') + 1 ,len(message)):
        region += message[r] + " "


    returned.append(rut)
    returned.append(nombres)
    returned.append(apellidos)
    returned.append(descripcion)
    returned.append(fecha_registro)
    returned.append(fecha_caducidad)
    returned.append(recinto)
    returned.append(direccion)
    returned.append(comuna)
    returned.append(provincia)
    returned.append(region)

    return returned


def show_frame():

    _, frame = cap.read()

    try:
        frame = cv2.resize(frame, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = classifier.detectMultiScale(gray, 1.2, 5)

        if faces is not None:
            for x, y, w, h in faces:
                roi = gray[ y:y + h, x:x + w ]

                cv2.imwrite('./data/captured.pgm', roi)

                message = sendFace()

                r = 0
                g = 255
                b = 0

                if message is not  None:
                   r = 255
                   g = 0
                   b = 0

                   returned = messageProcess(message)

                   labelRut.configure(text=rut + returned[0])
                   labelNombres.configure(text=nombres + returned[1])
                   labelApellidos.configure(text=apellidos + returned[2])
                   labelDescripcion.configure(text=descripcion + returned[3])
                   labelFechaRegistro.configure(text=fecha_registro + returned[4])
                   labelFechaCaducidad.configure(text=fecha_caducidad + returned[5])
                   labelRecinto.configure(text=recinto + returned[6])
                   labelDireccion.configure(text=direccion + returned[7])
                   labelComuna.configure(text=comuna + returned[8])
                   labelProvincia.configure(text=provincia + returned[9])
                   labelRegion.configure(text=region + returned[10])

                else:
                    r = 0
                    g = 255
                    b = 0

                    labelRut.configure(text=rut)
                    labelNombres.configure(text=nombres)
                    labelApellidos.configure(text=apellidos)
                    labelDescripcion.configure(text=descripcion)
                    labelFechaRegistro.configure(text=fecha_registro)
                    labelFechaCaducidad.configure(text=fecha_caducidad)
                    labelRecinto.configure(text=recinto)
                    labelDireccion.configure(text=direccion)
                    labelComuna.configure(text=comuna)
                    labelProvincia.configure(text=provincia)
                    labelRegion.configure(text=region)

                rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (b, g, r), 3)

    except:
        pass

    frame = cv2.flip(frame, flipCode=1)

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    img = Image.fromarray(cv2image)

    imgtk = ImageTk.PhotoImage(image=img)

    lmain.imgtk = imgtk

    lmain.configure(image=imgtk)

    #metodo recursivo!!!!!!!!!!!!
    lmain.after(10, show_frame)

show_frame()
window.mainloop()
