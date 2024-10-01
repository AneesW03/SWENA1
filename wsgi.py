import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User,Result,Competition,Organizer
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, get_all_competitions, get_user_by_username, get_student_results, create_organizer, create_competition, get_organizer_by_username, get_competitions_by_organizer, 
get_competition_results, import_results, get_all_competitions, get_all_organizers_json)


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('student', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a student (flask student create <username> <password>)")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')
#flask student create <username> <password>

@user_cli.command("list", help="Lists students in the database")
@click.argument("format", default="string")
def list_user_command(format):
    print(get_all_users_json())
#flask student list

@user_cli.command("viewCompetitions", help="View all Competitions")
def viewAllCompetitions():
    competitions = get_all_competitions()
    for competition in competitions:
        print(competition.get_json())
# flask student viewCompetitions

@user_cli.command("viewResults", help="View Student's results in all competitions (flask student viewResults <username>)")
@click.argument("username", default="rob")
def viewStudentResults(username):
    user = get_user_by_username(username)
    results = get_student_results(user.student_id)
    for result in results:
        print(result.get_json())
# flask student viewResults <username>

@user_cli.command("viewCompetitionResults", help="View single competition results (flask student viewCompetitionResults <competition_id>)")
@click.argument("comp_id", default="1")
def viewStudentResults(comp_id):
    results = get_competition_results(comp_id)
    for result in results:
        print(result.get_json())
# flask student viewCompetitionResults <competition_id>

app.cli.add_command(user_cli) # add the group to the cli



organizer_cli = AppGroup('organizer', help='Organizer object commands')

@organizer_cli.command("create", help="Creates a organizer")
@click.argument("username", default="org")
@click.argument("password", default="orgpass")
def create_user_command(username, password):
    create_organizer(username, password)
    print(f'{username} created!')
#flask organizer create <username> <password>     //working

@organizer_cli.command("list", help="Lists organizers in the database")
@click.argument("format", default="string")
def list_user_command(format):
    print(get_all_organizers_json())
#flask student list                                                                 //working

@organizer_cli.command("createCompetition", help="Creates a competition (flask organizer createCompetition <username> <CompetitionName> <description>)")
@click.argument("username", default="org")
@click.argument("name", default="myCompetition")
@click.argument("description", default="defaultDescription")
def createCompetition(username, name, description):
    organizer = get_organizer_by_username(username)
    create_competition(organizer.organizer_id, name, description)
    print("Created Successfully")
#flask organizer createCompetition <username> <competitionName> <description>       //working

@organizer_cli.command("viewCompetitions", help="View Organizations's Competitions (flask organizer viewCompetitions <username>)")
@click.argument("username", default="org")
def viewCompetitionsOrganizer(username):
    organizer = get_organizer_by_username(username)
    competitions = get_competitions_by_organizer(organizer.organizer_id)
    for competition in competitions:
        print(competition.get_json())
#flask organizer viewCompetitions <username>                                        //working

@organizer_cli.command("viewCompetitionResults", help="View Organization's Competition Results (flask organizer viewCompetitionResults <username>)")
@click.argument("username", default="org")
def viewOrganizerCompetitions(username):
    organizer = get_organizer_by_username(username)
    competitions = get_competitions_by_organizer(organizer.organizer_id)
    for competition in competitions:
        results = get_competition_results(competition.comp_id)
        for result in results:
            print(result.get_json())
# flask organizer viewCompetitionResults <username>                                //working

@organizer_cli.command("importResults", help="Import Results from CSV (flask organizer importResults <competition_id> <filePath>)")
@click.argument("comp_id", default="1")
@click.argument("file", default="./App/controllers/scores.csv")
def importResults(comp_id, file):
    import_results(comp_id, file)
# flask organizer importResults <comp_id>                                           //working

app.cli.add_command(organizer_cli)



'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
