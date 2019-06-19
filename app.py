import os
import random
from flask import Flask, redirect, render_template, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

# secret.key tp be REMOVED prior to submission
# Use an env variable instead
app.secret_key = 'qjfg[73hzd<Gid#-h'

app.config["MONGO_DBNAME"] = 'drinksdb'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)

@app.route("/")
def index():
    print("2")
    
    # Get all kv pairs
    allQuotes = (mongo.db.quotes.find_one ({},{ "_id": 0, "quote": 1}))
    # Store just the value array as x
    x = allQuotes.get("quote")
    i = random.randrange(0, len(x),2)
    quoteName = x[i]
    quoteText = x[i+1]
    print(quoteName, " - ", quoteText)
    
    
    return render_template('index.html',
    drinks = mongo.db.drinks.find())
    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)