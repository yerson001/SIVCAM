from requests import request
from flask import Flask, Response, request,render_template
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
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
import cv2

app = Flask(__name__)
camera=cv2.VideoCapture(0)
def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route("/sms",methods=['GET','POST'])
def sms():
    global camera
    body = request.values.get('Body')
    resp = MessagingResponse()
    #resp.message(str(body))
    count=0
    if body == 'foto':
        #resp.message("--------sisisisiisis------")
        message = Message()

        success,frame=camera.read()
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
        print(URL)

        message.body('Hello friend')
        message.media(URL)
        resp.append(message)
       

    elif body == 'texto':
        resp.message("hola este es un texto para responder ")
    else:
        resp.message("No entendi")

    #print(body)
    #render_template('index.html')
    return Response(str(resp),mimetype="application/xml")

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=="__main__":
    app.run(debug=True)
cv2.destroyAllWindows()