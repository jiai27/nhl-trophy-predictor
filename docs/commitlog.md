## This document will contain all notes about the commit it is apart of and ONLY that commit

## Decisions/Comments regarding the Rocket Richard Predictor Development:
- rr.ipynb is a testing environment
- rr1.ipynb is also a testing environment but with more direction and just to build the first pipeline baseline predictor
- made a new file 'helpersrr.py' to hold all helper functions originally made in rr and rr1
- rr2.ipynb is where I'm testing models using GSS + full EDGE stats

07/09/26
- rr2.ipynb
    - Thoughts before Implementing things
        - Why is EDGE Ver. A now the new best model?
            - It should be noted that the only reason EDGE Ver. A technically performed better than EDGE Ver. B was their difference in top 1 predictions across the 5 EDGE seasons
            - EDGE Ver. A's 42.9% obviously is more accurate than EDGE Ver. B's 33.3%, and this is due to EDGE Ver.B predicting slightly more players in the top 1 prediction then Ver. A
            - In commit 43d296b, the following top 1 predictions occurred:
                - 2021-2022:
                    - A predicted **Auston Matthews** and Johnny Gaudreau
                    - B predicted Johnny Gaudreau, **Auston Matthews** , Matthew Tkachuk, Jake Guentzel
                - 2022-2023: A and B predicted David Pastrnak only (wrong)
                - 2023-2024:
                    - A predicted **Auston Matthews** only
                    - B predicted **Auston Matthews** and Nathan Mackinnon
                - 2024-2025: neither A or B made a prediction
                - 2025-2026:
                    - A predicted **Nathan Mackinnon** and Jake Guentzel
                    - B predicted **Nathan Mackinnon** only
            - the metric I calculated top1 performance was as follows: for each season, (number of players correctly predicted--at most is 1/number of players predicted)
            - So if given a few more future seasons or mock seasons that contain EDGE stats, either Ver.B or A could perform better, but the inclusion/exclusion of the shots on goal details which is the only difference between Ver.B and Ver.A has little to no impact difference between the models since different seasons found different weights among different features, but the common features that had a lot of weight were **goals, assists, topShotSpeed, L/R Point Shots** 
        - Thus, although EDGE Ver. A is technically superior, it only had 3-4 less predicted players for top 1 winners, so I'll be fine tuning both EDGE Ver. A and B continuing onwards
        - i'll also be experimenting with different penalties for these two models
        - after this commit, I'll be finalizing one of these two models to act as the baseline for the other awards and generalizing the helper functions/scripts to get to other awards faster.
    ------------
    - 07/10/26: REPORT on EDGE A vs EDGE B:
    - I thought it should be worth doing one more go of testing on both EDGE Ver. A/B on their respective feature sets so I can also note down the features with the heaviest weights, here were the findings:
    - Top5 coefficients can be found at the end of this document (only for the last 2 seasons since it gets tedious)
        - 2021-2022
            - top1:
                - A: **Auston Matthews** and Johnny Gaudreau
                - B: **Auston Matthews**, Johnny Gaudreau, Matthew Tkachuk, Jake Guentzel
                - goals once again the top 1, A found top 3 to be goals, evPOints, points, B found top 3 to be goals, plusMinus, R Net Side Shots
            - top3:
                - A: predicted 5 players: **Auston Matthews (1st)**, Leon Draisaitl (3rd), Jake Guentzel (2nd), Evgeny Kuznetsov (2nd), Jakub Voracek (3rd)
                    - gamesPlayed, assists, skatingSpeed were top 3
                - B: predicted **Auston Matthews (1st)**, **Leon Draisaitl (2nd)**, Evgeny Kuznetsov (3rd); 2/3 correct
                    - assists, penaltyMinutes, longShots were top3
        - 2022-2023
            - top1:
                - A: predicted David Pastrnak (wrong)
                - B: predicted David Pastrnak (wrong)
                - goals was the highest for both A/B
            - top3:
                - A: predicted 6 players: Connor McDavid (3rd), David Pastrnak (3rd), **Mikko Rantanen (3rd)**, Leon Draisaitl (2nd), Brayden Point (3rd), Anze Kopitar (3rd), 1/6 correct
                    - gamesPlayed, assists, longShots were top 3 features
                - B: predicted **Connor McDavid (1st)**, **David Pastrnak (2nd)**, **Mikko Rantanen (3rd)** 3/3 correct
                    - topShotSpeed, assists, high slot shots were top 3 features
        - 2023-2024
            - top1: 
                - A: **Auston Matthews** only
                - B: **Auston Matthews** and Nathan Mackinnon
            - top3: 
                - A: predicted 8 players: Auston Matthews (2nd), **Sam Reinhart (2nd)**, Steven Stamkos (1st), Kirill Kaprizov (3rd), Filp Forsberg (3rd), David Pastrnak (3rd), Artemi Panarin (3rd), Nathan Mackinnon (3rd)
                    - gamesPLayers, assists and gameWinningGoals were the top 3 features
                - B: predicted **Auston Matthews (1st)**, **Sam Reinhart (2nd)**, Steven Stamkos (3rd)
                    - assists, L Circle shots, topShotSpeed were the top 3 features
        - 2024-2025
            - top1: A and B didn't predict anyone (still odd), coefficients revealed goals were the top value
            - top3:
                - A: only predicted Leon Draisaitl (2nd) incorrect placing but correct prediction
                - B: predicted **Leon Draisaitl (1st)**, Mark Scheifele (2nd), John Tavares (3rd), **Alex Ovechkin (3rd)**
        - 2025-2026
            - top1:
                - A: **Nathan Mackinnon** , Jake Guentzel (1/2 correct)
                - B: **Nathan Mackinnon** only, (1/1 correct)
            - top3: interestingly, A had 5 total predictions versus B's 3 total
                - A: predicted **Nathan Mackinnon at 1st**, Jack Eichel (2nd), Jake Guentzel (2nd), Mathew Barzal (2nd), Leo Carlsson (3rd); 1/5 correct. 
                - B: predicted **Nathan Mackinnon at 1st**, Jake Guentzel (2nd), **Connor McDavid (3rd)**; 2/3 correct

        - **Overall**: 
            - seems Ver.B actually IS the more optimal one due to Ver. A making a lot more false predictions and not constraining to just 1 or 3 predictions
            - Ver. A also seems to prioritize features that are irrelevent or kind of a given: gamesPlayed, 
            - Ver. B seems to prioritize shots from long distance and particularly mid to high slot shots 
            - I predict that the current Ver. A may be better for other awards that don't have a direct indicating victor statistic (RR's is # of goals) whereas Ver. B is better for RR prediction specifically
            - based on actual calculations, Ver. A is better than Ver. B in terms of top 1 prediction, but vice versa for top 3
        - Actual Calculations:
            - top1:
                - A: (1/2) + (0/1) + (1/1) + (0/1) + (1/2) = 3/7 = **42.9%**
                - B: (1/1) + (0/1) + (1/2) + (0/1) + (1/4) = 3/9 = **33.3%**
            - top3:
                - A: (1/5) + (0/1) + (1/8) + (1/6) + (1/5) = 4/25 = **16%**
                - B: (2/3) + (2/4) + (2/3) + (3/3) + (2/3) = 11/16 = **68.8%**

| Season Tested | Ranking | A/B | Feature Name | Feature Value |
|---|---|---|---|---|
|2025-2026|top 3| A | assists | 0.5374 |
|2025-2026|top 3| A | gamesPlayed | 0.4656 |
|2025-2026|top 3| A | skatingSpeed | 0.2127 |
|2025-2026|top 3| A | midShots | 0.1773 |
|2025-2026|top 3| A | highShots | 0.1602 |
|2025-2026|top 3| B | High Slot Shots | 0.0569 |
|2025-2026|top 3| B | longShots | 0.0557 |
|2025-2026|top 3| B | topShotSpeed | 0.0446 |
|2025-2026|top 3| B | penaltyMinutes | 0.0433 |
|2025-2026|top 3| B | timeOnIcePerGame | 0.0399 |
|2025-2026|top 1| A | evGoals| 0.4300 |
|2025-2026|top 1| A | **goals** | 0.3829 |
|2025-2026|top 1| A | points | 0.2360 |
|2025-2026|top 1| A | midGoals | 0.2294 |
|2025-2026|top 1| A | highGoals | 0.2162 |
|2025-2026|top 1| B | evGoals | 0.3384 |
|2025-2026|top 1| B | **goals** | 0.3180 |
|2025-2026|top 1| B | midGoals | 0.2316 |
|2025-2026|top 1| B | points | 0.2037 |
|2025-2026|top 1| B | highGoals | 0.1888 |
|2024-2025|top 3| A | assists | 0.3864 |
|2024-2025|top 3| A | topShotSpeed | 0.3650 |
|2024-2025|top 3| A | longShots | 0.2210 |
|2024-2025|top 3| A | gamesPlayed | 0.1937 |
|2024-2025|top 3| A | midShots | 0.1531 |
|2024-2025|top 3| B | Outside L Shots | 0.1363 |
|2024-2025|top 3| B | assists | 0.1337 |
|2024-2025|top 3| B | R Circle Shots | 0.0969 |
|2024-2025|top 3| B | skatingSpeed | 0.0713 |
|2024-2025|top 3| B | gamesPlayed | 0.0463 |
|2024-2025|top 1| A | **goals** | 0.3404 |
|2024-2025|top 1| A | midShots | 0.3149 |
|2024-2025|top 1| A | evPoints | 0.2233 |
|2024-2025|top 1| A | evGoals | 0.2178 |
|2024-2025|top 1| A | points | 0.2089 |
|2024-2025|top 1| B | **goals** | 0.2914 |
|2024-2025|top 1| B | midShots | 0.2321 |
|2024-2025|top 1| B | L Circle Shots | 0.2115 |
|2024-2025|top 1| B | evGoals | 0.1955 |
|2024-2025|top 1| B | points | 0.1677 |

- Fine Tuning Testing on EDGE Ver. B
    1. 'l1' penalty + 'saga' solver: (WORSE THAN CURRENT OPTIMAL)
        - 2022-2023
            - top 3: got correct predictions but 3 additional players predicted as well
            - top 1: finally got its first correct prediction of **Connor McDavid**, but with 3 other incorrect predictions
        - 2024-2025
            - top1: still unpredicted
            - top3: still predicted **Leon Draisaitl (1st)** and **Alex Ovechkin (3rd)**, but added 8 more extra predictions
    2. 'elasticnet' penalty + 'saga' solver: (WORSE THAN CURRENT OPTIMAL)
        - 2024-2025
            - top1: still unpredicted
            - top3: same as l1 + saga
        - 2025-2026
            - top1: predicted **Nathan Mackinnon** and Nikita Kucherov with points, plusMinus and R Net Side Shots as the highest coefficients; worse than optimal model
            - top3: preicted 5 players, **Connor McDavid (3rd)**, **Nathan Mackinnon (1st)**, the rest were incorrect; worse than optimal model
    3. No Penalty + 'saga' solver; (WORSE THAN CURRENT OPTIMAL)
        - 2022-2023
            - top1: 4 predictions, 1 of the 4 was **Connor McDavid (1st)**
            - top3: correct predictions but 1 additional player predicted as well
        - 2023-2024
            - top1: 4 predictions, 1/4 was **Auston Matthews (1st)**
            - top3: 5 predictions, 2/5 of were correct 
        - 2024-2025
            - top1: nothing predicted
            - top3: 2/12 predictions were correct
    4. No Penalty + 'lbfgs' solver (slightly WORSE THAN CURRENT OPTIMAL)
        - 2022-2023
            - top1: 1/4 predictions correct (better than optimal)
            - top3: 3/3 predictions correct (same as optimal)
        - 2023-2024
            - top1: 1/3 predictions correct (1 prediction worse than optimal)
            - top3: 2/3 predictions correct (same as optimal)
        - 2024-2025
            - top1: nothing predicted
            - top3: 2/4 predictions correct (same as optimal)
    5. 'l2' penalty + default 'lbfgs' solver + C=10 (default is 1)
        - 2021-2022
            - top1: 1/5 predictions correct (worse than optimal)
            - top3: 2/3 predictions correct (same as optimal)
        - 2022-2023
            - top1: 1/4 predicitons correct (technically better than optimal) - and ranked goals as highest feature
            - top3: 3/3 predictions correct (same as optimal)
        - 2023-2024
            - top1: 1/2 predictions correct (same as optimal)
            - top3: 2/3 predictions correct (same as optimal)
        - 2024-2025
            - top1: no predictions
            - top3: 2/4 predictions correct (same as optimal)
        - 2025-2026
            - top1: no predictions (worse than optimal)
            - top3: 2/3 predictions correct (same as optimal)
    6. 'l2 penalty + 'lbfgs' solver + C=0.1 
        - 2023-2024:
            - top1: 1/3 correct (worse than optimal)
            - top3: 2/3 correct (same as optimal)
        - 2024-2025:
            - top1: no predictions
            - top3: 2/4 correct (same as optimal)
        - 2025-2026:
            - top1: 1/1 correct (same as optimal) 
            - top3: 2/3 correct (same as optimal)

    7. 'l2' penalty + 'lbfgs' solver + C=0.01 (ever so slightly worse than optimal)
        - 2023-2024
            - top1: 1/3 correct (slightly worse than optimal)
            - top3: 2/3 correct (same as optimal)
        - 2024-2025
            - top1: no predictions
            - top3: 2/4 predictions correct (same as optimal)
        - 2025-2026
            - top1: 1/1 correct predictions (same as optimal)
            - top3: 2/3 correct (same as optimal)
    - 07/12/26
    - After fine tuning different C values and penalties and learners, I have deduced that the current RR#2 EDGE Ver. B Model is still the most optimal one, so this will be the model we move forward with for baseline testing.
