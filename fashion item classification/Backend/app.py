from flask import Flask, request, jsonify
from flask_cors import CORS

import tensorflow as tf
import numpy as np

from PIL import Image
import io


# ==========================================
# CREATE FLASK APP
# ==========================================

app = Flask(__name__)

CORS(app)


# ==========================================
# LOAD TRAINED MODEL
# ==========================================

MODEL_PATH = "fashion_item_classifier (1).keras"

model = tf.keras.models.load_model(MODEL_PATH)

print("====================================")
print("Fashion Classification Model Loaded")
print("====================================")


# ==========================================
# FASHION MNIST CLASS NAMES
# ==========================================

class_names = [
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot"
]


# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Fashion Item Classification API is running",
        "status": "success"
    })


# ==========================================
# PREDICTION ROUTE
# ==========================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Check if image exists
        if "image" not in request.files:

            return jsonify({
                "error": "No image uploaded"
            }), 400


        # Get uploaded image
        file = request.files["image"]


        # Open image
        image = Image.open(
            io.BytesIO(file.read())
        )


        # Convert to grayscale
        image = image.convert("L")


        # Resize to 28 x 28
        image = image.resize(
            (28, 28)
        )


        # Convert to NumPy array
        image_array = np.array(image)


        # Normalize pixel values
        image_array = (
            image_array.astype("float32") / 255.0
        )


        # Add channel dimension
        image_array = image_array.reshape(
            28,
            28,
            1
        )


        # Add batch dimension
        image_array = np.expand_dims(
            image_array,
            axis=0
        )


        # Make prediction
        predictions = model.predict(
            image_array,
            verbose=0
        )


        # Find predicted class
        predicted_class = np.argmax(
            predictions[0]
        )


        # Find confidence
        confidence = (
            predictions[0][predicted_class] * 100
        )


        # Get fashion item name
        predicted_item = class_names[
            predicted_class
        ]


        # Send result to frontend
        return jsonify({

            "prediction": predicted_item,

            "confidence": round(
                float(confidence),
                2
            ),

            "class_id": int(
                predicted_class
            )

        })


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )