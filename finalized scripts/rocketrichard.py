#will paste all final code here once the rocket richard predicting pipeline is fully fine-tuned


import numpy as np
import pandas as pd
from nhlpy import NHLClient
import ast
from notebooks.helpersrr import clear_csv, extractPlayerID, placeToStats, fetchSkaterStats, labelWinners, formatEdgeStats #--HELPER FUNCTIONS FOR FINE TUNING NOTEBOOKS AND FINAL PIPELINE--