from App.models import Competition
from App.database import db

def create_competition(org_id, org_name, org_description):
    newCompetition = Competition(organizer_id = org_id, name = org_name, description = org_description)
    db.session.add(newCompetition)
    db.session.commit()
    return newCompetition

def get_competition(id):
    return Competition.query.get(id)

def get_competitions_by_organizer(id):
    return Competition.query.filter_by(organizer_id = id).all()

def get_all_competitions():
    return Competition.query.all()

def get_all_competitions_json():
    competitions = Competition.query.all()
    if not competition:
        return []
    competitions = [competition.get_json() for competition in competitions]
    print(competitions)