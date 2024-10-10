import cv2
import numpy as np
import os 
from datetime import datetime
import csv
import pyodbc
import playsound


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

def getProfile(id):
    conn = pyodbc.connect('DRIVER={SQL Server};Server=DESKTOP-4J6P743;\
                          Database=CT270_ThongTin;Trusted_Connection=True;\
                          PORT=1433;UID:ct270user; PWD:159357;')
    cursor=conn.execute('SELECT * FROM NhanVien WHERE MaNV='+str(id))
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

def checkIn(id) :
    conn = pyodbc.connect('DRIVER={SQL Server};Server=DESKTOP-4J6P743;\
                          Database=CT270_ThongTin;Trusted_Connection=True;\
                          PORT=1433;UID:ct270user; PWD:159357;')
    cmd="UPDATE NhanVien SET TrangThai = 1 WHERE MaNV="+str(id)
    conn.execute(cmd)
    conn.commit()
    conn.close()

def checkOut(id) :
    conn = pyodbc.connect('DRIVER={SQL Server};Server=DESKTOP-4J6P743;\
                          Database=CT270_ThongTin;Trusted_Connection=True;\
                          PORT=1433;UID:ct270user; PWD:159357;')
    cmd="UPDATE NhanVien SET TrangThai = 0  WHERE MaNV="+str(id)
    conn.execute(cmd)
    conn.commit()
    conn.close()

def markCheckOut(name) :
    current_time_save = now.strftime("%Hh:%Mp:%Ss")
    with open('CheckOut.csv','a') as file:
        writer = csv.writer(file)
        writer.writerow([name, str(current_time_save), str(current_date)])
    file.close()
        
def forgetCheckOut(id, name) :
    checkOut(id)
    markCheckOut(name)

def earlyCheckOut(id, name) :
    checkOut(id)
    markCheckOut(name)

def markCheckIn (name) :
    current_time_save = now.strftime("%Hh:%Mp:%Ss")
    file = open('Attendance_Excel.csv','a')
    writer = csv.writer(file)
    if (current_time > GioLamViec) :
        writer.writerow([name, str(current_time_save), str(current_date), "Di Tre"])
    else :
        writer.writerow([name, str(current_time_save), str(current_date), "Dung Gio"])               
    #playsound.playsound("./Mp3/ChamCongXong.mp3")

fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (0,255,0)
fontcolor1 = (0,0,255)

cam = cv2.VideoCapture(0)
cam.set(3, 640) 
cam.set(4, 480) 

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

now = datetime.now()
current_date = now.strftime("%d-%m-%Y")
current_time = now.strftime("%H-%M-%S")

today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
GioLamViec = today8am.strftime("%H-%M-%S")

today18pm = now.replace(hour=18, minute=0, second=0, microsecond=0)
GioTanLam = today18pm.strftime("%H-%M-%S")

while (True):

    ret, img =cam.read()
    img = cv2.flip(img, 1) 

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:
       
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        
        profile=None
        if (confidence < 50):
            profile=getProfile(id)
            
        if(profile!=None):
            cv2.putText(img, "Name:" + str(profile[1]), (x+5,y-5), fontface, fontscale, fontcolor ,2)
            
            if(profile[2] == 0) :
                if (current_time >= GioTanLam) : 
                    continue
                    #playsound.playsound("./mp3/Goodbye.mp3")
                else :
                    markCheckIn(str(profile[1]))
                    checkIn(profile[0])
            else :
                if (current_time >= GioTanLam) :
                    checkOut(profile[0])
                    #playsound.playsound("./mp3/Goodbye.mp3")
                else :
                    continue
                    #playsound.playsound("./mp3/ChamCongRoi.mp3")
        else:
            cv2.putText(img, "Name: Unknown", (x+5,y-5), fontface, fontscale, fontcolor1, 2)
            #playsound.playsound("./mp3/DangKy.mp3")
                
    cv2.imshow('Camera',img) 
    k = cv2.waitKey(10) 
    if (k == 27 ) :
        break

cam.release()
cv2.destroyAllWindows()

