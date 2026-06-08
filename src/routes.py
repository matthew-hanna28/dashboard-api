from flask import Blueprint, jsonify, request
from flasgger import swag_from
from .logic import generate_palette
from flask import make_response

@api_bp.route('/api/download')
def download_palette():
    # ... generate palette ...
    response = make_response(jsonify(palette))
    response.headers["Content-Disposition"] = "attachment; filename=palette.json"
    return response

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

from flask import jsonify

# Add this to your api_bp
@api_bp.errorhandler(Exception)
def handle_exception(e):
    # This catches EVERYTHING unexpected
    return jsonify({
        "status": "error",
        "message": "An internal error occurred.",
        "detail": str(e)
    }), 500

@api_bp.route('/colors/css', methods=['GET'])
def get_css_export():
    # Generate palette...
    css_string = ":root {\n"
    for item in palette:
        css_string += f"  --color-{item['role'].replace(' ', '-').lower()}: {item['hex']};\n"
    css_string += "}"
    return css_string, 200, {'Content-Type': 'text/css'}