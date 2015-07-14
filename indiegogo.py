
import requests
from lxml import html
import sqlite3

# do this once it gets too big
# import logging

class InvalidUser(Exception):
	pass

# globals
BASE_URL = "http://www.indiegogo.com/"
INDIVIDUAL = BASE_URL + "individuals/{0}"
ACTIVITIES = INDIVIDUAL + "/activities"

# debug function
def debug():
	return get_individual(101)

# initializer
def db_init():
	db = sqlite3.connect("indigogo.db")
	cursor = db.cursor()
	cursor.execute("""
		CREATE TABLE test_user
		(id real, username text)
		""")

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
	return activities

def get_activity_links(activities):
	"""
	gets all activites from the user view.
	"""
	links = []
	for i, activity in enumerate(activities):
		link = next(activity.iterlinks())[2]
		links.append(link)
	return links

def get_categories(verified_contributions, activities):
	"""
	Not Implemented!
	"""
	for i, true in enumerate(verified_contributions):
		if true:
			pass # what? 

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
		
			
def store_valid_users(individual):
	if verify(individual):
		pass
		# store
	raise InvalidUser("Something went wrong")

if __name__ == '__main__':
	doc = debug()
