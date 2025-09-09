
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
 					


def calculate_score():
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

    factor_coregation = 10
    flash_level = "6c+"
    grade = "7a"
    climbing_days = "50"
    team_diff = 2

    # The calculations below are independent from routes
    # Route Matrix calculation
    """
    Each grade has a coresponding value (route kategori)
    """
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
    matrix_val = 1 + (route_category[grade]-(route_category[flash_level]-1))/factor_coregation
    if matrix_val <= 0:
        matrix_val = 0.05
    print("\t|-> matrix_val:", matrix_val)


    dict_climbing_days_factors = {
        "4": 0.98,
        "9": 0.96,
        "16": 0.94,
        "25": 0.92,
        "36": 0.90,
        "50": 0.88
    }
    f_days = 0
    for key in dict_climbing_days_factors:
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
        # flash_level score = route_category[flash_level]
        if int(route_category[flash_level]) < int(key):
            f_routes_below = dict_routes_below_level_factors[key]
            break
    print("\t|-> Routes below level factor:", f_routes_below)


    """

    route_score = 0
    route_point = 0 #total score
    if r1.score == "top":
        route_point = 1 * r1.factor 
        route_point = r1.factor * 0.8 / r1.max_score
        print("w")
    elif int(r1.score) >= 2:
        route_point = r1.factor * 0.8 / r1.max_score
    print(route_point)

    print(route_point * (matrix_val + 3) * f_days * f_team_diff )
    """


calculate_score()