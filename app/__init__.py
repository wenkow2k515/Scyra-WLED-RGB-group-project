from flask import Flask, url_for, render_template, request, redirect, flash, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange
import json
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Create data folder if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Mock color mappings based on mood categories
MOOD_COLORS = {
    'Happy': {'color': '#FFDE5E', 'name': 'Sunshine Yellow', 
              'description': 'A bright, cheerful yellow that amplifies your positive energy.'},
    'Calm': {'color': '#5E8AFF', 'name': 'Tranquility Blue', 
             'description': 'A soothing blue that enhances your peaceful state.'},
    'Stressed': {'color': '#5EFF8A', 'name': 'Serenity Green', 
                 'description': 'A gentle green to help balance and reduce your stress.'},
    'Energetic': {'color': '#FF5E5E', 'name': 'Vibrant Red', 
                  'description': 'A stimulating red that matches your high energy.'},
    'Tired': {'color': '#C45EFF', 'name': 'Rejuvenating Purple', 
              'description': 'A soft purple to help restore your energy levels.'},
    'Sad': {'color': '#FFA05E', 'name': 'Warm Amber', 
            'description': 'A comforting amber glow to gently lift your spirits.'}
}

@app.route('/')
def home():
    return render_template('home.html', title='Home')

@app.route('/rgb')
def rgb():
    return render_template('rgb.html', title='RGB')

@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html', title='About MoodBeam')

@app.route('/presets')
def presets():
    """Render the presets page."""
    return render_template('presets.html', title='Presets')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Login attempt: {username}, {password}")  # Debugging output
        flash('Login functionality not implemented yet.', 'info')
        return redirect(url_for('login'))
    return render_template('login.html', title='Login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        # Save the new user (for now, just print it for debugging)
        print(f"New user registered: {new_username}")
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))  # Redirect to the login page

    return render_template('register.html', title='Register account')

@app.route('/account')
def account():
    return render_template('account.html', title='Account')

@app.route('/mood_survey', methods=['GET', 'POST'])
def mood_survey():
    """Render the mood survey page and process submissions."""
    if request.method == 'POST':
        # Process the survey data
        survey_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'happiness': int(request.form.get('happiness', 3)),
            'stress': int(request.form.get('stress', 3)),
            'energy': int(request.form.get('energy', 3)),
            'tiredness': int(request.form.get('tiredness', 3)),
            'calmness': int(request.form.get('calmness', 3)),
            'sadness': int(request.form.get('sadness', 3)),
            'focus': int(request.form.get('focus', 3)),
            'optimism': int(request.form.get('optimism', 3)),
            'productivity': int(request.form.get('productivity', 3)),
            'gender': request.form.get('gender', 'prefer_not_to_say')
        }
        
        # Analyze mood based on survey responses
        mood_category = analyze_mood(survey_data)
        
        # Store survey data in session for results page
        session['survey_data'] = survey_data
        session['mood_category'] = mood_category
        
        # Save the survey data to a file
        save_survey_data(survey_data, mood_category)
        
        flash('Your mood has been analyzed!', 'success')
        return redirect(url_for('mood_results'))
        
    return render_template('mood_survey.html', title='Mood Survey')

@app.route('/mood_results')
def mood_results():
    """Display personalized lighting results based on mood analysis."""
    # Get data from session
    survey_data = session.get('survey_data', {})
    mood_category = session.get('mood_category', 'Calm') # Default to Calm if no data
    
    if not survey_data:
        flash('Please complete the mood survey first.', 'info')
        return redirect(url_for('mood_survey'))
    
    # Calculate scores for display
    positivity_score = calculate_positivity_score(survey_data)
    energy_score = calculate_energy_score(survey_data)
    calmness_score = calculate_calmness_score(survey_data)
    focus_score = calculate_focus_score(survey_data)
    
    # Get color recommendation based on mood
    color_info = MOOD_COLORS.get(mood_category, MOOD_COLORS['Calm'])
    
    # Get mood description
    mood_description = get_mood_description(mood_category)
    
    # Get color psychology explanation
    color_psychology_explanation = get_color_psychology_explanation(mood_category)
    
    return render_template(
        'mood_results.html', 
        title='Your MoodBeam Results',
        mood_category=mood_category,
        mood_description=mood_description,
        positivity_score=positivity_score,
        energy_score=energy_score,
        calmness_score=calmness_score,
        focus_score=focus_score,
        recommended_color=color_info['color'],
        color_name=color_info['name'],
        color_description=color_info['description'],
        color_psychology_explanation=color_psychology_explanation
    )

@app.route('/mood_dashboard')
def mood_dashboard():
    """Display the user's mood history and analytics dashboard."""
    # Get the user's mood history
    mood_data = get_mood_history()
    
    # Calculate summary metrics
    most_common_mood = get_most_common_mood(mood_data)
    avg_positivity = get_average_metric(mood_data, 'positivity')
    avg_energy = get_average_metric(mood_data, 'energy')
    days_tracked = len(mood_data)
    
    # Get insights
    best_mood = get_best_mood(mood_data)
    best_day = get_best_day(mood_data)
    productive_mood = get_productive_mood(mood_data)
    suggested_preset = get_suggested_preset(mood_data)
    connected_factors = get_connected_factors(mood_data)
    mood_pattern = get_mood_pattern(mood_data)
    
    return render_template(
        'mood_dashboard.html',
        title='My Mood Dashboard',
        most_common_mood=most_common_mood,
        avg_positivity=avg_positivity,
        avg_energy=avg_energy,
        days_tracked=days_tracked,
        best_mood=best_mood,
        best_day=best_day,
        productive_mood=productive_mood,
        suggested_preset=suggested_preset,
        connected_factors=connected_factors,
        mood_pattern=mood_pattern
    )

# Helper functions for mood analysis
def analyze_mood(survey_data):
    """Analyze mood based on survey responses."""
    # Simple algorithm to classify mood
    happiness = survey_data['happiness']
    stress = survey_data['stress']
    energy = survey_data['energy']
    tiredness = survey_data['tiredness']
    calmness = survey_data['calmness']
    sadness = survey_data['sadness']
    
    if happiness > 4 and stress < 3:
        return 'Happy'
    elif calmness > 4 and stress < 3:
        return 'Calm'
    elif stress > 4:
        return 'Stressed'
    elif energy > 4 and tiredness < 3:
        return 'Energetic'
    elif tiredness > 4:
        return 'Tired'
    elif sadness > 4 or happiness < 2:
        return 'Sad'
    else:
        # Default to Calm if no clear category
        return 'Calm'

def save_survey_data(survey_data, mood_category):
    """Save the survey data to a file."""
    # This is a simplified version. In a real app, you'd use a database.
    data_file = 'data/mood_data.json'
    
    # Add mood category to data
    survey_data['mood_category'] = mood_category
    
    # Load existing data if it exists
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            try:
                mood_data = json.load(f)
            except json.JSONDecodeError:
                mood_data = []
    else:
        mood_data = []
    
    # Add new data
    mood_data.append(survey_data)
    
    # Save data back to file
    with open(data_file, 'w') as f:
        json.dump(mood_data, f)

def get_mood_history():
    """Get the user's mood history."""
    # This is a simplified version. In a real app, you'd query a database.
    data_file = 'data/mood_data.json'
    
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    else:
        return []

def calculate_positivity_score(survey_data):
    """Calculate a positivity score based on happiness and optimism."""
    return round((survey_data['happiness'] + survey_data['optimism']) / 2 * 20)

def calculate_energy_score(survey_data):
    """Calculate an energy score."""
    # Inverse relationship with tiredness
    energy_val = survey_data['energy']
    inverse_tiredness = 6 - survey_data['tiredness']  # 5->1, 4->2, 3->3, 2->4, 1->5
    return round((energy_val + inverse_tiredness) / 2 * 20)

def calculate_calmness_score(survey_data):
    """Calculate a calmness score."""
    calmness_val = survey_data['calmness']
    inverse_stress = 6 - survey_data['stress']  # Inverse relationship with stress
    return round((calmness_val + inverse_stress) / 2 * 20)

def calculate_focus_score(survey_data):
    """Calculate a focus score."""
    return round(survey_data['focus'] * 20)

def get_mood_description(mood_category):
    """Get a description for the user's mood."""
    descriptions = {
        'Happy': "You're feeling positive and in good spirits. This uplifted emotional state can enhance creativity and social connections.",
        'Calm': "You're experiencing a sense of tranquility and balance. This peaceful state is excellent for reflection and mindfulness.",
        'Stressed': "You're feeling pressured or overwhelmed. While this state can be challenging, recognizing it is the first step toward managing it.",
        'Energetic': "You're feeling dynamic and full of vitality. This high-energy state is great for productivity and physical activities.",
        'Tired': "You're experiencing fatigue or low energy. This state signals a need for rest and rejuvenation.",
        'Sad': "You're feeling down or melancholy. This emotional state is a natural part of life's ups and downs, and often temporary."
    }
    return descriptions.get(mood_category, "Your mood shows a mix of different emotional elements.")

def get_color_psychology_explanation(mood_category):
    """Get an explanation of the color psychology for the recommended color."""
    explanations = {
        'Happy': "Yellow is associated with joy, happiness, and optimism. It can stimulate mental activity and generate positive energy. The bright tone matches and amplifies your current positive mood state.",
        'Calm': "Blue has been shown to produce calming chemicals in the body, lowering blood pressure and heart rate. It's ideal for maintaining and enhancing your current peaceful state.",
        'Stressed': "Green is the color of balance and harmony. Research shows it can reduce anxiety and promote a sense of refreshment. This color is specifically chosen to help counterbalance your stress.",
        'Energetic': "Red is a stimulating color that can increase heart rate and energy. Since you're already energetic, this color complements your current state while providing focus for your dynamism.",
        'Tired': "Purple combines the calming stability of blue with the energy of red. Studies suggest it can stimulate creativity while providing a sense of restoration, ideal for your current low-energy state.",
        'Sad': "Amber and orange tones evoke feelings of warmth and comfort. Research in color therapy suggests these hues can gently elevate mood and promote a sense of well-being when feeling down."
    }
    return explanations.get(mood_category, "Colors have a profound effect on our psychology and can influence our emotional states in subtle but significant ways.")

# Mock functions for dashboard metrics and insights
def get_most_common_mood(mood_data):
    """Get the most common mood from the history."""
    if not mood_data:
        return "No data yet"
    
    mood_counts = {}
    for entry in mood_data:
        mood = entry.get('mood_category', 'Unknown')
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    
    # Find the mood with the highest count
    if mood_counts:
        return max(mood_counts, key=mood_counts.get)
    return "Unknown"

def get_average_metric(mood_data, metric):
    """Get the average value for a specific metric."""
    if not mood_data:
        return 50  # Default to middle value
    
    if metric == 'positivity':
        total = sum(calculate_positivity_score(entry) for entry in mood_data)
    elif metric == 'energy':
        total = sum(calculate_energy_score(entry) for entry in mood_data)
    else:
        return 50  # Default
    
    return round(total / len(mood_data))

def get_best_mood(mood_data):
    """Get the mood with the highest happiness score."""
    return "Calm"  # Mock data

def get_best_day(mood_data):
    """Get the day with the best mood."""
    return "Weekends"  # Mock data

def get_productive_mood(mood_data):
    """Get the mood associated with highest productivity."""
    return "Energetic"  # Mock data

def get_suggested_preset(mood_data):
    """Get a suggested lighting preset based on mood history."""
    return "Energizing Morning"  # Mock data

def get_connected_factors(mood_data):
    """Get insights about connected factors in mood data."""
    return "sleep quality and energy levels"  # Mock data

def get_mood_pattern(mood_data):
    """Get a pattern from the mood data."""
    return "improve in the evening hours"  # Mock data

if __name__ == '__main__':
    app.run(debug=True)