import math, os
import random
from flask import flash, Flask, redirect, render_template, request, session, url_for
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from datetime import datetime

#from flask_paginate import Pagination, get_page_parameter


app = Flask(__name__)

# secret.key to be REMOVED prior to submission
# Use an env variable instead
app.secret_key = 'qjfg[73hzd<Gid#-h'

app.config["MONGO_DBNAME"] = 'drinksdb'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)


@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

@app.route("/")
def index():

    ## Get Quotes - can be refactored - and should be!
    # Get all kv pairs
    allQuotes = (mongo.db.quotes.find_one ({},{ "_id": 0, "quote": 1}))
    # Store just the value array as x
    x = allQuotes.get("quote")
    i = random.randrange(0, len(x),2)
    quoteName = x[i]
    quoteText = x[i+1]
    
    
    # Pagination
    drinks_per_page = 9
    current_page = int(request.args.get('current_page', 1))
    total_drinks = mongo.db.drinks.count()
    num_pages = range(1, int(math.ceil(total_drinks / drinks_per_page)) +1)
    drinks = mongo.db.drinks.find().sort('name', pymongo.ASCENDING).skip((current_page - 1) * drinks_per_page).limit(drinks_per_page)
    
    return render_template('index.html',
        drinks = drinks,
        current_page = current_page,
        pages = num_pages,
        categories = mongo.db.categories.find(),
        quoteName = quoteName,
        quoteText = quoteText)
    
    
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_list = mongo.db.users
        current_user = user_list.find_one({'userName': request.form['username']})
        if current_user:
            if request.form['password'] == current_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            flash("Incorrect username and/or password. Please try again.")
            return render_template('login.html')
        flash("Username {} does not exist.".format(request.form['username']))
    return render_template('login.html')
    
    
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
    

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_list = mongo.db.users
        check_existing = user_list.find_one({"userName": request.form['username']})
        if not check_existing:
            user_list.insert_one({"userName": request.form['username'], "password": request.form['password']});
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        flash("Sorry, username '{}' has been taken. Please choose another".format(request.form['username']))
        return redirect(url_for('register'))
    return render_template('register.html')

    
@app.route("/account")
def account():
    return render_template('account.html')


@app.route("/search")
def search():
    return render_template('search.html')
    

@app.route("/drink/<drink_id>", methods=['GET', 'POST'])
def drink(drink_id):
    drink = mongo.db.drinks.find_one({"_id": ObjectId(drink_id)})
    # Format Date
    date = datetime.strftime(drink.get('dateAdded'), '%d %B %Y')
    
    # Get Ingredients
    ingredients, measures = [], [] 
    full_ingredients=list(drink.get('ingredients').values())
    for i in range(0, len(full_ingredients),2):
        ingredients.append(full_ingredients[i])
        measures.append(full_ingredients[i+1])
    # Store number of ingredients
    num_ingredients = int(len(ingredients))
    
    # Instructions
    instructions = drink['instructions'].split(". ")
    print(type(instructions))
    
    return render_template('drink.html',
        drink=drink,
        date=date,
        instructions = instructions,
        ingredients = ingredients,
        measures = measures,
        num_ingredients=num_ingredients)


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)