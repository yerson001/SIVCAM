import cv2
import matplotlib.pyplot as plt
import numpy as np
# read image
img = cv2.imread("anel.jpeg")

# load face cascade and eye cascade
face_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml') 


# search face
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)
copi_img = np.copy(img)
for (x,y,w,h) in faces:
    #print('x = ',x,'y = ',y,'w = ',w,'h = ',h,'\n')
    copi_img = cv2.circle(copi_img, (x,y), radius=7, color=(0,255,0), thickness=-1)
    copi_img = cv2.circle(copi_img, (x+w,y), radius=7, color=(0,255,0), thickness=-1)
    copi_img = cv2.circle(copi_img, (x,y+h), radius=7, color=(0,255,0), thickness=-1)
    copi_img = cv2.circle(copi_img, (x+w,y+
    h), radius=7, color=(0,255,0), thickness=-1)
    #copi_img = cv2.circle(copi_img, (x,y-h), radius=7, color=(0,255,0), thickness=-1)
    cv2.rectangle(copi_img,(x,y),(x+w,y+h),(255,0,0),5)

plt.figure(figsize=(20,10))
plt.imshow(copi_img)


cv2.destroyAllWindows()