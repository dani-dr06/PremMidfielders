import pandas as pd

def prepare_data():

    # features used for clustering (copied from notebook file)
    features = [
        # attacking stats
        'Goals per match', 'Shots_PA', 'Shooting accuracy %',
        
        # defensive stats
        'Tackles_PA', 'Interceptions_PA', 
        'Recoveries_PA', 'Duels_won_PA', 'Tackle success %', 'Aerial_battles_won_PA',
        
        # playmaking stats
        'Assists_PA', 'Passes per match', 'Through_balls_PA', "Accurate_long_balls_PA",
        'Big_chances_PA'
    ]

    # new names for columns to make dashboard more aesthetically pleasing
    new_column_names = [
        # attacking stats
        'Goals', 'Shots', 'Shooting accuracy %',
        
        # defensive stats
        'Tackles', 'Interceptions', 
        'Recoveries', 'Duels won', 'Tackle success %', 'Aerial battles won',
        
        # playmaking stats
        'Assists', 'Passes', 'Through balls', "Accurate long balls",
        'Big chances created'
    ]

    # create a dictionary to use with pandas rename function
    column_dict = {old_name: new_name for old_name, new_name in zip(features, new_column_names)}

    # read in our dfs we saved in notebook
    cluster_stat_averages = pd.read_csv( "data/dash/Cluster_avg.csv", index_col=0)
    cluster_stat_averages.rename(columns=column_dict, inplace=True) # rename cols

    player_stats = pd.read_csv("data/dash/Clustered_player_stats.csv", usecols=['Player_Name', "Cluster", "Market Value (M Euro)"]+features)
    player_stats.rename(columns=column_dict, inplace=True) # rename cols
    player_stats.sort_values('Player_Name', inplace=True)

    # normalized_player_stats = pd.read_csv("data/dash/Normalized_player_stats.csv")
    # normalized_player_stats.rename(columns=column_dict, inplace=True) # rename cols

    # min max normalized stats
    normalized_player_stats = player_stats[['Player_Name', "Cluster", "Market Value (M Euro)"]].join(
        (player_stats[new_column_names] - player_stats[new_column_names].min()) / (player_stats[new_column_names].max() - player_stats[new_column_names].min())
        )

    # create a list with "player name - cluster" for dropdown menus in dash app
    player_names_and_clusters = [{"label": f"{name} - {cluster}", "value": name} for name, cluster in zip(player_stats['Player_Name'], player_stats['Cluster'])]

    return cluster_stat_averages, player_stats, normalized_player_stats, new_column_names, player_names_and_clusters
