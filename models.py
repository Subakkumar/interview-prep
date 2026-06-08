from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Problem(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty  = db.Column(db.String(20))   # easy / medium / hard
    category    = db.Column(db.String(50))   # arrays, dp, graphs, etc.
    examples    = db.Column(db.Text)         # JSON
    test_cases  = db.Column(db.Text)         # JSON
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':          self.id,
            'title':       self.title,
            'description': self.description,
            'difficulty':  self.difficulty,
            'category':    self.category,
            'examples':    json.loads(self.examples)   if self.examples   else [],
            'test_cases':  json.loads(self.test_cases) if self.test_cases else [],
        }

class Attempt(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))
    code       = db.Column(db.Text)
    language   = db.Column(db.String(20), default='python')
    passed     = db.Column(db.Boolean, default=False)
    score      = db.Column(db.Integer, default=0)   # 0-100
    feedback   = db.Column(db.Text)
    hints_used = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':         self.id,
            'problem_id': self.problem_id,
            'code':       self.code,
            'language':   self.language,
            'passed':     self.passed,
            'score':      self.score,
            'feedback':   self.feedback,
            'hints_used': self.hints_used,
            'created_at': self.created_at.isoformat()
        }