import os
import sys
from openai import OpenAI
from typing import Tuple, Dict, Any

# Initialize the OpenAI client with API key
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Mapping of color names to RGB tuples
COLOR_RGB_MAP = {
    # Energizing colors
    "Red": (255, 0, 0),
    "Bright Red": (255, 40, 40),
    "Ruby": (224, 17, 95),
    "Crimson": (220, 20, 60),
    
    # Warm colors
    "Orange": (255, 165, 0),
    "Coral": (255, 127, 80),
    "Amber": (255, 191, 0),
    "Peach": (255, 218, 185),
    
    # Uplifting colors
    "Yellow": (255, 255, 0),
    "Sunshine": (255, 236, 139),
    "Gold": (255, 215, 0),
    "Lemon": (255, 250, 205),
    
    # Balanced/natural colors
    "Green": (0, 255, 0),
    "Mint": (189, 252, 201),
    "Sage": (138, 154, 91),
    "Forest Green": (34, 139, 34),
    "Emerald": (80, 200, 120),
    
    # Refreshing colors
    "Cyan": (0, 255, 255),
    "Turquoise": (64, 224, 208),
    "Aqua": (127, 255, 212),
    "Sky Blue": (135, 206, 235),
    
    # Calming colors
    "Blue": (0, 0, 255),
    "Navy": (0, 0, 128),
    "Royal Blue": (65, 105, 225),
    "Periwinkle": (204, 204, 255),
    "Cornflower Blue": (100, 149, 237),
    
    # Creative colors
    "Purple": (128, 0, 128),
    "Lavender": (230, 230, 250),
    "Violet": (138, 43, 226),
    "Indigo": (75, 0, 130),
    
    # Nurturing colors
    "Pink": (255, 182, 193),
    "Rose": (255, 105, 180),
    "Magenta": (255, 0, 255),
    "Fuchsia": (255, 0, 128),
    
    # Neutral colors
    "Warm White": (255, 244, 229),
    "Cool White": (240, 255, 255),
    "Soft White": (255, 253, 245),
    "Cream": (255, 253, 208)
}

def generate_rule_based_feedback(form_data: Dict[str, Any]) -> Tuple[str, str, Tuple[int, int, int]]:
    """
    Generate feedback and color recommendations using rule-based logic when API is unavailable.
    
    This is a fallback for when the OpenAI API key is not available.
    """
    # Extract mood data from form
    energy = int(form_data.get("energy", 5))
    happiness = int(form_data.get("happiness", 5))
    stress = int(form_data.get("stress", 5))
    anxiety = int(form_data.get("anxiety", 5))
    creativity = int(form_data.get("creativity", 5))
    wants_to_relax = form_data.get("relax", "no") == "yes"
    wants_to_focus = form_data.get("focus", "no") == "yes"
    
    # Default values
    feedback = ""
    color_name = "Blue"
    
    # High energy and happiness
    if energy > 7 and happiness > 7:
        if wants_to_focus:
            feedback = "Your energy and happiness levels are high! Channel this positive energy into your tasks while maintaining focus. Consider taking short breaks to sustain your enthusiasm."
            color_name = "Yellow"
        else:
            feedback = "You're experiencing a wonderful balance of high energy and happiness. This is a great time for creative activities or social interactions that allow you to express your positive energy."
            color_name = "Orange"
    
    # Low energy, low happiness
    elif energy < 4 and happiness < 4:
        feedback = "You seem to be experiencing lower energy and mood today. Remember to be gentle with yourself and consider activities that bring you comfort. Small steps forward are still progress."
        color_name = "Lavender"
    
    # High stress or anxiety
    elif stress > 7 or anxiety > 7:
        if wants_to_relax:
            feedback = "Your stress and anxiety levels are elevated. Prioritize self-care activities like deep breathing, gentle movement, or spending time in nature to help restore your calm."
            color_name = "Blue"
        else:
            feedback = "You're experiencing heightened stress or anxiety. Consider setting small, achievable goals and breaking tasks into manageable parts to reduce feeling overwhelmed."
            color_name = "Cyan"
    
    # Average across the board
    elif all(4 <= x <= 6 for x in [energy, happiness, stress, anxiety, creativity]):
        feedback = "Your mood appears balanced across different dimensions. This stability can be a good foundation for both productive work and relaxation activities."
        color_name = "Green"
    
    # High creativity
    elif creativity > 7:
        feedback = "Your creativity is flowing strongly today! This is an excellent time to work on projects that require innovation or artistic expression. Allow your imagination to guide you."
        color_name = "Purple"
    
    # Wants to focus but low focus/energy
    elif wants_to_focus and energy < 5:
        feedback = "You want to focus but may be experiencing lower energy. Consider a short energizing activity before tackling important tasks, and break work into smaller segments."
        color_name = "Turquoise"
    
    # Wants to relax but high stress
    elif wants_to_relax and (stress > 6 or anxiety > 6):
        feedback = "Taking time to relax is a good choice given your stress levels. Consider activities that engage your senses and help your mind and body unwind."
        color_name = "Periwinkle"
    
    # Default case
    else:
        feedback = "Based on your mood indicators, today might be a good day to find balance between productivity and self-care. Listen to what your body and mind need most."
        color_name = "Emerald"
    
    # Return the feedback and color
    return feedback, color_name, COLOR_RGB_MAP[color_name]

def generate_feedback_and_color(form_data: Dict[str, Any]) -> Tuple[str, str, Tuple[int, int, int]]:
    """
    Generate personalized feedback and color recommendation based on mood survey data.
    
    Args:
        form_data: Dictionary containing form submission data with the following keys:
            - energy: Energy level (scale 1-10)
            - happiness: Happiness level (scale 1-10)
            - stress: Stress level (scale 1-10)
            - anxiety: Anxiety level (scale 1-10)
            - creativity: Creativity level (scale 1-10)
            - relax: Whether user wants to relax ("yes" or "no")
            - focus: Whether user wants to focus ("yes" or "no")
            - journal: Optional journal entry text
    
    Returns:
        Tuple containing:
            - feedback_text: Personalized feedback message (max 100 words)
            - color_name: Name of the recommended color
            - rgb_tuple: RGB values for the recommended color as (r, g, b)
    """
    # Check if OpenAI API key is configured
    if not client.api_key:
        print("OpenAI API key not found. Using rule-based feedback generation instead.")
        return generate_rule_based_feedback(form_data)
    
    # Extract mood and journal data from form_data
    energy = int(form_data.get("energy", 5))
    happiness = int(form_data.get("happiness", 5))
    stress = int(form_data.get("stress", 5))
    anxiety = int(form_data.get("anxiety", 5))
    creativity = int(form_data.get("creativity", 5))
    relax = form_data.get("relax", "no") == "yes"
    focus = form_data.get("focus", "no") == "yes"
    journal = form_data.get("journal", "")
    
    # Truncate journal if too long to avoid token limits
    journal_excerpt = journal[:500] + "..." if len(journal) > 500 else journal
    
    # Create prompt for OpenAI
    prompt = f"""
    Based on the following mood survey responses, provide a personalized feedback message (max 100 words) and recommend the most suitable color from the provided list.
    
    MOOD DATA:
    - Energy level (1-10): {energy}
    - Happiness level (1-10): {happiness}
    - Stress level (1-10): {stress}
    - Anxiety level (1-10): {anxiety}
    - Creativity level (1-10): {creativity}
    - Wants to relax: {"Yes" if relax else "No"}
    - Wants to focus: {"Yes" if focus else "No"}
    
    JOURNAL ENTRY:
    {journal_excerpt}
    
    COLOR MOOD ASSOCIATIONS:
    - Energizing colors (Red, Bright Red, Ruby, Crimson): Stimulating, energizing, passionate
    - Warm colors (Orange, Coral, Amber, Peach): Creative, enthusiastic, warm, sociable
    - Uplifting colors (Yellow, Sunshine, Gold, Lemon): Happy, optimistic, clarity, positivity
    - Balanced/natural colors (Green, Mint, Sage, Forest Green, Emerald): Balanced, growth, harmony, focus
    - Refreshing colors (Cyan, Turquoise, Aqua, Sky Blue): Refreshing, clear-minded, communication
    - Calming colors (Blue, Navy, Royal Blue, Periwinkle, Cornflower Blue): Calming, peaceful, reduces anxiety
    - Creative colors (Purple, Lavender, Violet, Indigo): Imagination, inspiration, spiritual
    - Nurturing colors (Pink, Rose, Magenta, Fuchsia): Gentle, compassionate, empathetic
    - Neutral colors (Warm White, Cool White, Soft White, Cream): Soothing, clean, pure, simple
    
    AVAILABLE COLORS (choose exactly one):
    Red, Bright Red, Ruby, Crimson, Orange, Coral, Amber, Peach, Yellow, Sunshine, Gold, Lemon, Green, Mint, Sage, Forest Green, Emerald, Cyan, Turquoise, Aqua, Sky Blue, Blue, Navy, Royal Blue, Periwinkle, Cornflower Blue, Purple, Lavender, Violet, Indigo, Pink, Rose, Magenta, Fuchsia, Warm White, Cool White, Soft White, Cream
    
    FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
    Feedback: [your personalized feedback message, max 100 words]
    Color: [one color name from the available list]
    """
    
    try:
        # Use OpenAI's API to generate the response (new client format)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using gpt-3.5-turbo which is more widely available
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides mood analysis and color recommendations based on psychological principles."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        # Extract the response content
        content = response.choices[0].message.content.strip()
        
        # Parse the response to extract feedback and color
        feedback = ""
        color_name = ""
        
        for line in content.split('\n'):
            if line.startswith("Feedback:"):
                feedback = line[len("Feedback:"):].strip()
            elif line.startswith("Color:"):
                color_name = line[len("Color:"):].strip()
        
        # Validate the color name and get RGB values
        if color_name not in COLOR_RGB_MAP:
            # Fallback to a default color if the returned color is not in our map
            color_name = "Blue"
        
        rgb_tuple = COLOR_RGB_MAP[color_name]
        
        return feedback, color_name, rgb_tuple
        
    except Exception as e:
        print(f"Error generating feedback with OpenAI API: {str(e)}")
        print("Falling back to rule-based feedback generation.")
        return generate_rule_based_feedback(form_data) 