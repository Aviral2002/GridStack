import os
import logging
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import pytesseract
import cv2
import numpy as np
import re
from datetime import datetime
import traceback
import time
from database import add_packaged_product

bp = Blueprint("expiry_date_detection", __name__)

logging.basicConfig(level=logging.DEBUG)

custom_config = r'--oem 1 --psm 6 -c tessedit_char_whitelist="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz/.-: "'

def preprocess_image(image_bytes):
    try:
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (400, 300))
        _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    except Exception as e:
        logging.error(f"Error in preprocess_image: {str(e)}")
        raise

def extract_dates(text):
    date_pattern = r'(\d{2}[/.-]\d{2}[/.-]\d{4})'
    dates = re.findall(date_pattern, text)
    
    mfg_date = exp_date = None
    for line in text.split('\n'):
        if 'MFG' in line.upper() and not mfg_date:
            mfg_date = next((d for d in dates if d in line), None)
        elif 'EXP' in line.upper() and not exp_date:
            exp_date = next((d for d in dates if d in line), None)
    
    return {'mfg_date': mfg_date, 'exp_date': exp_date}

def parse_date(date_string):
    if not date_string:
        return None
    try:
        return datetime.strptime(date_string, "%d/%m/%Y").date()
    except ValueError:
        return None

@bp.route("/ocr-scan", methods=['POST'])
@cross_origin(supports_credentials=True)
def detect_expiry_date():
    logging.info("Received OCR scan request")
    
    if 'image' not in request.files:
        logging.error("No image file provided")
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    brand = request.form.get('brand', 'Unknown')
    count = int(request.form.get('count', 1))
    
    try:
        image_bytes = image_file.read()
        preprocessed_img = preprocess_image(image_bytes)
        
        try:
            start_time = time.time()
            text = pytesseract.image_to_string(preprocessed_img, config=custom_config, timeout=15)
            end_time = time.time()
            logging.debug(f"OCR took {end_time - start_time:.2f} seconds")
        except RuntimeError as timeout_error:
            logging.error(f"OCR Timeout: {str(timeout_error)}")
            return jsonify({"error": "OCR process timed out"}), 500
        
        logging.debug(f"Extracted text: {text}")
        
        dates = extract_dates(text)
        logging.debug(f"Extracted dates: {dates}")
        
        if 'exp_date' in dates:
            expiry_date = parse_date(dates['exp_date'])
            if expiry_date:
                standardized_date = expiry_date.strftime("%Y-%m-%d")
                add_packaged_product(brand, standardized_date, count)
                return jsonify({
                    "success": True,
                    "expiry_date": standardized_date,
                    "manufacture_date": parse_date(dates.get('mfg_date', '')).strftime("%Y-%m-%d") if dates.get('mfg_date') else None,
                    "raw_text": text
                })
        
        return jsonify({
            "success": False,
            "message": "No valid expiry date found",
            "raw_text": text
        })
    
    except Exception as e:
        logging.error(f"Error in OCR processing: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

