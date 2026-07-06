| Date Logged/Tested | Experiment Number & Award | Features | Model | Season(s) Tested (Total) | Top-1 Acc% | Top-3 Acc% | Notes
|---|---|---|---|---|---|---|---|
|06/28/26| RR#1 | GSS only | LogisticRegression() | 2023-2026 (3)| *20% | *44% | Baseline Model
|07/02/26| RR#2 | GSS + EDGE | LogisticRegression() | 2021-2026 (5) | 33% | 68.8% | EDGE Model Ver.B
|**07/03/26**| **RR#3** | **GSS + part. EDGE** | **LogisticRegression()** | **2021-2026 (5)** | **42.9%** | **68.8%** | **EDGE Model Ver.A (best so far)**
|07/05/26 | RR#4 | GSS + EDGE | RandomForest() | 2021-2026 (5) | 0% | 68.8% | same top3 predictions as RR#2 |
|07/06/26| RR#5 | GSS + EDGE | GradientBoostingClassifier() | 2021-2026 (5) | 18.2% | 68.8% | uses default hyperparameters |

<!-- | .. | ... | ... | ... | ... | ... | ... | placeholder | --> 

### Abbreviations:
- GSS: "General Skater Stats", entails things like
    - number of assists, goals, points
    - gamesPlayed, otGoals, shootout Goals, etc.
- RR: "Rocket Richard Award", refers to tests done on the Rocket Richard Award specifically
    - this award is given to the player that finishes the NHL regular season with the highest number of goals (does not count playoff goals)
- EDGE: "EDGE Stats", the officially named statistics by the NHL regarding hyperspecific statistics of a player: top shot speed, skating speed etc.
    - "EDGE" means "all EDGE": all EDGE stats, particularly including shots on goal details (a heatmap of where players shoot at the goal from in different areas of the offensive zone)
    - Part. EDGE: partial EDGE stats, contains everything but the shots on goal details
- If an accuracy point has "*" at the beginning, check the notes section below for explanation
- Details on the accuracy calculation can be found in commitlog.md of the commit made on the date logged

### (*) Notes:
- RR#1:
    - for top 1 predictions, the seasons 2023-2024, 2024-2025 and 2025-2026 predicted a handful of players respectively: 5 players, 4 players, 4 players, but among those handfuls the real winner was always present
    - for top 3 predictions, sets of 3 players were predicted instead to resemble the top 3 placement of finalists
        - 2023-2024: predicted 2/3 of the finalists correctly, but only 1/3 were placed in top 3 correctly
        - 2024-2025: predicted 2/3 of the finalists correctly, but only 1/3 were placed in top 3 correctly
        - 2025-2026: predicted 2/3 of the finalists correctly, placed 2/3 of in the top 3 correctly
- RR#2 and RR#3 have more detailed records in their respective commits in commitlog.md

- RR#4:
    - top1: predicted nothing for all 5 test seasons
    - top3: had the exact same predictions as RR#2 which is really interesting