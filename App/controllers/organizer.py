from App.models import Organizer
from App.database import db

def create_organizer(username, password):
    newuser = Organizer(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_organizer_by_username(username):
    return Organizer.query.filter_by(username=username).first()

def get_organizer(id):
    return Organizer.query.get(id)

def get_all_organizers():
    return Organizer.query.all()

def get_all_organizers_json():
    users = Organizer.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_organizer(id, username):
    user = get_organizer(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None