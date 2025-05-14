# Intro
This is the application for running competitions for bornholm on the rocks.
The applicaiton is scoped for a userbase of less than 100 users.
The applicaiton interface is designed for mobile use and the administarion portion is designed for laptop use only.
Its created in flask and uses templates for displaying and updating contents for the users.
Please refer to the swagger or the admin page for more info on the functioning of the app or how endpoints are layed out.
## Running the application

### Git clone
Github
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

flask run --host=0.0.0.0
```
### Deployment
For deployment we can just run it via screen!: 
https://devhints.io/screen


```
screen -S botr
[when we want to exit we can just:]
ctrl+a and ctrl+d
screen -ls
screen -r botr
```

### testing
to test the application run the following
```
python -m pytest
```



# .:: TODO ::.
- fix login issues 
- fix authentication
- lav en intro side hvis det er første gang folk logger ind

- find udaf deployment
- create unittests and integration tests for everything
- ?? when uploading new file make it so that the database deletes itself and creates a new one
- lav det så at databasen ikke bliver slettet men at den bliver rykket til en .bak fil med tidspunkt
- hosting er lid flaky - kig lige på det
- implementer state management?
- maybe setup traefik

### TESTING ::.
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



2025-05-09 - test
- Måske drop Down boks på gradering og antal dag kan minimere fejl indtastninger…. Men det er total nice-2-have



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
