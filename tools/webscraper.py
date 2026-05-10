'''
author: jiai27
description:
    this is a file made from a web scraping tutorial by CodeHead (https://www.youtube.com/watch?v=hHQlcnubuFI) to scrape data on previous winners/finalists from the list of NHL Trophies on the official NHL Records website
    while award data given a particular player is available, 
    
scraping from: https://records.nhl.com/awards/trophies 
data collected using this file is in data/web_scraped folder

note: it is not recommended to use this file outside of development as this program may open multiple browser windows
and by no means is this file supposed to be properly optimized, its simply a tool i'm developing to web scrape as a one-time use
'''

#------1. FETCH THE LINK TO EVERY TROPHY-----
#---assisted---
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv


driver = webdriver.Chrome()
driver.get("https://records.nhl.com/awards/trophies")

time.sleep(5)  # let JS load

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

trophies = soup.find("div", class_="award-cards-container")
#---assisted---

trophy_container = trophies.find_all("h3",class_="trophy-name")
trophy_links = []

for i in range(len(trophy_container)):
    trophy_link = "https://records.nhl.com" + str(trophy_container[i].a["href"])
    trophy_links.append(trophy_link)
    #print(trophy_link)


def findWebType(url):
    '''
    helper function that detects the which of the 3 web types I defined that this particular award url is
    returns an integer between [1,3]
    '''
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    container = soup.find("div", class_="rt-thead -header")
    breakdown = container.find_all("div")

    if len(breakdown)-1 == 10:
        return 1
    elif len(breakdown)-1 == 4:
        return 2
    elif len(breakdown)-1 == 6:
        return 3
    return 0

#------2. PARSE A LINK AND RETURN ITS DATA-----

def getAwardData(award_link = None, web_type = 1):
    '''
    Takes an award url as an input and parses through the website to extract all data of that award's winners and/or finalists
    '''
    page_data = []
    driver = webdriver.Chrome()
    driver.get(award_link)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    award_name = soup.find("h2", class_="sc-fSwKIM lkqBDo")
    page_data.append(award_name.text)

    container = soup.find("div", class_="rt-tbody")
    records = container.find_all("div", class_="rt-tr-group")
    print(len(records))

    for i in range(len(records)):
        if i%2 == 0:        #if we're looking at an even year end (2025-26 is an even year end)
            full_record = records[i].find("div", class_="rt-tr -odd")
        else:               #elif we're looking at an odd year end (2024-25 is an odd year end)
            full_record = records[i].find("div", class_="rt-tr -even")


        season = full_record.find("div", class_="rt-td column-season")
        record_attributes = full_record.find_all("div", class_="rt-td")

        
        if web_type == 1:                         #10 entries indexed 0-9, only need a href of: 1 (winner), 4(runner-up 2nd), 7 (finalist)
            winner = record_attributes[1]
            runner_up = record_attributes[4]
            finalist = record_attributes[7]
            data_tuple = (season.text, winner.a['href'], runner_up.a['href'], finalist.a['href'])
            
        elif web_type == 2:                       #just a winner, href is at (1)
            winner = record_attributes[1]           
            data_tuple = (season.text, winner.a['href'])

        else:
            continue 
        
        page_data.append(data_tuple)
    return page_data


#----------3. PARSE ALL LINKS, TURN IT INTO A CSV AND ADD TO REPO
to_pop = ["https://records.nhl.com/awards/trophies/bill-masterton-memorial-trophy",
          "https://records.nhl.com/awards/trophies/clarence-s-campbell-bowl",
          "https://records.nhl.com/awards/trophies/jack-adams-award",
          "https://records.nhl.com/awards/trophies/jim-gregory-general-manager-of-the-year-award",
          "https://records.nhl.com/awards/trophies/king-clancy-memorial-trophy",
          "https://records.nhl.com/awards/trophies/lady-byng-memorial-trophy",
          "https://records.nhl.com/awards/trophies/lester-patrick-trophy",
          "https://records.nhl.com/awards/trophies/mark-messier-nhl-leadership-award",
          "https://records.nhl.com/awards/trophies/nhl-foundation-player-award",
          "https://records.nhl.com/awards/trophies/nhl-lifetime-achievement-award",
          "https://records.nhl.com/awards/trophies/ted-lindsay-award",
          "https://records.nhl.com/awards/trophies/willie-o-ree-community-hero-award",
          "https://records.nhl.com/awards/trophies/e-j-mcguire-award-of-excellence",
          "https://records.nhl.com/awards/trophies/maurice-rocket-richard-trophy",
          "https://records.nhl.com/awards/trophies/presidents-trophy",
          "https://records.nhl.com/awards/trophies/prince-of-wales-trophy",
          "https://records.nhl.com/awards/trophies/vezina-trophy",
          "https://records.nhl.com/awards/trophies/william-m-jennings-trophy",
          "https://records.nhl.com/awards/trophies/calder-memorial-trophy"]  

#fix for rocket richard, presidents trophy, prince of wales, vezina, jennings

final_links = []
for popper in trophy_links:
    if popper not in to_pop:
        final_links.append(popper)

#for link in final_links:
 #   print(link)


for link in final_links:
    link_type = findWebType(link)
    award_data = getAwardData(link, link_type)

    csv_title = "data/web-scraped/" + str(award_data[0].lower()) + ".csv"
    with open(csv_title, 'w') as f:
        write = csv.writer(f)
        write.writerows(award_data)

