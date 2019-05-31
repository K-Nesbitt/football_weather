#%%
from scipy import stats
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-darkgrid')

#%%
#The data from the website does not list the winner of the game
#so I will create a new column that denotes if the given team was the winner. 
#I set the values to 1 and 0 instead of True or False to make it easier for graphing.
def win_column(df, team_name):
    df['Win']= 0
    for i in range(len(df)):
        if df['Away_Team'][i] == team_name and df['Away_Team_Score'][i] > df['Home_Team_Score'][i]:
            df.at[i,'Win']= 1
        elif df['Home_Team'][i] == team_name and df['Home_Team_Score'][i] > df['Away_Team_Score'][i]:
            df.at[i,'Win'] = 1
        else:
            df.at[i,'Win'] = 0
    return df

#%%
#This function will calculate average temp and the number of wins
def calculate_averages(df):
    temp_avg = round(df['Weather_Temp'].mean(skipna=True), 2)
    num_wins_rate = round((df['Win'].sum()/ len(df)), 2)
    print('The average temperature of games from 2009 - 2018 is: ' + str(temp_avg)+ ' degrees Farenheit\n'
    'The average number of wins from 2009 - 2018 is: ' + str(num_wins_rate) + '\n')
    return temp_avg, num_wins_rate

#%%
#This function will plot a histogram of temperature values 
# when you pass in a dataframe and save the image as the specified title
def temp_hist_plot(df, filename):
    temp_avg = round(df['Weather_Temp'].mean(skipna=True), 2)
    below = df[df['Weather_Temp'] < temp_avg]
    above = df[df['Weather_Temp'] > temp_avg]

    fig, axs = plt.subplots(3,1, figsize=(8,8))

    ax0 = axs[0]
    ax0.set_title('Histogram of Temperatures')
    ax0.set_xlabel('Temperature in Farenheit')
    ax0.set_ylabel('Number of Games')
    ax0.hist(df['Weather_Temp'])


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
    plt.savefig('images/{}'.format(filename),facecolor = 'white' )
    return fig, axs

#%%
#This function will plot two histograms of the temperature
#for games won and games lost. 
def hist_win_loss(df, filename):
    win = df[df['Win']==1]
    lost = df[df['Win']!=1]
    
    fig, axs = plt.subplots(1,2, sharey=True, figsize = (8,8))

    ax0 = axs[0]
    ax0.set_title('Temperature by Games Won')
    ax0.set_xlabel('Temperature')
    ax0.set_ylabel('Number of Games')
    ax0.hist(win['Weather_Temp'], bins=10)

    ax1 = axs[1]
    ax1.set_title('Temperature by Games Lost')
    ax1.set_xlabel('Temperature')
    ax1.hist(lost['Weather_Temp'], bins=10)

    plt.tight_layout()
    plt.savefig('images/{}'.format(filename), facecolor = 'white')
    return fig, axs

#%%
#This will create two dataframes where the temperature 
# is less than or greater than the average. Take a sample of those 
#dataframes, and then run a test on the samples to determine if 
#their mean values are significantly different. Some default values were established
#but they were included in the definition for future ability to change.

def below_above_ttest(df, column_name='Win'):
    temp_avg = round(df['Weather_Temp'].mean(skipna=True), 0)
    below = df[df['Weather_Temp']< temp_avg]
    above = df[df['Weather_Temp'] > temp_avg]
    
    stat, pval = stats.ttest_ind(below[column_name], above[column_name], equal_var=False)
    print('The statistic value is {} and the pvalue is {}'.format(round(stat, 3), round(pval, 3)))


#%%
#This will create two dataframes of games won and games lost. Take a sample of those 
#dataframes, and then run a test on the samples to determine if 
#their mean values are significantly different. Some default values were established
#but they were included in the definition for future ability to change.

def win_loss_ttest(df, n=50, column_name='Weather_Temp'):
    win = df[df['Win']==1]
    lost = df[df['Win']!=1]

    stat, pval = stats.ttest_ind(win[column_name], lost[column_name], equal_var=False, nan_policy='omit')
    print('The statistic value is {} and the pvalue is {}'.format(round(stat, 3), round(pval, 3)))


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


#%%
#This function will return the average score of all games,
# games below average temperature, and games above average temperature

def score_averages(df):
    temp_avg = round(df['Weather_Temp'].mean(skipna=True), 0)
    below = df[df['Weather_Temp']< temp_avg]
    above = df[df['Weather_Temp'] > temp_avg]
    mean, below_mean, above_mean = round(df['Score'].mean(), 2), round(below['Score'].mean(),2), round(above['Score'].mean(),2)
   
    print('The average score of all games is '+ str(mean)+ '\n')
    print('The average score of games below average temperature is '+ str(below_mean)+ '\n')
    print('The average score of games above average temperature is ' + str(above_mean))


#%%
#This function will create a plot of score values by temperature. 
def plot_temp_score(df, filename):
    temp_avg = round(df['Weather_Temp'].mean(skipna=True), 0)
    below = df[df['Weather_Temp']< temp_avg]
    above = df[df['Weather_Temp'] > temp_avg]
    ax = plt.subplot()
    ax.set_title('Temperature vs. Score')
    ax.set_xlabel('Temperature of Game')
    ax.set_ylabel('Game Score')
    ax.plot(below['Weather_Temp'], below['Score'], 'bo')
    ax.plot(above['Weather_Temp'], above['Score'], 'ro')
    ax.axhline(df['Score'].mean(), color='yellow',  linewidth=4)
    ax.annotate('Average Score', xy=(90,24))
    plt.savefig('images/{}'.format(filename), facecolor = 'white')
#%%
