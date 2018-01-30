from bs4 import BeautifulSoup
import requests
import time
import os

class CSULB:

	name="CSULB"

	def __init__(self):
		pass

	def scrape(self):

		url = 'http://activitylog.upd.csulb.edu/'
		request = requests.get(url)
		soup = BeautifulSoup(request.text, "lxml")
		soup = BeautifulSoup( soup.html.body.form.prettify(), "lxml")
		x = str(soup.findAll('div')[1])

		count  = 0
		mylist = []
		mydict={}
		for string in x.split('      '):
			if(string.find('\n') > 0):
				string = string[0:string.find('\n')]
				if string.find('<') == -1 and string.find('Select') == -1:
					if count==0:
						mydict['case_number']=string
					elif count == 1:
						mydict['datetime_reported']=string
					elif count == 2:
						mydict['crime']=string
					elif count == 3:
						mydict['location']=string
					count += 1

					if count == 4:
						count = 0
						mylist.append(mydict)
						mydict={}

		mylist.pop(0)

		for x in range(0, len(mylist)):
			mylist[x]['date_occured']=""
			mylist[x]['time_occured']=""
			mylist[x]['description']=""
			mylist[x]['result']=""
		#mylist.reverse()
		if os.path.isfile('csulb.txt') == False:
			f = open('csulb.txt', 'w')
			f.write('none')
			f.close()
		f = open('csulb.txt','r')
		casenum = f.read()
		f.close()
		if casenum == "none":
			f = open('csulb.txt', 'w')
			f.write(mylist[0]['case_number'])
		else:
			exists = False
			for part in mylist:
				if part['case_number'] == casenum.rstrip("\n"):
					exists = True
			if exists == False:
				f = open('csulb.txt','w')
				f.write(mylist[0]['case_number'])
				f.close()
				return mylist
			list2 = []
			prev = ""
			for part in mylist:
				if part['case_number'] == casenum.rstrip("\n"):
					if prev != "":
						f = open('csulb.txt','w')
						f.write(prev)
						f.close()
					return list2
				else:
					list2.append(part)
					prev = part['case_number']
#so basically if the number is no longer there it's a problem
		return mylist
if __name__=="__main__":
    s=CSULB()

    x = s.scrape()
