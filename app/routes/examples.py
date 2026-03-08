from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.example import Example
from app.models.progress import Progress

examples_bp = Blueprint('examples', __name__)

@examples_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_example():
    if request.method == 'POST':
        example = Example(
            quien=request.form['quien'],
            verbo=request.form['verbo'],
            que=request.form['que'],
            a_quien=request.form.get('a_quien', ''),
            complementos=request.form.get('complementos', ''),
            tipo=request.form.get('tipo', 'general'),
            user_id=current_user.id
        )
        db.session.add(example)
        
        progress = Progress.query.filter_by(user_id=current_user.id).first()
        progress.total_examples += 1
        db.session.commit()
        
        flash('Ejemplo creado', 'success')
        return redirect(url_for('examples.list_examples'))
    
    return render_template('create_example.html')

@examples_bp.route('/list')
@login_required
def list_examples():
    examples = Example.query.filter_by(user_id=current_user.id).all()
    return render_template('examples.html', examples=examples)

@examples_bp.route('/<int:example_id>')
@login_required
def view_example(example_id):
    example = Example.query.get_or_404(example_id)
    if example.user_id != current_user.id:
        flash('No tienes permiso', 'danger')
        return redirect(url_for('examples.list_examples'))
    return render_template('view_example.html', example=example)
