import os
import requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
os.environ["DATABASE_URL"]='postgres://nodujvhkbnxhsg:ecae9a73eeadb899eb1bc04db6b924ea0fc9459423e3bd79bfae138c08441fbc@ec2-23-23-182-18.compute-1.amazonaws.com:5432/d5902kelgvk8jk'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    #return "Project 1: TODO"
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "cG46cghUhz8fZwTxDxiwVQ", "isbns": "9781632168146"})
    return res.json()
@app.route("/Registration",methods=['GET','POST'])
def Registration():
    
    return render_template('Registration.html',Title="REGISRATION FORM")
@app.route("/Login",methods=['GET','POST'])
def Login():
    #return request.method
    if request.method == 'POST':
        username=request.form['username']
        fullname=request.form['fullname']
        
        password=request.form['psw']
        query="INSERT INTO users (username, password, fullname) VALUES (:username,:password,:fullname)"
        #insert=(username, password, fullname)
        db.execute(query, {'username':username,'password':password,'fullname':fullname})
        db.commit()
    return render_template('Login.html',Title="LOGIN FORM")
@app.route("/Home",methods=['POST','GET'])
def Home():
    username=request.form['username']
    password=request.form['psw']

    session['username']=username
    session['password']=password
    query="SELECT username FROM users WHERE username=:username AND password=:password"
    user=db.execute(query, {'username':username, 'password':password}).fetchall()
    if (len(user)==0):
        return render_template('Login.html',Title="LOGIN FORM")
    else:
        return render_template('Home.html',username=username,Title="HOME")
@app.route("/ShowRating",methods=['POST','GET'])
def ShowRating():
    # if(request.method=='PUT'):
    #     return request.method
    book=request.form['books']
    searchkeyword=request.form['searchkeyword']
    if(book=='year'):
        query="SELECT * FROM books WHERE "+book+"=:searchkeyword"
    else:
        searchkeyword='%'+searchkeyword+'%'
        query="SELECT * FROM books WHERE "+book+" like  :searchkeyword "
    booklist=db.execute(query,{'searchkeyword':searchkeyword}).fetchall()
    #return booklist
    return render_template('Rating.html',booklist=booklist,Title="Show Rating" )

@app.route("/BookDetail/",methods=['POST','GET'])
def ModifyRating():
    isbn=request.form['isbn']
    rating=request.form['rating']
    booklist=request.form['booklist']
    username=session['username']
    query="INSERT INTO rating (username, isbn, rating) VALUES (:username, :isbn, :rating)"
    db.execute(query, {'username':username,'isbn':isbn,'rating':rating})
    db.commit()
    return render_template('Rating.html',booklist=booklist,Title="Book Detail" )

if(__name__=="__main__"):
    app.run(debug=True,use_reloader=False)

