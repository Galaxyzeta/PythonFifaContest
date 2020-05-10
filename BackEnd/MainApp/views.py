from django.http import HttpResponse
from django.http import HttpRequest
import pandas as pd
import math
from .utils.ResponseGenerator import ResponseFactory as rf
import json

FIFA_DIR = "./MainApp/static/csv/fifa.csv"
# Should be READONLY
df = pd.read_csv(FIFA_DIR, encoding="utf-8")


def resolveWage(x):
    if (x.endswith("K")):
        return x[1:-1]
    else:
        return 0

def resolveValue(x):
    if (x.endswith("M")):
        return float(x[1:-1])
    elif (x.endswith("K")):
        return float(x[1:-1])/10
    else:
        return 0

df["Wage"] = df["Wage"].apply(resolveWage)
df["Value"] = df["Value"].apply(resolveValue)
df["Value"] = df["Value"].astype("int64")

ability = ['Crossing',
           'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling',
           'Curve', 'FKAccuracy', 'LongPassing', 'BallControl', 'Acceleration',
           'SprintSpeed', 'Agility', 'Reactions', 'Balance', 'ShotPower',
           'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression',
           'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure',
           'Marking', 'StandingTackle', 'SlidingTackle', 'GKDiving', 'GKHandling',
           'GKKicking', 'GKPositioning', 'GKReflexes']


def hello(request: HttpRequest):
    with open("./MainApp/static/html/hello.html", mode="r") as fp:
        return HttpResponse(fp.read())


def getFifaDataPage(request: HttpRequest):
    # Read params
    page = None
    record = None
    # 表单验证 参数必须存在
    try:
        page = int(request.GET.get('page', None))
        record = int(request.GET.get('record', None))
        if page == None or record == None:
            return rf.getError("Page/Record missing!", None)
        elif page <= 0 or record <= 0:
            return rf.getError("Page/Record must be positive!", None)
    except:
        return rf.getError("Page/Record must be integer!", None)
    #
    # Data extract
    maxquery = len(df)
    start = (page - 1) * record
    end = page * record
    if end >= maxquery:
        end = maxquery

    ret: pd.DataFrame = df[start:end].copy(deep=True)
    ret.drop(columns=['index'], inplace=True)

    # Return Jason
    jason = ret.to_json(orient="records")
    return rf.getSucessful("Query OK!", jason)


'''
 获取数据库的最大页码，用于分页器显示最大页
'''


def getMaxDataPage(request: HttpRequest):
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

    return rf.getSucessful("Query OK!", math.ceil(len(df) / record))


def importantAbilitites(request: HttpRequest):
    construct = pd.DataFrame()
    best_players: pd.DataFrame = pd.DataFrame()
    best_players['Name'] = df['Name']
    for group, features in df.groupby(by="Position")[ability].mean().iterrows():
        importantFeatures = dict(features.nlargest(5))
        construct[group] = tuple(importantFeatures.keys())
    jason = construct.to_json()
    return rf.getSucessful("Query OK!", jason)


def bestPlayers(request: HttpRequest):
    construct = pd.DataFrame()
    best_players: pd.DataFrame = pd.DataFrame()
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
        jason[position] = best_players[['Name', position]].sort_values(by=position,
                                                                       ascending=False).dropna().reset_index(
            drop=True).iloc[0:5, 0:2].to_json(orient="records")
    return rf.getSucessful("Query OK!", jason)


'''
gk = ['GK']
fwd = ['LS', 'ST', 'RS','LF', 'CF', 'RF']
mid = ['LW','RW', 'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM', 'RM', 'LDM', 'CDM', 'RDM']
dfd = ['LWB','RWB', 'LB', 'LCB', 'CB']
'''


def bestTeam(request: HttpRequest):
    jason = json.loads(request.body)
    c_gk = ['GK']
    c_dfd = jason["back"]
    c_mid = jason["mid"]
    c_fwd = jason["front"]
    df = pd.read_csv(FIFA_DIR, encoding="utf-8")
    construct = pd.DataFrame()
    best_players: pd.DataFrame = pd.DataFrame()
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
        jason[position] = best_players[['Name', position]].sort_values(by=position,
                                                                       ascending=False).dropna().reset_index(
            drop=True).iloc[0:5, 0:2]

    choosed = {}
    # c_gk = ['GK']
    # c_dfd = ['LWB' , 'LCB' , 'RCB' , 'RWB']
    # c_mid = ['LW' , 'LCM' , 'CM' , 'RW']
    # c_fwd = ['LS' , 'RS']
    tot = [c_fwd, c_mid, c_dfd, c_gk]
    for maintype in tot:
        for pos in maintype:
            for playerId in range(len(jason[pos])):
                player = jason[pos].iloc[playerId, 0]
                if player in choosed.values():
                    continue
                else:
                    choosed[pos] = player
                    break
    return rf.getSucessful("Query OK!", choosed)


'''
 return top5 featured player  
'''


def featureRank(request: HttpRequest):
    feature = request.GET.get("feature")
    if not feature:
        return rf.getError("feature name is required", None)
    if not feature in df:
        return rf.getError("feature name is invalid", None)
    data = df.sort_values(feature, ascending=False).head(5)[
        ["Photo", "Name", "Age", "Nationality", "Position", "Overall", feature, "Real Face"]].to_json(orient="records")
    return rf.getSucessful("Query OK!", data)


def scatterPot(request: HttpRequest):
    factor1 = request.GET.get("factor1")
    factor2 = request.GET.get("factor2")
    if not factor1 or not factor2:
        return rf.getError("feature name is required", None)
    if not (factor1 in df) or not (factor2 in df):
        return rf.getError("feature name is invalid", None)
    metaColumns = ["Photo", "Name", "Age", "Nationality", "Position", "Overall", "Real Face"]
    if factor1 not in metaColumns:
        metaColumns.append(factor1)
    if factor2 not in metaColumns:
        metaColumns.append(factor2)
    data = df.sort_values('Overall', ascending=False)[metaColumns].head(500).to_json(orient="records")
    return rf.getSucessful("Query OK!", data)


# Range : a condition
# Groupby : column name ,a scatter value like country
def piePot(request: HttpRequest):
    target = request.GET.get("target")
    min = request.GET.get("min")
    groupBy = request.GET.get("groupby")
