# src/routes.py
from flask import Blueprint, jsonify, request
from .logic import generate_palette  # Import logic
from .utils import get_css_colors    # Import helper

api_bp = Blueprint('api', __name__)

@api_bp.route('/colors', methods=['GET'])
def get_color_palette():
    base_hex = request.args.get('base', '3498db')
    mode = request.args.get('mode', 'analogous')
    
    try:
        # Generate the palette using the logic function
        palette = generate_palette(base_hex, mode)
        return jsonify({"status": "success", "palette": palette})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400