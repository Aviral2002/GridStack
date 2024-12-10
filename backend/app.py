import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from routes import freshness_bp, expiry_bp, brand_bp, data_display_bp
from database import init_db

app = Flask(__name__)
CORS(app)

# Initialize the database
init_db()

# Register blueprints
app.register_blueprint(freshness_bp, url_prefix='/api/freshness')
app.register_blueprint(expiry_bp, url_prefix='/api/expiry')
app.register_blueprint(brand_bp, url_prefix='/api/brand')
app.register_blueprint(data_display_bp, url_prefix='/api/data')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

