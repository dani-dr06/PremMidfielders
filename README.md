# Premier League Midfielder Analysis

## Project Summary

- Scraped midfielder statistics from the Premier League site.

- Performed clustering analysis of midfielders into 3 separe groups (clusters).

- Created a Dash app to display cluster attribute comparisons.


## Project Overview
For this project, I decided to combine two things I love, data and soccer (or football). I wanted to put myself in the shoes of one of the smaller clubs in the Premier League and imagine I need to sign a new defensive midfielder for my team, as one of my starting defensive midfielders left the club. Data can provide impactful insights as to who would be an appropriate signing for the team.


## Data
I obtained statistics for over 100 Premier League midfielders from the [Premier League website](https://www.premierleague.com/stats). These statistics cover each player's entire Premier League career.

***See scraper.py***

## Project Steps

1. **Data Collection and Preprocessing**:
   - Obtained data using the **scraper.py** script
   - Transformed and stored data in CSV format.

2. **Clustering Analysis**:
   - Clustered players into 3 clusters, after finding 3 clusters to be the optimal number of clusters.
        - Cluster 0 showed great prowess in attacking facets of the game (Goals, Assists, Chances Created, etc.)
        - Cluster 1 resembled defensive midfielders, as they exceled at 
        defensive duties.
        - Cluster 2 midfielders did not excel at any particular task, but instead showed greater balance across statistics.

3. **Dash App**
    - Created a dashboard with multiple visualizations and functionalities.

    - Visualized differences in statistics between clusters.

    - Created a player recommendation section which allows user to find defensive midfielders which best meet their requirements for certain abilities (Tackling, Passing, Scoring, etc.).

    - Created a player comparison section to allow for an in depth comparison between 2 midfielders.

    


## Results and Conclusion
Under the assumption that we were in the shoes of a smaller club in the Premier League, I filtered for midfielders with a market value under 35M Euro. Based on this price filter, clustering results, and player analysis performed both in the Jupyter Notebook and through the player comparison feature , if looking for a purely defensive midfielder, I would recommend two options: Wilfred Ndidi and Idrissa Gueye.

However, there are certain aspects to take into consideration that I did not in this analysis. For example, age is an important factor in soccer transfers. Not only will signing a young player ensure that you have the position covered for a longer time, younger players also have room to grow and learn new skills, meaning a differing performance in the future, both in terms of quality and role on the pitch. Furthermore, younger players tend to have higher market value. Another important piece of missing information is what kind of team these players play for, as that certainly affects their statistics; both through team quality and team style of play (e.g., possession-based pressing team vs. defensive-minded counter attacking teams), the team a player belongs to has a massive impact on their performance and role.


## Scripts
1. scraper.py: used to collect data
2. dataloader.py: helper script with function to load data for Dash app
3. app.py: Dash app
4. PremAnalysis.ipynb: notebook file used to perform data exploration and clustering analysis prior to creating Dash app.