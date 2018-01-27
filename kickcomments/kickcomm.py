from selenium import webdriver
import pymysql.cursors
from selenium.common.exceptions import *
import selenium


def connection():
	conn = pymysql.connect(host="localhost", user="root", password="1234", db="twitterdb", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
	return conn

def checkTableExists(profile, cnxn):
	cursor = cnxn.cursor()
	cursor.execute("Select table_name from information_schema.tables where table_name = \'" + profile + "\'")
		# print(str(self.cursor.fetchall()[0]['table_name']))
	try:
		if (cursor.fetchall()[0]['table_name'] == profile):
			return True

	except IndexError:
		createTable(profile, cnxn)

def createTable(profile, cnxn):
		cursor = cnxn.cursor()
		# cursor.execute('DROP TABLE IF EXISTS ' + profile) #or die(mysql_error());
		print("Creating a table " + profile.upper())
		cursor.execute("CREATE TABLE "+ profile +" (id int PRIMARY KEY AUTO_INCREMENT, created_at varchar(500), tweeted_by varchar(500), tweets varchar(500))")
		cnxn.commit()
		print(profile.upper() + " table created Successfully")


def insert(profile, cnxn, created_at, tweeted_by, tweet):
		print("In insert method")
		query = "INSERT INTO " + profile + " (created_at, tweeted_by, tweets) VALUES (%s, %s, %s)"
		cursor = cnxn.cursor()
		cursor.execute(query, (created_at, tweeted_by.encode('utf-8'), tweet.encode('utf8')))
		commit(cnxn)

def commit(cnxn):
		cnxn.commit()

def closeCon(cnxn):
		cnxn.close()
		print("Connection Successfully Closed!")


conn = connection()			#establishes connection with the database
browser = webdriver.Firefox()          
browser.get("https://www.kickstarter.com/projects/ryangrepper/coolest-cooler-21st-century-cooler-thats-actually/comments")
profile = "coolestcooler_kick"
checkTableExists(profile, conn)

browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
s = browser.find_element_by_css_selector(".btn.btn--light-blue.btn--block.mt3.older_comments")
try:
	while(s):
		s.click()
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
except selenium.common.exceptions.ElementNotSelectableException(msg=None, screen=None, stacktrace=None):

	f = browser.find_elements_by_css_selector("div.main.clearfix.pl3.ml3")

	for i in f:
		s = i.find_element_by_css_selector("h3 span").text
		if (s == "Creator" or s == "Collaborator" or s == "2-time creator"):
			continue
		else:
			for j, k, l in zip(i.find_elements_by_css_selector("h3 a.author.green-dark"), i.find_elements_by_css_selector("h3 span a data"), i.find_elements_by_css_selector("p")):
				tweeted_by = j.text
				created_at = str(k.get_attribute('data-value'))
				tweet = l.text
				insert(profile, cnxn, created_at, tweeted_by, tweet)
				# print(j.text + " ::: " + str(k.get_attribute('data-value')) + " ::: " +l.text)

	closeCon(cnxn)

	browser.quit()

# div.superbacker-badge.tipsy_s

