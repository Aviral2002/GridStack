import numpy as np
import cv2

def preprocess_image(image_bytes):
    np_img = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

def extract_details(text):
    details = {
        "mrp": None,
        "pack_size": None,
        "mfg_date": None,
        "exp_date": None,
        "brand_name": None,
        "lot_no": None
    }
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if "mrp" in line.lower():
            details["mrp"] = line.split(":")[1].strip() if ":" in line else None
        elif "exp date" in line.lower():
            details["exp_date"] = line.split(":")[1].strip() if ":" in line else None
    return details
