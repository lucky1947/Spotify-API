'''
Lucky Chowdhury 
SI 206 Fall'18
Final Project - Main File
'''
# THIS PROJECT IS DEDICATED TO MY DEAR FRIEND EMMA COOK <3

# These import statements are necessary to run my code
import os
import sys
import csv 
import json
import spotipy
import sqlite3
import webbrowser
import matplotlib
import SpotifyInfo
import spotipy.util as util
import matplotlib.pyplot as plt

# This snippet of code authorizes the user and sets the scopes that can be used to access data
accountUsernameForEmma = 'nycsinger16'
scope = 'user-read-recently-played user-follow-read user-top-read user-read-private user-read-playback-state user-modify-playback-state'
token = util.prompt_for_user_token(accountUsernameForEmma, scope, client_id=SpotifyInfo.CLIENT_ID, 
	client_secret=SpotifyInfo.CLIENT_SECRET, redirect_uri=SpotifyInfo.REDIRECT_URI)
sp = spotipy.Spotify(auth=token)


# This function retrieves the top singers from Emma's account using a function in the spotipy library 
# It does not take in any parameters
def topSingersForEmma():
	singerIDList = []
	topSingers = sp.current_user_top_artists(limit=20, offset=0, time_range='medium_term')
	# This adds and saves the top 20 singers on Emma's account in a list
	for a in topSingers['items']:
		singerURI = a['uri']
		singerIDList. append(singerURI)
	return singerIDList

# This calls the function so that top singers are accessed
topSingersForEmma()


# This function retrieves the top songs from Emma's account using a function in the spotipy library 
# It takes in singerID as a parameter that is iterated through to find song information. 
def topSongsForEmma(singerID):
	singersList = []
	songsDictionary = {}
	# This saves the top songs on Emma's account in a dictionary and then saves it in a list 
	for singer in singerID:
		songData = sp.artist_top_tracks(singer, country='US')
		singerName = songData['tracks'][0]['artists'][0]['name']
		for song in songData['tracks']:
			songs = song['name']
			popularity = song['popularity']
			songsDictionary = {'singer': singerName, 'best songs': songs, 'popularity': popularity}
			singersList.append(songsDictionary)
	return singersList

# This stores the top songs for an artist into a list called spotifyData so that it can be accessed later 
spotifyData = topSongsForEmma(topSingersForEmma())


# This initializes the conncection and cursor so my code is linked to the new database that I will create so all my data transfers on to there 
conn = sqlite3.connect('/Users/luckychowdhury/Desktop/si-206-fp/SI_final_project.db')
cur = conn.cursor()


# This function creates a new SQLite table for the three columns: singer, their best songs, and popularity of those songs on spotify
# It takes in three parameters, connection and cursor (so my code is linked to the new database that I created),
# and the list spotifyData that contains all of Emma’s favorite singers and their songs 
def createSpotifyDatabase(conn, cur, spotifyData):

	cur.execute('DROP TABLE IF EXISTS Spotify')
	cur.execute('CREATE TABLE Spotify (SINGER TEXT, BEST_SONGS TEXT, FAME INTEGER)')
	for info in spotifyData:
		cur.execute('INSERT INTO Spotify (SINGER, BEST_SONGS, FAME) VALUES (?,?,?)''', (info['singer'], info['best songs'], info['popularity']))
	conn.commit()

# This calls the function so that the database table is created
createSpotifyDatabase(conn, cur, spotifyData)


# This function calculates the average fame score for a singer 
# It takes in four parameters conn, cur (so my code is linked to my database table),
# spotifyData (the list that stores all of Emma’s favorite singers and their songs),
# and artist_name (so I can call each of the artist’s names within this function to get their fame scores)
def avgArtistPop(conn, cur, spotifyData, artist_name):

	# This initializes the connection and cursor so my code is linked to the new database
	conn = sqlite3.connect('/Users/luckychowdhury/Desktop/si-206-fp/SI_final_project.db')
	cur = conn.cursor()
	# This accesses the necessary column in the database
	data = cur.execute('SELECT * FROM Spotify WHERE SINGER="%s"' % artist_name)
	total = 0
	rowCounter = 0
	# This iterates through the rows to add total fame values and divide by number of times the singer appears in the database
	for row in data:
		total += (row[2])
		rowCounter += 1
	total = total / rowCounter
	print(total)
	return total

# This calls the function 19 times so that each singer's (listed on the database) average popularity is calculated 
avgArtistPop(conn, cur, spotifyData, "Voctave"), #ARTIST NUMBER 1	
avgArtistPop(conn, cur, spotifyData, "Queen"), #ARTIST NUMBER 2
avgArtistPop(conn, cur, spotifyData, "Michael Bublé"), #ARTIST NUMBER 3
avgArtistPop(conn, cur, spotifyData, "Sydney Lucas"), #ARTIST NUMBER 4
avgArtistPop(conn, cur, spotifyData, "Rihanna"), #ARTIST NUMBER 5
avgArtistPop(conn, cur, spotifyData, "Danny Elfman"), #ARTIST NUMBER 6
avgArtistPop(conn, cur, spotifyData, "Harry Gregson-Williams"), #ARTIST NUMBER 7
avgArtistPop(conn, cur, spotifyData, "Taylor Swift"), #ARTIST NUMBER 8
avgArtistPop(conn, cur, spotifyData, "Frank Sinatra"), #ARTIST NUMBER 9
avgArtistPop(conn, cur, spotifyData, "Beth Malone"), #ARTIST NUMBER 10
avgArtistPop(conn, cur, spotifyData, "5 Seconds of Summer"), #ARTIST NUMBER 11
avgArtistPop(conn, cur, spotifyData, "Little Mix"), #ARTIST NUMBER 12
avgArtistPop(conn, cur, spotifyData, "Natasha Richardson"), #ARTIST NUMBER 13
avgArtistPop(conn, cur, spotifyData, "Judy Kuhn"), #ARTIST NUMBER 14
avgArtistPop(conn, cur, spotifyData, "Billy Porter"), #ARTIST NUMBER 15
avgArtistPop(conn, cur, spotifyData, "Soundtrack/Cast Album"), #ARTIST NUMBER 16
avgArtistPop(conn, cur, spotifyData, "Clean Bandit"), #ARTIST NUMBER 17
avgArtistPop(conn, cur, spotifyData, "Green Day"), #ARTIST NUMBER 18
avgArtistPop(conn, cur, spotifyData, "The Piano Guys") #ARTIST NUMBER 19
# avgArtistPop(conn, cur, spotifyData, "Jonas Brothers") #ARTIST NUMBER 20 

#I commented Jonas Brothers out because the new database that was generated (after I ran my code again) 
# showed that Emma was not listening to them as much as before, therefore they were excluded from the database;
# but they are on the database that I submitted on December 10th


# This function creates a CSV file for the 19 singers and their average popularity based on the total songs' popularity for that singer
# It does not take in any parameters 
def createCSVFile():
	# This is a dictionary which I created to access the key, singer, and value, their name using the previous function avgArtistPop()
	singerNamesDict = {"Voctave":avgArtistPop(conn, cur, spotifyData, "Voctave"),  
	"Queen":avgArtistPop(conn, cur, spotifyData, "Queen"), #ARTIST NUMBER 2
	"Bublé":avgArtistPop(conn, cur, spotifyData, "Michael Bublé"), #ARTIST NUMBER 3
	"Lucas":avgArtistPop(conn, cur, spotifyData, "Sydney Lucas"), #ARTIST NUMBER 4
	"Rihanna":avgArtistPop(conn, cur, spotifyData, "Rihanna"), #ARTIST NUMBER 5
	"Elfman":avgArtistPop(conn, cur, spotifyData, "Danny Elfman"), #ARTIST NUMBER 6
	"Gregson-Williams":avgArtistPop(conn, cur, spotifyData, "Harry Gregson-Williams"), #ARTIST NUMBER 7
	"Swift":avgArtistPop(conn, cur, spotifyData, "Taylor Swift"), #ARTIST NUMBER 8
	"Sinatra":avgArtistPop(conn, cur, spotifyData, "Frank Sinatra"), #ARTIST NUMBER 9
	"Malone":avgArtistPop(conn, cur, spotifyData, "Beth Malone"), #ARTIST NUMBER 10
	"5 Seconds":avgArtistPop(conn, cur, spotifyData, "5 Seconds of Summer"), #ARTIST NUMBER 11
	"Little Mix":avgArtistPop(conn, cur, spotifyData, "Little Mix"), #ARTIST NUMBER 12
	"Richardson":avgArtistPop(conn, cur, spotifyData, "Natasha Richardson"), #ARTIST NUMBER 13
	"Kuhn":avgArtistPop(conn, cur, spotifyData, "Judy Kuhn"), #ARTIST NUMBER 14
	"Porter":avgArtistPop(conn, cur, spotifyData, "Billy Porter"), #ARTIST NUMBER 15
	"Soundtrack":avgArtistPop(conn, cur, spotifyData, "Soundtrack/Cast Album"), #ARTIST NUMBER 16
	"Bandit":avgArtistPop(conn, cur, spotifyData, "Clean Bandit"), #ARTIST NUMBER 17
	"Green Day":avgArtistPop(conn, cur, spotifyData, "Green Day"), #ARTIST NUMBER 18
	"Piano Guys":avgArtistPop(conn, cur, spotifyData, "The Piano Guys")} #ARTIST NUMBER 19
	# "Jonas Brothers":avgArtistPop(conn, cur, spotifyData, "Jonas Brothers")} #ARTIST NUMBER 20

	#I commented Jonas Brothers out because the new database that was generated (after I ran my code again) 
	# showed that Emma was not listening to them as much as before, therefore they were excluded from the database
	# but they are on the database that I submitted on December 10th

	# This creates a new Comma Separated Values file in Excel 
	outfile = open("LuckySpotifyData.csv", "w")

	# This code snippet labels the file and adds the previously calculated averages with their corresponding singers in the file in 2 columns
	with outfile:
		writer = csv.writer(outfile)
		header = ("Singer", "Average Fame on Spotify")
		writer.writerow(header)

		for singer in singerNamesDict:
			singerName = (singer, singerNamesDict[singer])
			writer.writerow(singerName)

# This calls the function so that the file is created
createCSVFile()
	
# THANK YOU FOR YOUR ATTENTION!
# I HOPE YOU ENJOYED MY PROJECT :D
