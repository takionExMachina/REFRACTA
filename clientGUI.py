
import cv2
import Tkinter as tk
import Image, ImageTk

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

labelText = tk.Label(labelFrame)
labelText.grid(row=0,column=0)

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

def show_frame():

    _, frame = cap.read()

    try:
        frame = cv2.resize(frame, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = classifier.detectMultiScale(gray, 1.2, 5)

        r = 0
        g = 255
        b = 0

        roi = None

        if faces is not None:
            for x, y, w, h in faces:
                roi = gray[x:x + w, y:y + h]

                cv2.imwrite('./data/captured.pgm', roi)

                message = sendFace()

                print message

                if message != 'No hay registros asociados a la persona':
                   r = 255
                   g = 0
                   b = 0
                else:
                   r = 0
                   g = 255
                   b = 0

                rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (b, g, r), 3)

                labelText.configure(text=message)

    except:
        pass

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    img = Image.fromarray(cv2image)

    imgtk = ImageTk.PhotoImage(image=img)

    lmain.imgtk = imgtk

    lmain.configure(image=imgtk)

    #metodo recursivo!!!!!!!!!!!!
    lmain.after(10, show_frame)

show_frame()
window.mainloop()