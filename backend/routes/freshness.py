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
import tensorflow as tf
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

@bp.route("/freshness-check", methods=['POST'])
@cross_origin()
def classify_freshness():
    logging.debug("Received freshness check request")
    
    if 'image' not in request.files:
        logging.error("No image file in request")
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    produce = request.form.get('produce', 'Unknown')
    
    try:
        img = Image.open(io.BytesIO(image_data)).resize((256, 256))
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

