from flask import Blueprint, jsonify, request
from .logic import generate_palette

api_bp = Blueprint('api', __name__)

@api_bp.route('/colors', methods=['GET'])
def get_colors():
    # Use request arguments with defaults
    base = request.args.get('base', '3498db')
    mode = request.args.get('mode', 'analogous')
    
    # Simple validation
    palette = generate_palette(base, mode)
    return jsonify({"status": "success", "palette": palette})