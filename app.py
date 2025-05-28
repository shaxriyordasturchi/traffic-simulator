import streamlit as st
import cv2
import numpy as np
import face_recognition
from utils import get_current_time, load_encodings
from db import init_db, mark_login, mark_logout, get_chat_id
from telegram_bot import send_telegram_message, ADMIN_CHAT_ID

init_db()
st.set_page_config("Yuz bilan kirish/chiqish", layout="centered")
st.title("🧑‍💼 Xodim Yuz Tanish Paneli")

option = st.selectbox("Amalni tanlang:", ["Ishga Kirish", "Ishdan Chiqish"])

if st.button("📷 Yuzni Skanirovka Qilish"):
    st.info("⏳ Kamera ishga tushdi. Yuzingizni ko‘rsating...")

    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    known_encodings, known_users = load_encodings()
    result = "Hech kim tanilmadi"
    recognized = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)
        face_encodings = face_recognition.face_encodings(rgb, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            if len(face_distances) == 0:
                continue
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                user = known_users[best_match_index]
                now = get_current_time()
                if option == "Ishga Kirish":
                    mark_login(user, now)
                    msg = f"✅ <b>{user['firstname']} {user['lastname']}</b> ishga KIRDI\n🕒 {now}"
                else:
                    mark_logout(user, now)
                    msg = f"❌ <b>{user['firstname']} {user['lastname']}</b> ishdan CHIQDI\n🕒 {now}"
                chat_id = get_chat_id(user['username'], ADMIN_CHAT_ID)
                send_telegram_message(chat_id, msg)
                result = f"{user['firstname']} {user['lastname']} aniqlandi"
                recognized = True
                break
            else:
                continue

        stframe.image(frame, channels="BGR")
        if recognized or cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    if not recognized:
        msg = f"🚨 Tanilmagan yuz aniqlandi. Kamera vaqti: {get_current_time()}"
        send_telegram_message(ADMIN_CHAT_ID, msg)
    st.success(result)
