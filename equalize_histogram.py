
import cv2

def EqualizeHistogram(img):
    eq = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return eq.apply(img)