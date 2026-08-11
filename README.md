# nhl-trophy-predictor - Overview
A personal (non-profitable) project using publicly available data collected by the NHL to ideally predict trophy winners of future seasons using a model trained on past seasons results. This project excludes awards that are related to cultural impact of the sport, subjective qualities like perseverance and team sport are difficult to measure (so excluding Bill Masterton, King Clancy, that kind of thing). Instead, this project is more targetted for awards that can be predicted using pure player statistics collected by the league. Currently this focuses on player specific awards, but team prediction is planned to be implemented in the future

### Motivation:
I wanted my first side project to be something directly related to a field I was interested in (ML) and in some sense tied to an interest of mine to stay motivated and more engrossed into that interest. After finding the abundance of data the NHL collects from players, particularly EDGE statistics which fascinated me a lot, I wanted to take advantage of this fountain of data for a project.
Additionally, I wanted to take what I learned in my recent classes and implement basic linear and logistic models to spout predictions.

## Current Features:
N/A, still developing the core stuff 

## Progress (08/11/26):
- added 2025-2026 award winners to csv files that didn't have them
- fetched all goalie stats from 1940-2026 for the Vezina trophy prediction
- fetched all goalie EDGE stats from 2021-2026 for the Vezina trophy prediction

## What's Next:
- Predict on the Vezina Trophy with the newly added goalie stats
- Redo Art Ross, Hart Trophy and Selke Trophy tests on the fixed version of the code
- Continue developing the prediction pipeline for other direct statistic awards (**Art Ross**, Vezina, etc.), then move onto more subjective awards (Conn Smythe, Hart, Ted Lindsay etc.)

