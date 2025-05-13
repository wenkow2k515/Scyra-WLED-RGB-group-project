import sys
sys.path.append('.')
from app.mood_utils import COLOR_RGB_MAP

# Test data for the function
test_form_data = {
    "energy": "7",
    "happiness": "6",
    "stress": "5",
    "anxiety": "4",
    "creativity": "8",
    "relax": "no",
    "focus": "yes",
    "journal": "Today I feel quite motivated to work on my project. I'm hoping to make good progress on implementing the mood analysis feature."
}

def mock_generate_feedback_and_color(form_data):
    """
    A test version of the function that returns mock data without calling the API.
    This is useful for testing integration without needing an API key.
    """
    # Mock feedback based on form data
    energy = int(form_data.get("energy", 5))
    happiness = int(form_data.get("happiness", 5))
    
    if energy > 6 and happiness > 5:
        feedback = "Your energy and happiness levels suggest you're in a positive state of mind for creative tasks. Consider channeling this energy into projects that require innovation."
        color_name = "Yellow"
    elif energy < 4:
        feedback = "Your energy levels are on the lower side. A gentle stimulating environment may help boost your mood and productivity."
        color_name = "Amber"
    else:
        feedback = "Your mood profile shows a balanced state. This is a good time for focused work or learning new skills."
        color_name = "Cyan"
    
    # Get RGB values for the color
    rgb_tuple = COLOR_RGB_MAP[color_name]
    
    return feedback, color_name, rgb_tuple

# Call the function and display results
print("\n===== Testing mock feedback and color function =====\n")
print(f"Test data: {test_form_data}")

try:
    feedback, color_name, rgb_values = mock_generate_feedback_and_color(test_form_data)
    
    print("\n===== RESULTS =====")
    print(f"Feedback: {feedback}")
    print(f"Color Name: {color_name}")
    print(f"RGB Values: {rgb_values}")
    print(f"Hex Color: #{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}")
    print("\n✅ Test completed successfully!")
    
except Exception as e:
    print(f"\n❌ Error occurred: {str(e)}") 