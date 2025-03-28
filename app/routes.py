from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, socketio
from app.models import User, BiometricData, TrainingSession
from app.services import KarvonenCalculator
import json

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')


@main.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not user.password == password:  # En producción usar check_password_hash
        flash('Credenciales incorrectas')
        return redirect(url_for('main.index'))

    login_user(user)
    return redirect(url_for('main.dashboard'))


@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'athlete':
        biometrics = BiometricData.query.filter_by(
            athlete_id=current_user.id
        ).order_by(BiometricData.timestamp.desc()).first()

        trainings = TrainingSession.query.filter(
            TrainingSession.athlete_id == current_user.id,
            TrainingSession.date >= datetime.utcnow()
        ).order_by(TrainingSession.date.asc()).limit(3).all()

        return render_template('dashboard.html',
                               biometrics=biometrics,
                               trainings=trainings)
    else:
        athletes = User.query.filter_by(coach_id=current_user.id).all()
        return render_template('coach_dashboard.html', athletes=athletes)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/api/wearable', methods=['POST'])
def wearable_webhook():
    data = request.json

    # Validación básica
    if not data.get('athlete_id'):
        return {'status': 'error', 'message': 'Missing athlete_id'}, 400

    # Procesar datos (simplificado)
    biometric = BiometricData(
        athlete_id=data['athlete_id'],
        heart_rate=data.get('heart_rate'),
        oxygen=data.get('oxygen'),
        calories=data.get('calories'),
        steps=data.get('steps'),
        source=data.get('source', 'unknown')
    )

    db.session.add(biometric)
    db.session.commit()

    # Emitir actualización en tiempo real
    socketio.emit('biometric_update', {
        'athlete_id': data['athlete_id'],
        'heart_rate': data.get('heart_rate'),
        'oxygen': data.get('oxygen')
    })

    return {'status': 'success'}