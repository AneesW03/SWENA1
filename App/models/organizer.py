from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Organizer(db.Model):
    organizer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    results = db.relationship('Competition', backref=db.backref('organizer'), lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
    
    def get_json(self):
        return{
            'organizer_id': self.organizer_id,
            'username': self.username
        }
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)