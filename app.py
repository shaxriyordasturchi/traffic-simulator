import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import numpy as np
import face_recognition
import os
import pickle
from datetime import datetime
from telegram_utils import send_telegram_message, send_telegram_photo

# ———— Sozlamalar ————
ENCODINGS_DIR = "encodings"
DB_PATH = "worktime.db"  # Bu keyinchalik kerak bo'ladi, hozir faqat saqlamaymiz

# Vaqt olish funksiyasi
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Yuzni tanish uchun oldindan saqlangan kodlar va ma'lumotlarni yuklaymiz
def load_known_faces():
    known_encodings = []
    known_users = []
    if not os.path.exists(ENCODINGS_DIR):
        os.makedirs(ENCODINGS_DIR)
    for file in os.listdir(ENCODINGS_DIR):
        if file.endswith(".pkl"):
            with open(os.path.join(ENCODINGS_DIR, file), "rb") as f:
                data = pickle.load(f)
                known_encodings.append(data['encoding'])
                known_users.append(data)
    return known_encodings, known_users

# Webcamedan har bir frame uchun yuzni aniqlash va qayta ishlash
def process_frame(frame, known_encodings, known_users):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        if len(face_distances) == 0:
            continue
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            user = known_users[best_match_index]
            name = f"{user['firstname']} {user['lastname']}"
            color = (0, 255, 0)  # yashil - topildi
            label = f"{name} - Tanildi"
            # Telegramga xabar va foto yuborish (bu yerda faqat xabar)
            send_telegram_message(f"✅ {name} ishga kirdi\n🕒 {get_current_time()}")

        else:
            name = "Noma'lum"
            color = (0, 0, 255)  # qizil - topilmadi
            label = "Noma'lum yuz aniqlangan!"
            # Telegramga noma'lum yuz haqida xabar
            send_telegram_message(f"⚠️ Noma'lum yuz aniqlangan!\n🕒 {get_current_time()}")
            # Rasmni vaqt nomi bilan saqlaymiz
            photo_path = f"unknown_faces/unknown_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            if not os.path.exists("unknown_faces"):
                os.makedirs("unknown_faces")
            cv2.imwrite(photo_path, frame)
            send_telegram_photo(photo_path, caption="⚠️ Noma'lum yuz!")

        # Yuz atrofida to'rtburchak chizamiz
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        # Label qo'yamiz
        cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    return frame

# ———— Streamlit interfeysi ————

st.set_page_config(page_title="Yuz bilan kirish", layout="centered")
st.title("🧑‍💼 Xodim yuzni tanib kirish tizimi")

option = st.selectbox("Amalni tanlang:", ["Ishga kirish", "Ishdan chiqish"])

if st.button("Kamerani ishga tushurish va yuzni tanish"):
    known_encodings, known_users = load_known_faces()
    if len(known_encodings) == 0:
        st.warning("Yuz kodlari topilmadi! 'encodings' papkasiga yuz kodlarini yuklang.")
    else:
        st.info("Kamera ishga tushdi. Yuzingizni ko'rsating...")
        
        def video_frame_callback(frame):
            img = frame.to_ndarray(format="bgr24")
            img = process_frame(img, known_encodings, known_users)
            return img

        webrtc_streamer(key="face-recognition", video_frame_callback=video_frame_callback)
