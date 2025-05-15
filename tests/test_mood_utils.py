import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

# Check if OpenAI API key is available
openai_key = os.environ.get("OPENAI_API_KEY")
has_api_key = bool(openai_key)

print("\n===== Testing generate_feedback_and_color function =====\n")

# Display API key status
if has_api_key:
    print(f"Using OpenAI API with key: {openai_key[:8]}...{openai_key[-4:]} (key partially hidden)")
else:
    print("OpenAI API key not found. Will use fallback rule-based generation.")

print(f"\nTest data: {test_form_data}")

try:
    print("\nCalling feedback generation function... (this might take a few seconds)")
    feedback, color_name, rgb_values = generate_feedback_and_color(test_form_data)
    
    print("\n===== RESULTS =====")
    print(f"Feedback: {feedback}")
    print(f"Color Name: {color_name}")
    print(f"RGB Values: {rgb_values}")
    print(f"Hex Color: #{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}")
    
    if has_api_key:
        print("\n✅ Test completed successfully with OpenAI API!")
    else:
        print("\n✅ Test completed successfully with rule-based fallback!")
    
except Exception as e:
    print(f"\n❌ Error occurred: {str(e)}")
    print("\nPlease check:")
    print("1. Your internet connection")
    print("2. If using API: Your OpenAI account has sufficient credits")

# Now test with API key temporarily disabled to demonstrate fallback
if has_api_key:
    print("\n\n===== Testing Fallback Functionality =====\n")
    print("Temporarily disabling API key to demonstrate fallback behavior...")
    
    # Save the original API key
    original_key = os.environ.get("OPENAI_API_KEY")
    
    try:
        # Temporarily remove API key from environment
        os.environ["OPENAI_API_KEY"] = ""
        
        # Reload the module to pick up the environment change
        import importlib
        from app import mood_utils
        importlib.reload(mood_utils)
        from app.mood_utils import generate_feedback_and_color
        
        # Test the function without API key
        print("\nCalling feedback generation function with API key disabled...")
        feedback, color_name, rgb_values = generate_feedback_and_color(test_form_data)
        
        print("\n===== FALLBACK RESULTS =====")
        print(f"Feedback: {feedback}")
        print(f"Color Name: {color_name}")
        print(f"RGB Values: {rgb_values}")
        print(f"Hex Color: #{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}")
        print("\n✅ Fallback test completed successfully!")
        
    finally:
        # Restore the original API key
        os.environ["OPENAI_API_KEY"] = original_key 