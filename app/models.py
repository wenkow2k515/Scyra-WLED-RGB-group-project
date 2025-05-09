from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    secret_question = db.Column(db.String(200), nullable=True)
    secret_answer = db.Column(db.String(200), nullable=True)
    
    # Relationship to UploadedData
    uploads = db.relationship('UploadedData', backref='user', lazy=True)
    # Relationship to MoodEntry (will be properly linked after MoodEntry is defined)
    mood_entries = db.relationship('MoodEntry', backref='user', lazy=True)

class UploadedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # uploaded data id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # reference to User
    preset_name = db.Column(db.String(100), nullable=False)  # preset name
    preset_data = db.Column(db.JSON, nullable=False)  # preset data stored as JSON
    is_public = db.Column(db.Boolean, default=False)  # New field

    # Add a getter/setter if your database doesn't support JSON natively
    @property
    def preset_data_json(self):
        """Return the preset data as a dict."""
        if isinstance(self.preset_data, str):
            return json.loads(self.preset_data)
        return self.preset_data

class SharedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # shared data id
    shared_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # user who shared
    shared_with_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # user who received
    preset_id = db.Column(db.Integer, db.ForeignKey('uploaded_data.id'), nullable=False)  # shared preset
    shared_by = db.relationship('User', foreign_keys=[shared_by_id], backref=db.backref('shared_by', lazy=True))  # relationship for sharer
    shared_with = db.relationship('User', foreign_keys=[shared_with_id], backref=db.backref('shared_data_received', lazy=True))                     
    preset = db.relationship('UploadedData', foreign_keys=[preset_id], backref=db.backref('shared_instances', lazy=True))

# New models for Mood Analysis
class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Mood metrics (scale of 1-10)
    energy_level = db.Column(db.Integer, nullable=False)
    happiness = db.Column(db.Integer, nullable=False)
    anxiety = db.Column(db.Integer, nullable=False)
    stress = db.Column(db.Integer, nullable=False)
    
    # Optional notes
    notes = db.Column(db.Text)
    
    # Relationship to ColorSuggestion
    color_suggestion = db.relationship('ColorSuggestion', backref='mood_entry', uselist=False, lazy=True)
    
    def __repr__(self):
        return f"MoodEntry(id={self.id}, user_id={self.user_id}, timestamp={self.timestamp})"


class ColorSuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood_entry_id = db.Column(db.Integer, db.ForeignKey('mood_entry.id'), nullable=False)
    
    # Colors (RGB values)
    primary_color = db.Column(db.String(6), nullable=False)  # Hex without #
    secondary_color = db.Column(db.String(6), nullable=True)
    accent_color = db.Column(db.String(6), nullable=True)
    
    # Lighting pattern recommendation
    effect_name = db.Column(db.String(50), nullable=True)
    brightness = db.Column(db.Integer, nullable=False, default=255)  # 0-255
    
    # Whether the suggestion was applied to WLED
    was_applied = db.Column(db.Boolean, default=False)
    
    # Optional feedback from user on the suggestion (1-5 stars)
    user_rating = db.Column(db.Integer, nullable=True)
    
    # Timestamp when applied
    applied_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f"ColorSuggestion(id={self.id}, mood_entry_id={self.mood_entry_id}, colors=[{self.primary_color},{self.secondary_color},{self.accent_color}])"