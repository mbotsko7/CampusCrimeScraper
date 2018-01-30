import pyrebase

def auth():
    auth = firebase.auth()
    email = ""
    password = ""
    user = auth.sign_in_with_email_and_password(email, password)
    return user
def purge():
    user = auth()
    print(user)
    db = firebase.database()
    all_crimes = db.child("CSUN").get()
    ids = []
    remove = []
    for crime in all_crimes.each():
      if ids.count(crime.val()["datetime_reported"]) != 0:
        remove.append(crime.key())
      else:
        ids.append(crime.val()["datetime_reported"])
    for val in remove:
      db.child("CSUN").child(val).remove()

    

config = {
"apiKey": "",
"authDomain" : "",
"databaseURL": "",
"storageBucket":""
}

firebase = pyrebase.initialize_app(config)
purge()
