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

# Credits
Mark for making everything

Thomas for ideas, and testing
