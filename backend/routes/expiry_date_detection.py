from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import pytesseract
import cv2
import numpy as np
import re
from datetime import datetime
import logging
import traceback
from database import add_packaged_product

bp = Blueprint("expiry_date_detection", __name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Tesseract path is not needed when installed system-wide
# pytesseract will find it automatically
custom_config = r'--oem 1 --psm 6 -c tessedit_char_whitelist="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz/.-: "'

def preprocess_image(image_bytes):
    try:
        # Convert bytes to numpy array
        np_arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        
        # Resize image to reduce processing time
        img = cv2.resize(img, (800, 600))
        
        # Apply simple thresholding
        _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return thresh
    except Exception as e:
        logging.error(f"Error in preprocess_image: {str(e)}")
        raise

def extract_dates_from_text(text):
    """Extract dates using multiple patterns and keywords"""
    dates = {}
    
    # Split text into lines for better processing
    lines = text.split('\n')
    
    # Pattern for text-based dates (e.g., SEP 2024)
    month_pattern = r'(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s*(\d{4})'
    
    # Pattern for numeric dates
    numeric_pattern = r'(\d{2}[/.-]\d{2}[/.-]\d{2,4})'
    
    for i, line in enumerate(lines):
        # Look for manufacturing date indicators
        if any(indicator in line.upper() for indicator in ['PKD', 'MFG', 'PACKED']):
            # Check current and next line for dates
            search_text = ' '.join(lines[i:i+2])
            month_match = re.search(month_pattern, search_text.upper())
            numeric_match = re.search(numeric_pattern, search_text)
            
            if month_match:
                dates['mfg_date'] = f"{month_match.group(1)} {month_match.group(2)}"
            elif numeric_match:
                dates['mfg_date'] = numeric_match.group(1)
        
        # Look for expiry date indicators
        if any(indicator in line.upper() for indicator in ['USE BY', 'EXP', 'BEST BEFORE']):
            # Check current and next line for dates
            search_text = ' '.join(lines[i:i+2])
            month_match = re.search(month_pattern, search_text.upper())
            numeric_match = re.search(numeric_pattern, search_text)
            
            if month_match:
                dates['exp_date'] = f"{month_match.group(1)} {month_match.group(2)}"
            elif numeric_match:
                dates['exp_date'] = numeric_match.group(1)
    
    # If no labeled dates found, try to find any dates in the text
    if not dates:
        all_month_dates = re.finditer(month_pattern, text.upper())
        all_numeric_dates = re.finditer(numeric_pattern, text)
        
        month_dates = list(all_month_dates)
        numeric_dates = list(all_numeric_dates)
        
        if month_dates:
            if len(month_dates) >= 2:
                dates['mfg_date'] = f"{month_dates[0].group(1)} {month_dates[0].group(2)}"
                dates['exp_date'] = f"{month_dates[1].group(1)} {month_dates[1].group(2)}"
            else:
                dates['exp_date'] = f"{month_dates[0].group(1)} {month_dates[0].group(2)}"
        elif numeric_dates:
            if len(numeric_dates) >= 2:
                dates['mfg_date'] = numeric_dates[0].group(1)
                dates['exp_date'] = numeric_dates[1].group(1)
            else:
                dates['exp_date'] = numeric_dates[0].group(1)
    
    return dates

def parse_date(date_string):
    """Parse date string into datetime object"""
    if not date_string:
        return None
        
    # Try text-based month format
    month_map = {
        'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
        'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
    }
    
    # Check for text month format (e.g., SEP 2024)
    match = re.match(r'(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s*(\d{4})', date_string.upper())
    if match:
        month_str, year_str = match.groups()
        try:
            month = month_map[month_str]
            year = int(year_str)
            return datetime(year, month, 1).date()
        except (ValueError, KeyError):
            pass
    
    # Try various numeric formats
    formats = [
        "%d/%m/%y", "%d/%m/%Y",  # DD/MM/YY, DD/MM/YYYY
        "%d-%m-%y", "%d-%m/%Y",  # DD-MM-YY, DD-MM/YYYY
        "%d.%m.%y", "%d.%m.%Y"   # DD.MM.YY, DD.MM.YYYY
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string.strip(), fmt).date()
        except ValueError:
            continue
    
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
        # Read and preprocess image
        image_bytes = image_file.read()
        preprocessed_img = preprocess_image(image_bytes)
        
        # Extract text using OCR with custom configuration and timeout
        try:
            start_time = time.time()
            text = pytesseract.image_to_string(preprocessed_img, config=custom_config, timeout=10)  # Increased timeout to 10 seconds
            end_time = time.time()
            logging.debug(f"OCR took {end_time - start_time:.2f} seconds")
        except RuntimeError as timeout_error:
            logging.error(f"OCR Timeout: {str(timeout_error)}")
            return jsonify({"error": "OCR process timed out"}), 500
        logging.debug(f"Extracted text: {text}")
        
        # Extract dates from text
        dates = extract_dates_from_text(text)
        logging.debug(f"Extracted dates: {dates}")
        
        if 'exp_date' in dates:
            expiry_date = parse_date(dates['exp_date'])
            if expiry_date:
                standardized_date = expiry_date.strftime("%Y-%m-%d")
                
                # Store in database
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