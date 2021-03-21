# import necessary libraries
from flask import Flask, render_template
# create instance of Flask app
app = Flask(__name__)
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo
# Create connection variable
conn = 'mongodb://localhost:27017'
# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)
# Connect to a database. Will create one if not already available.
db = client.team_db
# Drops collection if available to remove duplicates
db.team.drop()
