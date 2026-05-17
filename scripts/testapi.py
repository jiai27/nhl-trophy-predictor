'''
author: jiai27
description:
    this is a file that utilizes the nhl-api-py library developed by user @coreyjs on GitHub (https://github.com/coreyjs/nhl-api-py)
    official data extracted using this library is from: https://api-web.nhle.com/
'''

from nhlpy import NHLClient

client = NHLClient(
    debug=True,
    timeout=30
)


#---testing---
def main():
    career_stats = client.stats.player_career_stats(player_id="8478402")  # Connor McDavid
    
    '''
    for stat in career_stats:
        print(stat, type(stat))
        if stat == "awards":
            print(career_stats[stat])
    '''

    for record in career_stats["awards"]:
        print(record)     


    pass

if __name__ == "__main__":
    main()

