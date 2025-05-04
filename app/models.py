from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin  # Add this import

db = SQLAlchemy()

class User(db.Model, UserMixin):  # Add UserMixin inheritance
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    
    # Relationship to UploadedData
    uploads = db.relationship('UploadedData', backref='user', lazy=True)

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