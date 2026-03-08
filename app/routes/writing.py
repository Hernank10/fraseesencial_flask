from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.writing import Writing
from app.models.example import Example

writing_bp = Blueprint('writing', __name__)

@writing_bp.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    if request.method == 'POST':
        writing = Writing(
            title=request.form['title'],
            content=request.form['content'],
            text_type=request.form.get('text_type', 'general'),
            user_id=current_user.id
        )
        db.session.add(writing)
        db.session.commit()
        
        flash('Redacción guardada', 'success')
        return redirect(url_for('writing.list_writings'))
    
    examples = Example.query.filter_by(user_id=current_user.id).all()
    return render_template('write.html', examples=examples)

@writing_bp.route('/list')
@login_required
def list_writings():
    writings = Writing.query.filter_by(user_id=current_user.id).all()
    return render_template('writings.html', writings=writings)
