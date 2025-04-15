# Intro
This is the application for running competitions for bornholm on the rocks.
The applicaiton is scoped for a userbase of less than 100 users.
The applicaiton interface is designed for mobile use and the administarion portion is designed for laptop use only.
Its created in flask and uses templates for displaying and updating contents for the users.
Please refer to the swagger or the admin page for more info on the functioning of the app or how endpoints are layed out.
## Running the application

Github
```
git clone https://github.com/0xOvid/BotR_ClimbingCompetition
cd BotR_ClimbingCompetition/

pip install virtualenv
python3 -m venv botr

source botr/bin/activate
pip install flask
pip install Flask-BasicAuth
pip install flask-htmx

flask run --host=0.0.0.0
```

Local build
```
# On the build endpoint
.\build.ps1

# On the server
unzip botr_app.zip
# setup everything 
cd botr_app

pip install virtualenv
python3 -m venv botr

source botr/bin/activate
pip install flask
pip install Flask-BasicAuth
pip install flask-htmx

flask run --host=0.0.0.0
```

# .:: TODO ::.
- fix login issues 
- fix authentication
- lav en intro side hvis det er første gang folk logger ind

- find udaf deployment
- fiks æøå i uploads
- create unittests and integration tests for everything
- ?? when uploading new file make it so that the database deletes itself and creates a new one
- lav det så at databasen ikke bliver slettet men at den bliver rykket til en .bak fil med tidspunkt
- hosting er lid flaky - kig lige på det
- implementer state management?
- maybe setup traefik

- færdiggør

- Create a start competition state where databases cannot be deleted and only when in this mode or testing user ids can be updated
- opdater tekst på login page 
- måske gør så tablkes ikke bliver slettet men bare bliver markeret som deleted a.k.a. implementer soft delete i databasen

# .:: DONE ::.
- tjek om man kan få fil download til at virke for både windows og linux
- admin siden loader ikke uden database - fiks
- fix css its a bit to small for people on mobile
- something goes wrong when users update page
    * make sure results also get updated
    * userinfo updates
- når comp results bliver eksporteret skal den lige slette den originale fil først så den ikke bare skriver oven på 
- fiks navne på kolonner i eksport
- opdater dokomentation
- lav comments og clean kode
- generate user csv
- lav en swagger for siden 
- opdater admin siden så den ser lidt nice ud
- improve logging
- deployment
    * create deployment script
    * clean deployment: remove db, delete log file
    * one for zipping and prepping the file locally
    * then uploading to digital ocean
    * pip install everything
    * start server
