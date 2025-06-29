# BotR_ClimbingCompetition
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![Flask](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff)](#)
[![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white)](#)
[![HTMX](https://img.shields.io/badge/HTMX-36C?logo=htmx&logoColor=fff)](#)

# Table of Contents
- [About](#about)
- [Usage](#usage)
   - [Deployment](#deployment)
   - [Testing](#testing)
- [Todo](#todo)
- [Credits](#credits)
  
# About
This applicaiton was created to facilitate the Bonrholm on the Rocks (BotR) climbing competition of 2025.
The applicaiton is a simple flask app that recives and stores user input and stores it in an sqlite database.
This information is then used to keep track of climbers scores during the competition.
The applicaiotn also allows users to enter their name and other info. 
All of this cna then be exported at the end of the competition, to a csv file that can the be imported into a prepriotary excel macro sheet to perform the final calculations.

<p align="center">
<img src="/botr_demo.png" width="350">
</p>

# Usage
To use the applicaiton the following bash script can be run.
The script downloads the application. 
Installs required dependencies. 
Runs tests. 
And spins up the application ready for use.
The app is put in a while true loop to make sure that it will continue to run even if if it crashes. This is done to ensure no down time during a production run.

```
git clone https://github.com/0xOvid/BotR_ClimbingCompetition
cd BotR_ClimbingCompetition/

apt install python3.12-venv
python3 -m venv botr

source botr/bin/activate
pip install flask
pip install Flask-BasicAuth
pip install flask-htmx
pip install pytest
pip install requests
python -m pytest # for some reason tests fail on first run
python -m pytest
rm ./comp_exp.csv
rm ./record.log
rm ./tmptmpRoutes.csv
rm ./tmptmpUsers.csv

while true; do flask run --host=0.0.0.0 -p 80; sleep 10; done
```

## Deployment
For deployment we can just run it via screen!: 
https://devhints.io/screen

Idea: have one screen running the competition applicaiton
Have another doing backups of the database every 10 minutes and putting these in a seperate place for safe storage

```
screen -S botr
[when we want to exit we can just:]
ctrl+a and ctrl+d
screen -ls
screen -r botr
```

## Testing
to test the application run the following
```
python -m pytest
```



# TODO 

- lav en intro side hvis det er første gang folk logger ind

- find udaf deployment
- ?? when uploading new file make it so that the database deletes itself and creates a new one
- lav det så at databasen ikke bliver slettet men at den bliver rykket til en .bak fil med tidspunkt
- hosting er lid flaky - kig lige på det
- implementer state management?
- maybe setup traefik

- need to do stress testing on cloud
- also need to setup the app as a service that will just restart if it goes down

2025-05-09 - test
- Create a start competition state where databases cannot be deleted and only when in this mode or testing user ids can be updated
- opdater tekst på login page 
- måske gør så tables ikke bliver slettet men bare bliver markeret som deleted a.k.a. implementer soft delete i databasen

2025-06-26
- added stress testing w. k6
- reworked entire ui to look nicer with beercss

## .:: DONE ::.
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
2025-05-13
- uploads af filer er mærkelig og virker ikke ens hver gang
    * lav tests
    * bedre errors
    * fejlfind
    * fix
- gør admin pannel mere mobile friendly
- fix at man kun kan melde 2 slings eller der over (ikke 1)
- Der står 2 i upload filen, hvilke betyder, at der er to slynger før topankeret, Tænker det kan være en systematisk del, at du har sat top i stedet for det tal der er i upload filen. Ja det er en systematisk ting. Glæder også Borte med Blæsten”, hvor der skal være mulighed for 2-6 slynger og et t
- æåø i bruger info
- fiks æøå i uploads
2025-05-14
Setup full end to end test: where users are created, routs uploaded and competition "held" and the end results are checked
- create unittests and integration tests for everything
- TESTING - IMPLEMENTED::.
Since its a very self contained system we can create the following test:
- upload users and routes to database
    * different encoding styles
    * check the database after uploads
- login as user
    * just generate a samll database
- update user info
    * check database and maybe also competition export
- update varions competition stats
    * check exports
- change user name
    * check export
- login as another user
- do the same
    * again check the exported file
- as admin export the results
- check if everything is as expected
N/A?
- fix login issues 
- fix authentication
- Måske drop Down boks på gradering og antal dag kan minimere fejl indtastninger…. Men det er total nice-2-have
- færdiggør
2025-05-15 test:
- add 3 and + gradings to dropdown
- climbing days as dropdown 0-50
- fixed the number of slings in dropdown by doing some hacky js to remove them from the front end
- get username in export
- fixed number of slings missing last item, likely due to the face that we are removing "1" with js ... dont know ask thomas

# Credits
Mark for making everything
Thomas for ideas, and testing
