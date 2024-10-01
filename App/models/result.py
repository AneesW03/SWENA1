from App.database import db

class Result(db.Model):
    result_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.student_id"), nullable=False)
    comp_id = db.Column(db.Integer, db.ForeignKey("competition.comp_id"), nullable=False)
    score = db.Column(db.Float, nullable=False)

    def __init__(self, student_id, comp_id, score):
        self.student_id = student_id
        self.comp_id = comp_id
        self.score = score
    
    def get_json(self):
        return{
            'student_id': self.student_id,
            'comp_id': self.comp_id,
            'score': self.score
        }