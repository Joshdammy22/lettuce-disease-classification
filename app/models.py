from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from app import db, login_manager
import logging
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    images = db.relationship('Image', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_reset_token(self, expires_sec=1800):
        secret_key = current_app.config['SECRET_KEY']
        logging.debug(f"SECRET_KEY: {secret_key}, Type: {type(secret_key)}")
        s = Serializer(secret_key)
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        secret_key = current_app.config['SECRET_KEY']
        logging.debug(f"SECRET_KEY: {secret_key}, Type: {type(secret_key)}")
        s = Serializer(secret_key)
        try:
            user_id = s.loads(token, max_age=1800)['user_id']
        except Exception as e:
            logging.error(f"Token verification error: {e}")
            return None
        return User.query.get(user_id)

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    diagnosis = db.relationship('Diagnosis', backref='image', uselist=False)

    def __repr__(self):
        return f'<Image {self.id}>'

    def __repr__(self):
        return f'<Image {self.image_id}>'

class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)  # Foreign key to images
    disease_info_id = db.Column(db.Integer, db.ForeignKey('disease_info.id'))
    diagnosis = db.Column(db.String(100), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    diagnosis_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    disease_info = db.relationship('DiseaseInfo', backref='diagnoses')
    user = db.relationship('User', backref='diagnoses')

    def __repr__(self):
        return f'<Diagnosis {self.id}>'


class DiseaseInfo(db.Model):
    __tablename__ = 'disease_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    causes = db.Column(db.Text, nullable=False)
    recommendation_text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<DiseaseInfo {self.name}>'

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnoses.id'), nullable=False)
    accuracy_feedback = db.Column(db.String(200), nullable=True)
    recommendation_feedback = db.Column(db.String(200), nullable=True)
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    diagnosis = db.relationship('Diagnosis', backref=db.backref('feedback', lazy=True))

    def __repr__(self):
        return f'<Feedback {self.id}>'