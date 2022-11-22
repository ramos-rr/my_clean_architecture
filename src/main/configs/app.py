from flask import Flask
from flask_cors import CORS
from src.main.routes import api_routes_bp


# CREATE AN APP
app = Flask(__name__)
CORS(app)

# Register BLUEPRINT IN APP
app.register_blueprint(blueprint=api_routes_bp)
