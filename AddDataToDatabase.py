import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendance-system-realtime-default-rtdb.firebaseio.com/"
})

# Get a reference to the "Students" node in the database
ref = db.reference("Students")

data = {
    "20102018": {
        "Name": "Amir Aijaz",
        "major": "AI",
        "Starting_Year": "2020",
        "Total_attendance": "1",
        "Standing": "G",
        "Year": "4",
        "Last_attendance_time": "2023-05-20 00:54:34"
    },
    
    "20102075": {
        "Name": "Elon Musk",
        "major": "OpenAI",
        "Starting_Year": "2021",
        "Total_attendance": "6",
        "Standing": "A",
        "Year": "1",
        "Last_attendance_time": "2023-05-20 00:54:34"
    },

    "20102172": {
        "Name": "Mark Zuckerberg",
        "major": "Facebook",
        "Starting_Year": "2022",
        "Total_attendance": "7",
        "Standing": "B",
        "Year": "3",
        "Last_attendance_time": "2023-05-20 00:54:34"
    }
}

for key, value in data.items():
    ref.child(key).set(value)
