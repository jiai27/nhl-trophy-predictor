#will paste all final code here once the rocket richard predicting pipeline is fully fine-tuned


import numpy as np
import pandas as pd
from nhlpy import NHLClient
import ast
#from notebooks.helpersrr import clear_csv, extractPlayerID, placeToStats, fetchSkaterStats, labelWinners, formatEdgeStats #--HELPER FUNCTIONS FOR FINE TUNING NOTEBOOKS AND FINAL PIPELINE--
from helpersrr import *
from sklearn.linear_model import LogisticRegression

#---GLOBAL VARS--- change these for different versions
ranks = False
client = NHLClient()
first_ids, second_ids, third_ids = [],[],[]
masterTraining, masterTesting = pd.DataFrame(), pd.DataFrame()
model = LogisticRegression(max_iter=20000, class_weight="balanced")

#---GLOBAL VARS---

#---PIPELINE FUNCTIONS--- ; reflective of the "code blocks" in the rr2.ipynb file
def predictAward(): #<- this is a function moreso for the general pipeline
    '''
    purpose:    the 'main' function of the whole of project, executes all pipeline functions
    parameters: 
    returns:    dataframe of the predictions
    '''
    global ranks

    award_chosen = input("Which award would you like to predict on?: ") #requires some input filtering
    rocketRichardAliases = ['rocket richard', 'rr', 'RR', 'Rocket Richard', 'Rocket Richard Award',]  #placeholder
    #more aliases to follow for the generalized award script
    if award_chosen in rocketRichardAliases:        
        award_chosen = "rocketrichard"
    getStandingsIds(award_chosen)       #good now
    
    topWhich = input("Would you like to predict only the winner (top 1) or the finalists (top 3)? (1/3):")
    #while topWhich != "1" or topWhich != "3":
    #    topWhich = input("ERROR, [INPUT 1 OR 3]: Would you like to predict only the winner (top 1) or the finalists (top 3)? (1/3):")
    if topWhich == "1":
        ranks = False
    else:
        ranks = True

    yearToTest = input("Which season would you like to predict on? (Format: YYYY or YYYYYYYY | Enter nothing if you'd like to predict for the current ongoing season): ")
    #NO INPUT FILTERING YET
    print(f"Predicting for {yearToTest}...")
    spliceSets(yearToTest)                        #good now
    trainModel()                                  #good now
    testModel(yearToTest)                                   #good now
    return

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

    first_ids = placeToStats(award_standings[['szn', 'winner']])
    second_ids = placeToStats(award_standings[['szn','runner_up']])
    third_ids = placeToStats(award_standings[['szn', 'finalist']])
    return

def spliceSets(testingYear="20252026", withEdge = True):
    '''
    purpose:    splits training and testing sets either w/ or w/o edge stats
    parameters: 
        testingYear (string), only to be provided if withEdge == True: 
        withEdge (boolean) if prediction wants to use EDGE stats or not
    returns:    
    '''
    global masterTesting, masterTraining
    training_sets, testing_sets = [], []
    to_drop = ['positionCode', 'lastName', 'teamAbbrevs', 'shGoals', 'shPoints']        #remove irrelevant features
    if withEdge == True:
        currentEDGEszns = []
        edgeSzns = client.edge.skater_landing(season='20252026')['seasonsWithEdgeStats']
        for szn in edgeSzns:
            currentEDGEszns.append(szn['id'])
        
        for year in currentEDGEszns:
            #print(type(year), year)
            if ranks==True:
                modifiedDf = labelWinners(year=str(year)[:4], first_ids=first_ids, second_ids=second_ids, third_ids=third_ids, rank=True, edge=True)
            else:
                modifiedDf = labelWinners(year=str(year)[:4], first_ids=first_ids, second_ids=second_ids, third_ids=third_ids, rank=False, edge=True)
            feature_set = modifiedDf.drop(columns=to_drop)
            feature_set = feature_set.dropna()
            feature_set.loc[feature_set['shootsCatches'] == "L", 'shootsCatches'] = 0    #encode L -> 0 to fit model
            feature_set.loc[feature_set['shootsCatches'] == "R", 'shootsCatches'] = 1    #encode R -> 1 to fit model
            #print(year, testingYear, type(year), type(testingYear))
            if str(year) == testingYear:     #by default, 2025-2026 is the testing year
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
    '''
    global model
    if ranks == False:
        train_x = masterTraining.drop(columns=['skaterFullName','rrWinner','playerId','seasonId'])
        train_y = masterTraining['rrWinner']
    else:
        train_x = masterTesting.drop(columns=['skaterFullName','rrRank','playerId','seasonId'])
        train_y = masterTesting['rrRank']

    #print(type(train_x), type(train_y),train_x, train_y)
    model.fit(train_x, train_y)
    return

def testModel(testing_year="20252026"):
    '''
    purpose:    test the model on a given year (in the right domain possible)
    parameters: testing_year (string) indicating the NHL season we want to test the award on
    returns:    a dataframe comparing the model prediction to the actual results
    '''
    #global masterTesting, masterTraining
    #print(masterTesting, masterTraining)
    if ranks == False:
        #print(masterTesting.columns())
        test_x = masterTesting.drop(columns=['skaterFullName','rrWinner','playerId','seasonId'])
        test_y = masterTesting['rrWinner']
    else:
        #print(masterTesting.columns())
        test_x = masterTesting.drop(columns=['skaterFullName','rrRank','playerId','seasonId'])
        test_y = masterTesting['rrRank']

    pred_y1 = model.predict(test_x)
    predictions = pd.Series(pred_y1)
    predictions = predictions.rename('predictions')
    predictions = predictions.to_frame()
    results = masterTesting.join(predictions)
    
    feature_names = test_x.columns
    coefficients = pd.Series(model.coef_[0], index=feature_names)
    print(coefficients.sort_values())

    if ranks == False:
        show = results.loc[results['predictions'] == 1]
    else:
        show = results.loc[results['predictions'] != 0.0]
        show = show.dropna()

    if ranks == False:
        print(f'---PREDICTION FOR TOP 1 RECIPIENT OF [AWARD_NAME] OF THE {testing_year} SEASON---')
        print(show['skaterFullName'], show['goals'], show['rrWinner'], show['predictions'])
    else:
        print(f'---PREDICTION FOR TOP 3 RECIPIENTS OF [AWARD_NAME] OF THE {testing_year} SEASON---')
        print(show['skaterFullName'], show['goals'], show['rrRank'], show['predictions'])

    return show

#---PIPELINE FUNCTIONS--- ; reflective of the "code blocks" in the rr2.ipynb file

#predictAward()

def main():     #testing    

    predictAward()

if __name__ == "__main__":
    main()