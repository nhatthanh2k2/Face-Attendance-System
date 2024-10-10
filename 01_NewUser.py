import cv2
import os
import pyodbc
import playsound

cam = cv2.VideoCapture(0)
cam.set(3, 640) 
cam.set(4, 480) 
fontface = cv2.FONT_HERSHEY_SIMPLEX

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

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

id=input('Nhập mã nhân viên:')
name=input('Nhập tên nhân viên:')
print("Bắt đầu chụp ảnh nhân viên, nhấn ESC để thoát!")
insertOrUpdate(id,name)

count = 0

while(True):
    ret, img = cam.read()
    img = cv2.flip(img, 1) 
    centerH = img.shape[0] // 2
    centerW = img.shape[1] // 2
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

print("\nLấy ảnh đã hoàn thành!")
cam.release()
cv2.destroyAllWindows()


