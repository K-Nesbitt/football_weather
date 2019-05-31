#%%
from main_functions import *
import numpy as np 
import pandas as pd 

%load_ext autoreload
%autoreload 2

plt.style.use('seaborn-darkgrid')
%matplotlib inline

#%%
dolphins_df = pd.read_csv('data/dolphins_df', index_col=0)
win_column(dolphins_df, 'Miami Dolphins')
#%%
dolphins_df.tail()
#%%
calculate_averages(dolphins_df)

#%%

temp_hist_plot(dolphins_df, 'dolphins_temp_hist')
hist_win_loss(dolphins_df, 'dolphins_win_loss')

#%%
below_above_ttest(dolphins_df)

#%%
win_loss_ttest(dolphins_df)

#%%
dolphins_scores = team_scores(dolphins_df, 'Miami Dolphins')
dolphins_scores.head()

#%%
score_averages(dolphins_scores)

#%%
below_above_ttest(dolphins_scores, column_name='Score')

#%%
plot_temp_score(dolphins_scores, 'dolphins_score_plot')
