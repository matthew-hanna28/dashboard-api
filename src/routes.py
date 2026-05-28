from flask import Blueprint, jsonify, request
from flasgger import swag_from
from .logic import generate_palette

api_bp = Blueprint('api', __name__)

@api_bp.route('/colors', methods=['GET'])
@swag_from({
    'parameters': [
        {'name': 'base', 'in': 'query', 'type': 'string', 'default': '3498db'},
        {'name': 'mode', 'in': 'query', 'type': 'string', 'default': 'analogous', 
         'enum': ['analogous', 'complementary', 'triadic', 'monochromatic']}
    ],
    'responses': {
        200: {'description': 'A list of colors in the palette'},
        400: {'description': 'Invalid input'}
    }
})
def get_colors():
    base = request.args.get('base', '3498db').lstrip('#')
    mode = request.args.get('mode', 'analogous').lower()
    
    # Simple, clean validation
    if len(base) != 6:
        return jsonify({"error": "Invalid hex format"}), 400
        
    palette = generate_palette(base, mode)
    return jsonify({"status": "success", "palette": palette})