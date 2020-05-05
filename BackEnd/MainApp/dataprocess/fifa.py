import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

FIFA_DIR = "BackEnd/MainApp/static/csv/fifa.csv"

''' All Columns
'Unnamed: 0', 'ID', 'Name', 'Age', 'Photo', 'Nationality', 'Flag',
       'Overall', 'Potential', 'Club', 'Club Logo', 'Value', 'Wage', 'Special',
       'Preferred Foot', 'International Reputation', 'Weak Foot',
       'Skill Moves', 'Work Rate', 'Body Type', 'Real Face', 'Position',
       'Jersey Number', 'Joined', 'Loaned From', 'Contract Valid Until',
       'Height', 'Weight', 'LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW',
       'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM', 'RM', 'LWB', 'LDM',
       'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB', 'RB', 'Crossing',
       'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling',
       'Curve', 'FKAccuracy', 'LongPassing', 'BallControl', 'Acceleration',
       'SprintSpeed', 'Agility', 'Reactions', 'Balance', 'ShotPower',
       'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression',
       'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure',
       'Marking', 'StandingTackle', 'SlidingTackle', 'GKDiving', 'GKHandling',
       'GKKicking', 'GKPositioning', 'GKReflexes', 'Release Clause']
'''
position = ['LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW',
       'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM', 'RM', 'LWB', 'LDM',
       'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB', 'RB']

ability = ['Crossing',
       'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling',
       'Curve', 'FKAccuracy', 'LongPassing', 'BallControl', 'Acceleration',
       'SprintSpeed', 'Agility', 'Reactions', 'Balance', 'ShotPower',
       'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression',
       'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure',
       'Marking', 'StandingTackle', 'SlidingTackle', 'GKDiving', 'GKHandling',
       'GKKicking', 'GKPositioning', 'GKReflexes']


def bestPlayers():
	df = pd.read_csv(FIFA_DIR, encoding="utf-8")
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
	

def topOverall(topk=30):
	df = pd.read_csv(FIFA_DIR, encoding="utf-8")[['Name', 'Overall']]
	df.sort_values(by='Overall')
	df = df.head(topk)
	colors = [cm.inferno(x) for x in np.linspace(0, 1, topk)]
	plt.bar(df['Name'], df['Overall']-80, bottom=80, color=colors)
	plt.xticks(rotation=90)
	plt.title('Top {} Overall'.format(topk))
	plt.show()

def relationshipBetweenAgeAndAbilities():
	df = pd.read_csv(FIFA_DIR, encoding="utf-8")
	plt.scatter(df['Age'], df['Overall'])
	plt.show()

def completeDataSet(page, record):
	df = pd.read_csv(FIFA_DIR, encoding="utf-8")
	maxquery = len(df)
	start = (page-1)*record
	end = page*record
	if end >= maxquery:
		return None
	ret:pd.DataFrame = df[start:end]
	ret.drop(columns=['index'], inplace=True)
	jason = ret.to_json(orient="records")
	print(jason)
	return jason

def getMaxPages():
	df = pd.read_csv(FIFA_DIR, encoding="utf-8")
	return len(df)

if __name__ == "__main__":
	bestPlayers()