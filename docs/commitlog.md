## This document will contain all notes about the commit it is apart of and ONLY that commit

## Decisions/Comments/Notes regarding the development of general.py
- 08/10/26
    - Thoughts before implementation
        - I'm going to start by updating all of the csvs in data/formattedwebscraped first to be updated to the 2025/2026 season; this'll be done in models.ipynb
        - Actually, I lied, I'm going to do this by hand because its easier than trying to web scrape again
    - During implementation
        - While adding goalie stats (the general goalie stats aka GGS), I figured I should also add EDGE Goalie stats which made me change the EDGEstats folder from containing just the skater EDGE stats to splitting it into 2 folders -- the only reason I note this is I may have to come back to line 153 in helpers.py to account for goalie EDGE stats or not
        - 08/11/26
        - I've made alternate helper functions for the goalie stat formatting, originally found in models.ipynb but later added/updated to helpers.py. the following functions are part of this update/change:
            - fetchSkaterStats() has an alternate form: fetchGoalieStats()
            - formatEdgeStats() now has an extra parameter 'goalie' to indicate if you're formatting a goalie's stats or not
        - Between the keys from goalie_detail() labeled 'shotLocationSummary' and 'shotLocationDetails', Summary is obviously more general and Details is more detailed, thus to mimic the thoroughness the predictor uses for skaters, I'll be using the 'shotLocationDetails' as part of the feature set
        - within the 'shotLocationDetails' label, each area in the defensive zone has keys for: saves, savesPercentile, savepctg and savePctgPercentile. I'm leaning towards choosing either 'saves' (the actual # of saves) OR savepctg (number of saves relative to shots from that area)
        - it should be noted for skaters, I only included shots and goals for the categories of 'long shots', 'mid shots, 'high shots, and the rest of the area specific shots and goals were ONLY shots
        - so I'm thinking the better decision would be to add both 'saves' and 'savepctg', then experiment what plays better if I were to drop one of those features vs the other
        - used AI to write a few lines in fetchGoalieStats() to deal with empty pagination entries, that's it
