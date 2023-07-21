# Realtime-FaceRecognition-Attendance-System
This is a real-time attendance system using face recognition technology. The system can identify and mark the attendance of registered students as they appear in front of a camera. It offers a user-friendly interface and integrates with Firebase for data storage.
                  
## Features:               

- Real-time Face Recognition: The system uses the OpenCV library along with face_recognition to detect and recognize faces in real-time.
- Firebase Integration: Attendance data and student information are stored in the Firebase Realtime Database for easy access and retrieval.
- User-friendly Interface: The system provides a graphical interface that displays relevant student information and attendance status.
- Efficient Attendance Tracking: The system automatically updates the attendance count for each recognized student, based on their previous attendance record.    
          
## Requirements:

- Python
- OpenCV
- Firebase Admin SDK
- cvzone            
## Setup and Usage:               

- Install the required libraries and dependencies listed above.
- Make sure you have the "serviceAccountKey.json" file in the same directory, which is needed for Firebase initialization.
- Prepare a suitable "background.jpg" image to be displayed as the user interface backdrop.
- Create a "modes" folder containing images representing different modes (e.g., "Loading," "Attendance Success," etc.).
- Run the code and position the camera to capture the faces of students.                     
## How It Works:            

- The system continuously captures frames from the camera feed.
- It performs face recognition on each frame using pre-trained encodings of registered students.
- If a recognized face matches a student in the database, the system marks the student's attendance.
- The user interface displays relevant information about the recognized student, such as their name, major, standing, year, etc.
- The attendance count for the student is updated on Firebase if the recognition is successful and occurs after a certain interval (default is 30 seconds) since their last attendance.                  
## Important Note:                

- Ensure that all students to be recognized are pre-registered in the "Encode.p" file containing their face encodings.
- The system works best under good lighting conditions and clear camera capture of faces.
## Contributing:                       
Contributions to this project are welcome! If you encounter any issues or have suggestions for improvements, please feel free to submit a pull request.
