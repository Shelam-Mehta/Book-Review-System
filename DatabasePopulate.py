import os
import requests
from flask import Flask, session,render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import pandas as pd
from multiprocessing import Pool

os.environ["DATABASE_URL"] = 'postgres://nodujvhkbnxhsg:ecae9a73eeadb899eb1bc04db6b924ea0fc9459423e3bd79bfae138c08441fbc@ec2-23-23-182-18.compute-1.amazonaws.com:5432/d5902kelgvk8jk'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app = Flask(__name__)
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

data=pd.read_csv('books.csv')
print(data[0:5])
# query="create table books (isbn CHAR(30) PRIMARY KEY,title CHAR(30) NOT NULL,year  INT  NOT NULL,author CHAR(30) NOT NULL)"
# query='select * from books'
# print(db.execute(query).fetchall())
# db.commit()
def InsertData(isbn,title,author,year):
    query = "INSERT INTO books(isbn,title,author,year) VALUES (:isbn,:title,:author,:year)"
    db.execute(query,{'isbn':isbn,'title':title,'author':author,'year':year})
    db.commit()
if(__name__=='__main__'):
    count=0
    data.values.tolist()
    p = Pool()  # Pool tells how many at a time
    print("bhai")
    #records = p.map(InsertData, data)
    p.close()
    p.join()

# print(data[:5])
# for i in range(123,len(data)):
# if(len(db.execute('select isbn from books where isbn=:isbn',{'isbn':isbn}).fetchall())!=0):
        


