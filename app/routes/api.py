from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models.exercise_progress import ExerciseProgress
from app.models.progress import Progress
from datetime import datetime
import json
import os

api_bp = Blueprint('api', __name__)

def load_exercises():
    json_path = os.path.join('app', 'static', 'data', 'ejercicios.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

@api_bp.route('/check-flashcard', methods=['POST'])
@login_required
def check_flashcard():
    data = request.get_json()
    exercise_id = data.get('exercise_id')
    user_order = data.get('answer')
    
    ejercicios = load_exercises()
    ejercicio = next((e for e in ejercicios if e['id'] == exercise_id), None)
    
    if not ejercicio:
        return jsonify({'error': 'Ejercicio no encontrado'}), 404
    
    progress = ExerciseProgress.query.filter_by(
        user_id=current_user.id,
        exercise_id=exercise_id
    ).first()
    
    if not progress:
        progress = ExerciseProgress(
            user_id=current_user.id,
            exercise_id=exercise_id
        )
        db.session.add(progress)
    
    progress.attempts += 1
    progress.last_attempt = datetime.utcnow()
    
    is_correct = user_order == ejercicio['orden_correcto']
    
    if is_correct and not progress.completed:
        progress.completed = True
        progress.score = 100
        
        general_progress = Progress.query.filter_by(user_id=current_user.id).first()
        general_progress.correct_answers += 1
        general_progress.exercises_completed += 1
    
    db.session.commit()
    
    return jsonify({
        'is_correct': is_correct,
        'correct_order': ejercicio['orden_correcto'],
        'explicacion': ejercicio['explicacion']
    })
