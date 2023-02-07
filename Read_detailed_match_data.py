import pandas as pd
'''Each match history, has the 8 players combined boards in JSON, so you have 8 json entries to deal with.
so when you print row0, you're getting first game. There are 20 games. 20*8 160 json entries, 
 For example, you can have a "Match" table with columns such as "Match ID", "Level", "Placement", etc. Then you can have an 
 "Augments" table with columns "Match ID" and "Augment". Similarly, you can have tables for "Companion", "Traits", and "Units"
  with columns specific to their respective data. Finally, you can join the tables using the "Match ID" column as a key to 
  access the complete information about a match. '''

# data = {'augments': ['TFT6_Augment_SunfireBoard', 'TFT8_Augment_MalphiteSupport', 'TFT6_Augment_PortableForge'], 
#        'companion': {'content_ID': '489abd90-0929-447d-ba51-0326e0aa5469', 'item_ID': 42024, 'skin_ID': 24, 'species': 'PetDuckbill'}, 
#        'gold_left': 0, 'last_round': 38, 'level': 8, 'placement': 2, 'players_eliminated': 2, 

#        'puuid': 'KpEBEmPbOYu3PFA_zzhP4lDGNP8xVQVr7AiJM8YF8vmasWRBQMVTcVqf4XVg5i8rnD3tzxbaxNiq3w', 

#        'time_eliminated': 2209.98779296875, 'total_damage_to_players': 162, 
#        'traits': [{'name': 'Set8_AnimaSquad', 'num_units': 1, 'style': 0, 'tier_current': 0, 'tier_total': 3}, 
#                   {'name': 'Set8_Brawler', 'num_units': 2, 'style': 1, 'tier_current': 1, 'tier_total': 4}, 
#                   {'name': 'Set8_Defender', 'num_units': 2, 'style': 1, 'tier_current': 1, 'tier_total': 3}, 
#                   {'name': 'Set8_Duelist', 'num_units': 2, 'style': 1, 'tier_current': 1, 'tier_total': 4}, 
#                   {'name': 'Set8_Heart', 'num_units': 2, 'style': 1, 'tier_current': 1, 'tier_total': 3}, 
#                   {'name': 'Set8_Mascot', 'num_units': 2, 'style': 1, 'tier_current': 1, 'tier_total': 4}, 
#                   {'name': 'Set8_Recon', 'num_units': 1, 'style': 0, 'tier_current': 0, 'tier_total': 3}, 
#                   {'name': 'Set8_StarGuardian', 'num_units': 4, 'style': 1, 'tier_current': 1, 'tier_total': 4}, 
#                   {'name': 'Set8_Supers', 'num_units': 3, 'style': 3, 'tier_current': 1, 'tier_total': 1}], 
#        'units': [{'character_id': 'TFT8_Gangplank', 'itemNames': [], 'items': [], 'name': '', 'rarity': 0, 'tier': 2}, 
#                  {'character_id': 'TFT8_Rell', 'itemNames': ['TFT_Item_GuardianAngel', 'TFT_Item_RabadonsDeathcap'], 
#                   'items': [94, 33], 'name': 
# The data ends up looking like this, so you need to break it apart basically
# You would need a match id table containing name, gold_left, last_round, level, placements_ players_elim, 
# then an augments for that specific match_id, and units, and that needs to be done for each player 


read_data_df = pd.read_csv('detailed_matches3.csv', index_col=False)

# print(read_data_df)

row0 = read_data_df.loc[0]
# print(row0)
single_row = ''
for row in row0:
    print(row)
    print(type(row))
    single_row += row
    break

# print(read_data_df.m1.to_string(index=False))