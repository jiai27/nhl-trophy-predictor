## This document will contain all notes about the commit it is apart of and ONLY that commit

### General Notes from the last couple weeks:
- Since this project intends to use ongoing stats during the season, statistical awards like Art Ross, Rocket Richard and Jennings recipients are determined by their respective statistic and thus are technically predetermined as opposed to predicting a player; but until the season is finished, these awards are still treated as a regular award that needs prediction
- Every active NHL player with >=1 games played is eligible - maybe find a way to filter this down to a handful of players to avoid fluff | 
- Certain awards are restricted to positions and age groups (like Vezina only for goalies and Calder for Rookies)

## Decisions/Comments regarding the Rocket Richard Predictor Development:
- rr.ipynb is a testing environment
- rr1.ipynb is also a testing environment but with more direction and just to build the first pipeline baseline predictor
- in rr1.ipynb:
    - players have two sets of statistics that can be fetched: General Skater Statistics denoted GSS for simplicity (#points, #goals, penalty mins, etc) and EDGE stats (skating speed, shot speed, high danger analysis, very hyperspecific statistics), for now, the feature sets ONLY use the GSS and no EDGE stats, I plan to train on two sets of feature sets per award:
        1. GSS only
        2. GSS and EDGE Stats
    to deduce whether or not EDGE stats are actually worth incorporating or not. It's a lot more data to be trained on which could lower performance with and increase resources needed to make predictions, so I find this comparison to be quite important moving forward.
    I should also note in addition to the 'rrWinner' label I added into the feature set, I also added 'averageTOI' (average time on ice) as an additional maybe useful feature.
    - the 'shootsCatches' column is encoded to: 0 = left shooting, 1 = right shooting so the model can fit properly for logistic regression
    
    - The typical dataset for all skaters in one season has records for roughly ~950-1050 players, but a good chunk of these players in the dataset may be on long term injury, AHL callups for a small period of time, or due trade related reasons have small numbers in terms of stats and more importantly have missing values in the dataset. Due to their small playtime, they have missing values and have a close to zero chance of actually winning an award for that year. Thus I chose to omit records that have at least one NaN (not a number or not available) value in that statistic, which thins out the elegible players from ~900 to ~550 players.

    - I may also look into using SHAP, LIME or Yellowbrick to visualize the influence of features to the overall prediction for all awards, not just rocket richard


06/24/26
- model works and predicts end to end, but either SUCKS at predicting or just doesn't outright predict at all

06/28/26
- the prediction was fixed by adding the "class_weight='balanced'" line in the LogisticRegression object, essentially this ensures that minority classes are penalized heavier than majority classes; this is done because this is a heavily imbalanced dataset (there can only be 1 winner out of the ~900 eligible players)
- this resulted in the predictions going from one really bad prediction to 5 really good predictions (see the REPORT section below)
- one of these predictions was Auston Matthews (who was the winner of the 2023 rocket richard), therefore TECHNICALLY predicted the winner correctly
- this award prediction is moreso carried by the fact that I can order the predicted players by goals (descending) and just pick the top 1/3 players to predict as finalists/winners 
- therefore while this pipeline does work properly, it won't be as simple for the other awards that aren't dictated by one sole statistic

- another thing to note is for now, the top 3 predicting function doesn't work - FIXED THIS
- Another related issue: rocket richard is an award that can be awarded to multiple recipients, so due to the script I wrote, years where there were multiple recipients never outputted a skater csv, this'll be an issue for both this award and future awards - FIXED THIS, but note the rocket richard only existed for seasons 1998-present so only those skater data exists (will be adding more as more awards are worked on)

- new issue: top 3 rank predictions has 16 different sets of top 3 predictions; <- this can be classified as a fine tuning problem>
- another issue arose where for the 2023-2024 season, I have the labeled finalists of Auston Matthews and Sam Reinhart written down, but Zach Hyman is missing, the reason being the year after that (which is the 2024-2025 season which is higher in the csv) had two third place winners in Tage Thompson and Alex Ovechkin which offset the third_ids list, will have to fix this; FIXED THIS, instead used 3 for loops in the labelWinners() function - may arise a slight cost in performance?

- functionality for predicting top 1 or top 3 works fully for the rocket richard, but in terms of actual model quality (correct predictions), the report is:
REPORT:
    -2023-2024: overall good for a baseline model, but definitely will need fine tuning
        -top1: predicted 5 players, among them was Auston Matthews (actual winner), therefore predicted correctly (kind of)
        -top3: predicted 54 players in the top 3 rankings, Auston Matthews as top 1 (actual winner; therefore correct), predicted Sam Reinhart as top 1 (actual runner-up; wrong but VERY close), did NOT predict Zach Hyman (actual finalist) in the top 3 at all
            - for top 3, some notable names were predicted as among the top 3 instead: Nathan Mackinnon (51), Artemi Panarin (49), Nikita Kucherov (44), David Pastrnak (47), Kirill Kaprizov (46), Filip Forsberg (48)
    -2024-2025:
        -top1: predicted 4 players, among them was Leon Draisaitl (actual winner), therefore predicted correctly (kind of)
        -top3: predicted 4 sets of top 3 players (12 total players), Leon Draisaitl as top 1 (actual winner; therefore correct), predicted Alex Ovechkin as top 2 (actual finalist (top 3); wrong but VERY close), did NOT predict William Nylander (actual runner-up) OR Tage Thompson (actual finalist tied with Ovechkin)
            - for top 3, some notable names predicted instead as among the top 3 instead: Alex DeBrincat (39), David Pastrnak (43), John Tavares (38), Kyle Connor (41)
    -2025-2026:
        -top1: predicted 4 players, among them was Nathan Mackinnon (actual winner), therefore predicted correctly (kind of)
        -top3: predicted 20 players in the top 3 rankings, Nathan Mackinnon as top 1 (actual winner; therefore correct), predicted Connor McDavid as top 3 (actual finalist; therefore correct), did not predict Cole Caufield (actual runner-up) at all
            -for top 3, some notable named predicted as among the top 3 (goals) instead: Jason Robertson (45), Wyatt Johnston (45), Matt Boldy (42), Steven Stamkos (42), Nikita Kucherov (44)
            -some questionable predictions: (no diss to the actual players I'm just surprised the model thought they'd win the most goals scored award)
                -Clayton Keller (26) as top 2
                -Jack Hughes (27) as top 3
                -Jack Eichel (27) as top 3
                -Mathew Barzal (19) as top 3
    -OVERALL:
    - 3/3 on top 1 predictions (Matthews, Draisaitl, Mackinnon)
    - 4/9 if we're counting absolutely precise predictions and 6/9 for partially correct predictions (landed at least the top 3) for top 3 ranking predictions
    - for a baseline model, as in this is the first complete pipeline I built for this repository, this is honestly a lot better than I was expecting, some fine tuning ideas I have in mind for the future are: 
        -adding EDGE Stats to inflate more features to train on
        -using a different Linear Model than scikitlearn's Logistic Regression
        -removing some features that may be redundant or strongly correlated with 'goals'
        -changing the 'max_iter' property in the LogisticRegression model