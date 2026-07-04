## This document will contain all notes about the commit it is apart of and ONLY that commit

## Decisions/Comments regarding the Rocket Richard Predictor Development:
- rr.ipynb is a testing environment
- rr1.ipynb is also a testing environment but with more direction and just to build the first pipeline baseline predictor
- made a new file 'helpersrr.py' to hold all helper functions originally made in rr and rr1

07/03/26
- rr2.ipynb
    - I want to try testing on the other 4 of the 5 EDGE Stat Seasons I can work with when I'm doing EDGE Model Ver. A (the one with all EDGE stats EXCEPT for the shots on goal details)
    - after implementing the changes for Version A, the top 3 prediction did NOT change, but the top 1 prediction DID
    - the top 1 prediction had 2 predictions overall, Nathan Mackinnon (true winner, therefore correct) and Jake Guentzel (not a finalist at all)
    - so based off just the one test, version A is inferior in accuracy to version B
    - therefore like predicted, we will still be going through with version B for future predictions for now