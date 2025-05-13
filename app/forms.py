from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    secret_question = SelectField('Secret Question', choices=[
        ("What was your first pet's name?", "What was your first pet's name?"),
        ("In what city were you born?", "In what city were you born?"),
        ("What is your mother's maiden name?", "What is your mother's maiden name?"),
        ("What high school did you attend?", "What high school did you attend?"),
        ("What was your childhood nickname?", "What was your childhood nickname?")
    ], validators=[DataRequired()])
    secret_answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Create Account')

class PresetForm(FlaskForm):
    preset_name = StringField('Preset Name', validators=[DataRequired()])
    is_public = BooleanField('Make Public')
    submit = SubmitField('Save')

class SharePresetForm(FlaskForm):
    share_email = StringField('User Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Share')

class MoodSurveyForm(FlaskForm):
    # Original fields
    energy_level = IntegerField('Energy Level', validators=[DataRequired(), NumberRange(min=1, max=10)])
    happiness = IntegerField('Happiness', validators=[DataRequired(), NumberRange(min=1, max=10)])
    anxiety = IntegerField('Anxiety', validators=[DataRequired(), NumberRange(min=1, max=10)])
    stress = IntegerField('Stress', validators=[DataRequired(), NumberRange(min=1, max=10)])
    
    # New fields for the expanded survey
    focus = IntegerField('Focus', validators=[DataRequired(), NumberRange(min=1, max=10)])
    irritability = IntegerField('Irritability', validators=[DataRequired(), NumberRange(min=1, max=10)])
    calmness = IntegerField('Calmness', validators=[DataRequired(), NumberRange(min=1, max=10)])
    
    # For backward compatibility, keep both notes and journal fields
    notes = TextAreaField('Notes', validators=[Optional()])
    journal = TextAreaField('Journal Entry', validators=[Optional()])
    
    submit = SubmitField('Submit')