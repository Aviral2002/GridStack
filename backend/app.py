import os
from flask import Flask
from flask_cors import CORS
from database import init_db
from routes import freshness_bp, expiry_bp, brand_bp, data_display_bp
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Apply CORS with support for credentials
CORS(app, resources={r"/api/*": {"origins": os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')}})

# Initialize the database
init_db()

# Register blueprints
app.register_blueprint(freshness_bp, url_prefix='/api/freshness')
app.register_blueprint(expiry_bp, url_prefix='/api/expiry')
app.register_blueprint(brand_bp, url_prefix='/api/brand')
app.register_blueprint(data_display_bp, url_prefix='/api/data')

if __name__ == '__main__':
    app.run(debug=True)

