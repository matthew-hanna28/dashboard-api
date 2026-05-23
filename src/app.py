import random
import colorsys
from flask import Flask, jsonify, request

app = Flask(__name__)

def hex_to_rgb(hex_str):
    """Converts a hex string (e.g., '3498db') to an (R, G, B) tuple."""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Converts an (R, G, B) tuple to a hex string."""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb), int(rgb), int(rgb))

def generate_palette(base_hex, mode="analogous"):
    """
    Generates a 4-color palette based on color theory logic.
    Uses HSL (Hue, Saturation, Lightness) for smooth mathematical shifts.
    """
    try:
        r, g, b = hex_to_rgb(base_hex)
    except ValueError:
        # Fallback to a nice random color if input hex is invalid
        r, g, b = [random.randint(0, 255) for _ in range(3)]
        
    # Convert RGB (0-255) to HLS (0.0-1.0) for easier color wheel math
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    
    palette = []
    
    # Define hue shifts based on the chosen color harmony mode
    if mode == "complementary":
        # Direct opposite side of the color wheel (180 degrees / 0.5 turn)
        shifts = [0.0, 0.5, 0.05, 0.55] 
    elif mode == "triadic":
        # 120 degrees apart (0.33 and 0.66 turns)
        shifts = [0.0, 0.33, 0.66, 0.1]
    else:  # "analogous" default
        # Neighbors on the color wheel (approx 30 degrees apart)
        shifts = [0.0, 0.08, -0.08, 0.15]

    for i, shift in enumerate(shifts):
        # Calculate new hue and keep it within the 0.0-1.0 boundary
        new_h = (h + shift) % 1.0
        
        # Slightly vary lightness for the 4th accent color to keep it interesting
        new_l = max(0.1, min(0.9, l + 0.1 if i == 3 else l))
        
        # Convert back to RGB
        new_r, new_g, new_b = colorsys.hls_to_rgb(new_h, new_l, s)
        rgb_tuple = (int(new_r * 255), int(new_g * 255), int(new_b * 255))
        
        palette.append({
            "hex": rgb_to_hex(rgb_tuple),
            "rgb": f"rgb({rgb_tuple}, {rgb_tuple}, {rgb_tuple})",
            "role": "Base" if i == 0 else f"Harmonic Accent {i}"
        })
        
    return palette

@app.route('/api/colors', methods=['GET'])
def get_color_palette():
    # Grab query parameters from the URL, or use defaults
    # Example usage: /api/colors?base=3498db&mode=complementary
    base_color = request.args.get('base', '3498db')
    mode = request.args.get('mode', 'analogous').lower()
    
    palette = generate_palette(base_color, mode=mode)
    
    return jsonify({
        "status": "success",
        "requested_mode": mode,
        "input_base_color": f"#{base_color}",
        "palette": palette
    })

if __name__ == '__main__':
    app.run(debug=True)