# Football and Weather
This project is aimed at determining if a win can be predicted based upon the weather at the game. We will also consider the average score depending on the weather. 

I chose this project because of my general interest in football and how athletes perform under different conditions. 

I found the data of all games from 2009 to 2018 on the website: http://www.nflweather.com/. We will first investigate the SuperBowl 50 Champions, the Denver Broncos. 

## During  EDA I found:
The total games in my data set were 210. 
The average temperature of the games was 62 degrees Farenheit.
The winning rate was 0.54 (113/210).
Here are some histograms of the data:

![hist1](https://github.com/K-Nesbitt/football_weather/blob/master/images/broncos_temp_hist.png)

![hist2](https://github.com/K-Nesbitt/football_weather/blob/master/images/broncos_win_loss.png)

You can see in the above graph that there is a spike in the number of games in the range from about 70-75. There were exactly 32 games where the temperature was between 70 and 75 degrees Farenheit. About 56% of these games were at home so I considered what the average temperature is in Denver, CO during Football season (mainly Aug - Dec):

![weather graph](https://github.com/K-Nesbitt/football_weather/blob/master/images/Screen%20Shot%202019-05-30%20at%202.41.33%20PM.png)

This again seems puzzling since there is only one month were the average temperature is close to the peak temperature range. 

I looked into these games specifically to see if there were any other trends (dates, home vs away games, etc) but none were found. Here is a print out of the [data:](https://github.com/K-Nesbitt/football_weather/blob/master/data/Screen%20Shot%202019-05-30%20at%201.16.54%20PM.png)

## Statistical Test Elements:
1. Null Hypothesis: The sample means (winning rate) are identical
2. Alternative Hypothesis: The sample means are not identical
3. The statistical test I will use is a Bonferroni Test. A Bonferroni is a type of T-test that compares n samples.
4. Since there are two samples that I am comparing, alpha  = 0.05/2 = 0.025.

## Results
I ran a T-test on two samples of data; games that were below average temperature, and games that were above average temperature. 

      def below_above_ttest(df, column_name='Win'):
          temp_avg = round(df['Weather_Temp'].mean(skipna=True), 0)
          below = df[df['Weather_Temp']< temp_avg]
          above = df[df['Weather_Temp'] > temp_avg]
          stat, pval = stats.ttest_ind(below[column_name], above[column_name], equal_var=False)
          print('The statistic value is {} and the pvalue is {}'.format(round(stat, 3), round(pval, 3)))
                

By the histograms from above I hypothesized that there would be a some difference. The first time I ran a T-test on random samples of 50 and yielded these results:

      The statistic value is -0.601 and the pvalue is 0.549

I then ran the same test on the entire population and received these results:
      
      The statistic value is -2.945 and the pvalue is 0.004
     
I was apprehensive of this value since it was drastically different than my sample results. 

Out of curiosity and further wanting to check my hypothesis, I decided to run another T-test on two different samples. This time I created a sample of games won and of games lost. I then ran the T-Test against the weather of theses two samples. 

       The statistic value is -0.386 and the pvalue is 0.7

I then ran the same test against the entire population and not just a sample. These were the results:

      The statistic value is 2.203 and the pvalue is 0.029
      
The first p-value would lead me to reject the Null Hypothesis since it is less than my significance level. However, the second p-value is slightly higher than the significance level so I have failed to reject the Null Hypothesis. I assume that the first p-value is in the Type 1 error range and am rejecting even though it is True. 


The second hypothesis that I wanted to test was if there was a significant difference in the scores for low or high temperatures. To run this test I had to create a dataframe that had the date, score (specifically Denver), and the temperature. When I tested a sample of 50, I received these results:

     The statistic value is 0.489 and the pvalue is 0.626
 
 I then tested the entire population and my values changed to:
 
      The statistic value is -1.881 and the pvalue is 0.062
 
![plot1](https://github.com/K-Nesbitt/football_weather/blob/master/images/broncos_score_plot.png)

I am still unable to reject the Null Hypothesis. The average score for all games is 23.44 points, for games that are      below 62 degrees the average score is 22.04 points, and games that are above 62 degrees the average score is 24.78 points. 


## Reflection
I was unable to reject the Null Hypothesis that weather has no affect on the mean score, or chance of winning. 
I will need to collect more data or change my sample population to determine if I can reject the Null Hypothesis. 

For further study I would consider other teams and their conditions. For example, a team that has a home stadium average temperature around 80 degrees to determine if they play worse in colder temperatures. I can also consider teams that play in a Dome. 

## References
1. NFLWeather.com, http://www.nflweather.com/en/
2. TheWeatherChannel.com, https://weather.com/weather/monthly/l/675c2b6342b3512ea4f15bc9070663be6e36cc4bf61056076c500098c8eb3bbe


