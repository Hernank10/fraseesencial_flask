from flask import Blueprint, render_template, session, jsonify, request
from flask_login import login_required, current_user
from app.models.example import Example
from app.models.progress import Progress
import random

practice_bp = Blueprint('practice', __name__)

@practice_bp.route('/')
@login_required
def practice():
    examples = Example.query.filter_by(user_id=current_user.id).all()
    
    if not examples:
        return render_template('practice.html', error="Crea ejemplos primero")
    
    example = random.choice(examples)
    
    elements = [
        f"QUIÉN: {example.quien}",
        f"VERBO: {example.verbo}",
        f"QUÉ: {example.que}"
    ]
    
    if example.a_quien:
        elements.append(f"A QUIÉN: {example.a_quien}")
    
    random.shuffle(elements)
    
    correct_order = ["QUIÉN", "VERBO", "QUÉ"]
    if example.a_quien:
        correct_order.append("A QUIÉN")
    
    session['correct_order'] = correct_order
    session['current_example_id'] = example.id
    
    return render_template('practice.html', elements=elements)

@practice_bp.route('/check', methods=['POST'])
@login_required
def check():
    user_order = request.get_json().get('order', [])
    correct_order = session.get('correct_order', [])
    
    progress = Progress.query.filter_by(user_id=current_user.id).first()
    progress.exercises_completed += 1
    
    is_correct = user_order == correct_order
    
    if is_correct:
        progress.correct_answers += 1
        db.session.commit()
        return jsonify({'correct': True, 'message': '¡Correcto!'})
    else:
        db.session.commit()
        return jsonify({'correct': False, 'message': f'Incorrecto. Orden: {correct_order}'})
