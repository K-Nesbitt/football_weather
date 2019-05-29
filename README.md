# Football and Weather
This project is aimed at determining if a win can be predicted based upon the weather at the game. We will also consider the average score depending on the weather. 

I found the data of all games from 2009 to 2018 on the website: http://www.nflweather.com/. We will first investigate the SuperBowl 50 Champions, the Denver Broncos. 

## During  EDA I found:
The total games in my data set were 210. 
The average temperature of the games was 62 degrees Farenheit.
The winning rate was 0.54 (113/210).
Here are some histograms of the data:

![hist1](https://github.com/K-Nesbitt/football_weather/blob/master/images/temp_hist.png)

![hist2](https://github.com/K-Nesbitt/football_weather/blob/master/images/temp_win_loss.png)

## Statistical Test Elements:
1. H_0: The winning rate is 0.54, no matter the temperature
2. H_A: The winning rate will increase or decrease, DEPENDING on the temperature
3. The statistical test I will use is a Bonferroni Test. A Bonferroni is a T-test that specifies that we have n samples and thus alpha is divided by the n.
4. Since there are two samples that I am comparing, alpha  = 0.05/2 = 0.025.

## Results
I ran a T-test on two samples of data; games that were below average temperature, and games that were above average temperature. 

      stat, pval = stats.ttest_ind(sample_l['Win'], sample_g['Win'], equal_var=False)
      
    

By the histograms from above I hypothesized that there would be a some difference. However, my T-test yielded these results:

      The statistic value is -0.601 and the pvalue is 0.549
      
    



