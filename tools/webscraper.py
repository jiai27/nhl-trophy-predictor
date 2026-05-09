'''
author: jiai27
description:
    this is a file made from a web scraping tutorial by CodeHead (https://www.youtube.com/watch?v=hHQlcnubuFI) to scrape data on previous winners/finalists from the list of NHL Trophies on the official NHL Records website
scraping from: https://records.nhl.com/awards/trophies 
data collected using this file is in data/web_scraped folder

note: it is not recommended to use this file outside of development as this program may open multiple browser windows
'''

#------1. FETCH THE LINK TO EVERY TROPHY-----
#---assisted---
from selenium import webdriver
from bs4 import BeautifulSoup
import time

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

#------2. PARSE EVERY LINK-----
print(trophy_links)
def getAwardData(award_link = None, until_year = 2000):
    '''
    Takes an award url as an input and parses through the website to extract all data of that award's winners and finalists up until [until_year]
    '''
    driver = webdriver.Chrome()
    driver.get(award_link)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    records = soup.find_all("div", class_="rt-tr -group")
    for i in range(len(records)):
        if i%2 == 0:        #if we're looking at an even year end (2025-26 is an even year end)
            full_record = records[i].find("div", class_="rt-td -odd")
        else:               #elif we're looking at an odd year end (2024-25 is an odd year end)
            full_record = records[i].find("div", class_="rt-td -even")

        season = full_record.find("div", class_="rt-td column-season")  #season.text to get actual text
        rt_td = full_record.find_all("div", class_="rt-td")

        
       
        print(i, "\n", season.text, rt_td, type(rt_td), rt_td[0])

    return None

getAwardData("https://records.nhl.com/awards/trophies/art-ross-trophy")


#for link in trophy_links:
#    award_data = getAwardData(str(link))    