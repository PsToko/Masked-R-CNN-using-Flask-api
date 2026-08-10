import os
import uuid

from flask import Blueprint, request, jsonify, send_from_directory

from PIL import Image

from predictor import MaskRCNNPredictor
from draw import draw_predictions


predictor = MaskRCNNPredictor()


api = Blueprint(
    "api",
    __name__
)


OUTPUT_FOLDER = "outputs"

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


@api.route("/predict", methods=["POST"])
def predict():

    # -------------------------
    # Check image
    # -------------------------

    if "image" not in request.files:

        return jsonify({
            "error": "No image provided"
        }), 400


    file = request.files["image"]


    if file.filename == "":

        return jsonify({
            "error": "Empty filename"
        }), 400


    # -------------------------
    # Load image
    # -------------------------

    try:

        image = Image.open(
            file
        ).convert("RGB")

    except Exception:

        return jsonify({
            "error": "Invalid image"
        }), 400


    # -------------------------
    # Run Mask R-CNN
    # -------------------------

    results = predictor.predict(
        image
    )


    # -------------------------
    # Create output filename
    # -------------------------

    filename = f"{uuid.uuid4()}.png"

    output_path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )


    # -------------------------
    # Create annotated image
    # -------------------------

    draw_predictions(
        image,
        results,
        output_path
    )


    # -------------------------
    # Prepare JSON response
    # -------------------------

    predictions = []

    for result in results:

        predictions.append({
            "class_id": result["class_id"],
            "class_name": result["class_name"],
            "confidence": result["confidence"],
            "box": result["box"]
        })


    return jsonify({
        "predictions": predictions,
        "image": f"/outputs/{filename}"
    })


@api.route("/outputs/<filename>", methods=["GET"])
def get_output(filename):

    return send_from_directory(
        OUTPUT_FOLDER,
        filename
    )