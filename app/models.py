from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
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
    user = db.relationship('User', backref=db.backref('uploads', lazy=True))  # relationship to User

class SharedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # shared data id
    shared_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # user who shared
    shared_with_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # user who received
    preset_id = db.Column(db.Integer, db.ForeignKey('uploaded_data.id'), nullable=False)  # shared preset
    shared_by = db.relationship('User', foreign_keys=[shared_by_id], backref=db.backref('shared_by', lazy=True))  # relationship for sharer
    shared_with = db.relationship('User', foreign_keys=[shared_with_id], backref=db.backref('shared_with', lazy=True))  # relationship for receiver
    preset = db.relationship('UploadedData', backref=db.backref('shared_presets', lazy=True))  # relationship to UploadedData