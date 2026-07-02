## This document will contain all notes about the commit it is apart of and ONLY that commit

## Decisions/Comments regarding the Rocket Richard Predictor Development:
- rr.ipynb is a testing environment
- rr1.ipynb is also a testing environment but with more direction and just to build the first pipeline baseline predictor
- made a new file 'helpersrr.py' to hold all helper functions originally made in rr and rr1

06/30/26
- in rocketrichard.py
    - just added an import to the helper functions in the helper file 'helpersrr.py'
- in rr2.ipynb
    - this is a variant of the baseline model in rr1.ipynb, where the training and testing sets contain General Skater Stats, AND EDGE stats
    - it should be noted, the NHL started collecting these edge stats in the 2021-2022 season, thus only from 2021-2026 do EDGE stats exist (5 seasons total), thus the testing sets are the previous recent seasons without EDGE stats
    - some EDGE stats use different systems of measurement, for simplicitly, I will be favoring the metric system over the Imperial System since I'm more familiar with it
    - I'm going to be trying 2 forms of the EDGE stat feature set to try different forms of fine tuning
        1. one with All edge stats listed below EXCEPT for the shot on goal details (since this is an additional 17 features to designate the 17 different spots a shot can be made from)
        2. one with all edge stats listed below including shot on goal details

notes for formatEdgeStats on what to format and extract from the full player EDGE stat dictionary:
    - NOTE: a better way to view what exactly I'm extracting from the EDGE Stats API is by looking at https://www.nhl.com/nhl-edge/skaters/leon-draisaitl-8477934 of any player
    - from "player" dict, only need 'id' or just nothing at all if combining with general stats
    - don't need "seasonsWithEdgeStats"
    - from 'topShotSpeed' dict, only need 'metric'
    - from 'skatingSpeed' dict, only need 'metric'
    - from 'totalDistanceSkated' dict, only need 'metric'
    - from 'distanceMaxGame' dict, only need 'metric'
    - from 'sogSummary' dict, need seperate 'goals' and 'shots' from 'long', 'mid', and 'high' which represents long range shot, mid range shot, high danger range (short range) shot
        -note: the locationCode['all'] is already in GSS, so we want more specific ones
        -shootingPctg is (goals / shots); can be formed if needed
    - from 'sogDetails' dict, need ALL 17 areas' corresponding 'shots' numbers 
        -note: this whole dict is a breakdown of different shots from different areas in the offensive zone, thus is a LOT of data, but after filtering down players from ~900->~500, shouldn't be too performance heavy; will have to gauge tradeoffs after evaluating overall EDGE + GSS performance
    - from 'zoneTimeDetails' dict, need 
        ['offensiveZonePctg'],
        ['neutralZonePctg],
        ['defensiveZonePctg']
        -note: i can only access the offensive,neutral and defensive zone percentages of ALL strengths overall (5v5, 4v5, 5v4 etc) OR even strengths (5v5) only 
    
07/01/26
    - added formatEdgeStats() to the helpersrr.py file
    - added skater EDGE stats to data/api/EDGEstats from 2021-2026 since 2021 is when EDGE stats started getting collected
        - the idea is to keep the EDGE stats and General Skater Stats separate in those folders, then are actually merged together in the notebook/final model script
    - milestone 1 of rr2 is complete, next commit will be either all milestones of rr2 finished or one of them completed
    - it should be noted that the process of extracting the EDGE stats was a lot more lengthy since the functions weren't optimized, roughly 30 minutes total (should work on this in future API collections)
    - once I can confidently say the Rocket Richard Pipeline is properly produced, its roughly the same process for a lot of other awards, so the first hurdle is typically the hardest one the way I'm seeing it