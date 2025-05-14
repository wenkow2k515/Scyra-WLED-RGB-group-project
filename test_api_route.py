from flask import Flask, request, render_template_string, jsonify
from dotenv import load_dotenv
from app.mood_utils import generate_feedback_and_color, COLOR_RGB_MAP

# Load environment variables from .env file
load_dotenv()

# Create a simple Flask app
app = Flask(__name__)

# HTML template for the form
FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Mood Survey Test</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input[type="range"] { width: 100%; }
        .range-labels { display: flex; justify-content: space-between; font-size: 12px; }
        textarea { width: 100%; height: 100px; }
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; cursor: pointer; }
        .color-preview { margin-top: 30px; padding: 20px; border-radius: 5px; color: white; text-align: center; }
    </style>
</head>
<body>
    <h1>Test Mood Survey</h1>
    
    <form method="post" action="/test">
        <div class="form-group">
            <label for="energy">Energy Level (1-10)</label>
            <input type="range" id="energy" name="energy" min="1" max="10" value="5">
            <div class="range-labels">
                <span>1</span><span>2</span><span>3</span><span>4</span><span>5</span>
                <span>6</span><span>7</span><span>8</span><span>9</span><span>10</span>
            </div>
        </div>
        
        <div class="form-group">
            <label for="happiness">Happiness Level (1-10)</label>
            <input type="range" id="happiness" name="happiness" min="1" max="10" value="5">
            <div class="range-labels">
                <span>1</span><span>2</span><span>3</span><span>4</span><span>5</span>
                <span>6</span><span>7</span><span>8</span><span>9</span><span>10</span>
            </div>
        </div>
        
        <div class="form-group">
            <label for="stress">Stress Level (1-10)</label>
            <input type="range" id="stress" name="stress" min="1" max="10" value="5">
            <div class="range-labels">
                <span>1</span><span>2</span><span>3</span><span>4</span><span>5</span>
                <span>6</span><span>7</span><span>8</span><span>9</span><span>10</span>
            </div>
        </div>
        
        <div class="form-group">
            <label for="anxiety">Anxiety Level (1-10)</label>
            <input type="range" id="anxiety" name="anxiety" min="1" max="10" value="5">
            <div class="range-labels">
                <span>1</span><span>2</span><span>3</span><span>4</span><span>5</span>
                <span>6</span><span>7</span><span>8</span><span>9</span><span>10</span>
            </div>
        </div>
        
        <div class="form-group">
            <label for="creativity">Creativity Level (1-10)</label>
            <input type="range" id="creativity" name="creativity" min="1" max="10" value="5">
            <div class="range-labels">
                <span>1</span><span>2</span><span>3</span><span>4</span><span>5</span>
                <span>6</span><span>7</span><span>8</span><span>9</span><span>10</span>
            </div>
        </div>
        
        <div class="form-group">
            <label>Do you want to relax?</label>
            <input type="radio" id="relax_yes" name="relax" value="yes">
            <label for="relax_yes">Yes</label>
            <input type="radio" id="relax_no" name="relax" value="no" checked>
            <label for="relax_no">No</label>
        </div>
        
        <div class="form-group">
            <label>Do you want to focus?</label>
            <input type="radio" id="focus_yes" name="focus" value="yes">
            <label for="focus_yes">Yes</label>
            <input type="radio" id="focus_no" name="focus" value="no" checked>
            <label for="focus_no">No</label>
        </div>
        
        <div class="form-group">
            <label for="journal">Journal Entry</label>
            <textarea id="journal" name="journal" placeholder="Write how you're feeling today..."></textarea>
        </div>
        
        <button type="submit">Submit</button>
    </form>
    
    {% if feedback %}
    <div class="results">
        <h2>Results</h2>
        <p><strong>Feedback:</strong> {{ feedback }}</p>
        <p><strong>Recommended Color:</strong> {{ color_name }}</p>
        <div class="color-preview" style="background-color: rgb{{ rgb_values }}">
            <h3>Color Preview</h3>
            <p>RGB: {{ rgb_values }}</p>
            <p>HEX: {{ hex_color }}</p>
        </div>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    """Render the form page"""
    return render_template_string(FORM_TEMPLATE)

@app.route('/test', methods=['POST'])
def test_generate():
    """Handle form submission and generate feedback and color"""
    # Extract form data
    form_data = {
        "energy": request.form.get("energy", "5"),
        "happiness": request.form.get("happiness", "5"),
        "stress": request.form.get("stress", "5"),
        "anxiety": request.form.get("anxiety", "5"),
        "creativity": request.form.get("creativity", "5"),
        "relax": request.form.get("relax", "no"),
        "focus": request.form.get("focus", "no"),
        "journal": request.form.get("journal", "")
    }
    
    try:
        # Call the function to generate feedback and color
        feedback, color_name, rgb_values = generate_feedback_and_color(form_data)
        
        # Calculate hex color
        hex_color = f"#{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}"
        
        # Return the results
        return render_template_string(
            FORM_TEMPLATE,
            feedback=feedback,
            color_name=color_name,
            rgb_values=rgb_values,
            hex_color=hex_color
        )
    except Exception as e:
        # If there's an error, use a mock response instead
        feedback = f"Error: {str(e)}"
        color_name = "Blue"  # Default color
        rgb_values = COLOR_RGB_MAP[color_name]
        hex_color = f"#{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}"
        
        # Return the results with error message
        return render_template_string(
            FORM_TEMPLATE,
            feedback=feedback,
            color_name=color_name,
            rgb_values=rgb_values,
            hex_color=hex_color
        )

@app.route('/api/test', methods=['POST'])
def api_test():
    """JSON API endpoint for testing the function"""
    data = request.json or {}
    
    try:
        # Call the function to generate feedback and color
        feedback, color_name, rgb_values = generate_feedback_and_color(data)
        
        # Return the results as JSON
        return jsonify({
            "success": True,
            "feedback": feedback,
            "color_name": color_name,
            "rgb_values": rgb_values,
            "hex_color": f"#{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}"
        })
    except Exception as e:
        # Return error as JSON
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("\n===== Running Mood Analysis Test Server =====")
    print("Access the test form at http://127.0.0.1:5000/")
    print("Note: You need to have OPENAI_API_KEY set in your .env file for the actual API call to work")
    print("Otherwise, you will get an error message\n")
    app.run(debug=True) 