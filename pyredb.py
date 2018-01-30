import pyrebase


def auth():
    auth = firebase.auth()
    email = ""
    password = ""
    user = auth.sign_in_with_email_and_password(email, password)
    return user
def sendtodb():
    user = auth()
    db = firebase.database()
    data = {
        "act":"murder",
        "witness":"false",
        "evidence":"trace"
    }
    print( db.child("CSULB").order_by_child("datetime_reported").get(user['idToken']).val())

    

config = {
"apiKey": "",
"authDomain" : "",
"databaseURL": "",
"storageBucket":"",
"messagingSenderId": ""
}

firebase = pyrebase.initialize_app(config)
sendtodb()
