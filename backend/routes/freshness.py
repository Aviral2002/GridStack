from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
import logging
from database import add_fresh_produce

bp = Blueprint("freshness", __name__)

# Load the CNN model
model = load_model("models/freshnessIndex.h5")

@bp.route("/freshness-check", methods=['POST'])
@cross_origin()
def classify_freshness():
    logging.debug("Received freshness check request")
    
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
    
    file = request.files['image']
    produce = request.form.get('produce', 'Unknown')
    
    try:
        img = Image.open(io.BytesIO(image_data)).resize((254, 254))
        img = np.array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        prediction = model.predict(img)
        logging.debug(f"Raw prediction: {prediction}")
        result = "rotten" if prediction[0][0] > 0.5 else "fresh"
     
        add_fresh_produce(produce, result)

        return jsonify({"result": result,})

    except Exception as e:
        logging.error(f"Error in freshness check: {str(e)}")
        return jsonify({"error": str(e)}), 500

