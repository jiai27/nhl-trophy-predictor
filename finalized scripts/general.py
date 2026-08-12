'''
author: jiai27
description:
    this script will be relatively similar to rocketrichard.py, but instead of committing a general file to each award, 
    only this script will be ran to predict for different awards
'''

#---DEPENDENCIES---
import numpy as np
import pandas as pd
from nhlpy import NHLClient
from helpers import *       #HELPER FUNCTIONS FOR THE WHOLE PIPELINE

#models -- will require more as more award predictor models are developed, tested and added
from sklearn.linear_model import LogisticRegression
#---DEPENDENCIES---


#---GLOBAL VARS--- change these for different versions
ranks = False
client = NHLClient()
first_ids, second_ids, third_ids = [],[],[]
masterTraining, masterTesting = pd.DataFrame(), pd.DataFrame()
model = LogisticRegression(max_iter=30000, class_weight="balanced")     #baseline model for all awards (the most optimal version of the Rocket Richard Predictor)
displayAward = 'Maurice "Rocket" Richard Trophy'

#---GLOBAL VARS---

#---PIPELINE FUNCTIONS--- ; reflective of the "code blocks" in the rr2.ipynb file
def predictAward(): #<- this is a function moreso for the general pipeline
    '''
    purpose:    the 'main' function of the whole of project, executes all pipeline functions
    parameters: None
    returns:    None, prints the predictions in the console
    '''
    global ranks, displayAward

    award_chosen = input("Which award would you like to predict on?: ")                              #requires some input filtering
    rocketRichardAliases = ['rocket richard', 'rr', 'RR', 'Rocket Richard', 'Rocket Richard Award']  #placeholder
    artRossAliases = ['art','art ross', 'ar', 'Art', 'Ross', 'Art Ross', 'Art Ross Trophy', 'art Ross Trophy', 'Art ross Trophy', 'art ross Trophy', 'art ross trophy']
    vezinaAliases = ['vezina', 'vez', 'Vezina', 'Vezina trophy', 'vezina trophy', 'Vezina Trophy']
    hartAliases = ['hart trophy', 'hart', 'Hart', 'hart Trophy', 'Hart trophy', 'Hart Trophy', 'Hart Memorial Trophy']
    selkeAliases = ['selke', 'Selke', 'Selke Trophy', 'selke Trophy', 'selke Trophy', 'Frank J. Selke Trophy']
    norrisAliases = ['norris', 'Norris', 'Norris Trophy', 'Norris trophy', 'norris trophy', 'norris Trophy', 'james norris memorial trophy', 'James Norris Memorial Trophy']
    '''
        MORE ALIASES TO FOLLOW WHEN MORE AWARDS ARE ADDED
    '''
    if award_chosen in rocketRichardAliases:        
        award_chosen = "rocketrichard"                          #for locating the file in data/formattedwebscraped
        displayAward = 'Maurice "Rocket" Richard Trophy'        #for display
    elif award_chosen in artRossAliases:
        award_chosen = 'artrosstrophy'        
        displayAward = 'Art Ross Trophy'
    elif award_chosen in vezinaAliases:
        award_chosen = 'vezina trophy'
        displayAward = 'Vezina Trophy'
    elif award_chosen in hartAliases:
        award_chosen = 'hart memorial trophy'
        displayAward = 'Hart Memorial Trophy'
    elif award_chosen in selkeAliases:
        award_chosen = 'frank j. selke trophy'
        displayAward = 'Frank J. Selke Trophy'
    elif award_chosen in norrisAliases:
        award_chosen = 'james norris memorial trophy'
        displayAward = 'James Norris Memorial Trophy'

    else:
        
        raise SyntaxError("ERROR. Award not found. Try a different keyword?")

    getStandingsIds(award_chosen)       #good now
    
    #if award_chosen == 'vezina trophy':
    #    print(first_ids)
    #    print(second_ids)
    #    print(third_ids)
    

    print(f"Award Selected: {displayAward}")
    
    topWhich = input("Would you like to predict only the winner (top 1) or the finalists (top 3)? (1/3):")
    #while topWhich != "1" or topWhich != "3":
    #    topWhich = input("ERROR, [INPUT 1 OR 3]: Would you like to predict only the winner (top 1) or the finalists (top 3)? (1/3):")
    if topWhich == "1":
        ranks = False
    else:
        ranks = True

    yearToTest = input("Which season would you like to predict on? (Format: YYYY or YYYYYYYY | Enter nothing if you'd like to predict for the current ongoing/most recent season): ")
    if len(yearToTest) == 4 and 2021 <= int(yearToTest) <= 2026:    #ensures we can only predict on EDGE seasons
        second_year = int(yearToTest) + 1
        yearToTest = yearToTest + str(second_year)

    if yearToTest == "":
        latestYear = client.edge.skater_landing(season='20252026')['seasonsWithEdgeStats'][-1]['id']    #fetch the latest updated year in the API
        yearToTest = latestYear

    if ranks == True:
        print(f"Predicting Top 3 Recipients for the {yearToTest} NHL Season...")
    else:
        print(f"Predicting Winner for the {yearToTest} NHL Season...")

    if award_chosen == 'vezina trophy':
        spliceSets(yearToTest, vezina = True)
        trainModel()
        testModel(yearToTest)

    else:
        spliceSets(yearToTest)                        #good now
        trainModel()                                  #good now
        testModel(yearToTest)                         #good now
    
def getStandingsIds(award_name):
    '''
    purpose:    updates the global variables for the file: first_ids, second_ids, third_ids
    parameters: award_name (string) indicating the award the user wants to predict on
    returns:    None ; instead modifies the global variables: first_ids, second_ids, third_ids
    '''
    global first_ids, second_ids, third_ids
    filepath = f"../data/formattedwebscraped"
    award_path = filepath + f'/{award_name}.csv'
    award_standings = clear_csv(award_path)                            #requires prior preprocessing of the user's input; said preprocessing can occur in predictAward

    if displayAward == 'Maurice "Rocket" Richard Trophy':
        first_ids = placeToStats(award_standings[['szn', 'winner']], mode="rocketrichard")
        second_ids = placeToStats(award_standings[['szn','runner_up']], mode="rocketrichard")
        third_ids = placeToStats(award_standings[['szn', 'finalist']], mode="rocketrichard")
    else:       #for now, this is for most other awards since they are not formatted the same way the rocket richard csv is formatted
        first_ids = placeToStats(award_standings[['szn', 'winner']])
        second_ids = placeToStats(award_standings[['szn','runner_up']])
        third_ids = placeToStats(award_standings[['szn', 'finalist']])

    return

def spliceSets(testingYear=client.edge.skater_landing(season='20252026')['seasonsWithEdgeStats'][-1]['id'], withEdge = True, vezina = False):
    '''
    purpose:    splits training and testing sets either w/ or w/o edge stats
    parameters: 
        testingYear (string), only to be provided if withEdge == True: 
        withEdge (boolean) if prediction wants to use EDGE stats or not
    returns:    
    '''
    #print(testingYear, type(testingYear))
    global masterTesting, masterTraining
    training_sets, testing_sets = [], []
    to_drop = ['positionCode', 'lastName', 'teamAbbrevs', 'shGoals', 'shPoints']        #remove irrelevant features
    if withEdge == True:
        currentEDGEszns = []
        edgeSzns = client.edge.skater_landing(season='20252026')['seasonsWithEdgeStats']
        for szn in edgeSzns:
            currentEDGEszns.append(szn['id'])
        
        for year in currentEDGEszns:
            if vezina == False:
                if ranks==True:
                    modifiedDf = labelWinners(year=str(year)[:4], first_ids=first_ids, second_ids=second_ids, third_ids=third_ids, rank=True, edge=True,vezina=False)
                else:
                    modifiedDf = labelWinners(year=str(year)[:4], first_ids=first_ids, second_ids=second_ids, third_ids=third_ids, rank=False, edge=True,vezina=False)
            else:
                if ranks==True:
                    modifiedDf = labelWinners(year=str(year)[:4], first_ids=first_ids, second_ids=second_ids, third_ids=third_ids, rank=True, edge=True, vezina=True)
                else:
                    modifiedDf = labelWinners(year=str(year)[:4], first_ids=first_ids, second_ids=second_ids, third_ids=third_ids, rank=False, edge=True, vezina=True)
          
            for column in to_drop:
                if column in modifiedDf.columns:
                    modifiedDf = modifiedDf.drop(columns=column)
                    #print("dropping ",column)
            feature_set = modifiedDf
            #(f"before dropna for {year}", feature_set.shape)
            #print(feature_set.loc[feature_set.isna().any(axis=1)])
            if vezina == False:
                feature_set = feature_set.dropna()
            else:
                feature_set = feature_set.fillna(0)     #set all NaNs to 0
            feature_set.loc[feature_set['shootsCatches'] == "L", 'shootsCatches'] = 0    #encode L -> 0 to fit model
            feature_set.loc[feature_set['shootsCatches'] == "R", 'shootsCatches'] = 1    #encode R -> 1 to fit model
            #print(f"after dropna for {year}: ",feature_set.shape)
            #print(feature_set.loc[feature_set['rrRank'] != 0])
            if str(year) == str(testingYear):    
                testing_sets.append(feature_set)
            else:
                training_sets.append(feature_set)

        for train in training_sets:
            masterTraining = pd.concat([masterTraining, train])
        for test in testing_sets:
            masterTesting = pd.concat([masterTesting, test])
    #else:          --implement later for non-EDGE seasons ?
    #    pass   

    return      #don't need to return masterTraining/Testing because already global
    
def trainModel():
    '''
    purpose:    trains the model according to the selected 'baseline' / optimal model I have selected
    parameters: None
    returns:    None
    note:       the 'model' global variable changes depending on the award selected, may have to come back here and adapt for that change later
    '''
    #print(masterTraining['rrRank'].shape)
    global model
    if ranks == False:
        to_drop = ['skaterFullName','rrWinner','playerId','seasonId', 'goalieFullName']
        train_y = masterTraining['rrWinner']
    else:
        to_drop = ['skaterFullName','rrRank','playerId','seasonId', 'goalieFullName']
        train_y = masterTraining['rrRank']

    train_x = masterTraining

    for column in to_drop:
        if column in train_x.columns:
            train_x = train_x.drop(columns=column)

    #print(train_x, train_y, train_y.loc[train_y != 0])
    #print(train_x.shape, train_x.columns)
    #print(train_x.shape, train_y.shape)

    model.fit(train_x, train_y)
    return

def testModel(testing_year=client.edge.skater_landing(season='20252026')['seasonsWithEdgeStats'][-1]['id']):
    '''
    purpose:    test the model on a given year (in the right domain possible)
    parameters: testing_year (string) indicating the NHL season we want to test the award on
    returns:    a dataframe comparing the model prediction to the actual results
    '''
    if ranks == False:
        to_drop = ['skaterFullName','rrWinner','playerId','seasonId', 'goalieFullName']
        #test_y = masterTesting['rrWinner']
        
    else:
        to_drop=['skaterFullName','rrRank','playerId','seasonId','goalieFullName']
        #test_y = masterTesting['rrRank']

    test_x = masterTesting
    for column in to_drop:
        if column in test_x.columns:
            test_x = test_x.drop(columns=column)

    pred_y1 = model.predict(test_x)
    predictions = pd.Series(pred_y1)
    predictions = predictions.rename('predictions')
    predictions = predictions.to_frame()
    results = masterTesting.join(predictions)
    
    feature_names = test_x.columns
    coefficients = pd.Series(model.coef_[0], index=feature_names)
    print("---STATISTIC WEIGHTS---")
    print(coefficients.sort_values())

    if ranks == False:
        show = results.loc[results['predictions'] == 1]
    else:
        show = results.loc[results['predictions'] != 0.0]
        show = show.dropna()

    if ranks == False:      
        print(f'---PREDICTION FOR TOP 1 RECIPIENT OF {displayAward} OF THE {testing_year} SEASON---')
        if displayAward != "Vezina Trophy":
            print(show['skaterFullName'], show['goals'], show['rrWinner'], show['predictions'])                 #OUTPUTS HERE ARE BOUND TO CHANGE, ITS JUST GOALS AS A PLACEHOLDER FOR RR BUT WILL SHOW EVERYTHING IN THE FULL UI
        else:
            print(show['goalieFullName'], show['goals'], show['rrWinner'], show['predictions'])       
        print(f'---PREDICTION FOR TOP 1 RECIPIENT OF {displayAward} OF THE {testing_year} SEASON---')
    else:
        print(f'---PREDICTION FOR TOP 3 RECIPIENTS OF {displayAward} OF THE {testing_year} SEASON---')
        if displayAward != "Vezina Trophy":
            print(show['skaterFullName'], show['goals'], show['rrRank'], show['predictions'])
        else: 
            print(show['goalieFullName'], show['goals'], show['rrRank'], show['predictions'])
        print(f'---PREDICTION FOR TOP 3 RECIPIENTS OF {displayAward} OF THE {testing_year} SEASON---')

    return show


#---PIPELINE FUNCTIONS--- ; reflective of the "code blocks" in the rr2.ipynb file

predictAward()
