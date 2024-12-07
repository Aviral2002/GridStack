from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import requests
import logging
import io
import json

bp = Blueprint("brand_recognition", __name__)

# Replace with your Roboflow API details
ROBOFLOW_API_URL = 'https://detect.roboflow.com/brand-recignization-and-counting/2'
ROBOFLOW_API_KEY = 'hEmDOq25p2OMqt1yHbTW'

logging.basicConfig(level=logging.DEBUG)

@bp.route("/brand-recognition", methods=['POST'])
@cross_origin(supports_credentials=True)
def recognize_brand():
    try:
        if 'image' not in request.files:
            logging.error("No image file in request")
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files['image']
        image_bytes = image_file.read()
        
        # Log image details
        logging.debug(f"Image size: {len(image_bytes)} bytes")
        logging.debug(f"Image type: {image_file.content_type}")

        # Send to Roboflow
        try:
            response = requests.post(
                ROBOFLOW_API_URL,
                params={
                    "api_key": ROBOFLOW_API_KEY
                },
                files={
                    "file": ("image.jpg", image_bytes, image_file.content_type)
                },
                timeout=30  # Set a timeout for the request
            )
            logging.debug(f"Roboflow API response status: {response.status_code}")
            logging.debug(f"Roboflow API response headers: {json.dumps(dict(response.headers))}")
            logging.debug(f"Roboflow API response: {response.text}")
        
            response.raise_for_status()  # Raise an exception for bad status codes
        except requests.exceptions.RequestException as e:
            error_message = f"Error communicating with Roboflow API: {str(e)}"
            logging.error(error_message)
            return jsonify({"error": error_message, "brand": "Error"}), 500
        
        data = response.json()
        
        # Extract brand from Roboflow response
        predictions = data.get('predictions', [])
        if predictions:
            brand = predictions[0].get('class', 'Unknown')
        else:
            brand = 'Unknown'
        
        logging.info(f"Recognized brand: {brand}")
        return jsonify({"brand": brand})
    except json.JSONDecodeError as e:
        error_message = f"Error decoding JSON response from Roboflow: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message, "brand": "Error"}), 500
    except Exception as e:
        error_message = f"Unexpected error in brand recognition: {str(e)}"
        logging.error(error_message)
        return jsonify({"error": error_message, "brand": "Error"}), 500

