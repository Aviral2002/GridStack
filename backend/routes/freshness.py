from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image, UnidentifiedImageError
import io
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

bp = Blueprint("freshness", __name__)

# Load the CNN model
try:
    model = load_model("models/imageclassifier.h5")
    logging.info("Freshness Model Loaded Successfully")
except Exception as load_error:
    logging.error(f"Error loading model: {load_error}")
    model = None

@bp.route("/freshness-check", methods=['OPTIONS', 'POST'])
@cross_origin()
def classify_freshness():
    if request.method == 'OPTIONS':
        logging.debug("Received OPTIONS request")
        return jsonify(success=True)

    try:
        image_data = None
        
        # Check if the request has form-data
        if 'image' in request.files:
            logging.debug("Received image in form-data")
            file = request.files['image']
            image_data = file.read()
        # Check if the request has raw image data
        elif request.data:
            logging.debug("Received raw image data")
            image_data = request.data
        
        if image_data is None:
            logging.error("No image data in the request")
            return jsonify({"error": "No image provided"}), 400
        
        # Open the image file
        try:
            img = Image.open(io.BytesIO(image_data)).resize((254, 254))
            img = np.array(img) / 255.0
            img = np.expand_dims(img, axis=0)
            logging.debug("Image successfully preprocessed")
        except UnidentifiedImageError:
            logging.error("Cannot identify image file - ensure valid image")
            return jsonify({"error": "Invalid image file"}), 400
        except Exception as image_error:
            logging.error(f"Error processing image: {image_error}")
            return jsonify({"error": "Error processing image"}), 500

        # Predict freshness
        try:
            if model is None:
                raise RuntimeError("Model is not loaded")
            prediction = model.predict(img)
            logging.debug(f"Model Prediction: {prediction}")
            result = "rotten" if prediction[0][0] > 0.5 else "fresh"
            logging.debug(f"Model Output: {result}")
        except Exception as prediction_error:
            logging.error(f"Error during prediction: {prediction_error}")
            return jsonify({"error": "Error during prediction"}), 500

        return jsonify({"result": result})

    except Exception as e:
        logging.error(f"Freshness check error: {e}")
        return jsonify({"error": str(e), "result": "Error"}), 500