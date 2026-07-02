# nhl-trophy-predictor - Overview
A personal (non-profitable) project using publicly available data collected by the NHL to ideally predict trophy winners of future seasons using a model trained on past seasons results. This project excludes awards that are related to cultural impact of the sport, subjective qualities like perseverance and team sport are difficult to measure (so excluding Bill Masterton, King Clancy, that kind of thing). Instead, this project is more targetted for awards that can be predicted using pure player statistics collected by the league. Currently this focuses on player specific awards, but team prediction is planned to be implemented in the future

### Motivation:
I wanted my first side project to be something directly related to a field I was interested in (ML) and in some sense tied to an interest of mine to stay motivated and more engrossed into that interest. After finding the abundance of data the NHL collects from players, particularly EDGE statistics which fascinated me a lot, I wanted to take advantage of this fountain of data for a project.
Additionally, I wanted to take what I learned in my recent classes and implement basic linear and logistic models to spout predictions.

## Current Features:
N/A, still developing the core stuff 

## Progress (07/01/26):
- made formatEdgeStats() a helper function that does the below:
- extracted csvs for EDGE Stats of skaters from NHL seasons 2021-present into data/api/EDGEstats (since EDGE stats started being collected 2021)
- moved all helper functions to 'helpersrr.py', some functions will be recycled for other awards

## What's Next:
- continue fine tuning to the Rocket Richard Prediction Pipeline -> specifically use the newly collected EDGE stats
- look into using either SHAP, LIME or Yellowbrick to visualize feature influences in the prediction model - only applicable for supported models
- get the rocket richard prediction pipeline relatively finished and recycle pre-processing code for other award pipelines
- put all final code needed for the Rocket Richard award put into a singular python script instead of a notebook (once model is fully fine-tuned)