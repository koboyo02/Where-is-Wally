from tkinter import *
from tkinter import ttk
import time
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
import numpy as np
import cv2
import requests, uuid, json
from typing import Text

def visage(per_rechercher, i, y, video):
    montemps = time.time()
    entrer = 0
    sorti = 0
    espace = 0
    KEY = "81faab5a6f874007adc62c87e15e10e0"
    ENDPOINT = "https://grand-visage.cognitiveservices.azure.com/"
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    while(y < i):
        single_face_image_url = open(per_rechercher, "rb")
        detected_faces = face_client.face.detect_with_stream(
            image=single_face_image_url, detection_model='detection_03')
        if not detected_faces:
            print("Pas de visage sur l'image", single_face_image_url)

        first_image_face_ID = detected_faces[0].face_id

        multi_face_image_url = open('screen'+str(y)+'.jpg', "rb")
        multi_image_name = os.path.basename("/")
        detected_faces2 = face_client.face.detect_with_stream(
            image=multi_face_image_url, detection_model='detection_03')
        if not detected_faces2:
            print('Pas de visage sur vidéo',
                  multi_face_image_url, ' pour le moment')

        second_image_face_IDs = list(map(lambda x: x.face_id, detected_faces2))
        print('on est au screen'+str(y)+'.jpg')
        if not detected_faces or not detected_faces2:
            print()
        else:
            similar_faces = face_client.face.find_similar(
                face_id=first_image_face_ID, face_ids=second_image_face_IDs)
            if not similar_faces:
                espace = 1
                print()
            else:
                if entrer == 0:
                    entrer = time.strftime('%H:%M %d/%m/%Y', time.localtime())
                    print('il est entré à', entrer)
                    with open('heure_arriver'+per_rechercher+'.txt', 'w') as txtfile:
                        json.dump(entrer, txtfile)
                    espace = 0
                    print()
                elif sorti == 0 and espace == 1:
                    sorti = time.strftime('%H:%M %d/%m/%Y', time.localtime())
                    print('il est sortie à', sorti)
                    with open('heure_sorti'+per_rechercher+'.txt', 'w') as txtfile:
                        json.dump(sorti, txtfile)
                    print()
                    espace = 0
                elif sorti != 0 and entrer != 0:
                    sorti = 0
                    entrer = 0
                else:
                    print()
            for face in similar_faces:
                first_image_face_ID = face.face_id
                face_info = next(
                    x for x in detected_faces2 if x.face_id == first_image_face_ID)
        y += 25

cap = cv2.VideoCapture("Confinés et connectés - Code camp en full remote.mp4")
i = 0
y = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break
    if i % 25 == 0:
        cv2.imwrite('screen'+str(i)+'.jpg', frame)
    i += 1
cap.release()
cv2.destroyAllWindows()

print("test personne rechercher")
textper = input()

visage(textper, i, y, frame)

# window = Tk()
# window.geometry("700x300")

# label = Label(text="Personne rechercher")
# label.pack()

# entry1 = Entry(width=50)
# entry1.pack()

# quest = Label(text="Sur quel vidéo ?")
# quest.pack()

# entry2 = Entry(width=50)
# entry2.pack()

# btn = Button(window, height=1, width=10, text="C'est parti", bg="red", command=visage(entry1, i, y, frame))
# btn.pack()

# window.mainloop()