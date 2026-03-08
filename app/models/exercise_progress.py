from app import db
from datetime import datetime

class ExerciseProgress(db.Model):
    __tablename__ = 'exercise_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    exercise_id = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    attempts = db.Column(db.Integer, default=0)
    last_attempt = db.Column(db.DateTime)
    score = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<ExerciseProgress user:{self.user_id} ex:{self.exercise_id} completed:{self.completed}>'
