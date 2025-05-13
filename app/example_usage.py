from flask import request, render_template, redirect, url_for, flash
from app.mood_utils import generate_feedback_and_color

# Example route for handling the mood survey form submission
def example_mood_survey_route():
    """
    Example route that handles mood survey form submission and uses the 
    generate_feedback_and_color function to get personalized feedback and colors.
    
    This is just an example and should be adapted to fit your actual application structure.
    """
    if request.method == 'POST':
        # Get form data from request
        form_data = {
            "energy": request.form.get("energy"),
            "happiness": request.form.get("happiness"),
            "stress": request.form.get("stress"),
            "anxiety": request.form.get("anxiety"),
            "creativity": request.form.get("creativity"),
            "relax": request.form.get("relax"),
            "focus": request.form.get("focus"),
            "journal": request.form.get("journal")
        }
        
        try:
            # Generate personalized feedback and color recommendation
            feedback, color_name, rgb_values = generate_feedback_and_color(form_data)
            
            # Here you would typically save this data to your database
            # For example:
            # save_to_database(user_id, form_data, feedback, color_name, rgb_values)
            
            # Store feedback and color in session for display
            session = {
                'feedback': feedback,
                'color_name': color_name,
                'rgb_values': rgb_values
            }
            
            # Redirect to results page
            return redirect(url_for('mood.results'))
            
        except Exception as e:
            # Handle any errors
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for('mood.survey'))
    
    # If not POST, render the survey form
    return render_template('mood/survey.html')


# Example function to demonstrate how to incorporate the results into a template
def example_results_route():
    """
    Example route that displays the results page with the feedback and color.
    
    This is just an example and should be adapted to fit your actual application structure.
    """
    # In a real application, you might fetch this data from the database or session
    feedback = session.get('feedback', "No feedback available")
    color_name = session.get('color_name', "Blue")
    rgb_values = session.get('rgb_values', (0, 0, 255))  # Default to blue
    
    # Calculate hex color for display
    hex_color = f"#{rgb_values[0]:02x}{rgb_values[1]:02x}{rgb_values[2]:02x}"
    
    return render_template(
        'mood/results.html',
        feedback=feedback,
        color_name=color_name,
        hex_color=hex_color,
        rgb_values=rgb_values
    ) 