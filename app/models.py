from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'athlete' or 'coach'
    name = db.Column(db.String(100))

    # Campos específicos de atleta
    birth_date = db.Column(db.Date)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    resting_hr = db.Column(db.Integer)
    max_hr = db.Column(db.Integer)

    # Relaciones
    coach_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    athletes = db.relationship('User', backref='coach', remote_side=[id])

    def __repr__(self):
        return f'<User {self.email}>'


class BiometricData(db.Model):
    __tablename__ = 'biometric_data'

    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    heart_rate = db.Column(db.Integer)
    oxygen = db.Column(db.Integer)
    calories = db.Column(db.Integer)
    steps = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    source = db.Column(db.String(50))  # polar, garmin, etc.


class TrainingSession(db.Model):
    __tablename__ = 'training_sessions'

    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50))
    duration = db.Column(db.Integer)  # en minutos
    objective = db.Column(db.String(200))
    target_hr_zone = db.Column(db.String(50))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))