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
wget -O - https://raw.githubusercontent.com/0xOvid/BotR_ClimbingCompetition/refs/heads/main/make.sh | sh
```

The above runs the make.sh script which in turn runs the flask application with "screen". 

## Resterting the App
if the app needs restartign, terminate the screen session. Then go to the directory and use the follwoing comamnd to get everything running again:

```
screen -dm bash -c "
source botr/bin/activate
# Run in production
while true; do flask run --host=0.0.0.0 -p 80; sleep 10; done"
```



## Testing
to test the application run the following
```
python -m pytest
```



# TODO 
- lav en intro side hvis det er første gang folk logger ind
- lav det så at databasen ikke bliver slettet men at den bliver rykket til en .bak fil med tidspunkt
- implementer state management?
- maybe setup traefik

# TODO: 2025-08-03
- Add propper initialization script for initial seutp and testing

- figure out calculations for score in the app
- create structured logging - and maybe have it stored in the database
- Create leaderboard

- Create lock for database when competition in is swing
- Migrate do admin page v2.0


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

2025-05-09 - test
- Create a start competition state where databases cannot be deleted and only when in this mode or testing user ids can be updated
- opdater tekst på login page 
- måske gør så tables ikke bliver slettet men bare bliver markeret som deleted a.k.a. implementer soft delete i databasen

2025-06-26
- added stress testing w. k6
- reworked entire ui to look nicer with beercss

2025-08-08
- Can now add new routes while running without deleting stuffs
- Can now update routes
- Can write content, login and content pages
- Can now create and update content of rules and welcome message from admin dashboard
- Modals for user routes now shows when an error arose
- add cancle to edit routes
- add delete to edit routes
- log page added

2025-09-05
- got competition factors page setup and working, now needs to register updates
- got updating on settings working

2025-09-06
- Started on the calculation page for testing the settings

2025-09-08
- Got a PoC of calculations working, needs more testing

2025-09-16
- continued work on leaderboard and got PoC working, now waiting for check by thomas
- added the route factors to be displayed in admin pannel
- still needs testing and verification


2025-12-16
- rework look of users, nav, base
- update admin/users to use new route
- move add user functionality to seperate function
- users updated and validated
- nav look updated

2025-12-19
- routes page done
- now supports deleting all routes from db with warning, 
adding individual ones, editing these have also been tested, 
deleting has been tested.
- started some work on the other pages
- added functionality to clear log file from browser
- server management now working
- content addition now working
- added defaults to greetings and rule contents when empty

2025-12-20
- updated editing for individual routes
- fixed comp settings
- now factors get added to the database
- fixed some encoding errors in the content saving
- can now change the name of the contest in the content pannel
- almost close to testing ready
- added +1 to route points so it alligns with how thomas likes to do it



# Credits
Mark for making everything

Thomas for ideas, and testing
