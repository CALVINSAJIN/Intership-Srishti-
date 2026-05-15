"""Face Detection Attendance System — polished & stable build."""
from __future__ import annotations

import json
import re
import time
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image


# ---------------------------------------------------------------------------
# Paths & constants
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATASET_DIR = BASE_DIR / "dataset"
MODEL_DIR = BASE_DIR / "models"
STUDENTS_FILE = DATA_DIR / "students.csv"
ATTENDANCE_FILE = DATA_DIR / "attendance.csv"
ATTENDANCE_XLSX = DATA_DIR / "attendance.xlsx"
MODEL_FILE = MODEL_DIR / "lbph_model.yml"
LABELS_FILE = MODEL_DIR / "labels.json"

STUDENT_COLUMNS = ["student_id", "student_name", "registered_on", "image_count"]
ATTENDANCE_COLUMNS = ["student_id", "student_name", "date", "login_time", "session_id"]
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".pgm"}
FACE_SIZE = (200, 200)


# ---------------------------------------------------------------------------
# Theme & visual helpers
# ---------------------------------------------------------------------------

def apply_theme() -> None:
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=DM+Serif+Display&display=swap" rel="stylesheet">

        <style>
        /* ── Root palette ──────────────────────────────────────────── */
        :root {
            --bg:           #0d1117;
            --bg-surface:   #161b22;
            --bg-card:      #1c2230;
            --bg-hover:     #212a3a;
            --border:       rgba(255,255,255,0.07);
            --border-light: rgba(255,255,255,0.12);

            --accent:       #3b82f6;
            --accent-glow:  rgba(59,130,246,0.25);
            --accent-dim:   rgba(59,130,246,0.12);
            --green:        #22c55e;
            --green-dim:    rgba(34,197,94,0.12);
            --amber:        #f59e0b;
            --amber-dim:    rgba(245,158,11,0.12);
            --red:          #ef4444;

            --text-primary: #e6edf3;
            --text-secondary:#8b949e;
            --text-muted:   #484f58;

            --font-sans:    'DM Sans', sans-serif;
            --font-mono:    'DM Mono', monospace;
            --font-display: 'DM Serif Display', serif;

            --radius:       10px;
            --radius-lg:    16px;
        }

        /* ── Global reset ──────────────────────────────────────────── */
        * { box-sizing: border-box; }

        html, body, .stApp {
            font-family: var(--font-sans) !important;
            background: var(--bg) !important;
            color: var(--text-primary) !important;
        }

        /* Subtle grid texture */
        .stApp::before {
            content: '';
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(59,130,246,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(59,130,246,0.03) 1px, transparent 1px);
            background-size: 40px 40px;
            pointer-events: none;
            z-index: 0;
        }

        .block-container {
            max-width: 1200px !important;
            padding-top: 1.5rem !important;
            padding-bottom: 4rem !important;
            position: relative;
            z-index: 1;
        }

        /* ── Sidebar ───────────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background: var(--bg-surface) !important;
            border-right: 1px solid var(--border) !important;
        }

        [data-testid="stSidebar"] * {
            color: var(--text-primary) !important;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            border-radius: var(--radius);
            padding: 0.45rem 0.6rem !important;
            margin-bottom: 0.3rem !important;
            transition: background 0.15s ease;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: var(--bg-hover) !important;
        }

        /* ── Typography ────────────────────────────────────────────── */
        h1, h2, h3, h4 {
            font-family: var(--font-sans) !important;
            color: var(--text-primary) !important;
            letter-spacing: -0.02em;
        }

        p { color: var(--text-secondary); line-height: 1.65; }

        /* ── Metrics ───────────────────────────────────────────────── */
        [data-testid="stMetric"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            padding: 1.25rem 1.4rem !important;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        [data-testid="stMetric"]:hover {
            border-color: var(--border-light) !important;
            box-shadow: 0 0 0 1px var(--border-light) !important;
        }

        [data-testid="stMetricLabel"] > div {
            color: var(--text-secondary) !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
        }

        [data-testid="stMetricValue"] > div {
            color: var(--text-primary) !important;
            font-size: 1.7rem !important;
            font-weight: 700 !important;
        }

        [data-testid="stMetricDelta"] { display: none; }

        /* ── Forms & inputs ─────────────────────────────────────────── */
        [data-testid="stTextInput"] input,
        [data-testid="stDateInput"] input,
        [data-testid="stSelectbox"] > div > div {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-light) !important;
            border-radius: var(--radius) !important;
            color: var(--text-primary) !important;
            font-family: var(--font-sans) !important;
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stDateInput"] input:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px var(--accent-glow) !important;
        }

        [data-testid="stFileUploader"] section {
            background: var(--bg-card) !important;
            border: 1px dashed var(--border-light) !important;
            border-radius: var(--radius-lg) !important;
        }

        /* ── Buttons ────────────────────────────────────────────────── */
        .stButton > button,
        .stDownloadButton > button {
            font-family: var(--font-sans) !important;
            font-weight: 600 !important;
            border-radius: var(--radius) !important;
            min-height: 2.75rem !important;
            transition: all 0.18s ease !important;
            border: 1px solid var(--border-light) !important;
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background: var(--bg-hover) !important;
            border-color: rgba(255,255,255,0.2) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.3) !important;
        }

        .stButton > button[kind="primary"] {
            background: var(--accent) !important;
            border-color: var(--accent) !important;
            color: #ffffff !important;
            box-shadow: 0 0 20px var(--accent-glow) !important;
        }

        .stButton > button[kind="primary"]:hover {
            background: #2563eb !important;
            border-color: #2563eb !important;
            box-shadow: 0 0 32px rgba(59,130,246,0.4) !important;
        }

        /* ── Slider ─────────────────────────────────────────────────── */
        [data-testid="stSlider"] [class*="thumb"] {
            background: var(--accent) !important;
            box-shadow: 0 0 12px var(--accent-glow) !important;
        }

        [data-testid="stSlider"] [class*="track"] {
            background: var(--accent) !important;
        }

        /* ── DataFrames ─────────────────────────────────────────────── */
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            overflow: hidden !important;
        }

        /* ── Alerts ─────────────────────────────────────────────────── */
        [data-testid="stAlert"] {
            border-radius: var(--radius) !important;
            border: 1px solid var(--border) !important;
        }

        /* ── Container (bordered) ───────────────────────────────────── */
        [data-testid="stVerticalBlockBorderWrapper"] > div {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-lg) !important;
            padding: 1.5rem !important;
        }

        /* ── Progress bar ───────────────────────────────────────────── */
        [data-testid="stProgress"] > div > div > div > div {
            background: var(--accent) !important;
        }

        /* ── Scrollbar ──────────────────────────────────────────────── */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg); }
        ::-webkit-scrollbar-thumb { background: var(--border-light); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #484f58; }

        hr { border-color: var(--border) !important; }

        /* ── Custom components ──────────────────────────────────────── */

        /* Hero banner */
        .hero {
            position: relative;
            overflow: hidden;
            background: linear-gradient(135deg, #0d1117 0%, #0f1f3d 50%, #1a2f5e 100%);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            padding: 2.5rem 2.8rem;
            margin-bottom: 2rem;
        }

        .hero::before {
            content: '';
            position: absolute;
            top: -80px; right: -80px;
            width: 320px; height: 320px;
            background: radial-gradient(circle, rgba(59,130,246,0.18) 0%, transparent 70%);
            border-radius: 50%;
        }

        .hero::after {
            content: '';
            position: absolute;
            bottom: -60px; left: 30%;
            width: 200px; height: 200px;
            background: radial-gradient(circle, rgba(99,102,241,0.1) 0%, transparent 70%);
            border-radius: 50%;
        }

        .hero-tag {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: var(--accent-dim);
            border: 1px solid rgba(59,130,246,0.3);
            border-radius: 999px;
            color: #93c5fd;
            font-size: 0.73rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            padding: 0.3rem 0.75rem;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }

        .hero h1 {
            font-family: var(--font-display) !important;
            font-size: clamp(2rem, 5vw, 3.2rem) !important;
            font-weight: 400 !important;
            color: #ffffff !important;
            line-height: 1.1;
            margin: 0 0 0.9rem;
            letter-spacing: -0.01em !important;
        }

        .hero p {
            color: #93a5bf;
            font-size: 1.02rem;
            line-height: 1.6;
            max-width: 620px;
            margin: 0;
        }

        .hero-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 1.4rem;
        }

        .hero-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 999px;
            color: #cbd5e1;
            font-size: 0.78rem;
            font-weight: 500;
            padding: 0.3rem 0.7rem;
        }

        /* Sidebar brand */
        .sb-brand { padding: 1.25rem 0.1rem 1rem; }

        .sb-tag {
            color: #3b82f6;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .sb-title {
            color: #e6edf3;
            font-size: 1.3rem;
            font-weight: 700;
            margin-top: 0.35rem;
            letter-spacing: -0.02em;
        }

        .sb-copy {
            color: #8b949e;
            font-size: 0.84rem;
            line-height: 1.5;
            margin-top: 0.45rem;
        }

        .sb-model-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: var(--green-dim);
            border: 1px solid rgba(34,197,94,0.25);
            border-radius: 999px;
            color: #86efac;
            font-size: 0.76rem;
            font-weight: 600;
            padding: 0.3rem 0.7rem;
            margin-top: 0.85rem;
        }

        .sb-model-pill.no-model {
            background: var(--amber-dim);
            border-color: rgba(245,158,11,0.25);
            color: #fcd34d;
        }

        /* Section heading */
        .sec-head { margin: 2rem 0 1.2rem; }

        .sec-eyebrow {
            color: var(--accent);
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 0.3rem;
        }

        .sec-head h2 {
            margin: 0 !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }

        .sec-head p {
            color: var(--text-secondary);
            margin: 0.4rem 0 0;
            font-size: 0.93rem;
        }

        /* Step badge for registration */
        .step-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.6rem; height: 1.6rem;
            background: var(--accent-dim);
            border: 1px solid rgba(59,130,246,0.3);
            border-radius: 50%;
            color: #93c5fd;
            font-size: 0.72rem;
            font-weight: 700;
            margin-right: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    model_pill_class = "sb-model-pill" if MODEL_FILE.exists() else "sb-model-pill no-model"
    st.markdown(
        f"""
        <section class="hero">
            <div class="hero-tag">&#128247; Computer Vision Attendance</div>
            <h1>Face Attendance System</h1>
            <p>Register student faces, run live webcam recognition, and export clean attendance logs — all in one focused dashboard.</p>
            <div class="hero-pills">
                <span class="hero-pill">&#9679; OpenCV LBPH</span>
                <span class="hero-pill">&#9679; Real-time detection</span>
                <span class="hero-pill">&#9679; CSV &amp; Excel export</span>
                <span class="hero-pill">&#9679; Session tracking</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_section_heading(eyebrow: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="sec-head">
            <div class="sec-eyebrow">{eyebrow}</div>
            <h2>{title}</h2>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Project file setup
# ---------------------------------------------------------------------------

def ensure_project_files() -> None:
    for folder in (DATA_DIR, DATASET_DIR, MODEL_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    if not STUDENTS_FILE.exists():
        pd.DataFrame(columns=STUDENT_COLUMNS).to_csv(STUDENTS_FILE, index=False)
    if not ATTENDANCE_FILE.exists():
        pd.DataFrame(columns=ATTENDANCE_COLUMNS).to_csv(ATTENDANCE_FILE, index=False)


# ---------------------------------------------------------------------------
# CSV / data helpers
# ---------------------------------------------------------------------------

def read_csv(path: Path, columns: list[str]) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=columns)
    try:
        frame = pd.read_csv(path, dtype=str).fillna("")
    except (pd.errors.EmptyDataError, pd.errors.ParserError, OSError):
        return pd.DataFrame(columns=columns)

    for column in columns:
        if column not in frame.columns:
            frame[column] = ""
    return frame[columns]


def read_students() -> pd.DataFrame:
    return read_csv(STUDENTS_FILE, STUDENT_COLUMNS)


def read_attendance() -> pd.DataFrame:
    return read_csv(ATTENDANCE_FILE, ATTENDANCE_COLUMNS)


def write_attendance(frame: pd.DataFrame) -> None:
    """Write attendance CSV (and optionally Excel if openpyxl is available)."""
    frame.to_csv(ATTENDANCE_FILE, index=False)
    try:
        import importlib
        if importlib.util.find_spec("openpyxl") is not None:
            frame.to_excel(ATTENDANCE_XLSX, index=False)
    except Exception:
        pass  # Excel export is optional; CSV is the source of truth


# ---------------------------------------------------------------------------
# Student ID / path helpers
# ---------------------------------------------------------------------------

def normalize_student_id(raw_student_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]", "", raw_student_id.strip())
    return cleaned.upper()


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value.strip())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "student"


def student_folder(student_id: str, student_name: str) -> Path:
    return DATASET_DIR / f"{student_id}_{slugify(student_name)}"


def iter_image_files(folder: Path) -> Iterable[Path]:
    for path in sorted(folder.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            yield path


# ---------------------------------------------------------------------------
# OpenCV helpers
# ---------------------------------------------------------------------------

@st.cache_resource
def face_cascade() -> cv2.CascadeClassifier:
    cascade_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(str(cascade_path))
    if cascade.empty():
        raise RuntimeError("Unable to load OpenCV Haar cascade for face detection.")
    return cascade


def lbph_is_available() -> bool:
    return hasattr(cv2, "face") and hasattr(cv2.face, "LBPHFaceRecognizer_create")


def create_recognizer() -> cv2.face_LBPHFaceRecognizer:
    if not lbph_is_available():
        raise RuntimeError(
            "LBPH recognizer is unavailable. Install opencv-contrib-python from requirements.txt."
        )
    return cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)


def detect_faces(gray_image: np.ndarray) -> np.ndarray:
    return face_cascade().detectMultiScale(
        gray_image,
        scaleFactor=1.15,
        minNeighbors=5,
        minSize=(70, 70),
    )


def largest_face(faces: np.ndarray) -> tuple[int, int, int, int] | None:
    if len(faces) == 0:
        return None
    return max(faces, key=lambda rect: rect[2] * rect[3])


def prepare_face(face_image: np.ndarray) -> np.ndarray:
    resized = cv2.resize(face_image, FACE_SIZE)
    return cv2.equalizeHist(resized)


def crop_largest_face(gray_image: np.ndarray) -> np.ndarray | None:
    face = largest_face(detect_faces(gray_image))
    if face is None:
        return None
    x, y, width, height = face
    return gray_image[y : y + height, x : x + width]


# ---------------------------------------------------------------------------
# Camera
# ---------------------------------------------------------------------------

def open_camera() -> cv2.VideoCapture:
    """Try multiple backends so the app works on Linux, Windows, and macOS."""
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_V4L2, cv2.CAP_ANY]
    for backend in backends:
        try:
            cam = cv2.VideoCapture(0, backend)
            if cam.isOpened():
                return cam
            cam.release()
        except Exception:
            continue
    # Last resort — default
    return cv2.VideoCapture(0)


# ---------------------------------------------------------------------------
# Student / image management
# ---------------------------------------------------------------------------

def count_registered_images(student_id: str) -> int:
    total = 0
    for folder in DATASET_DIR.glob(f"{student_id}_*"):
        if folder.is_dir():
            total += sum(1 for _ in iter_image_files(folder))
    return total


def upsert_student(student_id: str, student_name: str) -> None:
    students = read_students()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    image_count = str(count_registered_images(student_id))

    if student_id in students["student_id"].values:
        students.loc[students["student_id"] == student_id, "student_name"] = student_name
        students.loc[students["student_id"] == student_id, "image_count"] = image_count
    else:
        students = pd.concat(
            [
                students,
                pd.DataFrame(
                    [
                        {
                            "student_id": student_id,
                            "student_name": student_name,
                            "registered_on": now,
                            "image_count": image_count,
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )

    students.to_csv(STUDENTS_FILE, index=False)


def save_face_image(folder: Path, student_id: str, face_image: np.ndarray, index: int) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_path = folder / f"{student_id}_{timestamp}_{index:03d}.png"
    cv2.imwrite(str(output_path), prepare_face(face_image))
    return output_path


def save_uploaded_faces(
    student_id: str,
    student_name: str,
    uploaded_files: list,
) -> tuple[int, int]:
    folder = student_folder(student_id, student_name)
    saved = 0
    skipped = 0

    for index, uploaded_file in enumerate(uploaded_files, start=1):
        try:
            image = Image.open(uploaded_file).convert("RGB")
        except Exception:
            skipped += 1
            continue

        rgb_image = np.array(image)
        gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
        face_image = crop_largest_face(gray_image)
        if face_image is None:
            skipped += 1
            continue
        save_face_image(folder, student_id, face_image, index)
        saved += 1

    if saved:
        upsert_student(student_id, student_name)
    return saved, skipped


# ---------------------------------------------------------------------------
# Webcam capture for registration
# ---------------------------------------------------------------------------

def capture_faces_from_webcam(student_id: str, student_name: str, sample_count: int) -> int:
    folder = student_folder(student_id, student_name)
    camera = open_camera()
    if not camera.isOpened():
        st.error(
            "Unable to access the webcam. "
            "Check that no other app is using the camera and that permissions are granted."
        )
        return 0

    preview = st.empty()
    progress = st.progress(0)
    status = st.empty()
    saved = 0
    last_saved_at = 0.0
    started_at = time.time()
    timeout_seconds = max(30, sample_count * 2)

    try:
        while saved < sample_count and time.time() - started_at < timeout_seconds:
            ok, frame = camera.read()
            if not ok:
                status.warning("Camera frame could not be read — retrying…")
                time.sleep(0.05)
                continue

            gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detect_faces(gray_image)
            face = largest_face(faces)

            if face is not None:
                x, y, width, height = face
                cv2.rectangle(frame, (x, y), (x + width, y + height), (59, 130, 246), 2)
                cv2.putText(
                    frame,
                    f"Captured {saved}/{sample_count}",
                    (x, max(20, y - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (59, 130, 246),
                    2,
                )
                if time.time() - last_saved_at >= 0.35:
                    save_face_image(
                        folder, student_id,
                        gray_image[y : y + height, x : x + width],
                        saved + 1,
                    )
                    saved += 1
                    last_saved_at = time.time()

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            preview.image(rgb_frame, channels="RGB", use_container_width=True)
            progress.progress(min(saved / sample_count, 1.0))
            status.info(f"Keep your face centred and well-lit — {saved}/{sample_count} samples captured.")
            time.sleep(0.03)
    finally:
        camera.release()

    if saved:
        upsert_student(student_id, student_name)
    status.success(f"✔ Captured {saved} face sample(s).")
    return saved


# ---------------------------------------------------------------------------
# Model training
# ---------------------------------------------------------------------------

def train_model() -> tuple[int, int]:
    recognizer = create_recognizer()
    students = read_students()
    student_names = {
        row["student_id"]: row["student_name"]
        for _, row in students.iterrows()
        if row["student_id"]
    }

    faces: list[np.ndarray] = []
    labels: list[int] = []
    label_lookup: dict[int, dict[str, str]] = {}
    student_to_label: dict[str, int] = {}

    for folder in sorted(DATASET_DIR.iterdir()):
        if not folder.is_dir():
            continue
        parts = folder.name.split("_", 1)
        student_id = parts[0] if parts else ""
        if not student_id:
            continue

        student_name = student_names.get(
            student_id,
            parts[1].replace("_", " ") if len(parts) > 1 else student_id,
        )
        if student_id not in student_to_label:
            label = len(student_to_label)
            student_to_label[student_id] = label
            label_lookup[label] = {"student_id": student_id, "student_name": student_name}
        label = student_to_label[student_id]

        for image_path in iter_image_files(folder):
            try:
                gray_image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
                if gray_image is None:
                    continue
                face_image = crop_largest_face(gray_image)
                if face_image is None:
                    face_image = gray_image
                faces.append(prepare_face(face_image))
                labels.append(label)
            except Exception:
                continue  # skip corrupt images

    if not faces:
        raise RuntimeError(
            "No registered face images found. Register at least one student first."
        )

    MODEL_DIR.mkdir(exist_ok=True)
    recognizer.train(faces, np.array(labels, dtype=np.int32))
    recognizer.write(str(MODEL_FILE))
    LABELS_FILE.write_text(json.dumps(label_lookup, indent=2), encoding="utf-8")
    return len(faces), len(label_lookup)


def load_model() -> tuple[cv2.face_LBPHFaceRecognizer, dict[str, dict[str, str]]]:
    if not MODEL_FILE.exists() or not LABELS_FILE.exists():
        raise RuntimeError(
            "Recognition model is missing. Train the model after registering faces."
        )
    recognizer = create_recognizer()
    recognizer.read(str(MODEL_FILE))
    try:
        labels = json.loads(LABELS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeError(f"Could not read model labels: {exc}") from exc
    return recognizer, labels


def model_summary() -> str:
    if not MODEL_FILE.exists() or not LABELS_FILE.exists():
        return "No trained model"
    try:
        labels = json.loads(LABELS_FILE.read_text(encoding="utf-8"))
        return f"{len(labels)} student(s) trained"
    except (json.JSONDecodeError, OSError):
        return "Model needs refresh"


# ---------------------------------------------------------------------------
# Attendance helpers
# ---------------------------------------------------------------------------

def already_marked(student_id: str, current_date: str) -> bool:
    attendance = read_attendance()
    if attendance.empty:
        return False
    return bool(
        (
            (attendance["student_id"] == student_id)
            & (attendance["date"] == current_date)
        ).any()
    )


def mark_attendance(student_id: str, student_name: str, session_id: str) -> dict[str, str] | None:
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    if already_marked(student_id, current_date):
        return None

    record = {
        "student_id": student_id,
        "student_name": student_name,
        "date": current_date,
        "login_time": now.strftime("%H:%M:%S"),
        "session_id": session_id,
    }
    attendance = read_attendance()
    attendance = pd.concat([attendance, pd.DataFrame([record])], ignore_index=True)
    write_attendance(attendance)
    return record


def reset_attendance_session() -> None:
    st.session_state.attendance_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.marked_students_session = set()


def session_state_defaults() -> None:
    if "attendance_session_id" not in st.session_state:
        reset_attendance_session()
    if "marked_students_session" not in st.session_state:
        st.session_state.marked_students_session = set()


def validate_student_inputs(raw_student_id: str, raw_student_name: str) -> tuple[str, str] | None:
    student_id = normalize_student_id(raw_student_id)
    student_name = raw_student_name.strip()
    if not student_id:
        st.error("Enter a valid Student ID (letters, digits, hyphens and underscores only).")
        return None
    if not student_name:
        st.error("Enter the student name.")
        return None
    return student_id, student_name


# ---------------------------------------------------------------------------
# Face recognition
# ---------------------------------------------------------------------------

def recognize_frame(
    frame: np.ndarray,
    recognizer: cv2.face_LBPHFaceRecognizer,
    labels: dict[str, dict[str, str]],
    confidence_threshold: int,
) -> list[dict[str, str | float]]:
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detect_faces(gray_image)
    results: list[dict[str, str | float]] = []

    for x, y, width, height in faces:
        face_image = prepare_face(gray_image[y : y + height, x : x + width])
        label, confidence = recognizer.predict(face_image)
        label_info = labels.get(str(label))

        if label_info and confidence <= confidence_threshold:
            student_id = label_info["student_id"]
            student_name = label_info["student_name"]
            display_text = f"{student_name} ({confidence:.1f})"
            color = (34, 197, 94)   # green
            status = "recognized"
        else:
            student_id = ""
            student_name = "Unknown"
            display_text = f"Unknown ({confidence:.1f})"
            color = (239, 68, 68)   # red
            status = "unknown"

        cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)
        cv2.putText(
            frame,
            display_text,
            (x, max(22, y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            color,
            2,
        )
        results.append(
            {
                "student_id": student_id,
                "student_name": student_name,
                "confidence": float(confidence),
                "status": status,
            }
        )

    return results


# ---------------------------------------------------------------------------
# Live attendance scan
# ---------------------------------------------------------------------------

def run_attendance_scan(confidence_threshold: int, scan_seconds: int) -> None:
    try:
        recognizer, labels = load_model()
    except Exception as exc:
        st.error(str(exc))
        return

    camera = open_camera()
    if not camera.isOpened():
        st.error(
            "Unable to access the webcam. "
            "Check that no other app is using it and that permissions are granted."
        )
        return

    preview = st.empty()
    status = st.empty()
    marked_table = st.empty()
    newly_marked: list[dict[str, str]] = []
    end_time = time.time() + scan_seconds
    marked_session: set[str] = st.session_state.marked_students_session

    try:
        while time.time() < end_time:
            ok, frame = camera.read()
            if not ok:
                status.warning("Camera frame could not be read — retrying…")
                time.sleep(0.05)
                continue

            results = recognize_frame(frame, recognizer, labels, confidence_threshold)
            for result in results:
                student_id = str(result["student_id"])
                student_name = str(result["student_name"])
                if result["status"] != "recognized" or not student_id:
                    continue
                if student_id in marked_session:
                    continue
                record = mark_attendance(
                    student_id=student_id,
                    student_name=student_name,
                    session_id=st.session_state.attendance_session_id,
                )
                marked_session.add(student_id)
                if record:
                    newly_marked.append(record)

            seconds_left = max(0, int(end_time - time.time()))
            status.info(f"⏱ Scanning… {seconds_left}s remaining.")
            preview.image(
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                channels="RGB",
                use_container_width=True,
            )
            if newly_marked:
                marked_table.dataframe(
                    pd.DataFrame(newly_marked), hide_index=True, use_container_width=True
                )
            time.sleep(0.03)
    finally:
        camera.release()
        st.session_state.marked_students_session = marked_session

    if newly_marked:
        st.success(f"✔ Marked {len(newly_marked)} new attendance record(s).")
    else:
        st.info("No new attendance records were marked in this scan.")


# ---------------------------------------------------------------------------
# Page renderers
# ---------------------------------------------------------------------------

COLUMN_CONFIG = {
    "student_id": "Student ID",
    "student_name": "Student name",
    "registered_on": "Registered on",
    "image_count": "Face samples",
    "date": "Date",
    "login_time": "Login time",
    "session_id": "Session ID",
}


def render_registration() -> None:
    render_section_heading(
        "Enrollment",
        "Face Registration",
        "Add student details, collect face samples, then train the recognition model.",
    )

    students = read_students()
    total_images = (
        0 if students.empty
        else sum(count_registered_images(r["student_id"]) for _, r in students.iterrows())
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Registered students", len(students))
    m2.metric("Face samples on disk", total_images)
    m3.metric("Model status", model_summary())

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        col_a, col_b = st.columns(2)
        with col_a:
            raw_student_id = st.text_input(
                "Student ID", placeholder="e.g. STU001",
                help="Only letters, digits, hyphens and underscores are allowed.",
            )
        with col_b:
            raw_student_name = st.text_input("Full name", placeholder="e.g. Jane Smith")

        samples = st.slider(
            "Webcam samples to capture", min_value=5, max_value=50, value=20, step=5,
            help="More samples generally improve recognition accuracy.",
        )
        uploaded_files = st.file_uploader(
            "Upload face images (optional alternative to webcam)",
            type=["jpg", "jpeg", "png", "bmp"],
            accept_multiple_files=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        btn1, btn2, btn3 = st.columns(3)

        with btn1:
            if st.button("📷  Capture from Webcam", type="primary", use_container_width=True):
                validated = validate_student_inputs(raw_student_id, raw_student_name)
                if validated:
                    capture_faces_from_webcam(*validated, sample_count=samples)

        with btn2:
            if st.button("🖼  Save Uploaded Faces", use_container_width=True):
                validated = validate_student_inputs(raw_student_id, raw_student_name)
                if validated:
                    if not uploaded_files:
                        st.warning("Upload at least one image first.")
                    else:
                        saved, skipped = save_uploaded_faces(*validated, uploaded_files=uploaded_files)
                        st.success(f"✔ Saved {saved} face image(s). Skipped {skipped}.")

        with btn3:
            if st.button("🧠  Train / Refresh Model", use_container_width=True):
                with st.spinner("Training recognition model…"):
                    try:
                        image_count, student_count = train_model()
                        st.success(
                            f"✔ Model trained — {image_count} image(s) for {student_count} student(s)."
                        )
                    except Exception as exc:
                        st.error(str(exc))

    render_section_heading(
        "Roster",
        "Registered Students",
        "Current student records and the number of usable face samples on disk.",
    )
    students = read_students()
    if students.empty:
        st.info("No students registered yet. Use the form above to get started.")
    else:
        students = students.copy()
        students["image_count"] = (
            students["student_id"].apply(count_registered_images).astype(str)
        )
        students.to_csv(STUDENTS_FILE, index=False)
        st.dataframe(
            students,
            use_container_width=True,
            hide_index=True,
            column_config=COLUMN_CONFIG,
        )


def render_live_attendance() -> None:
    render_section_heading(
        "Live scan",
        "Live Attendance",
        "Start the webcam scanner, tune recognition confidence, and track marks for the active session.",
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Model status", model_summary())
    m2.metric("Session ID", st.session_state.attendance_session_id)
    m3.metric("Marked this session", len(st.session_state.marked_students_session))

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        ctrl1, ctrl2 = st.columns(2)
        with ctrl1:
            confidence_threshold = st.slider(
                "Recognition confidence threshold",
                min_value=35, max_value=120, value=75,
                help="LBPH confidence is lower for better matches. Raise this value if known faces appear as Unknown.",
            )
        with ctrl2:
            scan_seconds = st.slider(
                "Scan duration (seconds)", min_value=10, max_value=120, value=30, step=5,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        act1, act2, act3 = st.columns(3)

        with act1:
            if st.button("▶  Start Webcam Scan", type="primary", use_container_width=True):
                run_attendance_scan(confidence_threshold, scan_seconds)

        with act2:
            if st.button("🔄  New Session", use_container_width=True):
                reset_attendance_session()
                st.success("✔ New attendance session started.")

        with act3:
            if st.button("🧠  Train Model", use_container_width=True):
                with st.spinner("Training…"):
                    try:
                        image_count, student_count = train_model()
                        st.success(
                            f"✔ Model trained — {image_count} image(s) for {student_count} student(s)."
                        )
                    except Exception as exc:
                        st.error(str(exc))

    render_section_heading(
        "Today",
        "Today's Attendance",
        "Real-time view of attendance records for the current date.",
    )
    today = datetime.now().strftime("%Y-%m-%d")
    attendance = read_attendance()
    today_records = attendance[attendance["date"] == today] if not attendance.empty else attendance

    if today_records.empty:
        st.info("No attendance records for today yet. Start a scan above.")
    else:
        st.dataframe(
            today_records.sort_values("login_time"),
            hide_index=True,
            use_container_width=True,
            column_config=COLUMN_CONFIG,
        )


def filter_attendance(
    frame: pd.DataFrame,
    selected_dates: tuple[date, date] | tuple,
    student: str,
) -> pd.DataFrame:
    if frame.empty:
        return frame

    filtered = frame.copy()
    filtered["_date"] = pd.to_datetime(filtered["date"], errors="coerce").dt.date

    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered = filtered[
            (filtered["_date"] >= start_date) & (filtered["_date"] <= end_date)
        ]

    if student != "All":
        filtered = filtered[filtered["student_name"] == student]

    return filtered.drop(columns=["_date"])


def render_reports() -> None:
    render_section_heading(
        "Reporting",
        "Attendance Report",
        "Filter by date range and student, then export CSV or Excel.",
    )
    attendance = read_attendance()

    if attendance.empty:
        st.info("Attendance records will appear here after the first live scan.")
        return

    attendance_dates = pd.to_datetime(attendance["date"], errors="coerce").dt.date.dropna()
    min_date = attendance_dates.min()
    max_date = attendance_dates.max()
    student_names = ["All"] + sorted(n for n in attendance["student_name"].unique() if n)

    with st.container(border=True):
        f1, f2 = st.columns(2)
        with f1:
            selected_dates = st.date_input("Date range", value=(min_date, max_date))
            if isinstance(selected_dates, date):
                selected_dates = (selected_dates, selected_dates)
        with f2:
            selected_student = st.selectbox("Student", student_names)

    filtered = filter_attendance(attendance, selected_dates, selected_student)

    st.markdown("<br>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Records", len(filtered))
    m2.metric("Unique students", filtered["student_id"].nunique() if not filtered.empty else 0)
    m3.metric("Unique dates", filtered["date"].nunique() if not filtered.empty else 0)

    st.dataframe(
        filtered,
        hide_index=True,
        use_container_width=True,
        column_config=COLUMN_CONFIG,
    )

    csv_bytes = filtered.to_csv(index=False).encode("utf-8")
    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button(
            "⬇  Download CSV",
            data=csv_bytes,
            file_name="attendance_report.csv",
            mime="text/csv",
            use_container_width=True,
        )

    if ATTENDANCE_XLSX.exists():
        with dl2:
            st.download_button(
                "⬇  Download Excel",
                data=ATTENDANCE_XLSX.read_bytes(),
                file_name="attendance.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

def render_sidebar() -> str:
    trained = MODEL_FILE.exists()
    pill_class = "sb-model-pill" if trained else "sb-model-pill no-model"
    pill_icon = "●" if trained else "○"

    st.sidebar.markdown(
        f"""
        <div class="sb-brand">
            <div class="sb-tag">Attendance Suite</div>
            <div class="sb-title">Face Attendance</div>
            <div class="sb-copy">Registration, live recognition, and reporting for classroom attendance.</div>
            <div class="{pill_class}">{pill_icon}&nbsp; {model_summary()}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section = st.sidebar.radio(
        "Navigate",
        ["Face Registration", "Live Attendance", "Attendance Report"],
        label_visibility="collapsed",
    )
    st.sidebar.divider()
    st.sidebar.caption("Powered by Streamlit · OpenCV LBPH")
    return section


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(
        page_title="Face Attendance System",
        page_icon="📷",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_theme()
    ensure_project_files()
    session_state_defaults()

    render_hero()

    if not lbph_is_available():
        st.error(
            "OpenCV LBPH recognizer is not available. "
            "Install the correct package with: pip install opencv-contrib-python"
        )
        st.stop()

    section = render_sidebar()
    if section == "Face Registration":
        render_registration()
    elif section == "Live Attendance":
        render_live_attendance()
    else:
        render_reports()


if __name__ == "__main__":
    main()
