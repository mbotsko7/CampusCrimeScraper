#!/usr/bin/python3
import os
import urllib.request           #script for URL request handling
import urllib.parse             #script for URL handling
import random

import http.cookiejar #for logging in
import http.cookies
from bs4 import BeautifulSoup




class SFSU:

	name="SFSU"

	cookies=[]
	cj = None
	opener = None
	user_agents=[]

	def __init__(self):

		self.user_agents.append("Mozilla/5.0 (X10; Ubuntu; Linux x86_64; rv:25.0)")
		self.user_agents.append("Mozilla/5.0 (Windows NT 6.0; WOW64; rv:12.0)")
		self.user_agents.append("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537")
		self.user_agents.append("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/540 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/540")
		self.user_agents.append("Mozilla/5.0 (Windows; U; Windows NT 5.2; it; rv:1.8.1.11) Gecko/20071327 Firefox/2.0.0.10")
		self.user_agents.append("Opera/9.3 (Windows NT 5.1; U; en)")


		#initializes url variables
		self.cj=http.cookiejar.CookieJar()
		self.opener=urllib.request.build_opener(urllib.request.HTTPRedirectHandler(),urllib.request.HTTPHandler(debuglevel=0),urllib.request.HTTPCookieProcessor(self.cj))
		# self.opener.addheaders = [('User-agent', self.user_agents[0]), ('Content-Type', 'application/xml')]


	def scrape(self):

		user_agent = self.user_agents[random.randint(0, len(self.user_agents)-1)]

		self.opener.addheaders = [('User-agent', user_agent)]

		response = self.opener.open("https://upd.sfsu.edu/crimelog")


		# print(f.read())
		if response.status==200:
			response=response.read().decode('UTF-8', errors='ignore')


			soup = BeautifulSoup(response, 'html.parser')

			#html
			soup=soup.contents[2]
			#body
			soup=soup.contents[3]
			#<div id="main"
			soup=soup.contents[5]
			#<div class="row"
			soup=soup.contents[1]
			#<section
			soup=soup.contents[7]
			#<div class="region"
			soup=soup.contents[5]
			#<div id="block...
			soup=soup.contents[1]
			#<div class="view..."
			soup=soup.contents[1]
			#<div class="view-content"
			soup=soup.contents[3]


			items=[]
			for x in range(0, len(soup.contents)):
				name = soup.contents[x].name

				#gets each report
				if name!=None:
					item = soup.contents[x]


					temp={}
					try:
						#crime's location
						location=item.contents[1]
						location = location.contents[1].string
						temp['location']=location

						#Type of crime committed
						crime=item.contents[5]
						crime = crime.contents[1].string
						temp['crime']=crime

						#case number
						case_number = item.contents[9]
						case_number = case_number.contents[3].string
						temp['case_number']=case_number

						#date and time of report
						time_reported = item.contents[13]
						time_reported = time_reported.contents[3].string
						time_reported = time_reported.replace("@", "")
						temp['datetime_reported']=time_reported

						#date timeframe of crime occurance
						date_occured = item.contents[17]
						date_occured = date_occured.contents[3].string
						temp['date_occured']=date_occured

						#time occured
						time_occured = item.contents[21]
						time_occured = time_occured.contents[3].string
						temp['time_occured']=time_occured

						#time occured
						case_disposition = item.contents[25]
						case_disposition = case_disposition.contents[3].string
						temp['result']=case_disposition

						#case synopsis
						synopsis = item.contents[27]
						synopsis = synopsis.contents[3].string
						temp['description']=synopsis


						items.append(temp)

					except Exception as error:
						pass


			
			#puts most recent items at back of list
			#items.reverse()
			if os.path.isfile('sfsu.txt') == False:
				f = open('sfsu.txt', 'w')
				f.write('none')
				f.close()
			f = open('sfsu.txt','r')
			casenum = f.read()
			f.close()
			if casenum == "none":
				f = open('sfsu.txt', 'w')
				f.write(items[0]['case_number'])
			else:
				list2 = []
				prev = ""
				for part in items:
					if part['case_number'] == casenum.rstrip("\n"):
						if prev != "":
							f = open('sfsu.txt','w')
							f.write(prev)
							f.close()
						return list2
					else:
						list2.append(part)
						prev = part['case_number']

			return items


		else:
			print("Problem scraping")
			return []
if __name__=="__main__":
    s=SFSU()

    x = s.scrape()
    print(x)
