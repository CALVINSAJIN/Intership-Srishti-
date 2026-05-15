# Face Detection Attendance System using Streamlit

A Streamlit application that registers student faces, recognizes faces from a live webcam feed, marks attendance automatically, and stores attendance records in CSV and Excel format.

## Features

- Face registration with webcam capture or uploaded images.
- OpenCV Haar cascade face detection.
- OpenCV LBPH face recognition model.
- Live attendance marking from webcam video.
- Duplicate prevention for the current session and the same attendance date.
- Student name, login time, and date shown in the app.
- Attendance reports with date/student filters.
- CSV and Excel export support.

## Project Structure

```text
.
|-- app.py
|-- requirements.txt
|-- .streamlit/
|   `-- config.toml
|-- data/
|   |-- attendance.csv
|   `-- students.csv
|-- dataset/
|   `-- README.md
|-- models/
|   `-- .gitkeep
`-- screenshots/
    `-- README.md
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## How to Use

1. Go to **Face Registration**.
2. Enter student ID and student name.
3. Capture face samples from the webcam or upload clear face images.
4. Click **Train / Refresh Recognition Model**.
5. Go to **Live Attendance** and click **Start Webcam Attendance**.
6. View saved records in **Attendance Report**.

## Notes for Best Recognition

- Register at least 15-25 samples per student.
- Capture faces with different small head angles and lighting conditions.
- Keep one face clearly visible during registration.
- The app uses a local webcam through OpenCV, so it is best run on your laptop or lab computer instead of a hosted Streamlit server.
- `opencv-contrib-python` is required because LBPH lives in `cv2.face`.

## GitHub Submission Checklist

1. Register real or consented students.
2. Train the model from the app.
3. Capture screenshots and place them in `screenshots/`.
4. Keep private student images out of public repositories unless consent is available.
5. Commit and push:

```powershell
git init
git add .
git commit -m "Build Streamlit face attendance system"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```
