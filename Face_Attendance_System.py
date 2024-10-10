
import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from tkinter import messagebox
import pyodbc
import playsound
from datetime import datetime
from tkinter import PhotoImage
from tkinter import Label


# Nhan gia tri id va name de cap nhat / them vao csdl
def insertOrUpdate(id, name):
    conn = pyodbc.connect('DRIVER={SQL Server};Server=DESKTOP-4J6P743;\
                          Database=CT270_ThongTin;Trusted_Connection=True;\
                          PORT=1433;UID:ct270user; PWD:159357;')
    cursor=conn.execute('SELECT * FROM NhanVien WHERE MaNV='+str(id))
    isRecordExist=0
    for row in cursor:
        isRecordExist = 1
        break
    if isRecordExist==1:
        cmd="UPDATE NhanVien SET HoTen=' "+str(name)+" ' WHERE MaNV="+str(id)
    else:
        cmd="INSERT INTO NhanVien(MaNV,HoTen,TrangThai) Values("+str(id)+",' "+str(name)+" ', 0 )"
    conn.execute(cmd)
    conn.commit()
    conn.close()

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

def checkInDB(id) :
    conn = pyodbc.connect('DRIVER={SQL Server};Server=DESKTOP-4J6P743;\
                          Database=CT270_ThongTin;Trusted_Connection=True;\
                          PORT=1433;UID:ct270user; PWD:159357;')
    cmd="UPDATE NhanVien SET TrangThai = 1 WHERE MaNV="+str(id)
    conn.execute(cmd)
    conn.commit()
    conn.close()

def checkOutDB(id) :
    conn = pyodbc.connect('DRIVER={SQL Server};Server=DESKTOP-4J6P743;\
                          Database=CT270_ThongTin;Trusted_Connection=True;\
                          PORT=1433;UID:ct270user; PWD:159357;')
    cmd="UPDATE NhanVien SET TrangThai = 0  WHERE MaNV="+str(id)
    conn.execute(cmd)
    conn.commit()
    conn.close()

# luu thoi gian check out
def markCheckOutCSV(name) :
    current_time_save = now.strftime("%Hh:%Mp:%Ss")
    file = open('CheckOut.csv','a') 
    writer = csv.writer(file)
    writer.writerow([name, str(current_time_save), str(current_date)])
    file.close()
        
#xu ly quen check out
def forgetCheckOut() :
    txt_id=(txt.get())
    name=(txt2.get())
    id = int(txt_id,10)
    checkOutDB(id)
    markCheckOutCSV(name)

#xu ly check out som
def earlyCheckOut(id, name) :
    checkOutDB(id)
    markCheckOutCSV(name)

def markCheckInCSV (name) :
    current_time_save = now.strftime("%Hh:%Mp:%Ss")
    with open('Attendance_Excel.csv','a') as file:
        writer = csv.writer(file)
        if (current_time > GioLamViec) :
            writer.writerow([name, str(current_time_save), str(current_date), "Di Tre"])
        else :
            writer.writerow([name, str(current_time_save), str(current_date), "Dung Gio"])               
    #playsound.playsound("./Mp3/ChamCongXong.mp3")

#Set UI
window = tk.Tk()
fira_mono = font.Font(family='Fira Mono', size=36, weight='bold')
window.title("Face Attendance")
 
window.geometry('1280x720')
window.configure(background='white')

#window.attributes('-fullscreen', True)

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

bg = PhotoImage(file = "bg.png") 
label1 = Label( window, image = bg) 
label1.place(x = 0, y = 0) 

message = tk.Label(window, text="Face Attendace System"  ,fg="teal"  ,width=45  ,height=3, font=(fira_mono, 30, 'bold')) 
message.place(x=100, y=20)

lbl = tk.Label(window, text="Enter ID",width=20  ,height=2  ,fg="darkred"  , font=(fira_mono, 15, ' bold ') ) 
lbl.place(x=100, y=200)

txt = tk.Entry(window,width=40  , fg="black",font=(fira_mono, 15, ' bold '))
txt.place(x=400, y=215)

lbl2 = tk.Label(window, text="Enter Name",width=20  ,fg="darkred"   ,height=2 ,font=(fira_mono, 15, ' bold ')) 
lbl2.place(x=100, y=300)

txt2 = tk.Entry(window,width=40  , fg="black",font=(fira_mono, 15, ' bold ')  )
txt2.place(x=400, y=315)
 
def clearID():
    txt.delete(0, 'end')    
    # res = ""
    # message.configure(text= res)

def clearName():
    txt2.delete(0, 'end')    
    # res = ""
    # message.configure(text= res)    
    
def new_User():       

    txt_id=(txt.get())
    name=(txt2.get())
    id = int(txt_id,10)
    insertOrUpdate(id,name)

    cam = cv2.VideoCapture(0)
    cam.set(3, 640) 
    cam.set(4, 480) 
    fontface = cv2.FONT_HERSHEY_SIMPLEX
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    count = 0
    while(True):

        ret, img = cam.read()
        img = cv2.flip(img, 1)
        centerH = img.shape[0] // 2;
        centerW = img.shape[1] // 2;
        sizeboxW = 300;
        sizeboxH = 400;
        cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                    (centerW  + sizeboxW // 2, centerH  + sizeboxH // 2), (255, 255, 255), 5)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        faces = face_detector.detectMultiScale(img_gray, 1.3, 5)
        for (x,y,w,h) in faces:           
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            cv2.imwrite("dataset/User." + str(id) + '.' + str(count) + ".jpg", img_gray[y:y+h,x:x+w])
            cv2.imshow('Camera', img)

        k = cv2.waitKey(100) & 0xff 
        if k == 27:
            break
        elif count >= 300: 
            break    
    cam.release()
    cv2.destroyAllWindows() 
    

# function to get the images and label data
def getImagesAndLabels(path):
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    # lay tat ca anh trong thu muc
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
    # tao list chua face va id    
    faceSamples=[]
    ids = []
    for imagePath in imagePaths:

        PIL_img = Image.open(imagePath).convert('L') # chuyen sang anh xam
        img_numpy = np.array(PIL_img,'uint8') # chuyen anh thanh mang numpy

        id = int(os.path.split(imagePath)[-1].split(".")[1]) # lay id tu anh
        faces = detector.detectMultiScale(img_numpy)    # trich xuat khuon mat tu anh numpy

        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w]) # tim khuon mat cat va gan vao list
            ids.append(id)

    return faceSamples,ids


path = 'dataset'
def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces,ids = getImagesAndLabels(path)

    recognizer.train(faces, np.array(ids))
    recognizer.write('trainer/trainer.yml') 

    messagebox.showinfo('Title', 'Train finish!')




fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (0,255,0)
fontcolor1 = (0,0,255)

#set time
now = datetime.now()
current_date = now.strftime("%d-%m-%Y")
current_time = now.strftime("%H-%M-%S")
today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
GioLamViec = today8am.strftime("%H-%M-%S")
today18pm = now.replace(hour=18, minute=0, second=0, microsecond=0)
GioTanLam = today18pm.strftime("%H-%M-%S")

def Attendance():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    # turn on camera
    cam = cv2.VideoCapture(0)
    cam.set(3, 900) # set video widht
    cam.set(4, 680) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)

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
                        markCheckInCSV(str(profile[1]))
                        checkInDB(profile[0])
                else :
                    if (current_time >= GioTanLam) :
                        checkOutDB(profile[0])
                        #playsound.playsound("./mp3/Goodbye.mp3")
                    else :
                        continue
                        #playsound.playsound("./mp3/ChamCongRoi.mp3")
            else:
                cv2.putText(img, "Name: Unknown", (x+5,y-5), fontface, fontscale, fontcolor1, 2)
                #playsound.playsound("./mp3/DangKy.mp3")
                    
        cv2.imshow('Camera',img) 
        k = cv2.waitKey(10) # Press 'ESC' for exiting video
        if (k == 27 ) :
            break
    cam.release()
    cv2.destroyAllWindows()

  
clearButton = tk.Button(window, text="Clear ID", command=clearID  ,fg="darkred"  ,bg="silver"  ,width=20  ,height=2 ,activebackground = "limegreen" ,font=(fira_mono, 15, ' bold '))
clearButton.place(x=900, y=200)
clearButton2 = tk.Button(window, text="Clear Name", command=clearName  ,fg="darkred"  ,bg="silver"  ,width=20  ,height=2, activebackground = "limegreen" ,font=(fira_mono, 15, ' bold '))
clearButton2.place(x=900, y=300)  

new_user = tk.Button(window, text="New User", command=new_User  ,fg="black"  ,bg="aquamarine"  ,width=20  ,height=3, activebackground = "limegreen" ,font=(fira_mono, 15, ' bold '))
new_user.place(x=200, y=450)
trainImg = tk.Button(window, text="Train Images", command=TrainImages  ,fg="black"  ,bg="aquamarine"  ,width=20  ,height=3, activebackground = "limegreen" ,font=(fira_mono, 15, ' bold '))
trainImg.place(x=500, y=450)
attendance = tk.Button(window, text="Attendance", command=Attendance  ,fg="black"  ,bg="aquamarine"  ,width=20  ,height=3, activebackground = "limegreen" ,font=(fira_mono, 15, ' bold '))
attendance.place(x=800, y=450)


earlyCheckout = tk.Button(window, text="Early CheckOut", command=earlyCheckOut  ,fg="black"  ,bg="aquamarine"  ,width=20  ,height=3, activebackground = "limegreen" ,font=(fira_mono, 15, ' bold '))
earlyCheckout.place(x=200, y=600)
forgetCheckout = tk.Button(window, text="Forget CheckOut", command=forgetCheckOut ,fg="black"  ,bg="aquamarine"  ,width=20  ,height=3, activebackground = "limegreen" ,font=(fira_mono, 15, ' bold '))
forgetCheckout.place(x=500, y=600)
quitWindow = tk.Button(window, text="Quit", command=window.destroy  ,fg="black"  ,bg="aquamarine"  ,width=20  ,height=3, activebackground = "limegreen" ,font=(fira_mono, 15, ' bold '))
quitWindow.place(x=800, y=600)

window.mainloop()