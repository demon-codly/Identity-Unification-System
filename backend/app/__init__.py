"""
Flask Application Factory
"""
from flask import Flask
from flask_cors import CORS


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Enable CORS for React frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Register blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    return app
