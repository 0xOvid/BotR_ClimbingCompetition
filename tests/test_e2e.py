# run tests:  python -m pytest
# https://www.digitalocean.com/community/tutorials/unit-test-in-flask

# Import sys module for modifying Python's runtime environment
import sys
# Import os module for interacting with the operating system
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask app instance from the main app file
from app import app 
# Import pytest for writing and running tests
import pytest

@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client

def test_home_redirect(client):
    """Test the home route."""
    response = client.get('/')
    assert response.status_code == 302

def test_get_login(client):
    """Test the login route"""
    response = client.get('/login')
    assert response.status_code == 200

import sqlite3
def connect_to_db():
    """
    Connect to database and return connection object
    """
    try: 
        conn = sqlite3.connect(db_file) 
    except: 
        quit()
    return conn
db_file = "Sqlite3.db"
"""
test the login page
Authorization: Basic YWRtaW46YWRtaW4= = admin:admin
"""
admin_auth_header = {
    "Authorization": "Basic YWRtaW46YWRtaW4="
}

def test_add_users(client):
    """
    Test the user uplaod function
    """
    response = client.get('/admin', headers=admin_auth_header)
    assert response.status_code == 200
    users_csv = open("./tests/testUsers.csv", 'rb')
    # Upload
    data = {"users": (users_csv, "testUsers.csv")}
    response = client.post('/admin', headers=admin_auth_header, data=data, content_type="multipart/form-data")
    assert response.status_code == 302
    # check uplaod status in db
 
    conn = connect_to_db()
    cursor = conn.cursor()
    # Check if db exsists, if not create one
    users = cursor.execute("SELECT * FROM users").fetchall()

    assert users[0][1] == "aaa" # username
    assert users[0][2] == "47bce5c74f589f4867dbd57e9ca9f808" #password
    assert users[2][1] == "ccc" # username
    assert users[2][2] == "9df62e693988eb4e1e1444ece0578579" #password
    users_csv.close()

def test_add_routes(client):    
    """
    Test the routes uplaod function
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    # Route csv - uses file with wierd formating
    route_csv = open("./tests/testRoutes.csv", 'rb')
    # Upload
    routeData = {"route": (route_csv, "testRoutes.csv")}
    response = client.post('/admin', headers=admin_auth_header, data=routeData, content_type="multipart/form-data")
    assert response.status_code == 302
    # Check db status
    routes = cursor.execute("SELECT * FROM routes").fetchall()
    assert routes[5][2] == "The Nose"
    assert routes[5][3] == 4
    assert routes[5][4] == "Elkapitan"

    assert routes[17][2] == "Gaia Love"
    assert routes[17][3] == 7
    assert routes[17][4] == "Store gumbas"
    
    route_csv.close()
    
# stress test
import requests
import os
import subprocess
import re
from dataclasses import dataclass

@dataclass
class Climber:
    """ Class representing climber and their info"""
    username: str
    password: str
    name: str
    teamName: str
    maxFlash: str
    days: str
    gender: str


def climber_update_and_comp_post(climber):
    with requests.Session() as session:
        conn = connect_to_db()
        cursor = conn.cursor()
        # login
        res = session.post(
            url="http://127.0.0.1:5000/login",
            data={"username": climber.username,
                  "password": climber.password}
            )
        # An authorised request.
        res = session.get('http://127.0.0.1:5000/routes')
        # check that we are successfully logged in
        assert res.status_code == 200
        # update climber info
        # name
        res = session.post(
            url="http://127.0.0.1:5000/climber_id",
            data={"navn": climber.name,
                  "gender": "None"}
            )
        # team name
        res = session.post(
            url="http://127.0.0.1:5000/climber_id",
            data={"team_name": climber.teamName}
            )
        # max flash
        res = session.post(
            url="http://127.0.0.1:5000/climber_id",
            data={"max_flash": climber.maxFlash}
            )
        # climbing days
        res = session.post(
            url="http://127.0.0.1:5000/climber_id",
            data={"dage_i_moselykken": climber.days}
            )
        # gender
        res = session.post(
            url="http://127.0.0.1:5000/climber_id",
            data={"gender": climber.gender}
            )
        # check in db
        climber_info = cursor.execute("SELECT * FROM climber_id WHERE name = \""+ climber.name+"\"").fetchall()
        assert climber_info[0][1] == climber.name
        assert climber_info[0][2] == climber.gender
        assert climber_info[0][3] == climber.teamName
        assert climber_info[0][4] == climber.maxFlash
        assert climber_info[0][5] == climber.days
        # update climber competition results
        # get route uuids
        res = session.get('http://127.0.0.1:5000/routes')
        routeUuids = re.findall("""id\=\"([a-zA-Z0-9]{32})""", res.text)

        res = session.post(
            url="http://127.0.0.1:5000/route_post?uuid="+routeUuids[0],
            data={"row": "Top"}
            )
        res = session.post(
            url="http://127.0.0.1:5000/route_post?uuid="+routeUuids[1],
            data={"row": "2"}
            )
        res = session.post(
            url="http://127.0.0.1:5000/route_post?uuid="+routeUuids[2],
            data={"row": "2"}
            )
        res = session.post(
            url="http://127.0.0.1:5000/route_post?uuid="+routeUuids[3],
            data={"row": "Top"}
            )

def test_e2e(client):
    flaskServer = subprocess.Popen(["flask","run"])
    # test for first climber
    # move to function and define the climber as a dataclass and then pass that to the test function
    testClimberA = Climber(
        username = "aaa",
        password = "aaa",
        name = "testAaa",
        teamName= "teamAaa",
        maxFlash = "9a",
        days = "32",
        gender = "M"
    )
    climber_update_and_comp_post(testClimberA)
    testClimberB= Climber(
        username = "bbb",
        password = "bbb",
        name = "testBbb",
        teamName= "teamBbb",
        maxFlash = "1a",
        days = "322",
        gender = "K"
    )
    climber_update_and_comp_post(testClimberB)
    # export results and check if correct
    expectedResultsA = "testAaa; M; teamAaa; 9a; 32; Top; 2; 2; Top; - ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;\n"
    expectedResultsB = "testBbb; K; teamBbb; 1a; 322; Top; 2; 2; Top; - ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;- ;\n"

    response = client.get('/export_results', headers=admin_auth_header)
    # check rsults
    with open('comp_exp.csv', 'r') as fin:
        data = fin.read().splitlines(True)

    assert data[1][34+5:] == expectedResultsA
    assert data[2][34+5:] == expectedResultsB

    flaskServer.terminate()

    # delete files
    os.remove("Sqlite3.db")
    os.remove("tmpRoutes.csv")
    os.remove("tmpUsers.csv")

    
