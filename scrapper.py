import pandas as pd
import requests
pd.set_option('display.max_columns', None) # To be able to see all columns in a wide data frame
import time 
import numpy as np


test_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season=2012-13&SeasonType=Regular%20Season&StatCategory=PTS'
r = requests.get(test_url).json()

table_headers = r['resultSet']['headers']

df_cols = ['Year', 'Season_type'] + table_headers
df = pd.DataFrame(columns=df_cols)

season_types = ['Regular%20Season', 'Playoffs']
years = ['2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22', '2022-23']
begin_loop = time.time()
for year in years:
  for season in season_types:
    api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=Totals&Scope=S&Season='+year+'&SeasonType='+season+'&StatCategory=PTS'
    r = requests.get(url=api_url).json()
    temp_df1 = pd.DataFrame(r['resultSet']['rowSet'], columns=table_headers)
    temp_df2 = pd.DataFrame({'Year':[year for i in range(len(temp_df1))],
                            'Season_type':[season for i in range(len(temp_df1))]})
    temp_df3 = pd.concat([temp_df2, temp_df1], axis = 1) # concat on columns
    df = pd.concat([df, temp_df3], axis = 0) # concat on index
"""
Sometimes there are bugs that cause the program not to run due to some error and the extraction is not complete. 
If you can't run the code, try adding these comment lines for a less "robotic" extraction behavior to see if you can extract the data. 
I had no problem extracting without the lag time. 

    print(f'Finished scrapping data for the {year} {season}.')
    lag = np.random.uniform(low=5, high=40)
    print(f'...waiting {round(lag, 1)} seconds')
    time.sleep(lag)
print(f'Process completed! Total run time: {round((time.time() - begin_loop)/60, 2)}')
"""
df.to_csv('nba_players_data.csv', index=False)