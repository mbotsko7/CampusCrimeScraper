#!/usr/bin/python
import pyrebase
import datetime                   #data and time handling
from datetime import date
from pyfcm import FCMNotification

class Database:

	host="localhost"; #localhost
	username=""; #database username
	password=""; #password for user to database
	db_name="";
	global previous
	previous = {}
	db=None
	global firebase
	global config
	config = {"apiKey": "","authDomain" : "","databaseURL": "","storageBucket":""}
	firebase = pyrebase.initialize_app(config)
	def __init__(self):
		# connect
		#self.db = MySQLdb.connect(host=self.host, user=self.username, passwd=self.password, db=self.db_name)

		self.firebase = pyrebase.initialize_app(config)

	def authenticate(self):
		auth = firebase.auth()
		email = ""
		passw = ""
		user = auth.sign_in_with_email_and_password(email, passw)
		return user

	def sendtodb(self, school, data):
		user = self.authenticate()
		db = firebase.database()
		# data = {
		#     "act":"murder",
		#     "witness":"false",
		#     "evidence":"trace"
		# }
		db.child(school).push(data, user['idToken'])



	#used for creating tables once
	def temp(self):
		cursor = self.db.cursor()

		#create necessary data table for each supported school
		cursor.execute("""CREATE TABLE NewReports(
			Datetime_scraped VARCHAR(255),
			Case_ID VARCHAR(255),
			School VARCHAR(255),
			Crime VARCHAR(255),
			Severity INT,
			Datetime_reported VARCHAR(255),
			Date_occured VARCHAR(255),
			Time_occured VARCHAR(255),
			Location VARCHAR(255),
			Description VARCHAR(255),
			Result VARCHAR(255),
			PRIMARY KEY(Case_ID)
		);""")

	# 	#create necessary data table for each supported school
	# 	# cursor.execute("""DROP TABLE NewReports""")


	# 	#commit your changes
		self.db.commit()




	#creates new table for a school with their abbreviation being used
	def create_new_school_table(self, school):
		cursor = self.db.cursor()



		#create necessary data table for each supported school
		cursor.execute("""CREATE TABLE """+str(school.upper())+"""(
			Case_ID VARCHAR(255),
			Crime VARCHAR(255),
			Severity INT,
			Datetime_reported VARCHAR(255),
			Date_occured VARCHAR(255),
			Time_occured VARCHAR(255),
			Location VARCHAR(255),
			Description VARCHAR(255),
			Result VARCHAR(255),
			PRIMARY KEY(Case_ID)
		);""")

		#commit your changes
		self.db.commit()

	#report is dictionary with key values of
	# 'case_number', 'crime', 'severity', 'datetime_reported', 'date_occured', 'time_occured', 'location', 'synopsis', 'case_disposition'
	def insert_report(self, school, report):
		
		dataMsg = {
			"crime" : report['crime'],
			"severity" : report["severity"],
			"datetime_reported" : report["datetime_reported"],
			"date_occured" : report["date_occured"],
			"time_occured" : report["time_occured"],
			"location" : report["location"],
			"description" : report["description"],
			"result" : report["result"]
		}
		self.sendtodb(school, dataMsg)
	#	self.notify()


	def notify(self):
		push = FCMNotification(api_key="")
		self.db.query("select * from tokens")
		results = self.db.store_result()
		results = results.fetch_row(maxrows=0)
		l = []
		for x in results:
			l.append(x[0])
		title = 'Crime Alert!'
		body = 'Crime!'
		msg  = {'location':'Bookstore', 'case_id':'170214-0692'}
		push.notify_multiple_devices(registration_ids=l,message_title = title, message_body=body, data_message=msg)
	def cleanse_new_reports(self):
		cursor = self.db.cursor()

		#create necessary data table for each supported school
		cursor.execute("SELECT Datetime_scraped, Case_ID FROM NewReports")

		#commit your changes
		self.db.commit()

		# for x in range(0, len(cursor)):
		# 	print(cursor[x])

		case_ids_delete=[]
		for row in cursor:
			#date and time the report was scraped
			datetime_scraped = row[0]
			datetime_scraped = datetime.datetime.strptime(datetime_scraped, "%Y-%m-%d %H:%M:%S")

			#current date and time
			new_datetime = self.get_current_datetime()
			new_datetime = datetime.datetime.strptime(new_datetime, "%Y-%m-%d %H:%M:%S")

			difference = new_datetime - datetime_scraped


			#if 10 minutes has passed
			if difference.seconds/60 >=10:
				case_ids_delete.append(row[1])


		# print("Case IDs to delete")
		for x in range(0, len(case_ids_delete)):
			# print(str(x)+": "+str(case_ids_delete[x]))

			cursor.execute("""DELETE FROM NewReports WHERE Case_ID = %s""", (case_ids_delete[x],))

		self.db.commit()

		# print()


	def get_current_datetime(self):
		curDate=str(datetime.datetime.utcnow())


		return curDate.split(".")[0]

	def test(self):
		x = self.read_reports('CSULB')
		print(x)
		self.insert_new_report('CSULB', x[0])


if __name__=="__main__":
	db=Database()

	# db.read_reports("SFSU")
	# print()
	# db.read_reports("CSULB")

	# db.read_new_reports()
	#db.temp()
	#db.notify()
	#db.cleanse_new_reports()

	# datetime = db.get_current_datetime()
	# print(datetime)

	#db.create_new_school_table("CSULB")
