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
    db.child("crime").push(data, user['idToken'])

    

config = {
"apiKey": "",
"authDomain" : "",
"databaseURL": "",
"storageBucket":""
}

firebase = pyrebase.initialize_app(config)
sendtodb()
