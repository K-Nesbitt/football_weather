#%%
from main_functions import *
import numpy as np 
import pandas as pd 

%load_ext autoreload
%autoreload 2

plt.style.use('seaborn-darkgrid')
%matplotlib inline

#%%
broncos_df = pd.read_csv('data/broncos_df', index_col=0)
win_column(broncos_df, 'Denver Broncos')
#%%
broncos_df.info()

#%%
calculate_averages(broncos_df)

#%%
temp_hist_plot(broncos_df, 'broncos_temp_hist')
hist_win_loss(broncos_df, 'broncos_win_loss')


#%%
#Discovering why there is a peak in the temp range(70,75)
temp_70 = broncos_df[broncos_df['Weather_Temp'].between(70,75, inclusive=True)].reset_index()
len(temp_70)

#%%
#Do we have more home games with this temperature?
home_70 = temp_70[temp_70['Home_Team']=='Denver Broncos']
len(home_70)/len(temp_70)

#%%
below_above_ttest(broncos_df)

#%%
win_loss_ttest(broncos_df)

#%%
broncos_scores = team_scores(broncos_df, 'Denver Broncos')
broncos_scores.info()


#%%
score_averages(broncos_scores)

#%%
below_above_ttest(broncos_scores, column_name='Score')

#%%
plot_temp_score(broncos_scores, 'broncos_score_plot')

#%%
