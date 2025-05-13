from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_required, current_user
from datetime import datetime

from app.models import db, MoodEntry, ColorSuggestion
from app.forms import MoodSurveyForm
from app.color_recommendation import get_color_recommendation, hex_to_rgb  # Import hex_to_rgb function
from app.mood_utils import generate_feedback_and_color, COLOR_RGB_MAP

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
    return render_template('mood/index.html', title='Mood Dashboard', mood_entries=mood_entries)

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

        # Generate AI feedback
        ai_feedback = None
        try:
            # Map form data to what the OpenAI function expects
            ai_form_data = {
                "energy": str(energy_level),
                "happiness": str(happiness),
                "stress": str(stress),
                "anxiety": str(anxiety),
                "creativity": str(focus),  # Use focus as creativity
                "relax": "yes" if calmness > 6 else "no",
                "focus": "yes" if focus > 6 else "no",
                "journal": journal_content or ""
            }
            
            # Get AI feedback
            feedback, color_name, rgb_values = generate_feedback_and_color(ai_form_data)
            ai_feedback = feedback
            
            # Store in session for display in results page
            session['ai_feedback'] = feedback
            session['ai_color_name'] = color_name
        except Exception as e:
            # Log error but continue without AI feedback
            print(f"Error generating AI feedback: {str(e)}")
            session['ai_feedback'] = None

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
            journal=journal_content,
            ai_feedback=ai_feedback  # Store the AI feedback in the database
        )
        db.session.add(mood_entry)
        db.session.commit()

        # Generate and save color suggestion using new algorithm
        color_suggestion = generate_enhanced_color_suggestion(mood_entry, ai_color_name=color_name)
        db.session.add(color_suggestion)
        db.session.commit()

        flash('Mood survey submitted successfully!', 'success')
        return redirect(url_for('mood.results', mood_entry_id=mood_entry.id))

    return render_template('mood/survey.html', title='Mood Survey', form=form)

def generate_enhanced_color_suggestion(mood_entry, ai_color_name=None):
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
    
    # Use the new color recommendation algorithm or the AI color if available
    if ai_color_name and ai_color_name in COLOR_RGB_MAP:
        # If we have a valid AI color recommendation, use it
        rgb_values = COLOR_RGB_MAP[ai_color_name]
        
        # Convert to hex without the # prefix
        primary_hex = '%02x%02x%02x' % rgb_values
        secondary_hex = primary_hex  # Use same color for simplicity
        accent_hex = primary_hex     # Use same color for simplicity
        
        # Get brightness based on energy level
        brightness = get_brightness(mood_entry.energy_level)
        
        # Create custom recommendation using AI color
        recommendation = {
            'primary_hex': primary_hex.upper(),
            'secondary_hex': secondary_hex.upper(),
            'accent_hex': accent_hex.upper(),
            'brightness': brightness
        }
    else:
        # Fall back to the regular algorithm if no AI color
        recommendation = get_color_recommendation(mood_data)
    
    # Create color suggestion - we're still storing hex in the database for compatibility
    suggestion = ColorSuggestion(
        mood_entry_id=mood_entry.id,
        primary_color=recommendation['primary_hex'],
        secondary_color=recommendation['secondary_hex'],
        accent_color=recommendation['accent_hex'],
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
    db_color_suggestion = ColorSuggestion.query.filter_by(mood_entry_id=mood_entry_id).first()
    
    # Convert hex colors to RGB format for display
    if db_color_suggestion:
        color_suggestion = db_color_suggestion.__dict__.copy()
        
        # Convert hex to RGB format
        primary_rgb = hex_to_rgb(db_color_suggestion.primary_color)
        secondary_rgb = hex_to_rgb(db_color_suggestion.secondary_color)
        accent_rgb = hex_to_rgb(db_color_suggestion.accent_color)
        
        color_suggestion['primary_color'] = f"rgb({primary_rgb[0]},{primary_rgb[1]},{primary_rgb[2]})"
        color_suggestion['secondary_color'] = f"rgb({secondary_rgb[0]},{secondary_rgb[1]},{secondary_rgb[2]})"
        color_suggestion['accent_color'] = f"rgb({accent_rgb[0]},{accent_rgb[1]},{accent_rgb[2]})"
    else:
        color_suggestion = None
    
    # Check for AI feedback - first try the database, then the session
    ai_feedback = mood_entry.ai_feedback
    ai_color_name = session.get('ai_color_name', None)
    
    # If not in database, try getting from session (for backward compatibility)
    if not ai_feedback:
        ai_feedback = session.get('ai_feedback')
        
        # If we found it in the session, save it to the database for future reference
        if ai_feedback and not mood_entry.ai_feedback:
            mood_entry.ai_feedback = ai_feedback
            db.session.commit()
            
        # Clear from session after use
        if 'ai_feedback' in session:
            session.pop('ai_feedback')
        if 'ai_color_name' in session:
            session.pop('ai_color_name')
    
    return render_template(
        'mood/results.html', 
        title='Mood Analysis Results', 
        mood_entry=mood_entry,
        color_suggestion=color_suggestion,
        ai_feedback=ai_feedback,
        ai_color_name=ai_color_name
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
    
    # Convert hex to RGB
    primary_rgb = hex_to_rgb(suggestion.primary_color)
    secondary_rgb = hex_to_rgb(suggestion.secondary_color)
    accent_rgb = hex_to_rgb(suggestion.accent_color)
    
    # Prepare the color data for the WLED controller in RGB format
    colors = {
        'primary': f"rgb({primary_rgb[0]},{primary_rgb[1]},{primary_rgb[2]})",
        'secondary': f"rgb({secondary_rgb[0]},{secondary_rgb[1]},{secondary_rgb[2]})",
        'accent': f"rgb({accent_rgb[0]},{accent_rgb[1]},{accent_rgb[2]})",
        'brightness': suggestion.brightness
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
        'mood/history.html',
        title='Mood History',
        mood_entries=mood_entries
    )

# The following route is deprecated since we've integrated AI feedback directly 
# into the regular mood survey workflow
# @mood.route('/ai-analysis', methods=['GET', 'POST'])
# @login_required
# def ai_analysis():
#     """
#     Route for AI-powered mood analysis that uses the OpenAI API 
#     to generate personalized feedback and color recommendations.
#     """
#     if request.method == 'POST':
#         # Extract form data
#         form_data = {
#             "energy": request.form.get("energy", "5"),
#             "happiness": request.form.get("happiness", "5"),
#             "stress": request.form.get("stress", "5"),
#             "anxiety": request.form.get("anxiety", "5"),
#             "creativity": request.form.get("creativity", "5"),
#             "relax": request.form.get("relax", "no"),
#             "focus": request.form.get("focus", "no"),
#             "journal": request.form.get("journal", "")
#         }
#         
#         try:
#             # Generate personalized feedback and color recommendation
#             feedback, color_name, rgb_values = generate_feedback_and_color(form_data)
#             
#             # Create a new mood entry
#             new_entry = MoodEntry(
#                 user_id=current_user.id,
#                 timestamp=datetime.now(),
#                 energy_level=int(form_data["energy"]),
#                 happiness=int(form_data["happiness"]),
#                 anxiety=int(form_data["stress"]),
#                 stress=int(form_data["anxiety"]),
#                 focus=int(form_data["creativity"]),  # Using creativity as focus
#                 irritability=5,  # Default value
#                 calmness=5,      # Default value
#                 journal=form_data["journal"]
#             )
#             
#             # Add to database
#             db.session.add(new_entry)
#             db.session.flush()  # Get the ID without committing
#             
#             # Convert RGB to hex
#             r, g, b = rgb_values
#             hex_color = f"{r:02x}{g:02x}{b:02x}".upper()
#             
#             # Create a color suggestion
#             suggestion = ColorSuggestion(
#                 mood_entry_id=new_entry.id,
#                 primary_color=hex_color,
#                 secondary_color=hex_color,  # Using same color for simplicity
#                 accent_color=hex_color,     # Using same color for simplicity
#                 brightness=get_brightness(int(form_data["energy"]))
#             )
#             
#             # Add to database
#             db.session.add(suggestion)
#             db.session.commit()
#             
#             # Store feedback in session
#             session['ai_feedback'] = feedback
#             
#             # Redirect to results page with the new entry ID
#             return redirect(url_for('mood.results', mood_entry_id=new_entry.id))
#             
#         except Exception as e:
#             # Handle any errors
#             db.session.rollback()
#             flash(f"An error occurred: {str(e)}", "error")
#             return render_template('mood/ai_survey.html')
#     
#     # GET request - show the survey form
#     return render_template('mood/ai_survey.html')