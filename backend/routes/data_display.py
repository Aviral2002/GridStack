from flask import Blueprint, jsonify
from flask_cors import cross_origin
from database import (
    get_all_packaged_products,
    get_all_fresh_produce,
)

bp = Blueprint("data_display", __name__)

@bp.route("/get-all-data", methods=['GET'])
@cross_origin()
def get_all_data():
    try:
        packaged_products = get_all_packaged_products()
        fresh_produce = get_all_fresh_produce()
        return jsonify({
            "packaged_products": packaged_products,
            "fresh_produce": fresh_produce
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500