#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np 

#%%
# The function takes the url of the website for the team data, and the filename you want to save it as. 
# You must pass in the full url because in order to get team data from nflweather.com you must first search for a specific team. 

# This code will find each piece of data, strip away the excess text, 
# and join all pieces together in a tuple. The tuples are then added to a set 
# to eliminate the duplicate games (which I saw on the website).

def web_scrape(url, filename):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, features="lxml")
    team_data = soup.findAll(class_= 'span3 wbkg')

    table_set = set()
    for i in range(len(team_data)):
        
        date = soup.findAll('div', {'class':'gt-header'})[i].text.strip().split('\n')[0]
        away_team = soup.findAll('div', {'class':'gt-away'})[i].text.strip().split('\n')[0]
        away_team_score = soup.findAll('div', {'class':'gt-away'})[i].text.strip().split('\n')[1]
        home_team = soup.findAll('div', {'class':'gt-home'})[i].text.strip().split('\n')[0]
        home_team_score = soup.findAll('div', {'class':'gt-home'})[i].text.strip().split('\n')[1]
        weather = soup.findAll('div', {'class':'gt-weather'})[i].text.strip().split('f')[0]
        if weather == 'DOME':
            weather_temp = np.NaN
            weather_type = 'DOME'
        else:
            weather_temp = np.int(weather) if '/' not in weather else np.NaN 
            # There was one game that the weather was recorded as 33/51. Since I could not 
            #definitively determine the weather and it was only one game with this record,
            #I decided to record the temp as NaN for that game. 
            weather_type = soup.findAll('div', {'class':'gt-weather'})[i].text.strip().split('f')[1]
        game_row = (date, away_team, np.int(away_team_score), home_team, np.int(home_team_score), weather_temp, weather_type)
        table_set.add(game_row)
    table_list = list(table_set)
    df = pd.DataFrame(table_list, columns = ('Date', 'Away_Team', 'Away_Team_Score', 'Home_Team', 'Home_Team_Score', 'Weather_Temp', 'Weather_Type'))
    df.to_csv(filename)
    return None

web_scrape('http://www.nflweather.com/en/searches/100257', 'data/broncos_df')

web_scrape('http://www.nflweather.com/en/searches/100258', 'data/dolphins_df')




#%%
