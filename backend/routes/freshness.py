from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
import logging
from database import add_fresh_produce

bp = Blueprint("freshness", __name__)

# Load the CNN model
def load_model_with_custom_objects():
    def input_layer_deserializer(config):
        # Remove 'batch_shape' from config as it's not a valid argument
        config_copy = config.copy()
        config_copy.pop('batch_shape', None)
        return tf.keras.layers.InputLayer(**config_copy)

    custom_objects = {
        'InputLayer': input_layer_deserializer
    }
    return tf.keras.models.load_model("models/GridStack4.0.keras", custom_objects=custom_objects)

# Load model once when the application starts
model = load_model_with_custom_objects()

@bp.route("/freshness-check", methods=['POST'])
@cross_origin()
def classify_freshness():
    logging.debug("Received freshness check request")
    
    # Ensure the request contains an image file
    if 'image' not in request.files:
        logging.error("No image file in request")
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    produce = request.form.get('produce', 'Unknown')

    try:
        # Read the image data
        img = Image.open(file.stream).resize((256, 256))  # Use file.stream here
        img = np.array(img) / 255.0  # Normalize the image
        img = np.expand_dims(img, axis=0)  # Add batch dimension

        # Make prediction
        prediction = model.predict(img)
        logging.debug(f"Raw prediction: {prediction}")
        
        # Determine result based on the prediction
        result = "rotten" if prediction[0][0] > 0.5 else "fresh"

        # Store fresh produce record in the database
        add_fresh_produce(produce, result)

        return jsonify({"result": result, "produce": produce})

    except Exception as e:
        logging.error(f"Error in freshness check: {str(e)}")
        return jsonify({"error": str(e)}), 500
