import os
import requests

from flask import Flask, session, render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import pandas as pd

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

query="create table Rating (isbn VARCHAR(30)  REFERENCES books(isbn) ON DELETE CASCADE,username VARCHAR(30)  REFERENCES users(username) ON DELETE CASCADE,rating INT NOT NULL ,PRIMARY KEY (username,isbn))"
db.execute(query)
db.commit()