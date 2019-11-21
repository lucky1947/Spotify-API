'''
Lucky Chowdhury 
SI 206 Fall'18
Final Project - Visualization #1: Bar Graph
'''
# Import statements for libraries necessary to create charts
import matplotlib
import matplotlib.pyplot as plt


# This code generates a bar chart of Emma's top 7 singers and their average popularity score
# This is my main visualization and due to all 19 singers' names not fitting on the x-axis, I used Emma's favorite singers
# and made a smaller chart instead

y = (29, 36.3, 41.6, 49.4, 66.2, 70, 73.1)
x = ("Natasha Richardson", "Soundtrack/Cast", "Voctave", "Danny Elfman", "Michael BublÃ", "5 Seconds of Summer", "Queen")

bar1 = plt.bar(x, y,)
bar1[0].set_color("k")
bar1[1].set_color("g")
bar1[2].set_color("k")
bar1[3].set_color("g")
bar1[4].set_color("k")
bar1[5].set_color("g")
bar1[6].set_color("k")

plt.title("Average Popularity of Songs by Emma's Favorite Singers")
plt.xlabel('Singer')
plt.ylabel('Average Popularity on Spotify')
plt.show()
	
