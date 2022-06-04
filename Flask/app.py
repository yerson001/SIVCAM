from requests import request
from flask import Flask, Response, request,render_template
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
import numpy as np
import imutils
import os
import pyrebase
import cv2
import time
Datos = 'p'
if not os.path.exists(Datos):
    print('Carpeta creada: ',Datos)
    os.makedirs(Datos)


faceCascade = cv2.CascadeClassifier("face.xml")
fullbody = cv2.CascadeClassifier("haarcascade_fullbody.xml")

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


app = Flask(__name__)
camera=cv2.VideoCapture(0)

grabando = -1

def Video(duracion):
    global grabando
    grabando = 2
    print("-------fun grabando-----------")
    """
    global grabando
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

    start_time = time.time()
    while( int(time.time() - start_time) < duracion ):
        ret, frame = cap.read()
        if ret==True:
            frame = cv2.flip(frame,0)
            out.write(frame)
            #cv2.imshow('frame',frame)
        #else:
        #    break
    print("-------enviar mensage-----------")
    """
    
def generate_frames():
    send_sms = 0
    global grabando
    while True:
        success,frame=camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            #flags=cv2.CV_HAAR_SCALE_IMAGE
        )
        Cuerpo = fullbody.detectMultiScale(gray)
            # Draw a rectangle around the faces

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #send_sms = 1
            #grabando = 1
            #print("rostros------")
        
        for (x, y, w, h) in Cuerpo:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            #video(10)
            #send_sms += 1
        if grabando == 1:
            #Video(10)
            start_time = time.time()
            grabando=2
        if grabando==2:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter('resultado.mp4',fourcc, 20.0, (640,480))
            if( int(time.time() - start_time) < 5):#capture_duration
                ret, frame = camera.read()
                if ret==True:
                    #frame = cv2.flip(frame,0)
                    out.write(frame)
                    #cv2.imshow('frame',frame)
                else:
                    break
            else:
                grabando=-1
        #send_sms = send_sms + 1
        #if send_sms == 100:
        #    print("----------------se detecto una imagen-------------------------")
            

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
    #	🔔 💡
    if body == 'foto':
        #resp.message("--------sisisisiisis------")
        message = Message()
        #print(send_sms)
        success,frame=camera.read()
        cv2.imwrite(Datos+'/objeto_{}.jpg'.format(count),frame)
        my_image = Datos+'/objeto_{}.jpg'.format(count)
        #print('name:',str(my_image))
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
        #print(URL)

        message.body('Encenario 1')
        message.media(URL)
        resp.append(message)
       

    elif body == 'texto':
        resp.message("hola este es un texto para responder ")
    elif body == 'video':
        resp.message("https://be93-179-6-164-232.ngrok.io/video")
    else:
        resp.message("COMANDOS QUE PUEDES ENVIAR: foto[Captura una imagen con la cámara 📷 ] \n video[Transmision en vivo 🎥🔴]")

    #print(body)
    #render_template('index.html')
    return Response(str(resp),mimetype="application/xml")

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=="__main__":
    app.run(debug=True)
cv2.destroyAllWindows()