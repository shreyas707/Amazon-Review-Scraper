import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import pdb
import requests
import time
from random import randint
import csv

class amazon_review_scraper:

	# Ignore SSL certificate errors
	ssl._create_default_https_context = ssl._create_unverified_context

	csv_data = []

	csv_head = ["Rating", "Title", "Date", "Verified Purchase", "Body", "Helpful Votes"]

	def __init__(self, url, start_page, end_page, time_upper_limit):
		self.url = url
		self.set_url()
		self.start_page = int(start_page)
		self.end_page = int(end_page)
		self.time_upper_limit = time_upper_limit

	def set_sleep_timer(self):
		sleep_time = randint(0, int(self.time_upper_limit))
		print("\nSleeping for " + str(sleep_time) + " seconds.")
		time.sleep(sleep_time)

	def set_url(self):
		# removing pageNumber parameter if it exists in the url
		url = self.url.split("&pageNumber")
		if len(url) > 1:
			self.url = url[0]
		else :
			self.url = url

	def set_start_page(self, start_page):
		url = self.url + "&pageNumber=" + str(start_page)
		return url

	def build_rating(self, review):
		return str(review).split("<span class=\"a-icon-alt\">")[1].split("</span>")[0].split(" ")[0]

	def build_title(self, review):
		return str(review).split("data-hook=\"review-title\"")[1].split("\">")[1].split("</a>")[0]

	def build_date(self, review):
		return str(review).split("data-hook=\"review-date\">")[1].split("</span>")[0].split("on ")[1]

	def build_verified_purchase(self, review):
		# Yes = purchased, No = not purchased
		try: 
			str(review).split("data-hook=\"avp-badge\">")[1].split("</span>")[0]
			return "Yes"
		except:
			return "No"

	def build_body(self, review):
		body = str(review).split("data-hook=\"review-body\">")[1].split("</span>")[0] + "\n"
		# to remove <br>, <br/> and </br>
		body = body.replace("<br>", ".").replace("<br/>", ".").replace("</br>", ".").strip()
		return body

	def build_votes(self, review):
		try :
			votes = str(review).split("data-hook=\"helpful-vote-statement\"")[1].split(">")[1].split("<")[0].strip().split()
			if votes[0] == "One" :
				return "1"
			else :
				return votes[0]
		except :
			return "0"

	def scrape(self):

		start_page = self.start_page
		end_page = self.end_page
		
		if end_page < start_page:
			print("Start page cannot be greater than end page. Please try again.")
			exit()

		self.csv_data.append(self.csv_head)

		while start_page <= end_page :

			try:
				url = self.set_start_page(start_page)
			except:
				print("URL entered is wrong. Please try again with the right URL.")
				exit()

			# Sleep because Amazon might block your IP if there are too many requests every second
			self.set_sleep_timer()

			print("Scraping page " + str(start_page) + ".")

			# Amazon blocks requests that don't come from browser. Hence need to mention user-agent
			user_agent = 'Mozilla/5.0'
			headers = {'User-Agent' : user_agent}

			values = {}

			data = urllib.parse.urlencode(values).encode('utf-8')
			req = urllib.request.Request(url, data, headers)
			response = urllib.request.urlopen(req)
			html = response.read()

			soup = BeautifulSoup(html, 'html.parser')
			reviews = soup.find_all("div", attrs={"class": "a-section review"})

			for review in reviews :

				csv_body = []

				# Star Rating
				rating = self.build_rating(review)
				csv_body.append(rating)

				# Title
				title = self.build_title(review)
				csv_body.append(title)
				
				# Date
				date = self.build_date(review)
				csv_body.append(date)

				# Verified Purchase			
				verified_purchase = self.build_verified_purchase(review)
				csv_body.append(verified_purchase)

				# Body
				body = self.build_body(review)
				csv_body.append(body)

				# Helpful Votes
				votes = self.build_votes(review)
				csv_body.append(votes)

				self.csv_data.append(csv_body)

			start_page += 1

	def write_csv(self, file_name):

		print("\nWriting to file.\n")

		with open((file_name + '.csv'), 'w') as csv_file :
			writer = csv.writer(csv_file, delimiter=',')
			writer.writerows(self.csv_data)
