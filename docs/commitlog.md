## This document will contain all notes about the commit it is apart of and ONLY that commit

## Decisions/Comments regarding the Rocket Richard Predictor Development:
- rr.ipynb is a testing environment
- rr1.ipynb is also a testing environment but with more direction and just to build the first pipeline baseline predictor
- made a new file 'helpersrr.py' to hold all helper functions originally made in rr and rr1
- rr2.ipynb is where I'm testing models using GSS + full EDGE stats

07/14/26
- Thoughts before implementation:
    - Before I begin to generalize functions, notebooks, etc. for different awards, I'd like to fully implement the preprocessing, training, and model prediction for RR in the form of a python script (.py file) as opposed to an interactable notebook (.ipynb) so that the whole thing runs end to end (with given user inputs) 

07/29/26
- I've fully implemented the rocketrichard.py processing file meaning the full script pipeline works now
- The reason for the long time gap in commits is that I had to work at K-Days for 10 days straight (07/17 - 07/26)
- Some parts of the functions in the prediction pipeline of rocketrichard.py are already sort of built for generalization across other awards
- The input filtering has a little placeholder but by all means is not the final set of input filtering
- The formatting in the terminal of the predictor really sucks but this is to be patched by front-end UI later in the project, point is it works and that's what is important