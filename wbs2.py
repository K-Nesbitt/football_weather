#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
%matplotlib inline

#%%
x = requests.get('http://www.nflweather.com/en/searches/100250')
soup = BeautifulSoup(x.text)

#%%
games = soup.findAll(class_= 'span3 wbkg')
len(games)

#%%
soup.findAll('div', {'class':'gt-header'})[0].text.strip().split('\n')[0]

#%%
away_team = soup.findAll('div', {'class':'gt-away'})
away_team[0].text.strip().split('\n')

#%%
home_team = soup.findAll('div', {'class':'gt-home'})
home_team[0].text.strip().split('\n')

#%%
weather = soup.findAll('div', {'class':'gt-weather'})
weather[0].text.strip().split('f')

#%%
table_set = set()
for i in range(len(games)):
    
    date = soup.findAll('div', {'class':'gt-header'})[i].text.strip().split('\n')[0]
    away_team = soup.findAll('div', {'class':'gt-away'})[i].text.strip().split('\n')[0]
    away_team_score = soup.findAll('div', {'class':'gt-away'})[i].text.strip().split('\n')[1]
    home_team = soup.findAll('div', {'class':'gt-home'})[i].text.strip().split('\n')[0]
    home_team_score = soup.findAll('div', {'class':'gt-home'})[i].text.strip().split('\n')[1]
    weather_temp = soup.findAll('div', {'class':'gt-weather'})[i].text.strip().split('f')[0]
    if weather_temp == 'DOME':
        weather_type = None
    else:
        weather_type = soup.findAll('div', {'class':'gt-weather'})[i].text.strip().split('f')[1]
    game_row = (date, away_team, away_team_score, home_team, home_team_score, weather_temp, weather_type)
    table_set.add(game_row)

#%%

   
#%%
table_list = list(table_set)
game_df = pd.DataFrame(table_list, columns = ('Date', 'Away_Team', 'Away_Team_Score', 'Home_Team', 'Home_Team_Score', 'Weather_Temp', 'Weather_Type'))

#%%
game_df.info()


#%%
