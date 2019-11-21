'''
Lucky Chowdhury 
SI 206 Fall'18
Final Project - Visualization #2: Scatter Plot
'''

import matplotlib
import matplotlib.pyplot as plt
import csv 

# This visual is not intended for extra credit because it displays the same metrics as the bar graph, only with all the data;
# The scatter plot shows all 19 singers from the database; the names do not all fit nicely but the averages do
# Because my csv file does not have the averages in ascending order, neither does my scatter plot


# This reads from my csv file and creates a scatter plot for average popularity of the singer's songs on Spotify
singers = []
fame = []
with open("LuckySpotifyData.csv", 'r') as f:
	next(f) # get rid of the header
	for line in f:
		temp_data = line.split(',')
		singers.append((temp_data[0]))
		fame.append((temp_data[1]))


plt.scatter(singers, fame)
plt.title("Average Popularity of Songs Sung by Emma's Favorite Singers")
plt.xlabel('Singer')
plt.ylabel('Average Popularity on Spotify')
plt.show()