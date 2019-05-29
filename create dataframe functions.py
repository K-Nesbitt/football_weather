#%%
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
%matplotlib inline

plt.style.use('seaborn-darkgrid')

#%%
#This will get the HTML code from the website 
# and save it as a file 'broncos.html'
data = requests.get('http://www.nflweather.com/en/searches/100250')

with open('/Users/keatra/Galvanize/football_weather/data/broncos.html', 'w') as file:
    file.write(data.text)

#%%
# This will create a BeautifulSoup object of our HTML code so we 
# can run the web scrap program.
soup = BeautifulSoup(data.text)


#%%
# This is my actual web scraping code. The function takes the BeautifulSoup object
# that was created from an HTML file and returns the information of the data frame
# for that team.
# This code will find each piece of data, strip away the excess text, 
# and join all pieces together in a tuple. The tuples are then added to a set 
# to eliminate the duplicate games (which I saw on the website).
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
            # There was one game that the weather was recorded as 33/51. Since I could not 
            #definitively determine the weather and it was only one game with this record,
            #I decided to record the temp as NaN for that game. 
            weather_type = soup_object.findAll('div', {'class':'gt-weather'})[i].text.strip().split('f')[1]
        game_row = (date, away_team, away_team_score, home_team, home_team_score, weather_temp, weather_type)
        table_set.add(game_row)
    table_list = list(table_set)
    game_df = pd.DataFrame(table_list, columns = ('Date', 'Away_Team', 'Away_Team_Score', 'Home_Team', 'Home_Team_Score', 'Weather_Temp', 'Weather_Type'))
    return game_df

game_df = web_scrape(soup)

#%%
#The data from the website does not list the winner of the game
#so I will create a new column that denotes if the given team was the winner. 
#I set the values to 1 and 0 instead of True or False to make it easier for graphing.
def win_column(df, team_name):
    for i in range(len(df)):
        if df['Away_Team'][i] == team_name and df['Away_Team_Score'][i] > df['Home_Team_Score'][i]:
            df.at[i,'Win']= 1
        elif df['Home_Team'][i] == team_name and df['Home_Team_Score'][i] > df['Away_Team_Score'][i]:
            df.at[i,'Win'] = 1
        else:
            df.at[i,'Win'] = 0
    return df 

game_win_df = win_column(game_df, 'Denver Broncos')

#%%
#This function will calculate average temp and the number of wins
def calculate_averages(df):
    temp_avg = round(df['Weather_Temp'].mean(skipna=True), 2)
    num_wins_rate = round((df['Win'].sum()/ len(df)), 2)
    print('The average temperature of games from 2009 - 2018 is: ' + str(temp_avg)+ 'degrees Farenheit\n'
    'The average number of wins from 2009 - 2018 is: ' + str(num_wins_rate) + '\n')
    return temp_avg, num_wins_rate

calculate_averages(game_win_df)
#%%
#Plot histogram of temperature values and save the image
temp_avg = round(game_win_df['Weather_Temp'].mean(skipna=True), 2)
below = game_win_df[game_win_df['Weather_Temp'] < temp_avg]
above = game_win_df[game_win_df['Weather_Temp'] > temp_avg]

fig, axs = plt.subplots(3,1, figsize=(8,8))

ax0 = axs[0]
ax0.set_title('Histogram of Temperatures')
ax0.set_xlabel('Temperature in Farenheit')
ax0.set_ylabel('Number of Games')
ax0.hist(game_win_df['Weather_Temp'])


ax1 = axs[1]
ax1.set_title('Histogram of Below Average Temperatures')
ax1.set_xlabel('Temperature in Farenheit')
ax1.set_ylabel('Number of Games')
ax1.hist(below['Weather_Temp'], bins=20)


ax2 = axs[2]
ax2.set_title('Histogram of Above Average Temperatures')
ax2.set_xlabel('Temperature in Farenheit')
ax2.set_ylabel('Number of Games')
ax2.hist(above['Weather_Temp'], bins=20)

plt.tight_layout()
plt.savefig('images/temp_hist',facecolor = 'white' )


#%%
#This will create a dataframe where the temperature 
# is less than the average
def less_than(df):
    temp_avg = round(df['Weather_Temp'].mean(skipna=True), 2)
    wins_only = df[df['Win']==1]
    less = wins_only[wins_only['Weather_Temp']< temp_avg]
    return less

below_temp = less_than(game_win_df)

#%%
#This is a histogram of the below average temperature games that Broncos won
fig, ax = plt.subplots(figsize=(8,4))
ax.set_title('Histogram of Below Average Temperatures')
ax.set_xlabel('Temperature in Farenheit')
ax.set_ylabel('Number of Games')
ax.hist(below_temp['Weather_Temp'])
plt.savefig('images/below_temp_wins',facecolor = 'white' )
#%%
#This will create a dataframe where the temperature is 
#greater than the average
def greater_than(df):
    temp_avg = round(df['Weather_Temp'].mean(skipna=True), 2)
    wins_only = df[df['Win']==1]
    greater = wins_only[wins_only['Weather_Temp'] > temp_avg]
    return greater

above_temp = greater_than(game_win_df)

#%%
#This is a histogram of the above average temperature games that Broncos won
fig, ax = plt.subplots(figsize=(8,4))
ax.set_title('Histogram of Above Average Temperatures')
ax.set_xlabel('Temperature in Farenheit')
ax.set_ylabel('Number of Games')
ax.hist(above_temp['Weather_Temp'])
plt.savefig('images/above_temp_wins',facecolor = 'white' )
#%%
#This will create a random selection from each dataframe and 
#%%
#This function will create a new dataframe with the Date, Score (for just the desired team),
# and the temperature of the game. This dataframe may be useful to see if weather affects
#the average score of the game.
def team_scores(df, team_name):
    new_df = pd.DataFrame()
    for i in range(len(df)):
        new_df.at[i,'Date'] = df['Date'][i]
        new_df.at[i,'Score'] = df['Away_Team_Score'][i] if df['Away_Team'][i] == team_name else df['Home_Team_Score'][i]
        new_df.at[i, 'Weather_Temp'] = df['Weather_Temp'][i]
    return new_df
t_score = team_scores(game_win_df, 'Denver Broncos')

#%%

