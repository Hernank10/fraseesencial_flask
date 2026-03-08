from app import db

class Progress(db.Model):
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    exercises_completed = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    total_examples = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    @property
    def success_rate(self):
        if self.exercises_completed == 0:
            return 0
        return round((self.correct_answers / self.exercises_completed) * 100, 1)
    
    def __repr__(self):
        return f'<Progress user:{self.user_id} completed:{self.exercises_completed}>'
