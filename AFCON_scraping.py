# CHANGE URL & FEATURES WANTED

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import sys, getopt
import csv

def scrapeURL(url):
    res = requests.get(url)
    ## The next two lines get around the issue with comments breaking the parsing.
    comm = re.compile("<!--|-->")
    soup = BeautifulSoup(comm.sub("",res.text),'lxml')
    all_tables = soup.findAll("tbody")
    team_table = all_tables[0]
    player_table = all_tables[2]

    #Parse player_table
    pre_df_player = dict()
    features_wanted_player = {"player": 'Player',"position": 'Position', "team": 'Team', "age": 'Age', "games": 'Matches Played', "games_starts": 'Games Started', "minutes": 'Minutes', "minutes_90s": 'Minutes Per90', "goals": 'Goals', "assists": 'Assists', "goals_assists": 'Goals\Assists', "goals_pens": 'Non-Penalty Goals', "pens_made": 'Penalty Goals', "pens_att": 'Penalty Attempted', "cards_yellow": 'Yellow Cards', "cards_red": 'Red Cards', "goals_per90": 'Goals Per90', "assists_per90": 'Assists Per90', "goals_assists_per90": 'Goals\Assists Per90', "goals_pens_per90": 'Non-Penalty Goals Per90', "goals_assists_pens_per90": 'Non-Penalty Goals\Assists Per90'}
    rows_player = player_table.find_all('tr')
    for row in rows_player:
        if(row.find('th',{"scope":"row"}) != None):
            for f in features_wanted_player:
                cell = row.find("td",{"data-stat": f})
                if cell is not None:
                    if f == "team":
                        text = cell.find('a').text.strip()
                    else:    
                        text = cell.text.strip()
                else:
                    text = None
                feature_name = features_wanted_player[f]    
                if feature_name in pre_df_player:
                    pre_df_player[feature_name].append(text)
                else:
                    pre_df_player[feature_name] = [text]
    df_player = pd.DataFrame.from_dict(pre_df_player)
   
    #Parse team_table
    pre_df_squad = dict()
    #Note: features does not contain squad name, it requires special treatment
    features_wanted_squad = {"players_used": 'Number of Players', "avg_age": 'Averagae Age', "possession": 'Possession', "games": 'Matches Played', "goals": 'Goals', "assists": 'Assists', "goals_pens": 'Non-Penalty Goals', "pens_made": 'Penalty Goals', "pens_att": 'Penalty Attempted', "cards_yellow": 'Yellow Cards', "cards_red": 'Red Cards', "goals_per90": 'Goals per90', "assists_per90": 'Assists per90', "goals_pens_per90": 'Non-Penalty Goals per90'}
    rows_squad = team_table.find_all('tr')
    for row in rows_squad:
        if(row.find('th',{"scope":"row"}) != None):
            name = row.find('th',{"data-stat":"team"}).find('a').text.strip()
            if 'Team' in pre_df_squad:
                pre_df_squad['Team'].append(name)
            else:
                pre_df_squad['Team'] = [name]              
            for f in features_wanted_squad:
                cell = row.find("td",{"data-stat": f})
                if cell is not None:
                    text = cell.text.strip()
                else:
                    text = None
                feature_name = features_wanted_squad[f]     
                if feature_name in pre_df_squad:
                    pre_df_squad[feature_name].append(text)
                else:
                   pre_df_squad[feature_name] = [text]
    df_squad = pd.DataFrame.from_dict(pre_df_squad)
    
    return df_player, df_squad
    
    
def main(url):
    print(url)
    df_player, df_squad = scrapeURL(url)
    df_player.to_csv("AFCON Players Stats.csv")
    df_squad.to_csv("AFCON Squads Stats.csv")

    print(" SUCCESS !")
    


main("https://fbref.com/en/comps/656/2024/stats/2024-league-Stats")