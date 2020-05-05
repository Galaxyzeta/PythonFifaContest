from django.http import HttpResponse
from django.http import HttpRequest
import pandas as pd
import math
from .utils.ResponseGenerator import ResponseFactory as rf

FIFA_DIR = "./MainApp/static/csv/fifa.csv"
# Should be READONLY
df = pd.read_csv(FIFA_DIR, encoding="utf-8")

ability = ['Crossing',
       'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling',
       'Curve', 'FKAccuracy', 'LongPassing', 'BallControl', 'Acceleration',
       'SprintSpeed', 'Agility', 'Reactions', 'Balance', 'ShotPower',
       'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression',
       'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure',
       'Marking', 'StandingTackle', 'SlidingTackle', 'GKDiving', 'GKHandling',
       'GKKicking', 'GKPositioning', 'GKReflexes']

def hello(request:HttpRequest):
    with open("./MainApp/static/html/hello.html", mode="r") as fp:
        return HttpResponse(fp.read())

def getFifaDataPage(request:HttpRequest):
    # Read params
    page = None
    record = None
    try:
        page = int(request.GET.get('page', None))
        record = int(request.GET.get('record', None))
        if page == None or record == None:
            return rf.getError("Page/Record missing!", None)
        elif page <= 0 or record <= 0:
            return rf.getError("Page/Record must be positive!", None)
    except:
        return rf.getError("Page/Record must be integer!", None)
    
    # Data extract
    maxquery = len(df)
    start = (page-1)*record
    end = page*record
    if end >= maxquery:
        return rf.getError("Query limit exceeded!", None)
    ret:pd.DataFrame = df[start:end]
    ret.drop(columns=['index'], inplace=True)
    
    # Return Jason
    jason = ret.to_json(orient="records")
    return rf.getSucessful("Query OK!", jason)


def getMaxDataPage(request:HttpRequest):
    # Read params
    record = None
    try:
        record = int(request.GET.get('record', None))
        if record == None:
            return rf.getError("Record missing!", None)
        elif record <= 0:
            rf.getError("Record must be a positive integer!", None)
    except:
        return rf.getError("Record must be a positive integer!", None)
    
    return rf.getSucessful("Query OK!", math.ceil(len(df)/record))

def importantAbilitites(request:HttpRequest):
    construct = pd.DataFrame()
    best_players:pd.DataFrame = pd.DataFrame()
    best_players['Name'] = df['Name']
    for group, features in df.groupby(by="Position")[ability].mean().iterrows():
        importantFeatures = dict(features.nlargest(5))
        construct[group] = tuple(importantFeatures.keys())
    jason = construct.to_json()
    return rf.getSucessful("Query OK!", jason)

def bestPlayers(request:HttpRequest):
    construct = pd.DataFrame()
    best_players:pd.DataFrame = pd.DataFrame()
    best_players['Name'] = df['Name']
    jason = dict()
    for group, features in df.groupby(by="Position")[ability].mean().iterrows():
        importantFeatures = dict(features.nlargest(5))
        construct[group] = tuple(importantFeatures.keys())
    for position in construct.columns:
        best_players[position] = 0
        for factor in construct[position]:
            best_players[position] += df[factor]
    for position in construct.columns:
        jason[position] = best_players[['Name', position]].sort_values(by=position, ascending=False).dropna().reset_index(drop=True).iloc[0:5,0:2].to_json(orient="records")
    return rf.getSucessful("Query OK!", jason)