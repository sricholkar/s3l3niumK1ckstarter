from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import pymysql.cursors


class Twitter():

	##constructor which is invodked automatically when an object for a class is created
	def __init__(self, campaign, profile):
		self.driver = webdriver.Firefox()
		self.driver.get(campaign)
		self.cnxn = self.connection()
		self.checkTableExists(profile, self.cnxn)
		self.pages(profile)

	##establisches connection with MySQL database
	def connection(self):
		conn = pymysql.connect(host="localhost", user="root", password="1234", db="twitterdb", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
		return conn

	##checks if a table "XXXXXX" already exists, if not invokes createTable function to create new table
	def checkTableExists(self, profile, cnxn):
		self.cursor = self.cnxn.cursor()
		self.cursor.execute("Select table_name from information_schema.tables where table_name = \'" + profile + "\'")
		# print(str(self.cursor.fetchall()[0]['table_name']))
		try:
			if (self.cursor.fetchall()[0]['table_name'] == profile):
				return True

		except IndexError:
			self.createTable(profile, self.cnxn) #invokes createTable function

	##creates a new table "XXXXX"
	def createTable(self, profile, cnxn):
		self.cursor = self.cnxn.cursor()
		self.cursor.execute('DROP TABLE IF EXISTS ' + profile) #or die(mysql_error());
		print("Creating a table " + profile.upper())
		self.cursor.execute("CREATE TABLE "+ profile +" (id int PRIMARY KEY AUTO_INCREMENT, created_at varchar(500), tweeted_by varchar(500), tweets varchar(500))")
		self.cnxn.commit()
		print(profile.upper() + " table created Successfully")

	##inserts tweets into the MySQL database sequentuelly with time
	def insert(self, profile, cnxn, created_at, tweeted_by, tweet):
		print("In insert method")
		query = "INSERT INTO " + profile + " (created_at, tweeted_by, tweets) VALUES (%s, %s, %s)"
		cursor = self.cnxn.cursor()
		cursor.execute(query, (created_at, tweeted_by.encode('utf-8'), tweet.encode('utf8')))
		self.commit(self.cnxn)                                                                    ##invokes commit function

	##commits the given query
	def commit(self, cnxn):
		self.cnxn.commit()

	##closes connection to database
	def closeCon(self, cnxn):
		self.cnxn.close()
		print("Connection Successfully Closed!")

	def pages(self, profile, last_height = 0):

		##scrolls down untill the last created tweet
		try:
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			new_height = self.driver.execute_script("return document.body.scrollHeight")
			time.sleep(3)
			#print(new_height)
			#print(last_height)
			if (new_height == last_height):
				raise Exception("End of Scroll")
			else:
				last_height = new_height
				self.pages(profile, last_height)

		##retrieves the tweets and inserts the tweets into the database
		except Exception:
			page_list_of_tweets = self.driver.find_elements_by_css_selector("div.js-tweet-text-container")
			tweet_date = self.driver.find_elements_by_class_name("_timestamp")
			tweeted_by_list = self.driver.find_elements_by_css_selector("div.content div.stream-item-header a span[dir='ltr']")
			print("Inserting tweets into the table " + profile.upper()+ "......" )
			# num_of_tweets = counter
			for i, j, k in zip(page_list_of_tweets, tweet_date, tweeted_by_list):
				try:
					timestamp = tweet_date[page_list_of_tweets.index(i)].get_attribute('data-time')
				except IndexError:
					break
				time_stamp = datetime.strftime(datetime.fromtimestamp(int(timestamp)), "%Y-%m-%d")
				tweet = i.text

				# tweet_info = str(datetime.fromtimestamp(int(timestamp))) + " , " + str(k.text) + " , " + str(i.text)
				print(tweet)
				tweeted_by = k.text
				
				self.insert(profile, self.cnxn, time_stamp, tweeted_by, tweet)
				# with open("coolestcooler.csv", "a", encoding="utf-8") as cc:
				# 	cc.write(tweet_info + "\n")
			# counter = num_of_tweets
			end()

	##closes the database connection and quits the browser
	def end():
		self.closeCon(self.cnxn)
		print("finished retrieving tweets")
		print("quitting browser.........")
		self.driver.quit()
		time.sleep(2000) #program sleeps for 2 seconds
		print("End")
		

##program starts execting from main function.
if __name__ == "__main__":

	profileList = ["explodingkittens", "zungle", "baubax", "lifeonpurple", "starcitizen", "bragi", "sondorsebike", "gloomhaven", "oculusrift", "picobrewbeer", 
					"fidgetcube", "getsequent", "hyper", "vmullerdesigner", "livwatches", "ridehelix", "gramovox", "teamkano", "elevationlab", "korindesign", 
					"getbetterback", "pebble", "oculusrift", "pono", "worldofeternity", "theveronicamarsmovie", "lifeonpurple", "shenmue_3"]

	search_methods = ["https://twitter.com/search?q=@" + profile, "https://twitter.com/hashtag/" + profile + "?src=hash"]

	for method in search_methods:
		for profile in profileList:
			Twitter(method, profile)
	

 		
	# twitter = Twitter("https://twitter.com/hashtag/coolestcooler?src=hash", "coolestcooler")
	# twitter = Twitter("https://twitter.com/search?q=@coolest_cooler", "coolestcooler")

	

 	
 	

    


