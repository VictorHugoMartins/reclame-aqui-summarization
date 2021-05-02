from ratings import Ratings
from ranking import Ranking

import utils

import sqlite3
import argparse
import logging

SCRIPT_VERSION_NUMBER = "1.0"
logger = logging.getLogger()

def parse_args():
	"""
	Read and parse command-line arguments
	"""
	parser = argparse.ArgumentParser(
		description='Manage a database of Booking listings.',
		usage='%(prog)s [options]')
	parser.add_argument("-ratings", "--ratings",
						default=False, action="store_true",
						help="""search for textual conversations between enterprise and client/employee""")
	parser.add_argument("-ranking", "--ranking",
						default=False, action="store_true",
						help="""search for enterprise's classification in service categories in current week""")
	parser.add_argument('-e', '--enterprise',
					   metavar='enterprise_name', type=str,
					   help="""search by a enterprise
					   """)
	parser.add_argument('-p', '--page_quantity',
					   metavar='page quantity', type=int,
					   help="""quantity of pages to explore and scrape (default is 10)
					   """)
	
	args = parser.parse_args()
	return (parser, args)

def format_enterprise(enterprise):
	enterprise = enterprise.lower()
	enterprise = enterprise.replace(" ", "-")
	return enterprise

def main():

	Ratings.get_categorized_reviews("kids-mania")
	exit(0)
	
	(parser, args) = parse_args()

	if args.ratings and args.enterprise and args.page_quantity:
		Ratings.get_reviews(format_enterprise(args.enterprise), args.page_quantity)
	elif args.ranking:
		Ranking.get_ranking()
	else:
		print("Invalid arguments")

if __name__ == "__main__":
	main()