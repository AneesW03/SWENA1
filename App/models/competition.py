from App.database import db

class Competition(db.Model):
    comp_id = db.Column(db.Integer, primary_key=True)
    organizer_id = db.Column(db.Integer, db.ForeignKey("organizer.organizer_id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    results = db.relationship('Result', backref=db.backref('competition'), lazy=True)

    def __init__(self, organizer_id, name, description):
        self.organizer_id = organizer_id
        self.name = name
        self.description = description

    def get_json(self):
        return{
            'comp_id:': self.comp_id,
            'name': self.name,
            "description": self.description
        }