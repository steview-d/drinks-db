import math
import os
import random
from flask import (flash, Flask, redirect, render_template, request, session,
                   url_for)
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from datetime import datetime

from py_helper.helper import get_suggestions, sort_drinks, get_ingredients

app = Flask(__name__)

# import local env vars if in local dev environment
if os.path.exists('env.py'):
    import env

app.config['SECRET_KEY'] = os.getenv('SECRET')
app.config["MONGO_DBNAME"] = 'drinksdb'
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mongo = PyMongo(app)

# Lists for help with building HTML element ID's in drink_form.html
class_num = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10]
class_name = ['One', 'One', 'Two', 'Two', 'Three', 'Three', 'Four', 'Four',
              'Five', 'Five', 'Six', 'Six', 'Seven', 'Seven', 'Eight', 'Eight',
              'Nine', 'Nine', 'Ten', 'Ten']

# Values for sorting options
num_drinks_list = ['4', '8', '12', "All"]
sort_by_list = ['name', 'views', 'comments', 'favorites', 'difficulty', 'date']
sort_order_list = ['Ascending', 'Descending']

# Default Sort Options:
# drinks_per_page | num_drinks_display | sort_by |
# relevance flag | sort_order | sort_order_txt
default_sort_options = [8, '8', 'name', 0, 1, 'Ascending']


# Routes

@app.route("/")
def landing():
    return render_template('landing.html')


@app.route("/all_drinks", methods=['POST', 'GET'])
def index():
    categories = mongo.db.categories.find()
    glass_types = mongo.db.glass.find()
    difficulties = mongo.db.difficulty.find()

    # Get Num (arg2) Suggested Drinks For User
    suggestions = get_suggestions(mongo, 4)

    # Sort Options
    # Check if session exists
    if session.get('sort_options') is None:
        session['sort_options'] = default_sort_options

    if request.method == "POST":
        sort_drinks(mongo)
        return redirect(url_for('index'))

    # Set Drinks Display Options
    drinks_per_page = session['sort_options'][0]
    sort_by = session['sort_options'][2]
    sort_order = session['sort_options'][4]
    sort_options = session['sort_options']

    # Pagination
    current_page = int(request.args.get('current_page', 1))
    total_drinks = mongo.db.drinks.count()
    num_pages = range(1, int(math.ceil(total_drinks / drinks_per_page)) + 1)
    drinks = mongo.db.drinks.find().sort(sort_by, sort_order).skip(
        (current_page - 1) * drinks_per_page).limit(drinks_per_page)

    # Summary - (example) 'showing 1 - 9 of 15 results'
    x = current_page * drinks_per_page
    first_result_num = x - drinks_per_page + 1
    last_result_num = x if x < total_drinks else total_drinks

    return render_template('index.html',
                           drinks=drinks,
                           categories=categories,
                           glass_types=glass_types,
                           difficulties=difficulties,
                           suggestions=suggestions,
                           # Pagination & Sumarry
                           current_page=current_page,
                           pages=num_pages,
                           first_result_num=first_result_num,
                           last_result_num=last_result_num,
                           # Display Options
                           sort_options=sort_options,
                           # Items for Drop Downs
                           num_drinks_list=num_drinks_list,
                           sort_by_list=sort_by_list,
                           sort_order_list=sort_order_list)


@app.route("/login", methods=['POST', 'GET'])
def login():
    # Confirm not already logged in
    if session.get('username'):
        flash("Already logged in. Logout first to login as a different user.")
        return redirect(url_for('index'))

    # User login - check user/pass and route accordingly
    if request.method == 'POST':
        user_list = mongo.db.users
        current_user = user_list.find_one(
            {'userName': request.form['username']})
        if current_user:
            if request.form['password'] == current_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index'))
            flash("Incorrect username and/or password. Please try again.")
            return render_template('login.html', title="Log In")
        flash("Username '{}' does not exist.".format(request.form['username']))
    return render_template('login.html', title="Log In")


@app.route("/logout")
def logout():
    # Log user out by clearing session data
    session.pop('username', None)
    flash("Logged Out Successfully")
    return redirect(url_for('index'))


@app.route("/register", methods=['POST', 'GET'])
def register():
    # Confirm not already logged in
    if session.get('username'):
        flash("Already logged in. Logout first to register a new user.")
        return redirect(url_for('index'))

    # User registration - check user/pass and route accordingly
    if request.method == 'POST':
        user_list = mongo.db.users
        check_existing = user_list.find_one(
            {"userName": request.form['username']})
        if not check_existing:
            user_list.insert_one({"userName": request.form['username'],
                                  "password": request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        flash(
            "Sorry, username '{}' has been taken. Please choose "
            "another".format(
                request.form['username']))
        return redirect(url_for('register'))
    return render_template('register.html', title="Register")


@app.route("/account/<account_name>")
def account(account_name):
    # Check to make sure account being accessed through url matches
    # account stored in session.
    if account_name != session.get('username'):
        flash("You can only access your own account page.")
        return redirect(url_for('index'))
    else:
        user = mongo.db.users.find_one({"userName": account_name})

        drinks_submitted_by_user = mongo.db.drinks.find(
            {"userName": account_name})
        drinks_favorited_by_user = mongo.db.drinks.find(
            {"favoritesTxt": account_name})

        # Page Title
        title = str(user['userName']).title() + "'s Account"

        # For all drinks submitted by the user, get their total views,
        # comments, and how many times they have been favorited by other users
        total_views = 0
        total_favorites = 0
        total_comments = 0
        for drink in drinks_submitted_by_user:
            total_views += drink['views']
            total_favorites += drink['favorites']
            total_comments += drink['comments']

        # Get drinks with most views, comments, favorites, for current user
        if drinks_submitted_by_user.count() != 0:
            most_viewed = mongo.db.drinks.find_one({
                "userName": account_name}, sort=[("views", -1)])
            if most_viewed['views'] == 0:
                most_viewed = None

            most_favorited = mongo.db.drinks.find_one({
                "userName": account_name}, sort=[("favorites", -1)])
            if most_favorited['favorites'] == 0:
                most_favorited = None

            most_commented = mongo.db.drinks.find_one({
                "userName": account_name}, sort=[("comments", -1)])
            if most_commented['comments'] == 0:
                most_commented = None

        else:
            most_viewed, most_favorited, most_commented = None, None, None

        # Get general db stats
        total_drinks = mongo.db.drinks.count()
        total_categories = mongo.db.categories.count()
        total_glass_types = mongo.db.glass.count()
        total_difficulties = mongo.db.difficulty.count()

        # Get totals for drinks submitted and favorited for the user
        total_drinks_by_user = drinks_submitted_by_user.count()
        total_user_fave_drinks = drinks_favorited_by_user.count()

        # Pagination - User Submitted Drinks
        drinks_per_page = 4 if total_drinks_by_user < 21 else 8
        drinks_page = int(request.args.get('drinks_page', 1))
        num_dr_pages = range(1, int(math.ceil(
            total_drinks_by_user / drinks_per_page)) + 1)
        drinks_submitted_by_user = mongo.db.drinks.find(
            {"userName": account_name}).sort("date", -1).skip(
            (drinks_page - 1) * drinks_per_page).limit(drinks_per_page)

        # Pagination - Users Favorite Drinks
        favorite_drinks_per_page = 4 if total_user_fave_drinks < 21 else 8
        favorites_page = int(request.args.get('favorites_page', 1))
        num_fv_pages = range(1, int(math.ceil(
            total_user_fave_drinks / favorite_drinks_per_page)) + 1)
        drinks_favorited_by_user = mongo.db.drinks.find(
            {"favoritesTxt": account_name}).sort("date", -1).skip(
            (favorites_page - 1) * favorite_drinks_per_page).limit(
            favorite_drinks_per_page)

        # Drinks Submitted By User Summary - (ex.) 'showing 1 - 9 of 15
        # results'
        x = drinks_page * drinks_per_page
        first_dr_result_num = x - drinks_per_page + 1
        last_dr_result_num = x if x < total_drinks_by_user else \
            total_drinks_by_user

        # Drinks Favorited By User Summary - (ex.) 'showing 1 - 9 of 15
        # results'
        x = favorites_page * favorite_drinks_per_page
        first_fv_result_num = x - favorite_drinks_per_page + 1
        last_fv_result_num = x if x < total_user_fave_drinks else \
            total_user_fave_drinks

        return render_template('account.html',
                               user=user,
                               users_drinks=drinks_submitted_by_user,
                               favorited_drinks=drinks_favorited_by_user,
                               title=title,
                               # User stats
                               views=total_views,
                               favorites=total_favorites,
                               comments=total_comments,
                               most_viewed=most_viewed,
                               most_favorited=most_favorited,
                               most_commented=most_commented,
                               total_drinks_by_user=total_drinks_by_user,
                               total_user_fave_drinks=total_user_fave_drinks,
                               # DB Stats
                               total_drinks=total_drinks,
                               total_categories=total_categories,
                               total_glass_types=total_glass_types,
                               total_difficulties=total_difficulties,
                               # Pagination
                               drinks_page=drinks_page,
                               dr_pages=num_dr_pages,
                               favorites_page=favorites_page,
                               fv_pages=num_fv_pages,
                               # Summaries
                               first_dr_result_num=first_dr_result_num,
                               last_dr_result_num=last_dr_result_num,
                               first_fv_result_num=first_fv_result_num,
                               last_fv_result_num=last_fv_result_num)


@app.route("/drink/<drink_id>", methods=['POST', 'GET'])
def drink(drink_id):
    drink = mongo.db.drinks.find_one({"_id": ObjectId(drink_id)})

    # Format Date
    date = datetime.strftime(drink.get('date'), '%d %B %Y')

    # Page Title
    title = drink['name']

    # List of path partials to exclude from view counter
    exclude_paths = ['drink/', 'toggle_favorite']

    # Increment view counter
    # Continue only if previous url is not in exclude paths
    if request.referrer and not any(
            s in request.referrer for s in exclude_paths):
        # Update views if drink by a different user, or no user logged in
        if session.get('username') is None or session['username'] != drink[
                'userName']:
            mongo.db.drinks.update_one(
                {'_id': ObjectId(drink_id)}, {'$inc': {'views': int(1)}})
    views = mongo.db.drinks.find_one({"_id": ObjectId(drink_id)})['views']

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
        new_comment = session['username'] + ":" + request.form.get('comment')

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
                '$addToSet': {'commentsTxt': new_comment}})
            # Set value of comments to length of commentsTxt array
            comments_txt_length = len(mongo.db.drinks.find_one({
                '_id': ObjectId(drink_id)})['commentsTxt'])
            mongo.db.drinks.find_one_and_update({
                '_id': ObjectId(drink_id)}, {
                '$set': {'comments': comments_txt_length}})
            flash("Comment posted, thanks {}".format(session['username']))

        return redirect(url_for('drink', drink_id=drink_id))

    # Check if drink is in users favorites list
    try:
        user_favorites = \
            mongo.db.users.find_one({'userName': session['username']})[
                'favoritesTxt']
    except KeyError:
        user_favorites = []
    is_favorite = 1 if drink_id in user_favorites else 0

    # Get Quotes
    all_quotes = mongo.db.quotes.find_one({}, {"_id": 0, "quote": 1})['quote']
    quote = all_quotes[random.randrange(len(all_quotes))]
    quote_name, quote_text = quote.split(':', 1)

    return render_template('drink.html',
                           title=title,
                           drink=drink,
                           date=date,
                           views=views,
                           instructions=instructions,
                           comment_user=comment_user,
                           comment_text=comment_text,
                           is_favorite=is_favorite,
                           quote_name=quote_name,
                           quote_text=quote_text)


@app.route("/toggle_favorite/<drink_id>/<is_favorite>")
def toggle_favorite(drink_id, is_favorite):
    # Add or remove drink from favorites list for users and drinks collections
    action = '$pull' if is_favorite == "1" else '$addToSet'
    mongo.db.users.find_one_and_update({
        'userName': session['username']}, {
        action: {'favoritesTxt': drink_id}})
    mongo.db.drinks.find_one_and_update({
        '_id': ObjectId(drink_id)}, {
        action: {'favoritesTxt': session['username']}})

    # Set value of favorites to length of favoritesTxt array
    favorites_txt_length = len(mongo.db.drinks.find_one({
        '_id': ObjectId(drink_id)})['favoritesTxt'])
    mongo.db.drinks.find_one_and_update({
        '_id': ObjectId(drink_id)}, {
        '$set': {'favorites': favorites_txt_length}})

    return redirect(url_for('drink', drink_id=drink_id))


@app.route("/add_drink", methods=['POST', 'GET'])
def add_drink():
    # Check to make sure a user is logged in
    if not session.get('username'):
        flash("You must be logged in to add a drink.")
        return redirect(url_for('index'))

    # Page Title
    title = "Add Drink"

    # Dropdown menu contents
    all_categories = mongo.db.categories.find()
    all_glass_types = mongo.db.glass.find()
    all_difficulties = mongo.db.difficulty.find()

    # Default number of boxes to provide for ingredients & measures
    num_boxes = 8

    if request.method == 'POST':
        drink_dict = request.form.to_dict()

        # Append 'Duplicate' string to name if already exists
        if mongo.db.drinks.find_one({"name": drink_dict['name'].title()}):
            drink_dict['name'] = drink_dict['name'].title() + " [DUPLICATE]"
            flash("Duplicate Name Detected - Please Change To Another")
        else:
            drink_dict['name'] = drink_dict['name'].title()

        drink_dict['userName'] = session['username']

        # Add date
        date_today = datetime.strptime(
            datetime.utcnow().isoformat(), '%Y-%m-%dT%H:%M:%S.%f')
        drink_dict['date'] = date_today

        # Process ingredients & measures
        drink_dict['ingredients'] = get_ingredients(drink_dict)

        drink_dict['views'] = int(0)
        drink_dict['favoritesTxt'] = []
        drink_dict['favorites'] = 0
        drink_dict['commentsTxt'] = []
        drink_dict['comments'] = 0

        mongo.db.drinks.insert_one(drink_dict)

        new_drink_id = mongo.db.drinks.find_one({"name": drink_dict['name']})[
            '_id']
        flash("DRINK ADDED SUCCESSFULLY")
        return redirect(url_for('drink', drink_id=new_drink_id))

    return render_template('add_drink.html',
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

    # Check user is trying to edit only their own drink
    user = session.get('username')
    if user != drink['userName']:
        flash("You can only edit drinks you have submitted yourself.")
        return redirect(url_for('drink', drink_id=drink_id))

    date = datetime.strftime(drink.get('date'), '%d %B %Y')

    # Page Title
    title = "Editing " + str(drink['name'])

    # Dropdown menu contents
    all_categories = mongo.db.categories.find()
    all_glass_types = mongo.db.glass.find()
    all_difficulties = mongo.db.difficulty.find()

    # Number of boxes to provide for ingredients & measures
    num_boxes = len(drink['ingredients'])

    if request.method == 'POST':
        drink_dict = request.form.to_dict()

        if mongo.db.drinks.find_one({'$and': [{
            'name': drink_dict['name'].title()},
                {'_id': {'$ne': ObjectId(drink_id)}}]}):
            drink_dict['name'] = drink_dict['name'].title() + " [DUPLICATE]"
            flash("Duplicate Name detected - Please Change To Another")
        else:
            drink_dict['name'] = drink_dict['name'].title()

        # Process ingredients & measures
        drink_dict['ingredients'] = get_ingredients(drink_dict)

        mongo.db.drinks.update_one(drink, {"$set": drink_dict})
        flash("UPDATE SUCCESSFUL")
        return redirect(url_for('drink', drink_id=drink_id))

    return render_template('edit_drink.html',
                           drink=drink,
                           date=date,
                           title=title,
                           all_categories=all_categories,
                           all_glass_types=all_glass_types,
                           all_difficulties=all_difficulties,
                           # Helpers for ingredient input
                           class_num=class_num,
                           class_name=class_name,
                           num_boxes=num_boxes,
                           # Values to match in dropdowns
                           category_match=drink['category'],
                           glass_type_match=drink['glassType'],
                           difficulty_match=drink['difficulty'])


@app.route("/delete_drink/<drink_id>")
def delete_drink(drink_id):
    drinks = mongo.db.drinks

    # Check user attempting to delete drink is allowed
    if session.get('username') != drinks.find_one({
            "_id": ObjectId(drink_id)})['userName']:
        flash("Oh no you don't! That's not your drink to delete.")
        return redirect(url_for('drink', drink_id=drink_id))
    else:
        # Get list of users who have favorited this drink and remove
        # the drink from their favorites list
        user_faves = drinks.find_one({
            "_id": ObjectId(drink_id)})['favoritesTxt']
        for name in user_faves:
            mongo.db.users.find_one_and_update({
                'userName': name}, {'$pull': {'favoritesTxt': drink_id}})

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
    title = "Search"

    # Search
    if request.args:
        # Put user selected filters into 'filter_dict' for use in search query
        filters = request.args.to_dict()
        filter_dict = {}
        list_of_filters = ['category_filter', 'glassType_filter',
                           'difficulty_filter']
        for k, v in filters.items():
            if k in list_of_filters and v != "":
                new_k = k.split("_")[0]
                filter_dict[new_k] = v

        # Track filter values with pagination
        category_filter = filters[
            'category_filter'] if 'category_filter' in filters else []
        glass_type_filter = filters[
            'glassType_filter'] if 'glassType_filter' in filters else []
        difficulty_filter = filters[
            'difficulty_filter'] if 'difficulty_filter' in filters else []

        # Get Search Term
        find = request.args['find']

        # Sort Options
        # Check if session exists
        if session.get('sort_options') is None:
            session['sort_options'] = default_sort_options

        if request.method == "POST":
            sort_drinks(mongo)
            # State if sort by relevance first
            session['sort_options'][
                3] = 1 if 'relevance' in request.form else 0
            return redirect(url_for('search',
                                    category_filter=category_filter,
                                    glassType_filter=glass_type_filter,
                                    difficulty_filter=difficulty_filter,
                                    find=find))

        # Set Drinks Display Options
        results_per_page = session['sort_options'][0]
        sort_by = session['sort_options'][2]
        sort_order = session['sort_options'][4]

        current_page = int(request.args.get('current_page', 1))

        # Set 'sort_values' based on user input
        sort_values = [(sort_by, sort_order), ('name', pymongo.ASCENDING)] if \
            session['sort_options'][3] != 1 else [
            ('score', {'$meta': 'textScore'}),
            (sort_by, sort_order),
            ('name', pymongo.ASCENDING)]

        sort_options = session['sort_options']

        # Create 'search_str' for use in search
        search_str = {'$text': {'$search': find}} if find != "" else {
            'name': {'$regex': ""}}

        results = mongo.db.drinks.find(
            {'$and': [search_str, filter_dict]},
            {'score': {'$meta': 'textScore'}}
        ).sort(sort_values
               ).skip((current_page - 1) * results_per_page
                      ).limit(results_per_page)

        num_results = results.count()

        # If no results for search
        if num_results == 0:
            return render_template('search.html',
                                   title="No Results Found",
                                   find=find,
                                   num_results=num_results,
                                   # Items for filters
                                   all_categories=all_categories,
                                   all_glass_types=all_glass_types,
                                   all_difficulties=all_difficulties)

        # Pagination & Summary
        num_pages = range(1,
                          int(math.ceil(num_results / results_per_page)) + 1)
        x = current_page * results_per_page
        first_result_num = x - results_per_page + 1
        last_result_num = x if x < num_results else num_results

        # Set 'max-weight'
        # - used to calculate score relevance as % of max score returned
        max_weight = mongo.db.drinks.find_one(
            {'$and': [{'$text': {'$search': find}}, filter_dict]},
            {'score': {'$meta': 'textScore'}},
            sort=[('score', {'$meta': 'textScore'})])[
            'score'] if find != "" else None

        # Page Title
        title = "Search Results"

        return render_template('search.html',
                               title=title,
                               find=find,
                               # Results
                               results=results,
                               first_result_num=first_result_num,
                               last_result_num=last_result_num,
                               # Search result scores
                               max_weight=max_weight,
                               # Pagination | Navigation
                               results_per_page=results_per_page,
                               # Check if needed?
                               current_page=current_page,
                               pages=num_pages,
                               # Pagination | Filter Choices
                               category_filter=category_filter,
                               glassType_filter=glass_type_filter,
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


@app.route("/view_only/<option>/<choice>", methods=['GET', 'POST'])
def view_only(option, choice):
    if option == 'category':
        view = mongo.db.categories.find_one({option: choice})
    elif option == 'difficulty':
        view = mongo.db.difficulty.find_one({option: choice})
    else:
        view = mongo.db.glass.find_one({option: choice})

    title = view[option].title()

    # Sort Options
    # Check if session exists
    if session.get('sort_options') is None:
        session['sort_options'] = default_sort_options

    if request.method == "POST":
        sort_drinks(mongo)
        return redirect(url_for('view_only',
                                view=view,
                                option=option,
                                choice=choice))

    drinks_per_page = session['sort_options'][0]
    sort_by = session['sort_options'][2]
    sort_order = session['sort_options'][4]
    sort_options = session['sort_options']

    # Pagination
    current_page = int(request.args.get('current_page', 1))
    total_drinks = mongo.db.drinks.find({option: choice}).count()
    num_pages = range(1, int(math.ceil(total_drinks / drinks_per_page)) + 1)
    drinks = mongo.db.drinks.find({option: choice}) \
        .sort(sort_by, sort_order).skip(
        (current_page - 1) * drinks_per_page).limit(drinks_per_page)

    # Summary - (example) 'showing 1 - 9 of 15 results'
    x = current_page * drinks_per_page
    first_result_num = x - drinks_per_page + 1
    last_result_num = x if x < total_drinks else total_drinks

    return render_template('view_only.html',
                           view=view,
                           option=option,
                           choice=choice,
                           title=title,
                           drinks=drinks,
                           # Display Options
                           sort_options=sort_options,
                           # Pagination
                           current_page=current_page,
                           pages=num_pages,
                           first_result_num=first_result_num,
                           last_result_num=last_result_num,
                           # Items for Drop Downs
                           num_drinks_list=num_drinks_list,
                           sort_by_list=sort_by_list,
                           sort_order_list=sort_order_list)


# Error Handlers

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error=404), 404


@app.errorhandler(500)
def internal_server_error(e):
    session.clear()
    return render_template('error.html', error=500), 500


# Main

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=False)
