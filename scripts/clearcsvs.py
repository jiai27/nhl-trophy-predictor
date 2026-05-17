'''
author: jiai27
description:
    small script to clear all csvs
note:
    this script is ran on mac OS
'''

import os
import pandas as pd
import numpy as np

def clear_csv(csv_path):
    print(csv_path)
    df = pd.read_csv(csv_path, encoding='ascii')
    print(df.head(), df.shape)


    return None


#-- Source - https://stackoverflow.com/a/14462901
#-- Posted by Mike, modified by community. See post 'Timeline' for change history
#-- Retrieved 2026-05-17, License - CC BY-SA 3.0
#current_dir = os.getcwd()
path = ".."
os.chdir(path)  #take 1 step back
os.chdir("data/formattedwebscraped")

for csv in os.listdir():
    #if csv == "test.csv":
    #    new_file = clear_csv(csv)
    new_file = clear_csv(csv)