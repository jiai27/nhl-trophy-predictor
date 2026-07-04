import numpy as np
import pandas as pd
from nhlpy import NHLClient
import ast

#Global Vars:
client = NHLClient()

def clear_csv(csv_path):
    '''
    purpose:    takes a csv, clears it and returns the csv converted to Dataframe
    parameters: csv_path (a string) indicating the csv to clear and convert
    returns:    df (pandas DataFrame)
    '''
    print(csv_path)
    df = pd.read_csv(csv_path, encoding='ascii')
    df = df.dropna()
    return df


def extractPlayerID(url):
    '''
    purpose:    parses a url and returns that player's id (used by the NHL API) 
    parameters: player url (string)
    returns:    unique player ID (string)
    '''
    #every player ID used by the NHL website and API is 7 digits long
    split = url.rsplit("-")
    return split[-1]


def placeToStats(place_list):
    '''
    purpose:    takes a list of players from the webscraped csv and returns a list of the stats of players in the list
    parameters: place_list (a pandas dataframe of tuples)
    returns:    list of player IDs
    '''
    ids = []
    seasons = place_list.iloc[:,0]
    players = place_list.iloc[:,1]
    seasons = seasons.tolist()
    players = players.tolist()

    for i in range(len(players)):
        playerTuple = ast.literal_eval(players[i])    
        if type(playerTuple) != tuple:      #working with an entry where multiple players won this award
            for entry in playerTuple:
                id = extractPlayerID(entry[0])
                ids.append((seasons[i],id))
            continue
        
        id = extractPlayerID(playerTuple[0])
        ids.append((seasons[i],id))
    return ids


def fetchSkaterStats(year, csv=False, edge = False, versionA = False):
    '''
    purpose:        fetches all summary skater stats of a given year and compresses into the desired format
    parameters:     year (string), csv (boolean)
    returns:        a dataframe OR csv of all player stats of that given year
    '''
    year_df = []

    #format year for the filter (is a string when inputted)
    if len(year) == 4:
        int_year = int(year)
        interval = (int_year,int_year+1)
        year_interval = str(interval[0]) + str(interval[1])
    elif len(year) == 8:    #20252026
        year_interval = year
    else:
        raise SyntaxError("requires yyyy or yyyyyyyy format of season year")
    
    #since there are ~900 skaters each season, must account for pagination
    #earlier testing indicates a 100 entry limit per request
    if edge == True:    #get EDGE stats
        for i in range(10):
            startMark = 100*i
            endMark = 100*(i+1)
            statChunk = pd.DataFrame(client.stats.skater_stats_summary(  #extract players in intervals of 100
                start_season=year_interval,
                end_season=year_interval,
                start=startMark,
                limit=endMark
            ))
            ids = statChunk['playerId']     #get their ids
            new_df = []
            for id in ids:
                individual_stat = client.edge.skater_detail(player_id=id, season=year_interval)
                
                if versionA == False:
                    formatted_stat = formatEdgeStats(individual_stat=individual_stat,shotDetails=True)  #get their edge stats
                else:
                    formatted_stat = formatEdgeStats(individual_stat=individual_stat,shotDetails=False)
                new_df.append(formatted_stat)
            
            df = pd.DataFrame()
            for item in new_df:
                df = pd.concat([df, item])
    
    else:       #get GSS
        for i in range(10):
            startMark = 100*i
            endMark = 100*(i+1)
            statChunk = client.stats.skater_stats_summary(
                start_season=year_interval,
                end_season=year_interval,
                start = startMark,
                limit = endMark
            )
            for record in statChunk:
                year_df.append(record)
        df = pd.DataFrame(year_df)

    if csv == True:
        if edge == True:
            df.to_csv(f'../data/api/EDGEstats/skatersEDGE{year_interval}.csv', index = False)
        else:
            df.to_csv(f'../data/api/skaters/skaters{year_interval}.csv',index=False)
    else:
        return df
    
def labelWinners(year, first_ids, second_ids, third_ids, rank=False, edge=False, versionA = False):       #modified version of labelwinners for rr2
    '''
    purpose:    fetches a dataset of skaters and adds two columns: average TOI (extra feature) and either rrWinner or rrRank (target features) 
    parameters: -year (string) of a valid RR winner year; in yyyy or yyyyyyyy format
                -first_ids (list), a list of player_ids (strings) that won the award in question 
                -second_ids (list), a list of player_ids (strings) that were runner-ups of the award in question
                -third_ids (list), a list of player_ids (strings) that were third place finalists of the award in question
                -rank (boolean) if the dev wants labels to be one-hot encoded OR ranked by top 3 finalists
                -edge (boolean) if the dev is labeling winners on the combined EDGE set
    returns:    returns a dataframe of the selected year skaters with the labeled RR winner/finalists
    '''
    #format year for the filter (is a string when inputted)
    if len(year) == 4:
        int_year = int(year)
        interval = (int_year,int_year+1)
        year_interval = str(interval[0]) + str(interval[1])
    elif len(year) == 8:    #20252026
        year_interval = year
    else:
        raise SyntaxError("requires yyyy or yyyyyyyy format of season year")
    
    if edge == True:
        csv_path = f"../data/api/EDGEstats/skatersEDGE{year_interval}.csv"
        df = pd.read_csv(csv_path)
        regularDf = fetchSkaterStats(year=year, csv=False, edge=False)     #then combine it with regular GSS
        df = regularDf.merge(df)
        print("1: ",df.columns())
        if versionA == True:
            df = df.drop(columns=[
                'Behind the Net Shots',
                        'Beyond Red Line Shots',
                        'Center Point Shots',
                        'Crease Shots',
                        'High Slot Shots',
                        'L Circle Shots',
                        'L Corner Shots',
                        'L Net Side Shots',
                        'L Point Shots',
                        'Low Slot Shots',
                        'Offensive Neutral Zone Shots',
                        'Outside L Shots',
                        'Outside R Shots',
                        'R Circle Shots',
                        'R Corner Shots',
                        'R Net Side Shots',
                        'R Point Shots'
                        ]
            )

    else:
        csv_path = f"../data/api/skaters/skaters{year_interval}.csv"
        df = pd.read_csv(csv_path)

    print("2: ",df.columns())

    #add averageTOI
    df['averageTOI'] = np.zeros(df.shape[0])
    df['averageTOI'] = (df['timeOnIcePerGame']/60)
    startYear = year_interval[:4]               #get the first year in this season's year interval

    #add rr Winner ONLY
    if rank == False:       
        df['rrWinner'] = np.zeros(df.shape[0])      #create a new column for ranking
        for entry in first_ids:
            split = entry[0].rsplit("-")
            if str(split[0]) == (startYear):
                winner = entry[1]
                break
        df.loc[df['playerId'] == int(winner), 'rrWinner'] = 1   #modify the entry directly

    #add rr finalists
    else:
        df['rrRank'] = np.zeros(df.shape[0])      #create a new column for ranking
        for first in first_ids:
            season_year = first[0]
            season_year = season_year.rsplit("-")
            season_year = season_year[0]
            if season_year == startYear:
                winner = first[1]
                df.loc[df['playerId'] == int(winner), 'rrRank'] = 1
        
        for second in second_ids:
            season_year = second[0]
            season_year = season_year.rsplit("-")
            season_year = season_year[0]
            if season_year == startYear:
                runner_up = second[1]
                df.loc[df['playerId'] == int(runner_up), 'rrRank'] = 2
            
        for third in third_ids:
            season_year = third[0]
            season_year = season_year.rsplit("-")
            season_year = season_year[0]
            if season_year == startYear:
                finalist = third[1]
                df.loc[df['playerId'] == int(finalist), 'rrRank'] = 3
    return df

def formatEdgeStats(individual_stat, shotDetails = False):
    '''
    purpose:    takes a dictionary representing a player's comprehensive EDGE stats, and format them for a better overall feature-set
    parameters: individual_stat (dictionary), shotDetails (boolean on if we want shot location details included or not)
    returns:    df (pandas DataFrame)
    '''
    playerId = individual_stat['player']['id']
    topShotSpeed = individual_stat['topShotSpeed']['metric']
    skatingSpeed = individual_stat['skatingSpeed']['speedMax']['metric']
    totalDistanceSkated = individual_stat['totalDistanceSkated']['metric']
    distanceMaxGame = individual_stat['distanceMaxGame']['metric']

    longShots = individual_stat['sogSummary'][2]['shots']
    longGoals = individual_stat['sogSummary'][2]['goals']

    midShots = individual_stat['sogSummary'][3]['shots']
    midGoals = individual_stat['sogSummary'][3]['goals']

    highShots = individual_stat['sogSummary'][1]['shots']
    highGoals = individual_stat['sogSummary'][1]['goals']

    if shotDetails == True:
        #sogDetails
        sogS=[]
        for areas in individual_stat['sogDetails']:
            areaName = areas['area']
            areaShots = areas['shots']
            sogS.append((areaName,areaShots))
    
    offensiveZonePctg = individual_stat['zoneTimeDetails']['offensiveZonePctg']
    neutralZonePctg = individual_stat['zoneTimeDetails']['neutralZonePctg']
    defensiveZonePctg = individual_stat['zoneTimeDetails']['defensiveZonePctg']
    
    cols = ['playerId','topShotSpeed','skatingSpeed','totalDistanceSkated','distanceMaxGame','longShots','longGoals','midShots','midGoals','highShots','highGoals','offensiveZonePctg','neutralZonePctg','defensiveZonePctg']
    formattedFrame = pd.DataFrame(index=[0])

    for col in cols:
        formattedFrame[col] = locals()[col]

    if shotDetails == True:
        shotDetails = [
                    'Behind the Net',
                    'Beyond Red Line',
                    'Center Point',
                    'Crease',
                    'High Slot',
                    'L Circle',
                    'L Corner',
                    'L Net Side',
                    'L Point',
                    'Low Slot',
                    'Offensive Neutral Zone',
                    'Outside L',
                    'Outside R',
                    'R Circle',
                    'R Corner',
                    'R Net Side',
                    'R Point'
                    ]
        for col in shotDetails:
            for i in range(len(sogS)):
                if sogS[i][0] == col:
                    goalItem = sogS.pop(i)
                    newName = col + " Shots"        #rename the columns
                    formattedFrame[newName] = goalItem[1]
                    break

    return formattedFrame
