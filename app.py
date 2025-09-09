#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, send_file, send_from_directory
from flask_basicauth import BasicAuth
from flask_htmx import HTMX
import csv
import logging
import sqlite3
import uuid
from datetime import datetime
import hashlib
import os
import random
import string
from dataclasses import dataclass

"""
Setup flask app variables
"""
app = Flask(__name__)
htmx = HTMX(app)
basic_auth = BasicAuth(app)

"""
Setup authentication for admin user
"""
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'b3tt3r4dm1nCr3d3nt14l5!'
auth = Blueprint('auth', __name__)
# Allow hot reloading of templates
app.config['TEMPLATES_AUTO_RELOAD'] = True
"""
Setup session management
"""
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = '327d80059f70423b95f0fcae39bac6ef'

"""
Setup logging
"""
logging.basicConfig(filename='record.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""
Setup database
"""
db_file = "Sqlite3.db"

def cLog(msg, level=""):
    """
    Function for printing messages to std out and log file
    Levels: err and everything else
    """
    if level == "err":
        logger.error(msg)
    else:
        logger.info(msg)
    print(msg)

def connect_to_db():
    """
    Connect to database and return connection object
    """
    try: 
        conn = sqlite3.connect(db_file) 
        cLog("[+] Database Sqlite3.db loaded.") 
    except: 
        cLog("[!] Database Sqlite3.db not loaded.", "err")
        quit()
    return conn


def load_routes_from_csv(filename):
    """
    Take path to csv as input and parse the contents
    return array/list of list for the items
    The structure of the data should be:
    nr; area; name; grade; max_score
    I.e:
    4;Skolevæggen;Difficault;4a;5
    """
    """
    Take path to csv as input and parse the contents
    return array/list of list for the items
    The structure of the data should be:
    nr; area; name; grade; max_score
    I.e:
    4;Skolevæggen;Difficault;4a;5
    """
    cLog("[+] Loading routes from csv: " + filename)
    # Clean file by converting from nordic iso-8859 to standard UTF8 - static for now, should probabpy be done dyn>
    if os.name != 'nt':
        os.system("iconv --from-code=ISO-8859-1 --to-code=UTF-8 ./"+filename+" > ./tmp"+filename)
        os.system("cat tmp"+filename+" > "+filename)
    lines = []
    with open(filename,'r') as data:
        for line in csv.reader(data, delimiter=';'):
            lines.append(line)
    cLog("\t|- Csv parsed")
    return lines

@app.route('/')
def index():
    """
    Route for handeling the initial visit to the site
    """
    if 'logged_in' in session.keys():
        return redirect("/login")
    else:
        return redirect("/routes")

@app.route('/login')
def login():
    """
    Render login page
    """
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    """
    Handle user login, if successfull the session cookie will be set
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    if request.form.get("username") and request.form.get("password"):
        cLog(("[+] User attempting login: username", request.form.get("username"), "|| Password:", request.form.get("password")))
        h = str(request.form.get("password"))
        md5_hash = hashlib.md5()
        # Update the hash object with the input string encoded to bytes
        md5_hash.update(h.encode('utf-8'))
        user = cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (request.form.get("username"), md5_hash.hexdigest())).fetchall()
        if not user: 
            cLog("\t|- Login failed", "err")
            return redirect("/login")
        cLog("\t|- Login successfull")
        session["uuid"] = user[0][0]
        session["logged_in"] = True
        return redirect("/routes")
    # If unsuccessfull then the user is returned to the login page
    return redirect("/login")

@app.route('/logout')
def logout():
    """
    Clears session on logout
    """
    session.clear()
    return redirect("/login")

@app.route('/routes', methods=['GET', 'POST'])
def routes():
    """
    renders the main page where users can see routes, and enter their progress
    also users can enter personal information, all this is tied to the user uuid
    the uuid is set in the session on login, its created when users are added to the 
    database
    """
    # Check if key exists
    if 'logged_in' in session.keys():
        if session['logged_in'] == True:
            conn = connect_to_db()
            cursor = conn.cursor()
            
            # Get and render user info
            user_info = cursor.execute("SELECT * FROM climber_id WHERE uuid =\"" + session["uuid"] + "\"").fetchall()
            u_info = []
            for u in user_info[0]:
                u_info.append(u)

            # get all routes 
            routes = cursor.execute("SELECT * FROM routes").fetchall()
            # Get users routes in db
            # overwrite ones where user has submitted data
            # redner user infor and routes after updating
            climber_comp_routes = cursor.execute("SELECT * FROM competition WHERE uuid =\"" + session["uuid"] + "\"").fetchall()
            # transform from tuple  to list
            routes_list = []
            for r in routes:
                route_list = []
                for item in r:
                    route_list.append(item)
                routes_list.append(route_list)

            i = 0
            for r in routes_list:
                routes_list[i].append("-")
                for ur in climber_comp_routes:
                    route_uuid = r[0]
                    climber_route_uuid = ur[1]
                    if route_uuid == climber_route_uuid :
                        # route_uuid, nr, name, max_score, area, grade
                        #print("Route match, replacing: index: ", i , "| score:", ur[2] )
                        routes_list[i][6] = ur[2]
                        #print(routes_list[i])
                        continue
                        #routes[i] = routes[i] + (climber_route_uuid[2])
                    #else:
                        #routes_list[i].append("-")
                        #routes[i] = routes[i] + ("-",)
                i += 1
            return render_template('routes.html', user_info=u_info, routes=routes_list)
    return redirect("/login")

@app.route('/climber_id', methods=['POST'])
def climber_id():
    """
    Handle changes to climber info
    uses the uuid in the session to determine what to update in the 
    database.
    If the user does nto exsist then a new user is created
    """

    # Check if user exsists in database
    conn = connect_to_db()
    cursor = conn.cursor()
    # Check if contents record exsists
    user_exsist = cursor.execute("SELECT * FROM climber_id WHERE uuid = \"" + session["uuid"] + "\"").fetchall()
    if not user_exsist:
        # create user
        cLog("[+] Creating user")
        cursor.execute('''INSERT INTO climber_id (uuid, name, gender, team_name, dage_i_moselykken, max_flash) VALUES (?, ?, ?, ?, ?, ?)''', 
                                    (session["uuid"], request.form.get("navn"), request.form.get("gender"), request.form.get("team_navn"), request.form.get("dage_i_moselykken"), request.form.get("max_flash")))
        print("\t|- Commiting to database")
        # Save (commit) the changes
        conn.commit()
        # Close the connection
        conn.close()
    else:
        # create user depending on what info was entered in the 
        # web page
        cLog("[+] Updating user: "+session["uuid"])
        if request.form.get("navn"):
            print("\t|- Navn")
            cursor.execute('''UPDATE climber_id SET 
                            name = ?
                        WHERE uuid = ?''', 
                        (request.form.get("navn"), 
                        session["uuid"]))
        if request.form.get("gender"):
            cLog("\t|- Gender")
            cursor.execute('''UPDATE climber_id SET 
                            gender = ?
                        WHERE uuid = ?''', 
                        (request.form.get("gender"), 
                        session["uuid"]))
        if request.form.get("team_name"):
            cLog("\t|- team_name")
            cursor.execute('''UPDATE climber_id SET 
                            team_name = ?
                        WHERE uuid = ?''', 
                        (request.form.get("team_name"), 
                        session["uuid"]))
        if request.form.get("dage_i_moselykken"):
            cLog("\t|- dage_i_moselykken")
            cursor.execute('''UPDATE climber_id SET 
                            dage_i_moselykken = ?
                        WHERE uuid = ?''', 
                        (request.form.get("dage_i_moselykken"), 
                        session["uuid"]))
        if request.form.get("max_flash"):
            cLog("\t|- max_flash")
            cursor.execute('''UPDATE climber_id SET 
                            max_flash = ?
                        WHERE uuid = ?''', 
                        (request.form.get("max_flash"), 
                        session["uuid"]))

        cLog("\t|- Commiting to database")
        # Save (commit) the changes
        conn.commit()
        # Close the connection
        conn.close()
    # update user value
    return  '', 204

@app.route('/route_post', methods=['POST'])
def routes_post():
    """
    Handles upadtes to the routes
    updates are psoted via htmx when the users change anything
    iun the routes table
    """
    ##print(request)
    route_uuid = request.get_json()["id"]
    score = request.get_json()["score"]
    cLog("[+] Updating route:" + route_uuid + "|" + score)
    conn = connect_to_db()
    cursor = conn.cursor()
    # Update user in competition database
    #route_uuid = request.args.get('uuid')
    #score = request.form.get("row")
    # Check if contents record exsists
    record_exsists = cursor.execute("SELECT * FROM competition WHERE uuid = ? AND route_uuid = ?", 
                                    (session["uuid"], route_uuid)).fetchall()
    if not record_exsists:
        cLog("[+] Inserting into competition")
        now = datetime.now() # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        cursor.execute('''INSERT INTO competition (uuid, route_uuid, score, timestamp) VALUES (?, ?, ?, ?)''', 
                                    (session["uuid"], route_uuid, score, date_time))
    else:
        cLog("[+] Updating in competition")
        now = datetime.now() # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        cursor.execute('''UPDATE competition SET 
                            score = ?, 
                            timestamp = ?
                       WHERE uuid = ? AND route_uuid = ?''', 
                                    (score, date_time, session["uuid"], route_uuid))

    cLog("\t|- Commiting to database")
    # Save (commit) the changes
    conn.commit()
    # Close the connection
    conn.close()
    return  '', 204

def createDatabase(cursor, conn):
    """
    Creates all relevant databases for the project
    Uses IF NOT EXSISTS to avoid errors and issues
    Does not return anything
    """
    cLog("[+] Creating tables")

    cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (uuid text, username text, password text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS competition
             (uuid text, route_uuid text, score text, timestamp text)''')
    #cursor.execute('''CREATE TABLE IF NOT EXISTS routes
    #         (route_uuid text, nr, name text, max_score int, area text, grade text, factor int)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS routes
             (route_uuid text, nr, name text, max_score int, area text, grade text)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS climber_id
             (uuid text, name text, gender text, team_name text, max_flash text, dage_i_moselykken text)''')
    # Create table for factors
    cursor.execute('''CREATE TABLE IF NOT EXISTS factors
             (uuid text, category text, upper text, factor text)''')
    # Save (commit) the changes
    conn.commit()

@app.route('/admin', methods=['GET', 'POST'])
@basic_auth.required
def admin_page():
    """
    Renders the administrative page of the application
    in here the database can be managed
    users and routes can be added
    also competition results can be retrived
    """
    
    conn = connect_to_db()
    cursor = conn.cursor()
    # Check if db exsists, if not create one
    try:
        users = cursor.execute("SELECT * FROM users").fetchall()
    except:
        createDatabase(cursor, conn)
    
    users = cursor.execute("SELECT * FROM users").fetchall()
    routes = cursor.execute("SELECT * FROM routes").fetchall()
    comp = cursor.execute('''SELECT climber_id.name, routes.name, competition.score FROM competition 
                                JOIN climber_id ON climber_id.uuid = competition.uuid
                                JOIN routes ON competition.route_uuid = routes.route_uuid ''').fetchall()
    

    """
    Code here handles the different files that can be submitted to the database
    """
    if request.method == 'POST':
        """
        :: Routes :: 
        Handles when new routes are uploaded
        deletes the old table and creates a new table fo routes
        all routes are given a new uuid therefore the routes cannot be reused from
        previous uploads
        """
        try:
            if request.files['route']:
                cLog("[+] Recieved routes file")
                cLog("\t|- Saving routes file")
                uploaded_file = request.files['route']
                uploaded_file.save("tmpRoutes.csv")
                cLog("\t|- Saved as: tmpRoutes")
                cLog("\t|- Deleting exsisting routes from db")
                cursor.execute("DELETE FROM routes")
                lines = load_routes_from_csv("tmpRoutes.csv")
                cLog("\t|- Loading to db")
                for line in lines:
                    # still some issues with special chars
                    nr = line[0]
                    area = line[1] 
                    name = line[2] 
                    grade = line[3]
                    max_score = line[4]
                    try:
                        cLog(line)
                    except:
                        print("logging failed")
                    #cLog(line[1].encode("latin-1").decode("utf-8"))
                    cursor.execute('''INSERT INTO routes (route_uuid, nr, name, max_score, area, grade) VALUES (?, ?, ?, ?, ?, ?)''', 
                                (uuid.uuid4().hex, nr, name, max_score, area, grade))
                
                # Save (commit) the changes
                conn.commit()
                # Close the connection
                conn.close()
                return redirect("/admin", code=302)
        except Exception as error:
            cLog("[!] Invalid post /routes", "err")
            cLog(error, "err")
        
        """
        :: Users ::
        Handles the posting of new user records, the suer records
        just containe username and password. when these are posted 
        new users are created and exah user is given a new uuid
        """
        try:
            if request.files['users']:
                cLog("[+] Recieved users file")
                cLog("\t|- Saving users file")
                uploaded_file = request.files['users']
                uploaded_file.save("tmpUsers.csv")
                cLog("\t|- Saved as: tmpUsers")
                cLog("\t|- Deleting exsisting users from db")
                # All old users need to be deleted since the new users will have different ids
                cursor.execute("DELETE FROM users")
                lines = load_routes_from_csv("tmpUsers.csv")
                cLog("\t|- Loading to db")

                for line in lines:
                    h = str(line[1])
                    md5_hash = hashlib.md5()
                    # Update the hash object with the input string encoded to bytes
                    md5_hash.update(h.encode('utf-8'))
                    user_uuid = uuid.uuid4().hex
                    # Return the hexadecimal representation of the hash
                    try:
                        msg = "\tExecuting: INSERT INTO users (uuid, username, password) VALUES (", user_uuid, line[0], md5_hash.hexdigest(), ")"
                        cLog(msg)
                    except:
                        print("logging failed")
                    cursor.execute('''INSERT INTO users (uuid, username, password) VALUES (?, ?, ?)''', 
                                (user_uuid, line[0], md5_hash.hexdigest()))
                    # create user id - maybe we need to delete users from the comp db as well? 
                    cursor.execute('''INSERT INTO climber_id (uuid) VALUES ("''' + user_uuid + '''")''')
                
                conn.commit()
                conn.close()
                return redirect("/admin", code=302)
        except Exception as error:
            cLog("[!] Err post /users", "err")
            cLog(error, "err")
            return redirect("/admin", code=500)

    log = open("record.log").read()
    return render_template('admin.html', users=users, routes=routes, comp=comp, log=log)

# downloads
@app.route('/get_sqlite', methods=['GET'])
@basic_auth.required
def get_sqlite():
    """
    Exports the sqlite database as a single file
    """
    try:
        return send_file(db_file)
    except Exception as e:
	    return str(e)

@app.route('/get_log', methods=['GET'])
@basic_auth.required
def get_log():
    """
    Exports the log for this web app
    """
    try:
        return send_file("record.log")
    except Exception as e:
	    return str(e)

@app.route('/delete_db', methods=['GET'])
@basic_auth.required
def delete_db():
    """
    Deletes the full database, and after that creates a new one
    """
    cLog("[+] Deleting database contents")
    conn = connect_to_db()
    # Create a cursor object using the cursor() method
    cursor = conn.cursor()
    # Create tables
    cursor.execute('''DROP TABLE IF EXISTS competition''')
    cursor.execute('''DROP TABLE IF EXISTS climber_id''')
    cursor.execute('''DROP TABLE IF EXISTS routes''')
    cursor.execute('''DROP TABLE IF EXISTS users''')
    # populate routes
    conn.commit()
    createDatabase(cursor, conn)
    # Close the connection
    conn.close()
    return redirect("/admin", code=302)

@app.route('/export_results', methods=['GET'])
@basic_auth.required
def export_results():
    """
    Function exporting the competition results
    the exported results will be saved in a temporary file and the export will
    be in the following format:
    Rows: uuid, team, navn, køn, max flash, klstredage, antal ruter, rute_uuid, score, grade
    """
    cLog("[+] Exporting results as csv")
    # 
    # do one row pr route

    # get user info
    # Check if user exsists in database
    conn = connect_to_db()
    cursor = conn.cursor()
    # Check if contents record exsists
    users = cursor.execute("SELECT * FROM climber_id").fetchall()
    routes = cursor.execute("SELECT * FROM routes").fetchall()
    # create header row
    export = "uuid; brugernavn; navn; køn; team_navn; max_flash; dage_i_moselykken;"
    # add route uuid to header
    for route in routes:
        export += route[2] + "; "
    export += "\n"
    
    for user in users:
        # check if database for competition is empty, if not then continue
        
        username = str(cursor.execute("SELECT username FROM users WHERE uuid = \"" + user[0] + "\"").fetchall()[0])
        # remove: (' ',)
        username = username.replace("(", "")
        username = username.replace(")", "")
        username = username.replace("'", "")
        username = username.replace(",", "")
        # set user info
        export += str(user[0]) + "; " + username + "; " + str(user[1]) + "; " + str(user[2]) + "; " + str(user[3]) + "; " + str(user[4])  + "; " + str(user[5]) + "; "
        # go through routes and check if user has completed route
        # get all routes for user
        user_routes = cursor.execute("SELECT * FROM competition WHERE uuid = \"" + user[0] + "\"").fetchall()
        # go through all routes
        user_row = ""
        for route in routes:
            # check for routes user has done
            route_found = False
            for uRoute in user_routes:
                # user has done route
                if uRoute[1] == route[0]:
                    user_row += uRoute[2] + "; "
                    route_found = True
                    break
            if not route_found:
                user_row += "- ;"
        export += user_row + "\n"
    
    cLog("[+] Exporting competition results")
    export_filename = "comp_exp.csv"
    cLog("\t|- Deleting old files")
    if os.path.exists(export_filename):
        os.remove(export_filename)
    cLog("\t|- Writing new file")
    f = open(export_filename, "a")
    f.write(export)
    f.close()

    return  send_from_directory(".", export_filename)

@app.route('/generate_users_file', methods=['POST'])
@basic_auth.required
def generate_users_file():
    """
    Function to generate a csv with random usernames and passwords
    generates n users and pwd
    """
    export_users_file = "users_and_passwords.csv"
    str_len = 4
    usernames_and_passwords = []
    usernames = []
    cLog("[+] Generating usernames and passwords")
    cLog(("\t |- Generating n:", request.form.get("n")))
    for i in range(int(request.form.get("n"))):
        # We need to make sure that the userneme is unique
        while True:
            username = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(str_len))
            if username not in usernames:
                break
            cLog("\t |- Dublicate username found, recreating")
        usernames.append(username)
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(str_len))
        usernames_and_passwords.append(username + ";" + password)
        #print(username + ";" + password))
    cLog("[+] Exporting new users file")
    cLog("\t|- Deleting old files")
    if os.path.exists(export_users_file):
        os.remove(export_users_file)

    cLog("\t|- Writing new file")
    f = open(export_users_file, "a")
    for s in usernames_and_passwords:
        f.write(s+"\n")
    f.close()
    return send_from_directory(".", export_users_file)









"""
Revised admin page added some functionality and
put different functions in their own pages to avoid clutter
"""



@app.route('/admin/routes', methods=['GET'])
@basic_auth.required
def admin_routes_page():
    """
    Page gets all the routes in the database, also allows user
    to edit individual routes via the "route_edit.html".
    Lastly allows for adding individual routes during a competition
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    # Check if db exsists, if not create one
    try:
        users = cursor.execute("SELECT * FROM users").fetchall()
    except:
        createDatabase(cursor, conn)
    
    routes = cursor.execute("SELECT * FROM routes").fetchall()
    return render_template('admin/routes.html', routes=routes)


@app.route('/admin/routes', methods=['POST'])
@basic_auth.required
def admin_routes_add():
    """
    Function to add new routes to the database, new routes are given a unique uuid and 
    assigned the nr 0
    """
    msg = "[+] Adding new route;", request.form.values
    cLog(msg, "")
    #print(request.form.get("factor"))
    
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO routes (route_uuid, nr, name, max_score, area, grade) VALUES (?, ?, ?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "0", request.form.get("name"), request.form.get("max_score"), request.form.get("area"), request.form.get("grade"))
                    )
        
        # Save (commit) the changes
        conn.commit()
        # Close the connection
        conn.close()
    except:
        cLog("Error on insert of new route", "err")   

    return redirect("/admin/routes", code=302)

@app.route('/admin/routes/<uuid>', methods=['GET'])
@basic_auth.required
def admin_routes_edit_page(uuid):
    """
    Page allows admin to edit the specified route, uses uuid in url to know what route to get
    """
    # Get route info
    conn = connect_to_db()
    cursor = conn.cursor()
    # Check if db exsists, if not create one
    try:
        users = cursor.execute("SELECT * FROM users").fetchall()
    except:
        createDatabase(cursor, conn)
    route = cursor.execute("SELECT * FROM routes WHERE route_uuid = \"" + uuid + "\"").fetchall()

    return render_template('admin/routes_edit.html', route=route)

@app.route('/admin/routes/<uuid>', methods=['POST'])
@basic_auth.required
def admin_routes_update(uuid):
    """
    Updates route using uuid to get the right route, recives form from POST request
    """
    msg = "[+] Updating route:", uuid, "|", request.get_json()
    cLog(msg, "")

    conn = connect_to_db()
    cursor = conn.cursor()
    if request.get_json()["action"] == "delete":
        cursor.execute('''DELETE FROM routes WHERE route_uuid = \"''' + uuid + "\"")
    else: 
        cursor.execute('''UPDATE routes SET 
            name = ?,
            max_score = ?,
            area = ?,
            grade = ?,
            factor = ?
            WHERE route_uuid = ?''', 
            #(request.form.get("name"), request.form.get("max_score"), request.form.get("area"), request.form.get("grade"), uuid)
            (request.get_json()["name"], request.get_json()["max_score"], request.get_json()["area"], request.get_json()["grade"], request.get_json()["factor"], uuid)
            )
    # Save (commit) the changes
    conn.commit()
    # Close the connection
    conn.close()
    return redirect("/admin/routes", code=204)


@app.route('/admin/users', methods=['GET', 'POST'])
@basic_auth.required
def admin_users_page():
    """
    User admin page where user files can be uploaded and a user file 
    generated if needed
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    # Check if db exsists, if not create one
    try:
        users = cursor.execute("SELECT * FROM users").fetchall()
    except:
        createDatabase(cursor, conn)
    
    return render_template('admin/users.html', users=users)

@app.route('/admin/content', methods=['GET'])
@basic_auth.required
def admin_content_page():
    """
    Page for updating html on the different pages (rules and greeting message)
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    # Check if db exsists, if not create one
    try:
        users = cursor.execute("SELECT * FROM users").fetchall()
    except:
        createDatabase(cursor, conn)
    
    return render_template('admin/content.html', users=users)

@app.route('/admin/content', methods=['POST'])
@basic_auth.required
def admin_content_update():
    """
    Accepts JSON post requests {"type": "", "content": ""}
    with type being the resource to update
    and content being the content of the file to be written
    Writes file contents for other files to render.
    Vulnerable to SSTI i know, so dont run somewhere important
    """
    cLog(("[+] Updating content:", request.get_json()["type"]),"")
    with open("templates/"+request.get_json()["type"]+".html", "w") as f:
        f.write(request.get_json()["content"])
    cLog("\t|-> File written:"+request.get_json()["type"]+".html","")

    return redirect("/admin/routes", code=302)

@app.route('/admin/server', methods=['GET', 'POST'])
@basic_auth.required
def admin_server_mgmt_page():
    """
    Page for server management
    """
    return render_template('admin/server_management.html')

@app.route('/admin/log', methods=['GET', 'POST'])
@basic_auth.required
def admin_log_page():
    """
    Page for displaying server logs
    """
    log = open("record.log").read()
    return render_template('admin/log.html', log=log)

@app.route('/admin/comp_settings', methods=['GET', 'POST'])
@basic_auth.required
def admin_comp_page():
    """
    Page for displaying and allowing for changes to competition settings
    for factors of different counts
    """
    
    conn = connect_to_db()
    cursor = conn.cursor()
    # Check if contents record exsists
    factors = cursor.execute("SELECT * FROM factors").fetchall()
    
    # If factors is empty then initialize values
    if not factors:
        print("|-> Factors empty, populating with default values")
        # Antal klatredage i moselykken
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "antal_klatre_dage", "3", "1"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "antal_klatre_dage", "8", "0.98"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "antal_klatre_dage", "15", "0.96"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "antal_klatre_dage", "24", "0.94"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "antal_klatre_dage", "35", "0.92"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "antal_klatre_dage", "49", "0.90"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "antal_klatre_dage", "999", "0.88"))
        # Forskel i antal ruter klatret
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "forskel_i_ruter_klatret", "2", "1"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "forskel_i_ruter_klatret", "4", "0.95"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "forskel_i_ruter_klatret", "6", "0.9"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "forskel_i_ruter_klatret", "8", "0.85"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "forskel_i_ruter_klatret", "10", "0.8"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "forskel_i_ruter_klatret", "999", "0.7"))

        # Router under eget niveau
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "ruter_under_eget_niveau", "5", "0.14"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "ruter_under_eget_niveau", "10", "0.13"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "ruter_under_eget_niveau", "15", "0.05"))
        cursor.execute('''INSERT INTO factors (uuid, category, upper, factor) VALUES (?, ?, ?, ?)''', 
                    (uuid.uuid4().hex, "ruter_under_eget_niveau", "999", "0"))
        conn.commit()
    # get factors
    antal_klatre_dage = cursor.execute("SELECT * FROM factors WHERE category = \"antal_klatre_dage\"").fetchall()
    forskel_i_ruter_klatret = cursor.execute("SELECT * FROM factors WHERE category = \"forskel_i_ruter_klatret\"").fetchall()
    ruter_under_eget_niveau = cursor.execute("SELECT * FROM factors WHERE category = \"ruter_under_eget_niveau\"").fetchall()

    # render
    return render_template('admin/comp_settings.html', antal_klatre_dage=antal_klatre_dage, forskel_i_ruter_klatret=forskel_i_ruter_klatret, ruter_under_eget_niveau=ruter_under_eget_niveau)

@app.route('/admin/comp_settings/<id>', methods=['POST'])
@basic_auth.required
def update_comp_settings(id):
    """
    Route for updating competition factor settings
    """
    print("[+] Updating competition settings")

    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute('''UPDATE factors SET 
                    upper = ?,
                    factor = ?
                WHERE uuid = ?''', 
                (request.form.get("upper"), 
                request.form.get("factor"), 
                id))
    conn.commit()
    conn.close()
    print("\t|-> UUID:", id)
    print("\t|-> Factor:", request.form.get("factor"))
    print("\t|-> Upper:", request.form.get("upper"))

    return  '', 204


from dataclasses import dataclass
@dataclass
class Route:
    """ Class for representing routes """
    uuid: str
    name: str # Rutenavn
    nr: str # Rute tæller
    max_score: int # AntalSlynger
    area: str # Område
    grade: str # Rutegradering
    factor: int # Pointtop
    score: str 
 					


def calculate_score(uuid):
    """
    Function that calculates a given climbers score.
    The calculation is done as follows:
    1) The top "x" routes are found, here a restriction can be placed so the
    e.g. only the top 2 climbs of a certain grade is included
    2) Points are decided based on how much of the route was completed, the score is individual based on the route
     a) top = 100%
     b) above 2 quickdraws, score = 80%
     c) score = 0
    3) The above score is then timed with the constant "grade_point" and timed with the "flash score"
    grade_point =
    flash_score = 
    4) now we take the sum of eavh of the routes points as calculated above
    5) lastly this sum is timed with "visit_factor" and "noob_factor" and "team_factor" 
    team_factor = 
    """

    #cursor.execute('''INSERT INTO routes (route_uuid, nr, name, max_score, area, grade) VALUES (?, ?, ?, ?, ?, ?)''', 
    #            (uuid.uuid4().hex, nr, name, max_score, area, grade))

    """

    route_score = 0
    route_point = 0 #total score
    # If "top", rute point = 1 * gradpoint * flashpoint
    if r1.score == "top":
        route_point = 1 * r1.factor 
        route_point = r1.factor * 0.8 / r1.max_score
        print("w")
    # Elseif >= 2 (alt over 1), routepoint = 0.8 * (gradpoint/ max slynger) * resultat * flashpoint
    elif int(r1.score) >= 2:
        route_point = r1.factor * 0.8 / r1.max_score
    # Else routepoint = 0
    print(route_point)

    print(route_point * (matrix_val + 3) * f_days * f_team_diff )
    """


@app.route('/leaderboard', methods=['GET'])
@basic_auth.required
def leaderboard():
    
    return redirect("/admin")
    """
    renders the leaderboard for the competition
    """
    # Check if key exists
    if 'logged_in' in session.keys():
        if session['logged_in'] == True:
            # get user info
            # Check if user exsists in database
            conn = connect_to_db()
            cursor = conn.cursor()
            # Get all user uuids
            users = cursor.execute("SELECT uuid FROM users").fetchall()
            leaderboard = []
            # Go through each and calculate score
            i = 0
            for user in users:
                print("\t|-> Calculating result for:", user[0])
                # Getting users info
                user_info = cursor.execute("SELECT * FROM climber_id WHERE uuid = \"" + user[0] + "\"").fetchall()
                print("\t\t|- User info:", user_info)
                leaderboard.append([user_info[0][1], ""])
                flash_level = user_info[0][4]
                #grade = "7a"
                climbing_days = user_info[0][5]
                # Adjust
                team_diff = 0
                factor_coregation = 10
                total_route_score = 0
                results = cursor.execute("SELECT * FROM competition where uuid = \"" + user[0] + "\"").fetchall()
                print("\t\t|- Results[]:", results)
                # lav en sortering her efter de "x" højeste
                for r in results:
                    # The calculations below are independent from routes
                    # Route Matrix calculation
                    """
                    Each grade has a coresponding value (route kategori)
                    """
                    # get rute info
                    route = cursor.execute("SELECT * FROM routes where route_uuid = \"" + r[1] + "\"").fetchall()

                    route_category = {
                        "3g": 1,
                        "4a": 2,
                        "4b": 3,
                        "4c": 4,
                        "5a": 5,
                        "5b": 6,
                        "5c": 7,
                        "6a": 8,
                        "6a+": 9,
                        "6b": 10,
                        "6b+": 11,
                        "6c": 12,
                        "6c+": 13,
                        "7a": 14,
                        "7a+": 15,
                        "7b": 16,
                        "7b+": 17,
                        "7c": 18,
                        "7c+": 19,
                        "8a": 20,
                        "8a+": 21,
                        "8b": 22,
                        "8b+": 23,
                        "8c": 24,
                        "8c+": 25
                    }
                    matrix_val = 1 + (route_category[route[0][5]]-(route_category[flash_level]-1))/factor_coregation
                    if matrix_val <= 0:
                        matrix_val = 0.05
                    print("\t\t|-> matrix_val:", matrix_val)
                    # calc for route

                    # If "top", rute point = 1 * gradpoint * flashpoint
                    print("\t\t|- Result:", r)
                    print("\t\t|- Route:", route[0])
                    route_factor = route[0][6] 
                    route_max = route[0][3]
                    route_score = r[2]
                        
                    # Elseif >= 2 (alt over 1), routepoint = 0.8 * (gradpoint/ max slynger) * resultat * flashpoint
                    if route_score == 'None':
                        continue
                    if route_score == "Top":
                        #route_point = 1 * route_factor
                        #route_point = route_factor * 0.8 / route_max
                        route_point = route_factor * matrix_val
                    elif int(route_score) >= 2:
                        # der er noget der fucker op her!!! TODO 
                        route_point = (route_factor * 0.8 / route_max) * int(route_score)* matrix_val
                    # Else routepoint = 0
                    else:
                        route_point = 0
                    print("\t\t|- Route Points:", route_point)
                    total_route_score = total_route_score + route_point

                print("\t|-> Total score", total_route_score)
                dict_climbing_days_factors = {
                    "3": 1,
                    "8": 0.98,
                    "15": 0.96,
                    "24": 0.94,
                    "35": 0.93,
                    "49": 0.90,
                    "999": 0.88
                }
                f_days = 0
                for key in dict_climbing_days_factors:
                    if not climbing_days:
                        break
                    if int(climbing_days) <= int(key):
                        f_days = dict_climbing_days_factors[key]
                        break
                print("\t|-> f_days:", f_days)


                dict_team_diff_factors = {
                    "0": 1,
                    "3": 0.95,
                    "5": 0.9,
                    "7": 0.85,
                    "9": 0.8,
                    "11": 0.7
                }
                f_team_diff = 0
                for key in dict_team_diff_factors:
                    if int(team_diff) < int(key):
                        f_team_diff = dict_team_diff_factors[key]
                        break
                print("\t|-> Team diff factor:", f_team_diff)


                dict_routes_below_level_factors = {
                    "0": 0.14,
                    "6": 0.13,
                    "11": 0.05,
                    "15": 0,
                }
                f_routes_below = 0
                for key in dict_routes_below_level_factors:
                    if not flash_level:
                        break
                    # flash_level score = route_category[flash_level]
                    if int(route_category[flash_level]) < int(key):
                        f_routes_below = dict_routes_below_level_factors[key]
                        break
                print("\t|-> Routes below level factor:", f_routes_below)
                # iterate through results and calculate score
                # MAngler team factor
                f_korigeret_score = total_route_score * f_days * 1 * 1
                print("\t|-> Faktor korrigeret score" , f_korigeret_score)
                leaderboard[i][1]=f_korigeret_score
                # get "x" highest scores
                i += 1

            return render_template('leaderboard.html', leaderboard=leaderboard)
    return redirect("/login")


# init db on run
conn = connect_to_db()
cursor = conn.cursor()
# Check if db exsists, if not create one
try:
    users = cursor.execute("SELECT * FROM users").fetchall()
except:
    createDatabase(cursor, conn)
conn.close()


if __name__ == '__main__':
    app.run(debug=True)
