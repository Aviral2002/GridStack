from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from database import get_all_packaged_products, get_all_fresh_produce, delete_rows

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

@bp.route("/delete-rows", methods=['POST'])
@cross_origin()
def delete_data_rows():
    try:
        data = request.json
        table = data.get('type')
        ids = data.get('ids')
        
        if not table or not ids:
            return jsonify({"error": "Missing type or ids"}), 400
        
        delete_rows(table, ids)
        return jsonify({"success": True, "message": f"Deleted {len(ids)} rows from {table}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

