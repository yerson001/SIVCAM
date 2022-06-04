import cv2
import numpy as np
import imutils
import os
import pyrebase

Datos = 'p'
if not os.path.exists(Datos):
    print('Carpeta creada: ',Datos)
    os.makedirs(Datos)





config = {
  'apiKey': "AIzaSyD9nFNbz0PhUxQJUm4uNh8lgXec14Y65zo",
  'authDomain': "rpiimage-b6062.firebaseapp.com",
  'databaseURL': "https://rpiimage-b6062-default-rtdb.firebaseio.com",
  'projectId': "rpiimage-b6062",
  'storageBucket': "rpiimage-b6062.appspot.com",
  'messagingSenderId': "902149485764",
  'appId': "1:902149485764:web:bac0d04cf2ac2844164591",
  'measurementId': "G-FTQM2CJE4N"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

cap = cv2.VideoCapture(0)
x1, y1 = 190, 80
x2, y2 = 450, 398
count = 0
URL=''
while True:
    ret, frame = cap.read()
    if ret == False: break
    imAux = frame.copy()
    cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
    #objeto = imAux[y1:y2,x1:x2]
    #objeto = imutils.resize(objeto,width=38)
    #print(objeto.shape)
    k = cv2.waitKey(1)
    if k == ord('s'):
        cv2.imwrite(Datos+'/objeto_{}.jpg'.format(count),frame)
        my_image = Datos+'/objeto_{}.jpg'.format(count)
        print('name:',str(my_image))
        #Upload Image
        storage.child(my_image).put(my_image)
        count = count +1

        #Get URL image
        auth = firebase.auth()
        email = "yhon.sanchez@ucsp.edu.pe"
        password = "123456"
        user = auth.sign_in_with_email_and_password(email, password)
        url = storage.child(my_image).get_url(user['idToken'])
        URL = url
        #print(url)
    if k == 27:
        break
    cv2.imshow('frame',frame)
    #cv2.imshow('objeto',objeto)
cap.release()
cv2.destroyAllWindows()