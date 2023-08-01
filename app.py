from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
from datetime import datetime
import pyrebase


Config = {
  "apiKey": "AIzaSyApUSCYCmsYSTdsX45HmuGaaqG9C2dCz0o",
  "authDomain": "finalpy2.firebaseapp.com",
  "projectId": "finalpy2",
  "storageBucket": "finalpy2.appspot.com",
  "messagingSenderId": "145805406928",
  "appId": "1:145805406928:web:1ea3d7f4247da768a1a4d5",
  "measurementId": "G-63GF6RYNTW",
  "databaseURL": "https://finalpy2-default-rtdb.firebaseio.com/"
};

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'



@app.route('/', methods=['GET', 'POST'])
def signup():
    error = ""
    # trying = {"userid":"secret","userName":"Fatma Azaizah","date":"01-08-2023","story":"my journy in lessan was very exciting, i learned aot of usefull things that helped me alot finding a higher paied job, and in general just meeting new people and developing relationship with israelis"}
    # db.child("Posts").push(trying)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print("YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        user = {"email":request.form['email'],
            "password":request.form['password'],
            "full_name":request.form['full_name'],
            "username":request.form['username'],
            "alumni":request.form['alumni']}  
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)    
            UID = login_session['user']['localId']
            # cities = db.child("Cities").get().val().keys()
            # username = db.child("Users").child(UID).child("username").get().val()
            # pic = random.choice(list(db.child("Cities").get().val().keys()))
     
            db.child("Users").child(UID).set(user)
            print("LOOOOO")
            if request.form['alumni'] == "alumni" :
                return redirect(url_for('alumni'))
            else:
                return redirect(url_for('notalumni'))
        except:
            return render_template("signup.html",error = "authentication failed")
    else:
        return render_template("signup.html")



@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""

    if request.method == 'POST':

        try:
            email = request.form['email']
            password = request.form['password']


            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            if request.form['alumni'] == "alumni" :
                return redirect(url_for('alumni'))
            else:
                return redirect(url_for('notalumni'))
        except:
            error = "signin failed"  
    return render_template("signin.html",error = "Authentication failed")



# @app.route("/posts", methods = ["GET", "POST"])
# def home():
#     UID = login_session['user']['localId']
#     cities = db.child("Cities").get().val().keys()
#     username = db.child("Users").child(UID).child("username").get().val()
#     pic = random.choice(list(db.child("Cities").get().val().keys()))
#     try:
#         fav_cities = db.child("Users").child(UID).child("favs").get().val().keys()
#         return render_template("home.html", cities = cities, favs = fav_cities, username = username, pic = pic)
#     except:
#         return render_template("home.html", cities = cities, username = username, pic = pic)


@app.route('/alumni')
def alumni(): 
    posts = db.child("Posts").get().val()
    return render_template("alumni.html", posts=posts)



@app.route('/posting', methods=['GET', 'POST'])
def posting(): 
        if request.method == 'POST':
            UID = login_session['user']['localId']
            userName = request.form['username']
            date = request.form['date']
            story = request.form['story']
            post = {"userid":UID,"userName":userName,"date":date,"story":story}

            db.child("Posts").push(post)
            print("YOU HAVE REACHED HERE")
            return redirect(url_for('alumni'))
        return render_template("posting.html")

@app.route('/notalumni')
def notalumni():
    try :

        posts = db.child("Posts").get().val()
    except:
        ptint("nice")
        posts = {}
    return render_template("notalumni.html",posts = posts)

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))



if __name__ == '__main__':
    app.run(debug=True)