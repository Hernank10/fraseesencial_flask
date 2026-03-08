from app import db
from datetime import datetime

class Example(db.Model):
    __tablename__ = 'examples'
    
    id = db.Column(db.Integer, primary_key=True)
    quien = db.Column(db.String(100), nullable=False)
    verbo = db.Column(db.String(100), nullable=False)
    que = db.Column(db.String(200), nullable=False)
    a_quien = db.Column(db.String(200))
    complementos = db.Column(db.String(500))
    tipo = db.Column(db.String(50), default='general')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    writings = db.relationship('Writing', backref='source_example', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'quien': self.quien,
            'verbo': self.verbo,
            'que': self.que,
            'a_quien': self.a_quien,
            'complementos': self.complementos,
            'tipo': self.tipo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Example {self.quien} {self.verbo} {self.que}>'
