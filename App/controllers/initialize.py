from .user import create_user
from .organizer import create_organizer
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_organizer('org', 'orgpass')
