from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from app.models import db, MoodEntry, ColorSuggestion
from app.forms import MoodSurveyForm
from app.color_recommendation import get_color_recommendation  # Import the new color recommendation logic

# Create a Blueprint
mood = Blueprint('mood', __name__, url_prefix='/mood')

# Keep the old color mappings for backward compatibility
MOOD_COLOR_MAPPINGS = {
    'energetic': {'primary': 'FF5500', 'secondary': 'FFAA00', 'accent': 'FFFF00'},   # Orange/Yellow
    'calm': {'primary': '0066FF', 'secondary': '00CCFF', 'accent': 'E0F7FA'},        # Blue
    'happy': {'primary': 'FFEB3B', 'secondary': 'FFC107', 'accent': '76FF03'},       # Yellow/Green
    'sad': {'primary': '3F51B5', 'secondary': '7986CB', 'accent': 'B39DDB'},         # Purple/Blue
    'anxious': {'primary': '80DEEA', 'secondary': 'B2EBF2', 'accent': 'E0F7FA'},     # Light Blue
    'focused': {'primary': '4CAF50', 'secondary': '8BC34A', 'accent': 'CDDC39'},     # Green
    'relaxed': {'primary': '9C27B0', 'secondary': 'BA68C8', 'accent': 'E1BEE7'},     # Purple
    'tired': {'primary': '5D4037', 'secondary': '8D6E63', 'accent': 'D7CCC8'}        # Brown/Tan
}

# Brightness recommendations based on energy level
def get_brightness(energy_level):
    """Convert energy level (1-10) to brightness (0-255)"""
    # Higher energy = higher brightness
    return min(255, max(100, int(energy_level * 25.5)))

@mood.route('/')
@login_required
def index():
    """Mood analysis dashboard"""
    # Get user's mood entries (most recent first)
    mood_entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.timestamp.desc()).all()
    return render_template('index.html', title='Mood Dashboard', mood_entries=mood_entries)

@mood.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    form = MoodSurveyForm()  # Create form instance
    if form.validate_on_submit():  # Check if form is submitted and validated
        # Process form data
        energy_level = form.energy_level.data
        happiness = form.happiness.data
        anxiety = form.anxiety.data
        stress = form.stress.data
        
        # New fields
        focus = form.focus.data if hasattr(form, 'focus') and form.focus.data is not None else 5
        irritability = form.irritability.data if hasattr(form, 'irritability') and form.irritability.data is not None else 5
        calmness = form.calmness.data if hasattr(form, 'calmness') and form.calmness.data is not None else 5
        
        # Handle both journal and notes (for backward compatibility)
        journal_content = form.journal.data if hasattr(form, 'journal') and form.journal.data else form.notes.data

        # Save data to the database
        mood_entry = MoodEntry(
            user_id=current_user.id,
            energy_level=energy_level,
            happiness=happiness,
            anxiety=anxiety,
            stress=stress,
            focus=focus,
            irritability=irritability,
            calmness=calmness,
            journal=journal_content
        )
        db.session.add(mood_entry)
        db.session.commit()

        # Generate and save color suggestion using new algorithm
        color_suggestion = generate_enhanced_color_suggestion(mood_entry)
        db.session.add(color_suggestion)
        db.session.commit()

        flash('Mood survey submitted successfully!', 'success')
        return redirect(url_for('mood.results', mood_entry_id=mood_entry.id))

    return render_template('survey.html', title='Mood Survey', form=form)

def generate_enhanced_color_suggestion(mood_entry):
    """Generate color suggestion based on mood metrics using the enhanced algorithm"""
    # Prepare mood data for the recommendation algorithm
    mood_data = {
        'energy_level': mood_entry.energy_level,
        'happiness': mood_entry.happiness,
        'anxiety': mood_entry.anxiety,
        'stress': mood_entry.stress,
        'focus': mood_entry.focus,
        'irritability': mood_entry.irritability,
        'calmness': mood_entry.calmness
    }
    
    # Use the new color recommendation algorithm
    recommendation = get_color_recommendation(mood_data)
    
    # Create color suggestion
    suggestion = ColorSuggestion(
        mood_entry_id=mood_entry.id,
        primary_color=recommendation['primary_color'],
        secondary_color=recommendation['secondary_color'],
        accent_color=recommendation['accent_color'],
        effect_name=recommendation['effect_name'],
        brightness=recommendation['brightness']
    )
    
    return suggestion

# Keeping the original function for backward compatibility
def generate_color_suggestion(mood_entry):
    """Generate color suggestion based on mood metrics (original algorithm)"""
    # Determine primary mood based on highest/lowest values
    primary_mood = 'calm'  # Default
    
    # Simple algorithm to determine mood state
    if mood_entry.happiness > 7:
        if mood_entry.energy_level > 7:
            primary_mood = 'energetic'
        else:
            primary_mood = 'happy'
    elif mood_entry.happiness < 4:
        primary_mood = 'sad'
    elif mood_entry.anxiety > 7:
        primary_mood = 'anxious'
    elif mood_entry.stress > 7:
        if mood_entry.energy_level < 4:
            primary_mood = 'tired'
        else:
            primary_mood = 'anxious'
    elif mood_entry.energy_level > 7:
        primary_mood = 'energetic'
    elif mood_entry.energy_level < 4:
        primary_mood = 'tired'
    elif mood_entry.stress < 4 and mood_entry.anxiety < 4:
        primary_mood = 'relaxed'
        
    # Get color mapping for the primary mood
    colors = MOOD_COLOR_MAPPINGS.get(primary_mood, MOOD_COLOR_MAPPINGS['calm'])
    
    # Create color suggestion
    suggestion = ColorSuggestion(
        mood_entry_id=mood_entry.id,
        primary_color=colors['primary'],
        secondary_color=colors['secondary'],
        accent_color=colors['accent'],
        brightness=get_brightness(mood_entry.energy_level)
    )
    
    # Set effect based on mood
    if primary_mood in ['energetic', 'happy']:
        suggestion.effect_name = 'Rainbow'
    elif primary_mood in ['calm', 'relaxed']:
        suggestion.effect_name = 'Breath'
    elif primary_mood == 'focused':
        suggestion.effect_name = 'Solid'
    else:
        suggestion.effect_name = 'Fade'
        
    return suggestion

@mood.route('/results/<int:mood_entry_id>')
@login_required
def results(mood_entry_id):
    """Display mood analysis results and color suggestions"""
    # Get mood entry and verify ownership
    mood_entry = MoodEntry.query.get_or_404(mood_entry_id)
    if mood_entry.user_id != current_user.id:
        flash('You do not have permission to view this mood entry', 'error')
        return redirect(url_for('mood.index'))
    
    # Get the associated color suggestion
    color_suggestion = ColorSuggestion.query.filter_by(mood_entry_id=mood_entry_id).first()
    
    return render_template(
        'results.html', 
        title='Mood Analysis Results', 
        mood_entry=mood_entry,
        color_suggestion=color_suggestion
    )

@mood.route('/apply/<int:suggestion_id>', methods=['POST'])
@login_required
def apply_suggestion(suggestion_id):
    """Apply a color suggestion to the WLED controller"""
    # Get color suggestion and verify ownership
    suggestion = ColorSuggestion.query.get_or_404(suggestion_id)
    mood_entry = MoodEntry.query.get(suggestion.mood_entry_id)
    
    if mood_entry.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Permission denied'})
    
    # Mark as applied
    suggestion.was_applied = True
    suggestion.applied_at = datetime.utcnow()
    db.session.commit()
    
    # Prepare the color data for the WLED controller
    colors = {
        'primary': suggestion.primary_color,
        'secondary': suggestion.secondary_color,
        'accent': suggestion.accent_color,
        'brightness': suggestion.brightness,
        'effect': suggestion.effect_name
    }
    
    # Return the colors to be applied via JavaScript
    return jsonify({'success': True, 'colors': colors})

@mood.route('/rate/<int:suggestion_id>', methods=['POST'])
@login_required
def rate_suggestion(suggestion_id):
    """Rate a color suggestion"""
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Invalid request format'})
    
    data = request.get_json()
    rating = data.get('rating')
    
    if not rating or not isinstance(rating, int) or rating < 1 or rating > 5:
        return jsonify({'success': False, 'error': 'Invalid rating'})
    
    # Get color suggestion and verify ownership
    suggestion = ColorSuggestion.query.get_or_404(suggestion_id)
    mood_entry = MoodEntry.query.get(suggestion.mood_entry_id)
    
    if mood_entry.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Permission denied'})
    
    # Update rating
    suggestion.user_rating = rating
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Rating saved'})

@mood.route('/history')
@login_required
def history():
    """View mood history and trends"""
    # Get all mood entries for the current user
    mood_entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.timestamp.desc()).all()
    
    return render_template(
        'history.html',
        title='Mood History',
        mood_entries=mood_entries
    )