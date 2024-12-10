from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import requests
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv


# Load the .env file explicitly
load_dotenv(dotenv_path="../.env")

bp = Blueprint("brand_recognition", __name__)

ROBOFLOW_API_URL = os.getenv("VITE_ROBOFLOW_MODEL_ENDPOINT")
ROBOFLOW_API_KEY = os.getenv("VITE_ROBOFLOW_API_KEY")


if not ROBOFLOW_API_URL or not ROBOFLOW_API_KEY:
    raise ValueError("ROBOFLOW_API_URL and ROBOFLOW_API_KEY must be set in the environment")

logging.basicConfig(level=logging.INFO)

executor = ThreadPoolExecutor(max_workers=5)

def send_to_roboflow(image_bytes, content_type):
    try:
        response = requests.post(
            ROBOFLOW_API_URL,
            params={"api_key": ROBOFLOW_API_KEY},
            files={"file": ("image.jpg", image_bytes, content_type)},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with Roboflow API: {str(e)}")
        return None

@bp.route("/brand-recognition", methods=['POST'])
@cross_origin(supports_credentials=True)
def recognize_brand():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    
    future = executor.submit(send_to_roboflow, image_bytes, image_file.content_type)
    data = future.result()
    
    if data is None:
        return jsonify({"error": "Failed to communicate with Roboflow API", "brand": "Error"}), 500
    
    predictions = data.get('predictions', [])
    brand = predictions[0].get('class', 'Unknown') if predictions else 'Unknown'
    
    logging.info(f"Recognized brand: {brand}")
    return jsonify({"brand": brand})
