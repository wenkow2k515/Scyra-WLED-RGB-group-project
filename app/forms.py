from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    secret_question = SelectField('Secret Question', choices=[
        ('What was your first pet\'s name?', 'What was your first pet\'s name?'),
        ('In what city were you born?', 'In what city were you born?'),
        ('What is your mother\'s maiden name?', 'What is your mother\'s maiden name?'),
        ('What high school did you attend?', 'What high school did you attend?'),
        ('What was your childhood nickname?', 'What was your childhood nickname?')
    ], validators=[DataRequired()])
    secret_answer = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField('Register')

class PresetForm(FlaskForm):
    preset_name = StringField('Preset Name', validators=[DataRequired()])
    is_public = BooleanField('Make Public')
    submit = SubmitField('Save')

class SharePresetForm(FlaskForm):
    share_email = StringField('User Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Share')

class MoodSurveyForm(FlaskForm):
    energy_level = IntegerField('Energy Level', validators=[DataRequired(), NumberRange(min=1, max=10)])
    happiness = IntegerField('Happiness', validators=[DataRequired(), NumberRange(min=1, max=10)])
    anxiety = IntegerField('Anxiety', validators=[DataRequired(), NumberRange(min=1, max=10)])
    stress = IntegerField('Stress', validators=[DataRequired(), NumberRange(min=1, max=10)])
    notes = TextAreaField('Notes')
    submit = SubmitField('Submit')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Continue')