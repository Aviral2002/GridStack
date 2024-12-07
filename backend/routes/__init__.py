# routes/__init__.py

from .freshness import bp as freshness_bp
from .expiry_date_detection import bp as expiry_bp
from .brand_recognition import bp as brand_bp

# Export the blueprints as a package
__all__ = ["freshness_bp", "expiry_bp", "brand_bp"]
