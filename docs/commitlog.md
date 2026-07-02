## This document will contain all notes about the commit it is apart of and ONLY that commit

## Decisions/Comments regarding the Rocket Richard Predictor Development:
- rr.ipynb is a testing environment
- rr1.ipynb is also a testing environment but with more direction and just to build the first pipeline baseline predictor
- made a new file 'helpersrr.py' to hold all helper functions originally made in rr and rr1

07/02/26
- in rr2.ipynb
    - as mentioned in the previous commit, the NHL started collecting EDGE stats in 2021, meaning at the time of development, there are ONLY 5 complete seasons of EDGE stats, so the training/testing split will be split 4/1, that is; 4 seasons of data to train on and 1 season of data to test on -- this is because testing sets must have the exact same number of columns as the training set, so seasons prior to 2021 cannot be used for training or testing UNLESS I find a way to replicate or produce estimates for EDGE stats in the past
    - as since there's very little EDGE data compared to GSS data, I predict this model will not be as good as the baseline model found in rr1.ipynb, but I still think it'd be worth exploring to see if this would work (and working with EDGE stats felt like more practice)

- REPORT:
    - since 2021-2025 are 4 seasons used for training, and 2025-2026 is the 1 season used for testing, the results are surprisingly really good
    - 2025-2026:
        - top 1 prediction: predicted 1 player only (really good) that being Nathan Mackinnon as winner (who was the actual winner so correct)
        - top3: predicted 3 players only (really good) that being Nathan Mackinnon as top 1 (actual winner, so correct), Connor McDavid as top 3 (actual finalist, so correct) and Jake Guentzel as top 2 (didn't make top 3 but 38 goals is still a lot)
    - despite being a lot less testing and training sets compared to the baseline model in rr1, this model WITH EDGE stats performed a LOT better (3/4 correct predictions)
    - thus, in some sense, EDGE stats add a better performance, but only with the ability to predict for seasons after 2021, which for practical use is completely fine
    - it should also be noted that near the bottom of the notebook, some shot on goal details genuinely had some weight in prediction: L point shots, R Point Shots, Mid Shots, High Slot Shots, Long Slot Shots, topShotSpeed
    - for now, this version of the model is the one i'll be frontrunning for future season predictions
    - this version with all Shot on Goal Details is known as "EDGE Model Version B"