import sys
import unittest
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

class TestMockFeedbackAndColor(unittest.TestCase):
    def test_high_energy_happiness(self):
        form_data = {"energy": "8", "happiness": "7"}
        feedback, color_name, rgb = mock_generate_feedback_and_color(form_data)
        self.assertIn("positive state of mind", feedback)
        self.assertEqual(color_name, "Yellow")
        self.assertEqual(rgb, COLOR_RGB_MAP["Yellow"])

    def test_low_energy(self):
        form_data = {"energy": "3", "happiness": "6"}
        feedback, color_name, rgb = mock_generate_feedback_and_color(form_data)
        self.assertIn("lower side", feedback)
        self.assertEqual(color_name, "Amber")
        self.assertEqual(rgb, COLOR_RGB_MAP["Amber"])

    def test_balanced(self):
        form_data = {"energy": "5", "happiness": "5"}
        feedback, color_name, rgb = mock_generate_feedback_and_color(form_data)
        self.assertIn("balanced state", feedback)
        self.assertEqual(color_name, "Cyan")
        self.assertEqual(rgb, COLOR_RGB_MAP["Cyan"])

if __name__ == '__main__':
    unittest.main() 