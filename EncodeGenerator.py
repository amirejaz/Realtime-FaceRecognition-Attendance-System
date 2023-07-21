import cv2
import face_recognition
import os
import pickle
import firebase_admin
from firebase_admin import credentials, db, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-system-realtime-default-rtdb.firebaseio.com/",
    'storageBucket': "attendance-system-realtime.appspot.com"
})

folderPath = "images"
pathList = os.listdir(folderPath)
imgList = []
stdList = []

for path in pathList:
    imgstd = cv2.imread(os.path.join(folderPath, path))
    imgstd = cv2.resize(imgstd, (1400, 1650))  # Resize imgMode to match desired shape
    imgList.append(imgstd)
    stdList.append(os.path.splitext(path)[0])
    
    filename = f"{folderPath}/{path}"
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)
 
    # print(path)
    # print(os.path.splitext(path)[0])
print(imgList)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

print("Encoding Started......")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIDs = [encodeListKnown, stdList]
print("Encoding Complete")

file = open("Encode.p", "wb")
pickle.dump(encodeListKnownWithIDs, file)
file.close()
print("File Saved")
