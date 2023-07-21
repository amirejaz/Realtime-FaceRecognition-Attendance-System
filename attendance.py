import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-system-realtime-default-rtdb.firebaseio.com/",
    'storageBucket': "attendance-system-realtime.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 7000)
cap.set(4, 8000)

imgBackground = cv2.imread("background.jpg")

folderModePath = "modes"
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    imgMode = cv2.imread(os.path.join(folderModePath, path))
    imgMode = cv2.resize(imgMode, (1400, 1650))  # Resize imgMode to match desired shape
    imgModeList.append(imgMode)

#load the encoding file
print("Loading encode file.....")
file = open("Encode.p", "rb")
encodeListKnownWithIDs = pickle.load(file)
file.close()
encodeListKnown, studentIDs = encodeListKnownWithIDs
# print(studentIDs)
print("Loaded encode file")

modeType = 0
counter = 0
Id = -1
modeType = 0
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0,0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame =face_recognition.face_encodings(imgS, faceCurFrame)

    bgImg = imgBackground.copy()
    bgImg[600:600+img.shape[0], 200:200+img.shape[1]] = img
    bgImg[44:44+imgModeList[0].shape[0], 1650:1650+imgModeList[0].shape[1]] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print("Matches", matches)
            print("Face Distance", faceDis)

            matchIndex = np.argmin(faceDis)    

            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 200 + x1, 600 + y1, x2 - x1, y2 - y1
                # cv2.rectangle(imgBackground, bbox, (0, 255, 0), thickness=2)
                bgImg = cvzone.cornerRect(bgImg, bbox, rt=0)
                Id = studentIDs[matchIndex]

                if counter == 0:
                    cvzone.putTextRect(bgImg, "Loading....", (700, 1000))
                    resizeImg = cv2.resize(bgImg, (840, 600))
                    cv2.imshow("Face Attendance", resizeImg)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1
                    
            if counter != 0:
                if counter == 1:
                    #Get the data
                    studentInfo = db.reference(f"Students/{Id}").get()
                    print(studentInfo)
                    #get images
                    blob = bucket.blob(f"images/{Id}.jpg")
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                    imgStudent = cv2.resize(imgStudent, (570, 310))
                    # update attendance
                    datetimeObject = datetime.strptime(studentInfo["Last_attendance_time"], "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondsElapsed)
                    if secondsElapsed > 30:
                        ref = db.reference(f"Students/{Id}")
                        total_attendance = int(studentInfo["Total_attendance"])  # Convert to integer
                        total_attendance += 1
                        ref.child("Total_attendance").set(str(total_attendance))
                        ref.child("Last_attendance_time").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    else: 
                        modeType = 3
                        counter =0
                        bgImg[44:44+imgModeList[0].shape[0], 1650:1650+imgModeList[0].shape[1]] = imgModeList[modeType]
                
                if modeType != 3:

                    if 10<counter<20:
                        modeType = 2                
                    bgImg[44:44+imgModeList[0].shape[0], 1650:1650+imgModeList[0].shape[1]] = imgModeList[modeType]

                    if counter <= 10:    
                        cv2.putText(bgImg, str(studentInfo["Total_attendance"]), (1945, 240), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
                        cv2.putText(bgImg, str(Id), (2200, 1020), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
                        cv2.putText(bgImg, str(studentInfo["major"]), (2325, 1210), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
                        cv2.putText(bgImg, str(studentInfo["Standing"]), (1925, 1520), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
                        cv2.putText(bgImg, str(studentInfo["Year"]), (2335, 1520), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)
                        cv2.putText(bgImg, str(studentInfo["Starting_Year"]), (2687, 1520), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 2)

                        (w, h), _ = cv2.getTextSize(studentInfo["Name"], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (imgModeList[1].shape[1] - w) // 2 
                        cv2.putText(bgImg, str(studentInfo["Name"]), (1550+offset, 800), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0), 3)
                        
                        bgImg[360:360+310, 2060:2060+570] = imgStudent

                    counter += 1

                    if counter >= 20:
                        counter = 0
                        modeType = 0
                        studentInfo = []
                        imgStudent = []
                        bgImg[44:44+imgModeList[0].shape[0], 1650:1650+imgModeList[0].shape[1]] = imgModeList[modeType] 
    else: 
        modeType = 0
        counter = 0                

    resizeImg = cv2.resize(bgImg, (840, 600))
    cv2.imshow("Face Attendance", resizeImg)
    if cv2.waitKey(1) & 0xFF == 113:
        break

cap.release()
cv2.destroyAllWindows()
