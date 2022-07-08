from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd


# url for National Parks Services Park Search
url = "https://www.nps.gov/findapark/advanced-search.htm?&p=1&v=1"

# get the webpage using requests
nps_page = requests.get(url)
#print(nps_page.status_code)

# load the webpage into bs4 object
soup = BeautifulSoup(nps_page.text, "html.parser")

# extract the state names and abbreviations from the webpage
states = []
for select in soup.find_all(name = 'select', attrs = {"id" : "form-park"}):
    for option in select.find_all(name="option"):
        state_abv = [str(option), option.text]
        states.append(state_abv)

# clean the strings into a usable format
for listing in states:
    temp = listing[0].split('"')
    listing[0] = temp[1]
    listing[1] = listing[1].strip()

# using the state list created above, below will loop through each state abbreviation to search the NPS webpage for the parks in those states
search_url = "https://www.nps.gov/state/{0}/index.htm"
park_info = []
for state in states:
    nps_search = requests.get(search_url.format(state[0]))
    search_soup = BeautifulSoup(nps_search.text, "html.parser")
    for div in search_soup.find_all(name="div", attrs={"id" : "parkListResultsArea"}):
        for div2 in div.find_all(name="div", attrs={"class" : "list_left"}):
            park_info_temp = [state[0], state[1], div2.find(name="h2").text, div2.find(name="a").text]
            park_info.append(park_info_temp)
            # print(div2.find(name="h2").text)
            # print(div2.find(name="a").text)

# convert list of lists into a Pandas data frame
park_info_df = pd.DataFrame(park_info)

# change the header names, and change index range to start with 1
park_info_df = park_info_df.set_axis(["State Abbreviation", "State Name", "Site Type", "Site Name"], axis = "columns") 
park_info_df.index = np.arange(1,len(park_info_df)+1)

# export data frame to CSV to be used in PowerBI
#park_info_df.to_csv("Park_Info_Lookup")
