import math, os, random
from flask import flash, Flask, redirect, render_template, request, session, url_for
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from datetime import datetime

from py_helper.helper import get_suggestions, sort_drinks

app = Flask(__name__)

# secret.key to be REMOVED prior to submission
# Use an env variable instead
app.secret_key = 'qjfg[73hzd<Gid#-h'

app.config["MONGO_DBNAME"] = 'drinksdb'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)


# Lists for help with building HTML element ID's in drink_form.html
class_num = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
class_name = ['One', 'One', 'Two', 'Two', 'Three', 'Three','Four', 'Four',
    'Five', 'Five', 'Six', 'Six', 'Seven', 'Seven', 'Eight', 'Eight',
    'Nine', 'Nine', 'Ten', 'Ten']
    
# Values for sorting options
num_drinks_list = ['6', '9', '12', "All"]
sort_by_list = ['name', 'views', 'comments', 'favorites', 'difficulty', 'date']
sort_order_list = ['Ascending', 'Descending']

# Default Sort Options:
# drinks_per_page | num_drinks_display | sort_by | 
# relevance flag | sort_order | sort_order_txt
sort_options = [9, '9', 'name', 1, 1, 'Ascending']


@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

@app.route("/", methods=['POST', 'GET'])
def index():

    categories=mongo.db.categories.find()
        
    # Get Suggested Drinks For User
    suggestions=get_suggestions(mongo, 4)

    # Sort Options
    if request.method=="POST":
        sort_drinks(mongo, sort_options) 
        return redirect (url_for('index'))

    # Set Drinks Display Options
    drinks_per_page = sort_options[0]
    sort_by = sort_options[2]
    sort_order = sort_options[4]
    
    # Pagination
    total_drinks = mongo.db.drinks.count()
    current_page = int(request.args.get('current_page', 1))
    total_drinks = mongo.db.drinks.count()
    num_pages = range(1, int(math.ceil(total_drinks / drinks_per_page)) +1)
    drinks = mongo.db.drinks.find().sort(sort_by, sort_order).skip(
        (current_page - 1) * drinks_per_page).limit(drinks_per_page)
    
    # Summary - (example) 'showing 1 - 9 of 15 results'
    x=current_page * drinks_per_page
    first_result_num = x - drinks_per_page + 1
    last_result_num = x if x < total_drinks else total_drinks
    
    # Get Quotes
    allQuotes=mongo.db.quotes.find_one({}, { "_id": 0, "quote": 1})['quote']
    quote=allQuotes[random.randrange(len(allQuotes))]
    quote_name, quote_text = quote.split(':', 1)
    
    
    return render_template('index.html',
        drinks = drinks,
        categories = categories,
        suggestions=suggestions,
        # Pagination & Sumarry
        current_page = current_page,
        pages = num_pages,
        first_result_num=first_result_num,
        last_result_num=last_result_num,
        # Quotes
        quote_name = quote_name,
        quote_text = quote_text,
        # Display Options
        sort_options=sort_options,
        # Items for Drop Downs
        num_drinks_list=num_drinks_list,
        sort_by_list=sort_by_list,
        sort_order_list=sort_order_list)
  
  
@app.route("/login", methods=['POST', 'GET'])
def login():
    # User login - check user/pass and route accordingly
    if request.method=='POST':
        user_list = mongo.db.users
        current_user = user_list.find_one({'userName': request.form['username']})
        if current_user:
            if request.form['password'] == current_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('account', account_name = session['username']))
            flash("Incorrect username and/or password. Please try again.")
            return render_template('login.html', title="Log In")
        flash("Username {} does not exist.".format(request.form['username']))
    return render_template('login.html', title="Log In")
    
    
@app.route("/logout")
def logout():
    # Log user out by clearing session data
    session.pop('username', None)
    return redirect(url_for('index'))
    

@app.route("/register", methods=['POST', 'GET'])
def register():
    # User registration - check user/pass and route accordingly
    if request.method == 'POST':
        user_list = mongo.db.users
        check_existing = user_list.find_one({"userName": request.form['username']})
        if not check_existing:
            user_list.insert_one({"userName": request.form['username'], "password": request.form['password']});
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        flash("Sorry, username '{}' has been taken. Please choose another".format(request.form['username']))
        return redirect(url_for('register'))
    return render_template('register.html', title="Register")

    
@app.route("/account/<account_name>", methods=['GET', 'POST'])
def account(account_name):
    # Check to make sure account being accessed through url matches
    # account stored in session.
    # This stops users accessing any account through the url bar.
    if account_name != session['username']:
        return redirect(url_for('account', account_name = session['username']))
    else:
        user = mongo.db.users.find_one({"userName": account_name})
        
        drinks_submitted_by_user = mongo.db.drinks.find(
            {"userName": account_name})
        drinks_favorited_by_user = mongo.db.drinks.find(
            {"favoritesTxt": account_name})
        
        # Page Title
        title = str(user['userName']).title()+"'s Account"

        # For all drinks submitted by the user, get their total views &
        # how many times they have been favorited by other users
        total_views = 0
        total_favorites = 0
        for drink in drinks_submitted_by_user:
            total_views += drink['views']
            total_favorites += drink['favorites']
        
        # Get drink which has been most viewed & drink which has been most
        # favorited by others, for current user
        most_viewed = mongo.db.drinks.find_one({
            "userName": account_name}, sort=[("views", -1)])
        most_favorited = mongo.db.drinks.find_one({
            "userName": account_name}, sort=[("favorites", -1)])
        
        # Get totals for drinks submitted and favorited for the user
        total_drinks_by_user = drinks_submitted_by_user.count()
        total_fave_drinks_by_user = drinks_favorited_by_user.count()
        
        # Pagination - User Submitted Drinks
        drinks_per_page = 4
        drinks_page = int(request.args.get('drinks_page', 1))
        num_dr_pages = range(1, int(math.ceil(
            total_drinks_by_user / drinks_per_page)) +1)
        drinks_submitted_by_user = mongo.db.drinks.find(
            {"userName": account_name}).sort("date", -1).skip(
            (drinks_page - 1) * drinks_per_page).limit(drinks_per_page)

        # Pagination - Users Favorite Drinks
        favorite_drinks_per_page = 4
        favorites_page = int(request.args.get('favorites_page', 1))
        num_fv_pages = range(1, int(math.ceil(
            total_fave_drinks_by_user / favorite_drinks_per_page)) +1)
        drinks_favorited_by_user = mongo.db.drinks.find(
            {"favoritesTxt": account_name}).sort("date", -1).skip(
            (favorites_page - 1) * favorite_drinks_per_page).limit(
            favorite_drinks_per_page)

        # Drinks Submitted By User Summary - (ex.) 'showing 1 - 9 of 15 results'
        x=drinks_page * drinks_per_page
        first_dr_result_num = x - drinks_per_page + 1
        last_dr_result_num = x if x < total_drinks_by_user\
            else total_drinks_by_user
        
        # Drinks Favorited By User Summary - (ex.) 'showing 1 - 9 of 15 results'
        x=favorites_page * favorite_drinks_per_page
        first_fv_result_num = x - favorite_drinks_per_page + 1
        last_fv_result_num = x if x < total_fave_drinks_by_user\
            else total_fave_drinks_by_user
        
        return render_template('account.html',
        user=user,
        users_drinks=drinks_submitted_by_user,
        favorited_drinks=drinks_favorited_by_user,
        title=title,
        # User stats
        views=total_views,
        favorites=total_favorites,
        most_viewed=most_viewed,
        most_favorited=most_favorited,
        total_drinks_by_user=total_drinks_by_user,
        total_fave_drinks_by_user=total_fave_drinks_by_user,
        # Pagination
        drinks_page = drinks_page,
        dr_pages = num_dr_pages,
        favorites_page = favorites_page,
        fv_pages = num_fv_pages,
        # Summaries
        first_dr_result_num=first_dr_result_num,
        last_dr_result_num=last_dr_result_num,
        first_fv_result_num=first_fv_result_num,
        last_fv_result_num=last_fv_result_num)


@app.route("/drink/<drink_id>", methods=['GET', 'POST'])
def drink(drink_id):
    drink = mongo.db.drinks.find_one({"_id": ObjectId(drink_id)})
    
    # Format Date
    date = datetime.strftime(drink.get('date'), '%d %B %Y')
    
    # Page Title
    title = drink['name']
    
    # Increment view counter
    if session['username'] != drink['userName']:
        mongo.db.drinks.update_one(
            {'_id': ObjectId(drink_id)}, {'$inc': {'views': int(1)}})
    
    # Instructions
    instructions = drink['instructions'].split(". ")

    # Comments - Split on ':' to get user & comment
    comment_user, comment_text = [], []
    if drink['commentsTxt']:
        for comment in drink['commentsTxt']:
            user, text = comment.split(':', 1)
            comment_user.append(user)
            comment_text.append(text)
        
            
    # Posting a comment
    if request.form.get('comment'):
        # Format string for new comment
        new_comment=session['username'] + ":" + request.form.get('comment')
        
        if list(mongo.db.drinks.find({
            # Check if duplicate comment exists
            '$and': [{'_id': ObjectId(drink_id)}, {
                    'commentsTxt': {'$elemMatch': {'$eq': new_comment}}}]})):
                flash("Duplicate comment already exists \
                    - say something different!")
        else:
            # Post only if not a duplicate
            mongo.db.drinks.find_one_and_update({
                '_id': ObjectId(drink_id)}, {
                '$push': {'commentsTxt': new_comment}})
            mongo.db.drinks.find_one_and_update({
                '_id': ObjectId(drink_id)}, {
                '$inc': {'comments': int(1)}})
            flash("Comment posted, thanks {}".format(session['username']))
        
        return redirect(url_for('drink', drink_id = drink_id))

    # Check if drink is in users favorites list
    is_favorite = 1 if drink_id in mongo.db.users.find_one(
        {'userName': session['username']})['favoritesTxt'] else 0
    

    return render_template('drink.html',
        title=title,
        drink=drink,
        date=date,
        instructions = instructions,
        comment_user = comment_user,
        comment_text = comment_text,
        is_favorite=is_favorite)


@app.route("/toggle_favorite/<drink_id>/<is_favorite>")
def toggle_favorite(drink_id, is_favorite):
    # Add or remove drink from favorites list for users and drinks collections
    action = '$pull' if is_favorite == "1" else '$push'
    mongo.db.users.find_one_and_update({
        'userName': session['username']}, {
        action: {'favoritesTxt': drink_id}})
    mongo.db.drinks.find_one_and_update({
        '_id': ObjectId(drink_id)}, {
        action: {'favoritesTxt': session['username']}})
    
    # Set value of favorites to length of favoritesTxt array
    favoritesTxt_length = len(mongo.db.drinks.find_one({
        '_id': ObjectId(drink_id)})['favoritesTxt'])
    mongo.db.drinks.find_one_and_update({
        '_id': ObjectId(drink_id)}, {
        '$set': {'favorites': favoritesTxt_length}})
    
    return redirect(url_for('drink', drink_id=drink_id))


@app.route("/add_drink", methods=['GET', 'POST'])
def add_drink():
    user = session['username']
    
    # Page Title
    title="Add Drink"
    
    # Dropdown menu contents
    all_categories = mongo.db.categories.find()
    all_glass_types = mongo.db.glass.find()
    all_difficulties = mongo.db.difficulty.find()
    
    # Default number of boxes to provide for ingredients & measures
    num_boxes=8
    
    if request.method == 'POST':
        dict = request.form.to_dict()
        
        # Append 'Duplicate' string to name if already exists
        if mongo.db.drinks.find_one({"name": dict['name']}):
            dict['name']=dict['name'].title()+" [DUPLICATE]"
            flash("Duplicate Name detected - Please Choose Another")
        else:
            dict['name']=dict['name'].title()
            
        dict['userName']=user
        
        # Add date
        date_today = datetime.strptime(
            datetime.utcnow().isoformat(), '%Y-%m-%dT%H:%M:%S.%f')
        dict['date']=date_today
        
        # Sort and process ingredients
        ingredients = []
        for k,v in list(dict.items()):
            if ('ingredient' in k) or ('measure' in k):
                ingredients.append(v)
        
        dict['ingredients'] = ingredients        
        dict['views']=int(0)
        dict['favoritesTxt'] = []
        dict['favorites'] = 0
        dict['commentsTxt'] = []
        dict['comments'] = 0
        
        mongo.db.drinks.insert_one(dict)
        
        new_drink_id = mongo.db.drinks.find_one({"name": dict['name']})['_id']
        flash("DRINK ADDED SUCCESSFULLY")
        return redirect(url_for('drink', drink_id = new_drink_id))
    
    
    return render_template('add_drink.html',
        user=user,
        title=title,
        all_categories=all_categories,
        all_glass_types=all_glass_types,
        all_difficulties=all_difficulties,
        # Set to None when adding drinks as nothing to match
        category_match=None,
        glass_type_match=None,
        difficulty_match=None,
        # Helpers for ingredient input
        class_num=class_num,
        class_name=class_name,
        num_boxes=num_boxes)
        

@app.route("/edit_drink/<drink_id>", methods=['GET', 'POST'])
def edit_drink(drink_id):
    
    drink = mongo.db.drinks.find_one({"_id": ObjectId(drink_id)})
    
    # Check user can edit drink - and not fudged URL
    user = session['username']
    if user != "Admin" and user != drink['userName']:
        flash("CHEEKY! YOU CAN ONLY EDIT YOUR OWN DRINKS!")    
        return redirect(url_for('drink', drink_id = drink_id))

    date = datetime.strftime(drink.get('date'), '%d %B %Y')
    
    all_categories = mongo.db.categories.find()
    all_glass_types = mongo.db.glass.find()
    all_difficulties = mongo.db.difficulty.find()
    
    # Number of boxes to provide for ingredients & measures
    num_boxes = len(drink['ingredients'])
    
    if request.method == 'POST':
            dict = request.form.to_dict()
            
            # Title-case drink name
            dict['name']=dict['name'].title()
            
            # Get ingredients
            ingredients = []
            for k,v in list(dict.items()):
                if ('ingredient' in k) or ('measure' in k):
                    ingredients.append(v)
                    dict.pop(k)
            
            dict['ingredients'] = ingredients
            
            mongo.db.drinks.update_one(drink, {"$set": dict}) 
            flash("UPDATE SUCCESSFUL")    
            return redirect(url_for('drink', drink_id = drink_id))
    
    # Page Title
    title="Editing "+str(drink['name'])
    
    return render_template('edit_drink.html',
        title=title,
        drink=drink,
        date=date,
        all_categories=all_categories,
        all_glass_types=all_glass_types,
        all_difficulties=all_difficulties,
        class_num=class_num,
        class_name=class_name,
        num_boxes=num_boxes,
        # Values to match in dropdowns
        category_match=drink['category'],
        glass_type_match=drink['glassType'],
        difficulty_match=drink['difficulty'])


@app.route("/delete_drink/<drink_id>", methods=['GET', 'POST'])
def delete_drink(drink_id):
    drinks = mongo.db.drinks
    
    drink_name = drinks.find_one({"_id": ObjectId(drink_id)})['name']
    drinks.delete_one({"_id": ObjectId(drink_id)})
    
    flash("{} has been deleted".format(drink_name))
    return redirect(url_for('index'))


@app.route("/search", methods=['GET', 'POST'])
def search():

    # Get Categories for filter dropdowns
    all_categories = mongo.db.categories.find()
    all_glass_types = mongo.db.glass.find()
    all_difficulties = mongo.db.difficulty.find()
    
    # Page Title
    title="Search"
    
    if request.args:
        # Take the filters selected by the user and convert them
        # to a dict that can be used in the main search query 
        filters = request.args.to_dict()
        filter_dict={}
        list_of_filters=['category_filter', 'glassType_filter', 'difficulty_filter']
        for k,v in filters.items():
            if k in list_of_filters and v!="":
                new_k = k.split("_")[0]
                filter_dict[new_k]=v
        
        # Keep track of filter values when navigating
        # between multiple pages of results.
        # Refactor???
        try:
            category_filter=filters['category_filter']
        except:
            category_filter=[]
        try:
            glassType_filter=filters['glassType_filter']
        except:
            glassType_filter=[]
        try:
            difficulty_filter=filters['difficulty_filter']
        except:
            difficulty_filter=[]
        
        find=request.args['find']
        
        # Sort Options
        if request.method=="POST":

            sort_drinks(mongo, sort_options)
            
            try:
                request.form['relevance']
            except:
                sort_options[3]=0
            else:
                sort_options[3]=1

            return redirect (url_for('search',
                category_filter=category_filter,
                glassType_filter=glassType_filter,
                difficulty_filter=difficulty_filter,
                find=find))
                
                
                
        # Display Options
        results_per_page = sort_options[0]
        sort_by = sort_options[2]
        sort_order = sort_options[4]
        current_page = int(request.args.get('current_page', 1))
        
        # Query drinks db with search string and filters
        search_str = {'$text': {'$search': find }} if find != "" else {'name': {'$regex': ""}}
        
        
        if sort_options[3]!=1:
            # Standard Search
            results = mongo.db.drinks.find(
                {'$and': [search_str, filter_dict] }, {'score': {'$meta': 'textScore'}}
                ).sort(sort_by, sort_order
                ).skip((current_page - 1)*results_per_page).limit(results_per_page)
        
        else:
            # Return search results ordered first by relevance
            results = mongo.db.drinks.find(
                {'$and': [search_str, filter_dict] }, {'score': {'$meta': 'textScore'}}
                ).sort([('score', {'$meta': 'textScore'}), (sort_by, sort_order), ('name', pymongo.ASCENDING)]
                ).skip((current_page - 1)*results_per_page).limit(results_per_page)
        
        
        
        # ORIGINAL - Keep For Now For Reference
        # results = mongo.db.drinks.find(
        #     {'$and': [search_str, filter_dict] }, {'score': {'$meta': 'textScore'}}
        #     ).sort([('score', {'$meta': 'textScore'}), (sort_by, sort_order), ('name', pymongo.ASCENDING)]
        #     ).skip((current_page - 1)*results_per_page).limit(results_per_page)
        
        num_results=results.count()
            
        # If no results for search
        if num_results==0:
            return render_template('search.html',
                title="No Results Found",
                find=find,
                num_results=num_results,
                # Items for filters
                all_categories=all_categories,
                all_glass_types=all_glass_types,
                all_difficulties=all_difficulties)
        
        # Pagination
        num_pages = range(1, int(math.ceil(num_results / results_per_page)) + 1)
        
        # Summary - (example) 'showing 1 - 9 of 15 results'
        x=current_page * results_per_page
        first_result_num = x - results_per_page + 1
        last_result_num = x if x < num_results else num_results
        
        
        # From search results, find max value of 'score' to allow search.html
        # to calculate the results relevance as a % of highest scoring result
        if find != "":
            max_weight = mongo.db.drinks.find_one({'$and': [{'$text': {'$search': find }}, filter_dict] },{
                'score': {'$meta': 'textScore'}}, sort=[('score', {'$meta': 'textScore'})])['score']
        else:
            max_weight=None
            
        # Page Title
        title="Search Results"
        
        
        print("")    
        print(category_filter)        
        print("")        

        return render_template('search.html',
            title=title,
            find=find,
            # Results 
            results=results,
            first_result_num=first_result_num,
            last_result_num=last_result_num,
            # Search result scores
            max_weight = max_weight,
            # Pagination | Navigation
            results_per_page=results_per_page, # Check if needed?
            current_page = current_page,
            pages = num_pages,
            # Pagination | Filter Choices
            category_filter=category_filter,
            glassType_filter=glassType_filter,
            difficulty_filter=difficulty_filter,
            # Items for filters
            all_categories=all_categories,
            all_glass_types=all_glass_types,
            all_difficulties=all_difficulties,
            # Display Options
            sort_options=sort_options,
            # Items for Drop Downs
            num_drinks_list=num_drinks_list,
            sort_by_list=sort_by_list,
            sort_order_list=sort_order_list)
    
    return render_template('search.html',
        title=title,
        # Items for filters
        all_categories=all_categories,
        all_glass_types=all_glass_types,
        all_difficulties=all_difficulties)


@app.route("/category/<category_name>", methods=['GET', 'POST'])
def category(category_name):
    category = mongo.db.categories.find_one({"category": category_name})
    title=category['category'].title()
        
        
    # Sort Options
    if request.method=="POST":
        sort_drinks(mongo, sort_options) 
        return redirect (url_for('category', category_name = category_name))
    
    
    # Display Options
    drinks_per_page = sort_options[0]
    sort_by = sort_options[2]
    sort_order = sort_options[4]
    
    # Pagination
    total_drinks = mongo.db.drinks.count()
    current_page = int(request.args.get('current_page', 1))
    total_drinks = mongo.db.drinks.find({"category": category_name}).count()
    num_pages = range(1, int(math.ceil(total_drinks / drinks_per_page)) +1)
    drinks = mongo.db.drinks.find({"category": category_name}).sort(sort_by, sort_order).skip((current_page - 1) * drinks_per_page).limit(drinks_per_page)
    
    # Summary - (example) 'showing 1 - 9 of 15 results'
    x=current_page * drinks_per_page
    first_result_num = x - drinks_per_page + 1
    last_result_num = x if x < total_drinks else total_drinks
    
    
    
    return render_template('category.html',
        title=title,
        category=category,
        drinks = drinks,
        # Pagination
        current_page = current_page,
        pages = num_pages,
        first_result_num=first_result_num,
        last_result_num=last_result_num,
        # Display Options
        sort_options=sort_options,
        # Items for Drop Downs
        num_drinks_list=num_drinks_list,
        sort_by_list=sort_by_list,
        sort_order_list=sort_order_list)
        
        



# Error Handling Pages

@app.errorhandler(404)
def page_not_found(e):
    # return redirect(url_for('errors', filename='404.html')), 404
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    session.clear(e)
    # return redirect(url_for('errors', filename='500.html')), 500
    return render_template('500.html'), 500


## TESTING STUFF

## END TESTING


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)