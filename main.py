import cv2
from face_recognition.api import face_distance
import numpy as np
import face_recognition
import os
from datetime import datetime
import requests
import pickle
from pymongo import MongoClient
import datetime

# today = "{}".format(datetime.date.today())
today = '2022-05-01'
client=MongoClient("mongodb://localhost:27017/")
collection = client['test']['test-db']
data = []
for i in collection.find():
    data.append(i)
    # print(i)
    
names = []
for n in data:
    names.append(n['Name'].upper())
print(names)

flag = 0
if today not in data[0]['date-key']:
    collection.update_many({},{"$push":{"date-key":today}})
else:
    flag = 1

cap = cv2.VideoCapture(0)
path = 'Images'
images = [] 
classNames = []
mylist = os.listdir(path)

cap.set(3,1280)
cap.set(4,720)
for cls in mylist:
    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])


print(classNames)
def findEncoding(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist


encodelistknown = findEncoding(images)

pickle_out = open("encodelist.pickle","wb")
pickle.dump(encodelistknown, pickle_out)
pickle_out.close()
print("Encoding Complete")

# open_file = open("encodelist.pickle", "rb")
# encodelistknown = pickle.load(open_file)
# open_file.close()

# ret, img = cap.read()
while True:
    print(flag)
    ret, img = cap.read()
    img1 = img
    imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(imgS)
    encodeCurrentFrame = face_recognition.face_encodings(imgS, facesCurrentFrame)

    for encodeFace, faceloc in zip(encodeCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodelistknown, encodeFace)
        facedist = face_recognition.face_distance(encodelistknown, encodeFace)
        # print(matches, facedist)
        matchIndex = np.argmin(facedist)

        if matches[matchIndex] and facedist[matchIndex]< 0.45:
            name = classNames[matchIndex].upper()
            print(name)
            y1, x2, y2, x1 = faceloc
            y1, x2, y2, x1 = 4*y1, 4*x2, 4*y2, 4*x1
            cv2.rectangle(img,(x1,y1), (x2,y2), (0,255,0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2,y2), (0,255,0), cv2.FILLED)
            cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2)
            print(facedist[matchIndex])
            if name in names:
                if flag == 0:
                    collection.update_one({"Name":name},{"$push":{"date-value":1}})
                    data.remove(name.upper())
                else:
                    pass
            else:
                pass


    cv2.imshow('WebCam', img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

if flag == 0 and len(names) != 0:
    for name in names:  
        collection.update_one({"Name":name},{"$push":{"date-value":0}})
