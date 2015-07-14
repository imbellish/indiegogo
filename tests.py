import unittest
import sqlite3

from indiegogo import (
	get_individual, 
	get_username,
	get_activities,
	get_categories,
	get_activity_links,
	verify,
	verify_contribution
	)

# globals
BASE_URL = "http://www.indiegogo.com/"
INDIVIDUAL = BASE_URL + "individuals/{0}"
ACTIVITIES = INDIVIDUAL + "/activities"

def db_init():
	db = sqlite3.connect("test_db.db")
	cursor = db.cursor()
	cursor.execute("""
		DROP TABLE IF EXISTS test_user""")
	
	cursor.execute("""
		CREATE TABLE test_user
		(id real, username text)
		""")
	
	cursor.close()

# globals
support_user = get_individual(100)
support_activities = get_activities(support_user)

actual_user = get_individual(101)
actual_activities = get_activities(actual_user)

class TestIndieGoGo(unittest.TestCase):

	def setUp(self):
		# test_db implementation
		# valid user logic
		#self.support_user = get_individual(100)
		# set this up later
		#db_init()
		pass

	def test_individuals(self):
		observed = support_user.status_code
		expected = 200
		self.assertEqual(observed, expected, "Status code other than 200")

	def test_get_username(self):
		observed = get_username(support_user)
		expected = "GoGo Support"
		self.assertEqual(observed, expected)

	def test_verify(self):
		failure = verify(get_individual(1))
		success = verify(support_user)
		self.assertFalse(failure)
		self.assertTrue(success)

	def test_activities(self):
		observed = get_activities(support_user)
		expected = 46
		self.assertEqual(len(observed), expected)

	def test_financial_activities(self):

		# user 100 is a support user and does not 
		# financially contribute. Thus all should be false
		
		support_contributions = verify_contribution(support_activities)
		support_observed = True in support_contributions
		support_expected = False # DIFF: support is not expected to contribute

		# whereas user 101 is an actual contributor
		# and is very likely to to have contributions

		actual_contributions = verify_contribution(actual_activities)
		actual_observed = True in actual_contributions
		actual_expected = True 

		# verify the difference

		self.assertEqual(support_observed, support_expected)
		self.assertEqual(actual_observed, actual_expected)

	def test_get_activity_links(self):
		links = get_activity_links(actual_activities)
		# this is where you left off 
		expected = '/projects/1112759'
		self.assertEqual(links[0], expected)

	def test_get_categories(self):
		"""
		looks for 'i-glyph-icon-30-film' in class tree
		of each project
		"""
		links = get_activity_links(actual_activities)
		

		

if __name__ == '__main__':
	unittest.main()