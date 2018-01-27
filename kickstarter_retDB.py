from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time, re
import pymysql.cursors

##establishes connection
def connection():
		conn = pymysql.connect(host="localhost", user="root", password="1234", db="twitterdb", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
		return conn

##commits the given query
def commit(cnxn):
	cnxn.commit()

##closes connection to database
def closeCon(cnxn):
	cnxn.close()
	print("Connection Successfully Closed!")

def retrieveTweets(campaign):
	
	
	query = "Select id,tweets from "+ campaign +" WHERE tweeted_by != '@"+ campaign.lower()+"' ORDER BY RAND() LIMIT 100" 

	con = connection()
	cursor = con.cursor()
	cursor.execute(query)
	tweets_info = cursor.fetchall()
	num_of_tweets = len(tweets_info) + 1
	with open("New2/"+campaign + "_tweets.csv", "a", encoding="UTF-8") as camp:
		for num, tweet in zip(range(1,num_of_tweets),tweets_info):
			print(str(num) + "," +tweet['tweets'] + "\n")
			camp.write(str(num) + "," +tweet['tweets'] + "\n")
	commit(con)
	closeCon(con)


campaigns_twitter_profile = ["antoniasaintny", 'baubax', 'bragi', "brydgekeyboards", "coolestcooler", "edgeofbelgravia", "elevationlab", "emotiv", "explodingkittens", "fidgetcube", "getbetterback", "getbetterback", 
	"getsequent", "giflybike", "gloomhaven", "glowheadphones", "gramovox", "g_rotogether", "hellobragi",
	"hickies", "ikamper_inc", "junosmartmirror", "korindesign", "lifeonpurple", "livwatches", "nebia",
	"noriacool", "northaware", "oculusrift", "pebble", "picobrewbeer", "pono", "ridehelix", "shenmue_3",
	"sleepkokoon", "sondorsebike", "starcitizen", "tagabikes", "teamkano", "theveronicamarsmovie", "vmullerdesigner",
	"worldofeternity", "zungle"]



for campaign in campaigns_twitter_profile:
	# campaign = ''.join(e for e in campaign if e.isalnum())
	
	retrieveTweets(campaign)

