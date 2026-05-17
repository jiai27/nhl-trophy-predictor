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
import re


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

    if len(breakdown)-1 == 10:      #art ross, calder, selke, hart memorial
        return 1
    elif len(breakdown)-1 == 4:     #conn smythe
        return 2
    elif len(breakdown)-1 == 6:     #?? - no such thing?
        print("THIS ONE", url)
        return 3
    elif len(breakdown)-1 == 13:    #rocket richard exclusive
        return 4
    elif len(breakdown)-1 == 5:     #clarence campbell, president's, prince of wales (team specific awards), jennings
        return 5
    elif len(breakdown)-1 == 7:     #norris, vezina
        return 6

    print(len(breakdown)-1, url)
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
    print(web_type,len(records), award_link)

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

            if runner_up == None:
                data_tuple = (season.text, winner.a['href'])
                continue
            elif finalist == None:
                data_tuple = (season.text, winner.a['href'], runner_up.a['href'])
                continue
            else:
                data_tuple = (season.text, winner.a['href'], runner_up.a['href'], finalist.a['href'])
            
        elif web_type == 2:                       #just a winner, href is at (1)
            winner = record_attributes[1]           
            data_tuple = (season.text, winner.a['href'])

        elif web_type == 3:
            continue

        elif web_type == 4: #rocket richard; formatted as a tuple, (name, # goals)
            winner = (record_attributes[1], record_attributes[4])
            runner_up = (record_attributes[5], record_attributes[8])
            finalist = (record_attributes[9], record_attributes[12])

            def extract_from_entry(entry):
                """Handle the (element, stat) tuple used on this page and normalize links.
                Returns a single (href, stat) tuple, a list of (href, stat) tuples, or None."""
                if entry is None:
                    return None

                # entry is expected to be a tuple where the first element contains the anchor(s)
                elem = entry[0] if isinstance(entry, (list, tuple)) else entry
                stat_elem = entry[1] if isinstance(entry, (list, tuple)) and len(entry) > 1 else None

                if elem is None:
                    return None

                # parse stat (number of goals) from stat_elem if possible
                stat = None
                if stat_elem is not None:
                    stat_text = stat_elem.text.strip() if getattr(stat_elem, 'text', None) else str(stat_elem)
                    nums = re.findall(r"\d+", stat_text)
                    if nums:
                        try:
                            stat = int(nums[0])
                        except ValueError:
                            stat = stat_text
                    else:
                        stat = stat_text

                links = []
                for mlc in elem.find_all("div", class_="multiLineContainer"):
                    for a in mlc.select('a[href]'):
                        links.append(a['href'])

                # fallback to a direct anchor on the element
                if not links:
                    a = elem.find('a', href=True)
                    if a:
                        return (a['href'], stat) if stat is not None else a['href']
                    return None

                # attach stat to each link; if only one link, return a single tuple
                if len(links) == 1:
                    return (links[0], stat) if stat is not None else links[0]

                return [(h, stat) for h in links]

            winner_links = extract_from_entry(winner)
            runner_links = extract_from_entry(runner_up)
            finalist_links = extract_from_entry(finalist)

            if runner_links is None:
                data_tuple = (season.text, winner_links)
            elif finalist_links is None:
                data_tuple = (season.text, winner_links, runner_links)
            else:
                data_tuple = (season.text, winner_links, runner_links, finalist_links)

        elif web_type == 5: #the team specific ones
            winner = record_attributes[1]
            runner_up = record_attributes[3]
            #print(type(winner), type(runner_up))
            winner = record_attributes[1]
            runner_up = record_attributes[3]

            def extract_links(container):
                """Return a single href string if there's one recipient, a list if multiple, or None."""
                if container is None:
                    return None

                links = []
                # look for multiLineContainer blocks first
                for mlc in container.find_all("div", class_="multiLineContainer"):
                    for a in mlc.select('a[href]'):
                        links.append(a['href'])

                # fallback to a direct anchor on the container
                if not links:
                    a = container.find('a', href=True)
                    if a:
                        return a['href']
                    return None

                # if only one link found, return as a single string
                if len(links) == 1:
                    return links[0]

                return links

            hrefs = extract_links(winner)
            run_hrefs = extract_links(runner_up)

            # build data tuple depending on what we have
            # season, winner (str or list or None), runner_up (str or list or None)
            data_tuple = (season.text, hrefs, run_hrefs)

        elif web_type == 6: #vezina, norris
            winner = record_attributes[1]
            runner_up = record_attributes[3]
            finalist = record_attributes[5]
            #print(type(finalist))

            if runner_up.a == None:
                data_tuple = (season.text, winner.a['href'])
                

            elif finalist.a == None:
                #print("NONE")
                data_tuple = (season.text, winner.a['href'], runner_up.a['href'])
                
            else:
                data_tuple = (season.text, winner.a['href'], runner_up.a['href'], finalist.a['href'])

        else:
            continue 
        
        page_data.append(data_tuple)
        title = page_data[0]
    return page_data, title


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
          "https://records.nhl.com/awards/trophies/calder-memorial-trophy",
          "https://records.nhl.com/awards/trophies/art-ross-trophy",
          "https://records.nhl.com/awards/trophies/conn-smythe-trophy",
          "https://records.nhl.com/awards/trophies/frank-j-selke-trophy",
          "https://records.nhl.com/awards/trophies/hart-memorial-trophy",
          "https://records.nhl.com/awards/trophies/james-norris-memorial-trophy",
          "https://records.nhl.com/awards/trophies/william-m-jennings-trophy",

            
          "https://records.nhl.com/awards/trophies/art-ross-trophy",
          "https://records.nhl.com/awards/trophies/conn-smythe-trophy",
          "https://records.nhl.com/awards/trophies/frank-j-selke-trophy",
          "https://records.nhl.com/awards/trophies/hart-memorial-trophy",
          "https://records.nhl.com/awards/trophies/james-norris-memorial-trophy",
          "https://records.nhl.com/awards/trophies/presidents-trophy",
          "https://records.nhl.com/awards/trophies/prince-of-wales-trophy",
          "https://records.nhl.com/awards/trophies/vezina-trophy"
        ]  
#fix for presidents trophy, prince of wales, vezina - should be added properly now

#rocket richard may need future tweaking

final_links = []
for popper in trophy_links:
    if popper not in to_pop:
        final_links.append(popper)


for link in final_links:
    link_type = findWebType(link)
    award_data, title = getAwardData(link, link_type)

    csv_title = "data/web-scraped/" + str(title.lower()) + ".csv"
    with open(csv_title, 'w') as f:
        write = csv.writer(f)
        write.writerows(award_data)

