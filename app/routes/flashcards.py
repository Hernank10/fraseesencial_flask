from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models.exercise_progress import ExerciseProgress
from app.models.progress import Progress
import json
import os
from datetime import datetime

flashcards_bp = Blueprint('flashcards', __name__)

def load_exercises():
    json_path = os.path.join('app', 'static', 'data', 'ejercicios.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

@flashcards_bp.route('/')
@login_required
def flashcards():
    ejercicios = load_exercises()
    ejercicios_por_dificultad = {
        'fácil': [e for e in ejercicios if e['dificultad'] == 'fácil'],
        'medio': [e for e in ejercicios if e['dificultad'] == 'medio'],
        'difícil': [e for e in ejercicios if e['dificultad'] == 'difícil']
    }
    
    completed = ExerciseProgress.query.filter_by(
        user_id=current_user.id, completed=True
    ).all()
    completed_ids = [p.exercise_id for p in completed]
    
    return render_template('flashcards.html',
                         ejercicios_por_dificultad=ejercicios_por_dificultad,
                         total_ejercicios=len(ejercicios),
                         completed_ids=completed_ids)

@flashcards_bp.route('/<int:exercise_id>')
@login_required
def view_flashcard(exercise_id):
    ejercicios = load_exercises()
    ejercicio = next((e for e in ejercicios if e['id'] == exercise_id), None)
    
    if not ejercicio:
        return redirect(url_for('flashcards.flashcards'))
    
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
        db.session.commit()
    
    return render_template('flashcard_detail.html', 
                         ejercicio=ejercicio,
                         progress=progress)
