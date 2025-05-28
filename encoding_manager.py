import os
import face_recognition
import numpy as np
import cv2

ENCODING_DIR = "encodings"  # Yuz kodlari joylashadigan papka

# Agar papka mavjud bo'lmasa, yaratamiz
if not os.path.exists(ENCODING_DIR):
    os.makedirs(ENCODING_DIR)

def encode_and_save_face(user_name, image_path):
    """
    Berilgan rasm faylidan yuzni tanlab, kodlab, saqlaydi.
    user_name - foydalanuvchi ismi (fayl nomi uchun)
    image_path - foydalanuvchi rasmi yo'li (jpg/png)
    """
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) == 0:
        raise ValueError("Rasmda yuz topilmadi.")
    if len(face_locations) > 1:
        raise ValueError("Rasmda bir nechta yuz topildi, bittasini bering.")

    # Faqat bir yuz kodlanadi
    face_encoding = face_recognition.face_encodings(image, face_locations)[0]

    # Yuz kodini faylga saqlaymiz
    np.save(os.path.join(ENCODING_DIR, f"{user_name}.npy"), face_encoding)
    print(f"{user_name} uchun yuz kodi saqlandi.")

# Misol uchun yangi foydalanuvchini ro'yxatdan o'tkazish funksiyasi
def register_new_user(user_name, image_path):
    try:
        encode_and_save_face(user_name, image_path)
        return True, "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi."
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    # Test qilish uchun
    result, message = register_new_user("Ali", "test_faces/ali.jpg")
    print(message)
