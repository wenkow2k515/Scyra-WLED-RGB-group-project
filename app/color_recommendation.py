"""
Color recommendation algorithm for Mood-WLED app.
Maps emotional states to color recommendations based on color psychology.
"""

import random
from datetime import datetime

# Function to convert hex to RGB
def hex_to_rgb(hex_color):
    """Convert hex color (without #) to RGB tuple"""
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (r, g, b)

# Color definitions in hex (without #)
COLORS = {
    # Primary colors
    'red': 'FF0000',
    'blue': '0066FF',
    'yellow': 'FFEB3B',
    'green': '4CAF50',
    
    # Secondary colors
    'orange': 'FF9800',
    'purple': '9C27B0',
    'pink': 'FF4081',
    'teal': '009688',
    'cyan': '00BCD4',
    
    # Variations
    'amber': 'FFC107',      # Sunset orange, warm and cozy
    'magenta': 'E91E63',    # Creative, balanced
    'light_blue': '03A9F4', # Refreshing, clear
    'deep_blue': '3F51B5',  # Calming, secure
    'lavender': 'CE93D8',   # Gentle, spiritual
    'mint': '8BC34A',       # Fresh, balanced
    
    # Neutrals
    'warm_white': 'FFF8E1', # Relaxing, cozy
    'cool_white': 'ECEFF1', # Alert, clear
}

# Effects suitable for different moods
EFFECTS = {
    'calm': ['Solid', 'Breathing', 'Gentle Wave'],
    'energetic': ['Rainbow', 'Chase', 'Running', 'Colortwinkles'],
    'focus': ['Solid', 'Static'],
    'creative': ['Palette', 'Colorwaves', 'Colorloop'],
    'balance': ['Gentle Wave', 'Palette', 'Breathing']
}

def get_color_recommendation(mood_data):
    """
    Generate a color recommendation based on mood metrics.
    
    Args:
        mood_data: A dictionary with 7 mood dimensions (all scores 1-10)
            - energy_level: How energetic the person feels
            - happiness: How happy/positive the person feels
            - anxiety: How anxious the person feels
            - stress: How stressed the person feels
            - focus: How focused/concentrated the person feels
            - irritability: How irritable the person feels
            - calmness: How calm/peaceful the person feels
            
    Returns:
        A dictionary with color recommendations in RGB format
    """
    # Extract mood values (all 1-10 scale)
    energy = mood_data.get('energy_level', 5)
    happiness = mood_data.get('happiness', 5)
    anxiety = mood_data.get('anxiety', 5)
    stress = mood_data.get('stress', 5)
    focus = mood_data.get('focus', 5)
    irritability = mood_data.get('irritability', 5)
    calmness = mood_data.get('calmness', 5)
    
    # Calculate some combined metrics
    positive_mood = (happiness + calmness) / 2
    negative_mood = (anxiety + stress + irritability) / 3
    arousal = energy  # How activated/stimulated
    
    # Default colors (neutral)
    primary_color = COLORS['cool_white']
    secondary_color = COLORS['blue']
    accent_color = COLORS['light_blue']
    
    # Default brightness (0-255)
    brightness = 180  # Moderate default
    
    # Higher brightness for higher energy, but not too bright when stressed
    if energy > 7:
        brightness = min(255, 180 + (energy - 5) * 15)
    elif energy < 4:
        brightness = max(80, 180 - (5 - energy) * 20)
    
    # Adjust brightness for stress/anxiety
    if stress > 7 or anxiety > 7:
        brightness = min(brightness, 160)  # Cap brightness when stressed
    
    # ------------------------------
    # Primary mood state detection
    # ------------------------------
    
    # 1. CALM & HAPPY - Blue/Cyan/Green tones
    if happiness > 6 and calmness > 6 and anxiety < 5:
        primary_color = COLORS['cyan'] if focus > 5 else COLORS['teal']
        secondary_color = COLORS['light_blue']
        accent_color = COLORS['mint']
    
    # 2. ENERGETIC & HAPPY - Orange/Yellow/Amber tones
    elif energy > 7 and happiness > 6:
        if focus > 6:  # Energetic, happy, and focused
            primary_color = COLORS['yellow']
            secondary_color = COLORS['amber']
            accent_color = COLORS['orange']
        else:  # Energetic and happy but less focused
            primary_color = COLORS['orange']
            secondary_color = COLORS['amber']
            accent_color = COLORS['yellow']
    
    # 3. LOW ENERGY - Orange/Red gentle stimulation
    elif energy < 4 and happiness < 6:
        primary_color = COLORS['amber']
        secondary_color = COLORS['warm_white']
        accent_color = COLORS['orange']
    
    # 4. ANXIOUS/STRESSED - Blue calming tones
    elif anxiety > 7 or stress > 7:
        primary_color = COLORS['deep_blue']
        secondary_color = COLORS['light_blue']
        accent_color = COLORS['teal']
    
    # 5. IRRITABLE - Lavender/Blue soothing tones
    elif irritability > 7:
        primary_color = COLORS['lavender']
        secondary_color = COLORS['deep_blue']
        accent_color = COLORS['blue']
    
    # 6. UNFOCUSED but needs concentration - Green/Blue focus enhancement
    elif focus < 4 and energy > 3:
        primary_color = COLORS['green']
        secondary_color = COLORS['teal']
        accent_color = COLORS['blue']
    
    # 7. CREATIVE state - Purple/Pink/Magenta
    elif focus > 5 and happiness > 5 and energy > 5:
        primary_color = COLORS['purple']
        secondary_color = COLORS['magenta']
        accent_color = COLORS['pink']
    
    # 8. BALANCE needed (mixed signals) - Teal/Green balance restoration
    elif abs(positive_mood - negative_mood) < 2:
        primary_color = COLORS['teal']
        secondary_color = COLORS['green']
        accent_color = COLORS['blue']
    
    # 9. LOW HAPPINESS - Yellow/Amber to elevate mood
    elif happiness < 4 and energy > 3:
        primary_color = COLORS['yellow']
        secondary_color = COLORS['amber']
        accent_color = COLORS['warm_white']
    
    # 10. TIRED BUT HAPPY - Gentle Yellow/White
    elif energy < 4 and happiness > 6:
        primary_color = COLORS['warm_white']
        secondary_color = COLORS['yellow']
        accent_color = COLORS['amber']
    
    # Convert hex colors to RGB
    primary_rgb = hex_to_rgb(primary_color)
    secondary_rgb = hex_to_rgb(secondary_color)
    accent_rgb = hex_to_rgb(accent_color)
    
    # Prepare the result
    result = {
        'primary_color': f"rgb({primary_rgb[0]},{primary_rgb[1]},{primary_rgb[2]})",
        'secondary_color': f"rgb({secondary_rgb[0]},{secondary_rgb[1]},{secondary_rgb[2]})",
        'accent_color': f"rgb({accent_rgb[0]},{accent_rgb[1]},{accent_rgb[2]})",
        'brightness': brightness,
        'timestamp': datetime.now().isoformat()
    }
    
    # Also include the hex values for backwards compatibility
    result['primary_hex'] = primary_color
    result['secondary_hex'] = secondary_color
    result['accent_hex'] = accent_color
    
    return result


def generate_similar_color(base_color, variation=15):
    """Generate a similar color with slight variation for better visual appeal"""
    # Convert hex to RGB
    r = int(base_color[0:2], 16)
    g = int(base_color[2:4], 16)
    b = int(base_color[4:6], 16)
    
    # Add variation
    r = max(0, min(255, r + random.randint(-variation, variation)))
    g = max(0, min(255, g + random.randint(-variation, variation)))
    b = max(0, min(255, b + random.randint(-variation, variation)))
    
    # Convert back to hex
    return f'{r:02X}{g:02X}{b:02X}'


def get_color_name(hex_code):
    """Get the name of a color from its hex code"""
    for name, code in COLORS.items():
        if code.upper() == hex_code.upper():
            return name.replace('_', ' ').title()
    return "Custom Color"