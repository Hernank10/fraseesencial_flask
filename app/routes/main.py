from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.example import Example
from app.models.progress import Progress

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    examples = Example.query.filter_by(user_id=current_user.id).all()
    progress = Progress.query.filter_by(user_id=current_user.id).first()
    return render_template('dashboard.html', examples=examples, progress=progress)
