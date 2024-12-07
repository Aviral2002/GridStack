from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import pytesseract
import cv2
import numpy as np
import re
from datetime import datetime
import logging
import traceback

bp = Blueprint("expiry_date_detection", __name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_bytes):
    try:
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return thresh
    except Exception as e:
        logging.error(f"Error in preprocess_image: {str(e)}")
        raise

def extract_expiry_date(text):
    date_patterns = [
        r'\d{2}/\d{2}/\d{4}',  # DD/MM/YYYY
        r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
        r'\d{2}\.\d{2}\.\d{4}',  # DD.MM.YYYY
        r'\d{2}/\d{2}/\d{2}',  # DD/MM/YY
        r'\d{2}-\d{2}-\d{2}',  # DD-MM-YY
        r'\d{2}\.\d{2}\.\d{2}',  # DD.MM.YY
        r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[\s\.]?\d{1,2}[\s\.,]?\d{4}',  # Month DD, YYYY
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group()
    return None

@bp.route("/ocr-scan", methods=['POST'])
@cross_origin(supports_credentials=True)
def detect_expiry_date():
    logging.info("Received OCR scan request")
    
    if 'image' not in request.files:
        logging.error("No image file in request")
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    
    try:
        image_bytes = image_file.read()
        logging.debug(f"Image size: {len(image_bytes)} bytes")
        
        preprocessed_img = preprocess_image(image_bytes)
        logging.debug(f"Preprocessed image shape: {preprocessed_img.shape}")
        
        text = pytesseract.image_to_string(preprocessed_img)
        logging.debug(f"Extracted text: {text}")
        
        expiry_date = extract_expiry_date(text)
        logging.debug(f"Extracted expiry date: {expiry_date}")
        
        if expiry_date:
            try:
                parsed_date = datetime.strptime(expiry_date, "%d/%m/%Y")
                standardized_date = parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                standardized_date = expiry_date  # Keep original format if parsing fails
            
            return jsonify({
                "success": True,
                "expiry_date": standardized_date,
                "raw_text": text
            })
        else:
            return jsonify({
                "success": False,
                "message": "No expiry date found",
                "raw_text": text
            })
    
    except Exception as e:
        logging.error(f"Error in OCR processing: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

