from requests import request
from flask import Flask, Response, request,render_template
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.messaging_response import Body, Media, Message, MessagingResponse
import numpy as np
import imutils
import os
from twilio.rest import Client
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



account_sid = 'AC44ccb9137fb482535fbeeca61aba1f19'
auth_token = ''
client = Client(account_sid, auth_token)



firebase = pyrebase.initialize_app(config)
storage = firebase.storage()


app = Flask(__name__)
camera=cv2.VideoCapture(0)



flag = 1

def detector(frame,frame1):
    diff = cv2.absdiff(frame,frame1)
    gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    _,thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh,None,iterations=3)
    #cv2.imshow("dd",dilated)
    contours,_ = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame,contours,-1,(0,0,255),2)
    
    for cnt in contours:
        if cv2.contourArea(cnt) < 20000:
            continue
        x, y ,w , h = cv2.boundingRect(cnt)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
        
        return 1
    return 0

    
def generate_frames():
    send_sms = 0
    global grabando
    global flag
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
            
 
        _,frame2 = camera.read()
        _,frame1 = camera.read()
        i = detector(frame2,frame1)
        if i == 1 and flag:
            #print("se detecto movimiento")
            flag = 0
            message = client.messages.create(
                                from_='whatsapp:+14155238886',
                                #media_url = url,
                                body='⚠️​ ⛔​ Se detecto algo sospechoso​ 😱 🚨​',
                                to='whatsapp:+51963828458'
                            )

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
        resp.message('https://firebasestorage.googleapis.com/v0/b/rpiimage-b6062.appspot.com/o/app.jpeg?alt=media&token=8ac2de03-2c71-4519-b31f-d380807e24e6')

    #print(body)
    #render_template('index.html')
    return Response(str(resp),mimetype="application/xml")

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=="__main__":
    app.run(debug=True)
cv2.destroyAllWindows()

#KfFrU7kfzT48xG6kv-iDDE381hUUUKJSj-Pzh4CO
