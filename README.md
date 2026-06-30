# nhl-trophy-predictor - Overview
A personal (non-profitable) project using publicly available data collected by the NHL to ideally predict trophy winners of future seasons using a model trained on past seasons results. This project excludes awards that are related to cultural impact of the sport, subjective qualities like perseverance and team sport are difficult to measure (so excluding Bill Masterton, King Clancy, that kind of thing). Instead, this project is more targetted for awards that can be predicted using pure player statistics collected by the league. Currently this focuses on player specific awards, but team prediction is planned to be implemented in the future

### Motivation:
I wanted my first side project to be something directly related to a field I was interested in (ML) and in some sense tied to an interest of mine to stay motivated and more engrossed into that interest. After finding the abundance of data the NHL collects from players, particularly EDGE statistics which fascinated me a lot, I wanted to take advantage of this fountain of data for a project.
Additionally, I wanted to take what I learned in my recent classes and implement basic linear and logistic models to spout predictions.

## Current Features:
N/A, still developing the core stuff 

## Progress (06/30/26):
- extracted csvs for skaters from NHL seasons 1998-2026
- built an end-to-end prediction pipeline for the Rocket Richard award (not directly influenced by the highest # of goals which is the direct statistic)
    -can predict winner only, or the top 3 finalists for the award
    -includes feature sets, training/testing splits and lots of experimentation with models for this award
    -more on the decisions and results can be found in commitlog.md

## What's Next:
- fine tuning to the Rocket Richard Prediction Pipeline
- look to include EDGE statistics to find if it is worth incorporating for the other awards
- look into using either SHAP, LIME or Yellowbrick to visualize feature influences in the prediction model
- get the rocket richard prediction pipeline relatively finished and recycle pre-processing code for other award pipelines
- put all final code needed for the Rocket Richard award put into a singular python script instead of a notebook (once model is fully fine-tuned)
