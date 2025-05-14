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

def test_e2e(client):
    test_add_users(client)
    test_add_routes(client)
    # update climber info
    # check in db

    # update climber competition results
    # check rsults

    # delete files
    # clear database - check results

    
