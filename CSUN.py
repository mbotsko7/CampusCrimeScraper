from bs4 import BeautifulSoup
import requests
import time
import os


class CSUN:

	name="CSUN"

	def __init__(self):
		pass

	def scrape(self):

		url = 'https://www.csun.edu/police/daily-crime-log'
		request = requests.get(url)
		soup = BeautifulSoup(request.text, "lxml")
		soup = BeautifulSoup( soup.html.body.prettify(), "lxml")
		x = soup.findAll('div')
		looking = "tbody"
		found = ""
		for div in x:
			if(str(div).find(looking) != -1):
				found = str(div)

		val = 1
		mylist = found.split("<p>")
		caught = []
		upcoming = False
		count = 0
		for v in mylist:
			p = v.split("</p>")[0]
			if count < 9:
				count += 1
			else:
				#print p
				if p.find("Crime Report") != -1:
					continue
				elif p.find("<b>") != -1:
					break
				else:
					caught.append(p.strip())
		mydict = {}
		count = 0
		mylist = []
		cn = ""
		cr = ""
		date = ""
		loc = ""
		desc = ""
		res = ""
		for v in caught:

			if count == 0:
				if v == '':
					continue
				cn = v
			elif count == 1:
				cr = v
			elif count == 2:
				date = v
			elif count == 4:
				loc = v
			elif count == 5:
				desc = v
			elif count == 6:
				res = v
			count += 1
			if count == 7:
				count = 0
				mydict['case_number'] = cn
				mydict['datetime_reported'] = date
				mydict['crime'] = cr
				mydict['location'] = loc
				mydict['date_occured']=""
				mydict['time_occured']=""
				mydict['description']=desc
				mydict['result']=res
				mylist.append(mydict)
				mydict = {}
				cn = ""
				cr = ""
				date = ""
				loc = ""
				desc = ""
				res = ""
		if os.path.isfile('csun.txt') == False:
			f = open('csun.txt', 'w')
			f.write('none')
			f.close()
		f = open('csun.txt','r')
		casenum = f.read()
		f.close()
		if casenum == "none":
			f = open('csun.txt', 'w')
			f.write(mylist[0]['case_number'])
		else:
			list2 = []
			prev = ""
			for part in mylist:
				if part['case_number'] == casenum.rstrip("\n"):
					if prev != "":
						f = open('csun.txt','w')
						f.write(prev)
						f.close()
					return list2
				else:
					list2.append(part)
					prev = part['case_number']


		return mylist

if __name__=="__main__":
	s=CSUN()

	w = s.scrape()
	for x in w:
		print(x)
