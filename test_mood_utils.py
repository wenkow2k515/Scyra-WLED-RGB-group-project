import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if OpenAI API key is available
openai_key = os.environ.get("OPENAI_API_KEY")
if not openai_key:
    print("ERROR: OPENAI_API_KEY not found in environment variables or .env file.")
    print("Please add your API key to the .env file in the format: OPENAI_API_KEY=your_api_key_here")
    sys.exit(1)

# Add the app directory to the path to import the function
sys.path.append('.')
from app.mood_utils import generate_feedback_and_color

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

# Call the function and display results
print("\n===== Testing generate_feedback_and_color function =====\n")
print(f"Using OpenAI API with key: {openai_key[:8]}...{openai_key[-4:]} (key partially hidden)")
print(f"\nTest data: {test_form_data}")

try:
    print("\nCalling OpenAI API... (this might take a few seconds)")
    feedback, color_name, rgb_values = generate_feedback_and_color(test_form_data)
    
    print("\n===== RESULTS =====")
    print(f"Feedback: {feedback}")
    print(f"Color Name: {color_name}")
    print(f"RGB Values: {rgb_values}")
    print(f"Hex Color: #{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}")
    print("\n✅ Test completed successfully!")
    
except Exception as e:
    print(f"\n❌ Error occurred: {str(e)}")
    print("\nPlease check:")
    print("1. Your API key is correct")
    print("2. You have proper internet connection")
    print("3. Your OpenAI account has sufficient credits") 