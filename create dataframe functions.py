#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
%matplotlib inline

plt.style.use('seaborn-darkgrid')

#%%
#This will get the HTML code from the website and save it as a file 
data = requests.get('http://www.nflweather.com/en/searches/100250')

with open('/Users/keatra/Galvanize/football_weather/data/broncos.html', 'w') as file:
    file.write(data.text)

#%%
# This will create a BeautifulSoup object of our HTML code so we can run
# the web scrap program.
soup = BeautifulSoup(data.text)


#%%
# This is my actual web scraping code. The function takes the BeautifulSoup object
# that was created from an HTML file and returns the information of the data frame
# for that team.
# There are a total of 390 boxes. However, there are 4 boxes of information 
# for each game, 1 per quarter, since each game is now listed as 'Final', 
# we only need one box per game. This code will find each piece of data, 
# strip away the excess text, and join all pieces together in a tuple. 
# The tuples are then added to a set to eliminate the duplicate games. 
def web_scrape(soup_object):
    team_data = soup_object.findAll(class_= 'span3 wbkg')
    table_set = set()
    for i in range(len(team_data)):
        date = soup_object.findAll('div', {'class':'gt-header'})[i].text.strip().split('\n')[0]
        away_team = soup_object.findAll('div', {'class':'gt-away'})[i].text.strip().split('\n')[0]
        away_team_score = soup_object.findAll('div', {'class':'gt-away'})[i].text.strip().split('\n')[1]
        home_team = soup_object.findAll('div', {'class':'gt-home'})[i].text.strip().split('\n')[0]
        home_team_score = soup_object.findAll('div', {'class':'gt-home'})[i].text.strip().split('\n')[1]
        weather = soup_object.findAll('div', {'class':'gt-weather'})[i].text.strip().split('f')[0]
        if weather == 'DOME':
            weather_temp = np.NaN
            weather_type = 'DOME'
        else:
            weather_temp = int(float(weather)) if '/' not in weather else np.NaN
            weather_type = soup_object.findAll('div', {'class':'gt-weather'})[i].text.strip().split('f')[1]
        game_row = (date, away_team, away_team_score, home_team, home_team_score, weather_temp, weather_type)
        table_set.add(game_row)
    table_list = list(table_set)
    game_df = pd.DataFrame(table_list, columns = ('Date', 'Away_Team', 'Away_Team_Score', 'Home_Team', 'Home_Team_Score', 'Weather_Temp', 'Weather_Type'))
    return game_df

game_df = web_scrape(soup)

#%%
#The data from the website does not list the winner of the game
# so I will create a new column that denotes if the given team was the winner
def win_column(df, team_name):
    for i in range(len(df)):
        if df['Away_Team'][i] == team_name and df['Away_Team_Score'][i] > df['Home_Team_Score'][i]:
            df.at[i,'Win']= True
        elif df['Home_Team'][i] == team_name and df['Home_Team_Score'][i] > df['Away_Team_Score'][i]:
            df.at[i,'Win'] = True
        else:
            df.at[i,'Win'] = False
    return df 

game_win_df = win_column(game_df, 'Denver Broncos')

#%%
#This function will calculate the mean of different columns of the dataframe
def calculate_averages(df):
    temp_avg = round(df['Weather_Temp'].mean(skipna=True), 2)
    num_wins = df['Win'].sum()
    wins_temp_avg = round(df[df['Win']]['Weather_Temp'].mean(skipna=True), 2)
    print('The average temperature of games from 2009 - 2018 is: ' + str(temp_avg)+ 'degrees Farenheit\n'
    'The average number of wins from 2009 - 2018 is: ' + str(num_wins) + '\n'
    'The average temperature for winning games is: ' + str(wins_temp_avg))
    return temp_avg, num_wins, wins_temp_avg

calculate_averages(game_win_df)
#%%
#Plot histogram of temperature values and wins
fig, ax = plt.subplots(figsize=(8,4))

ax.set_title('Histogram of Temperatures', color='black')
ax.set_xlabel('Temperature in Farenheit', color='black')
ax.set_ylabel('Number of Games', color='black')
ax.hist(game_win_df['Weather_Temp'])
plt.savefig('images/temp_hist')
#%%
fig, ax = plt.subplots(figsize=(8,4))
ax.set_title('Temperature by Score')
ax.set_xlabel('Temperature')
ax.set_ylabel('Number of Points')
ax.plot(x = temp, y = score)

