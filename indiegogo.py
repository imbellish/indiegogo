
import requests
from lxml import html
import sqlite3
from collections import OrderedDict

# do this once it gets too big
# import logging

class InvalidUser(Exception):
	pass

# globals
BASE_URL = "http://www.indiegogo.com/"
INDIVIDUAL = BASE_URL + "individuals/{0}"
ACTIVITIES = INDIVIDUAL + "/activities"


# config
DESIRED_CATEGORY = "Film"
MINIMUM_CONTRIBS = 10

# debug function
def debug():
	return get_individual(101)

# initializer
def db_init():
	db = sqlite3.connect("indiegogo.db")
	cursor = db.cursor()
	cursor.execute("""
		DROP TABLE IF EXISTS user
		""")
	cursor.execute("""
		CREATE TABLE user
		(id real, username text, url text, contribs int)
		""")
	cursor.close()

# functions
def get_individual(number):
	individual = requests.get(
		INDIVIDUAL.format(number))
	individual.id = number
	return individual

def get_username(individual):
	"""
	gets inner text of class 'i-profileHeader-accountName'
	from raw HTML content
	"""
	doc = html.fromstring(individual.text)
	username = doc.find_class("i-profileHeader-accountName")[0].text
	return username

# unused function
def get_individual_username(number):
	"""
	returns get_individual and get_username
	as a tuple for easy db handling
	"""
	individual = get_individual(number)
	username = get_username(individual)
	return individual, username

def get_activities(individual):
	"""
	gets everything right of the small photo on the 
	activities page. returns div elements as a list.
	"""
	id = individual.id
	activities_page = requests.get(ACTIVITIES.format(id))
	doc = html.fromstring(activities_page.text)
	activities = doc.find_class("i-right-of-small-photo")
	activities[0].id = id
	return activities

def get_activity_links(activities):
	"""
	gets all activites from the user view.
	"""
	links = []
	for i, activity in enumerate(activities):
		link = next(activity.iterlinks())[2][1:]
		links.append(link)
	return links

def get_category(link):
	"""
	subject to change based on HTML classes. looks for 
	the category of an activities page. 
	"""
	req = requests.get(BASE_URL+link)
	doc = html.fromstring(req.text)
	link = doc.find_class('i-keep-it-together')
	links = link[1].iterlinks()
	parse = next(links)[2]
	category = parse.split("/")[2].title()
	if category == DESIRED_CATEGORY:
		return True


def verify(individual):
	if individual.status_code == 200:
		return True
	return False

def verify_contribution(activities):
	"""
	if activities text does not equal:
		'\n              Contributed to:\n            '
	then return True, else return False
	"""
	passtring = '\n              Contributed to:\n            '
	truth = lambda x: True if x is True else False
	for action in activities:
		yield truth(passtring == action[0].text)
		
			
def store_valid_user(id, individual, url, number_of_contribs):
	db = sqlite3.connect("indiegogo.db")
	cursor = db.cursor()
	cursor.execute("""
		INSERT INTO user VALUES
		(?, ?, ?, ?)
		""", (id, individual, url, number_of_contribs))
	#raise InvalidUser("Something went wrong")

if __name__ == '__main__':
	
	for i in range(101, 150):
		contribs = 0
		individual = get_individual(i)
		#activities = get_activities(individual)
		if verify(individual):
			id = individual.id 
			username = get_username(individual)
			url = individual.url

			activities = get_activities(individual)
			links = get_activity_links(activities)
			for link in links:
				if get_category(link):
					contrib += 1
			if contrib > 10:
				store_valid_user(id, username, url, contrib)

	"""

	# for i in range(1000000000)...
	#support_user = get_individual(100)
	#support_activities = get_activities(support_user)
	
	
	actual_user = get_individual(101)
	# if verify(actual_user):
	#     ...
	actual_activities = get_activities(actual_user)
	
	contributions = verify_contribution(actual_activities)
	for i, truth in enumerate(contributions):
		if truth:
			link = get_activity_links(actual_activities[i])
			category = get_category(link)"""


