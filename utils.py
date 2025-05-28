import pytz
from datetime import datetime
import pickle
import os

ENCODING_DIR = "encodings"

def get_current_time():
    tz = pytz.timezone("Asia/Tashkent")
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

def load_encodings():
    known_encodings = []
    known_users = []
    for file in os.listdir(ENCODING_DIR):
        if file.endswith(".pkl"):
            with open(os.path.join(ENCODING_DIR, file), "rb") as f:
                data = pickle.load(f)
                known_encodings.append(data['encoding'])
                known_users.append(data)
    return known_encodings, known_users
