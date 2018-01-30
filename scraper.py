import os.path                  #script for directory/file handling
import csv                      #script for CSV file handling
import sys                      #sys
import time                     #scripting timing handling
import datetime                 #data and time handling
import traceback
from datetime import date
from threading import Thread

from SFSU import SFSU
from CSUN import CSUN
from CSULB import CSULB

from db import Database



class Scraper:

	schools=[]
	db = None

	def __init__(self):
		self.schools.append(CSULB())
		self.schools.append(SFSU())
		self.schools.append(CSUN())
		self.db = Database()


	def scrape(self):

		thread1=Thread(target=self.scrape_school, args=(0,))
		thread2=Thread(target=self.scrape_school, args=(1,))
		thread3=Thread(target=self.scrape_school, args=(2,))
		thread1.start()
		thread2.start()
		thread3.start()
		thread1.join()
		thread2.join()
		thread3.join()

	#threaded function
	def scrape_school(self, school_index):

		school_name=self.schools[school_index].name

		while True:
			print("Scraping "+str())
			items = self.schools[school_index].scrape()
			#starts from most recent item.
			#database insertion throws error if report is already saved
			try:
				for x in range(len(items)-1, -1, -1):
					items[x]['severity']=0
					self.db.insert_report(school_name, items[x])
			except Exception as error:
				print("ERROR: "+str(error))
				traceback.print_exc()


			#scrapes every minute
			time.sleep(60)


	def cleanse_new_reports(self):

		while True:


			time.sleep(10)

	#appends data to csv file at path
	def append_to_csv(self, path, data):
		#appends to existing contents
		with open(path, 'a', newline='') as file:
			contents = csv.writer(file)
			contents.writerows(data)

	#returns contents of csv at path in list format
	def read_from_csv(self, path):
		if os.path.isfile(path)==True:
			with open(path, newline='') as file:
				contents = csv.reader(file)

				matrix = []
				for row in contents:
					temp_matrix=[]
					for stuff in row:
						temp_matrix.append(stuff)
					matrix.append(temp_matrix)

				return matrix
		else:
			return []

	#writes data to csv file at path
	def save_to_csv(self, path, data):
		#writes over existing contents
		with open(path, 'w', newline='') as file:
			contents = csv.writer(file)
			contents.writerows(data)



if __name__=="__main__":
	scraper=Scraper()

	scraper.scrape()
