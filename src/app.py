from flask import Flask, jsonify, request
from flask_caching import Cache # pip install flask-caching
import colorsys

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# --- Helper Functions ---
def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def get_css_colors(rgb):
    """Returns properly formatted CSS color strings."""
    r, g, b = rgb
    return {
        "rgb": f"rgb({r}, {g}, {b})",
        "rgba": f"rgba({r}, {g}, {b}, 1.0)"
    }

# --- Core Logic ---
@app.route('/api/colors', methods=['GET'])
@cache.cached(timeout=300, query_string=True) # Cache for 5 minutes
def get_color_palette():
    base_hex = request.args.get('base', '3498db').lstrip('#')
    mode = request.args.get('mode', 'analogous').lower()
    
    try:
        # (Insert your existing generate_palette logic here)
        # Note: In your loop, change the append line to:
        # palette.append({
        #     "hex": rgb_to_hex(rgb_tuple),
        #     **get_css_colors(rgb_tuple), # Unpacks the dict into the response
        #     "role": roles[i]
        # })
        return jsonify({"status": "success", "palette": palette})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400