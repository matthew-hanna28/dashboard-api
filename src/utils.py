def get_contrast_text(rgb):
    """
    Uses the YIQ brightness formula to determine if text should be 
    black or white based on background brightness.
    """
    r, g, b = rgb
    # Formula: (R*299 + G*587 + B*114) / 1000
    yiq = ((r * 299) + (g * 587) + (b * 114)) / 1000
    return "black" if yiq >= 128 else "white"