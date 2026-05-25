import random
import colorsys
from flask import Flask, jsonify, request

app = Flask(__name__)

def hex_to_rgb(hex_str):
    """Converts a hex string (e.g., '3498db' or '#3498db') to an (R, G, B) tuple."""
    hex_str = hex_str.lstrip('#')
    if len(hex_str) != 6:
        raise ValueError("Hex string must be exactly 6 characters long.")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Converts an (R, G, B) tuple to a hex string."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def generate_palette(base_hex, mode="analogous"):
    """
    Generates a 4-color palette based on color theory logic.
    Uses HSL (Hue, Lightness, Saturation) for smooth mathematical shifts.
    """
    r, g, b = hex_to_rgb(base_hex)
    
    # Convert RGB (0-255) to HLS (0.0-1.0)
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    palette = []
    
    # Define color harmony mode rules
    if mode == "complementary":
        shifts = [0.0, 0.5, 0.05, 0.55]  # Base, direct opposite, and slight variations
    elif mode == "split-complementary":
        shifts = [0.0, 0.42, 0.58, 0.15] # Base, and the two framing the complement (~150 and 210 degrees)
    elif mode == "triadic":
        shifts = [0.0, 0.33, 0.66, 0.1]   # 120 degrees apart
    elif mode == "monochromatic":
        shifts = [0.0, 0.0, 0.0, 0.0]     # Same hue, we will alter lightness/saturation below
    else:  # "analogous" default
        shifts = [0.0, 0.08, -0.08, 0.15] # Close neighbors (~30 degrees)

    for i, shift in enumerate(shifts):
        new_h = (h + shift) % 1.0
        new_l = l
        new_s = s
        
        # Unique adjustments per mode to make the palette look professionally designed
        if mode == "monochromatic":
            # Scale lightness across steps while keeping it within reasonable bounds
            lightness_steps = [0.0, -0.2, 0.2, -0.4] if l > 0.5 else [0.0, 0.2, -0.2, 0.4]
            new_l = max(0.05, min(0.95, l + lightness_steps[i]))
            # Slightly desaturate darker/lighter variants for a cleaner look
            if i > 0:
                new_s = max(0.1, min(1.0, s * 0.8))
        else:
            # For other modes, slightly vary the 4th color to act as a distinct accent
            if i == 3:
                new_l = max(0.1, min(0.9, l + 0.12 if l < 0.5 else l - 0.12))
                new_s = max(0.1, min(1.0, s * 1.1))

        # Convert back to RGB
        new_r, new_g, new_b = colorsys.hls_to_rgb(new_h, new_l, new_s)
        rgb_tuple = (int(new_r * 255), int(new_g * 255), int(new_b * 255))
        
        # Dynamic naming for roles
        roles = ["Base Color", "Harmonic Accent 1", "Harmonic Accent 2", "Intentional Highlight"]
        
        palette.append({
            "hex": rgb_to_hex(rgb_tuple),
            "rgb": f"rgb({rgb_tuple}, {rgb_tuple}, {rgb_tuple})",
            "role": roles[i]
        })
        
    return palette

@app.route('/api/colors', methods=['GET'])
def get_color_palette():
    base_color = request.args.get('base', '3498db')
    mode = request.args.get('mode', 'analogous').lower()
    
    # Supported modes list for error messaging or validation
    supported_modes = ["analogous", "complementary", "split-complementary", "triadic", "monochromatic"]
    if mode not in supported_modes:
        return jsonify({
            "status": "error",
            "message": f"Invalid mode '{mode}'. Supported modes are: {', '.join(supported_modes)}"
        }), 400

    try:
        palette = generate_palette(base_color, mode=mode)
        return jsonify({
            "status": "success",
            "requested_mode": mode,
            "input_base_color": f"#{base_color.lstrip('#')}",
            "palette": palette
        })
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": f"Invalid hex color format. {str(e)}"
        }), 400

if __name__ == '__main__':
    app.run(debug=True)