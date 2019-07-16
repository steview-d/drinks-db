import random
from flask import request, session


def get_suggestions(mongo, num_suggestions):
    """ Returns a specified number of drinks

    This function will find all drinks not submitted by the current
    user. Of those drinks, it will then randomly select and return a
    specifed number of them.

    Args:
        param1 : Always 'mongo'
        param2 : The number of drinks to return (int)

    Returns:
        A list of drinks, with each drink stored as a dictionary
    """

    if session.get('username') is not None:
        other_users_drinks = list(mongo.db.drinks.find({
            "userName": {"$nin": [session['username']]}}))
    else:
        other_users_drinks = []

    suggestions = []
    if other_users_drinks:
        while len(suggestions) < num_suggestions:
            suggestions.append(other_users_drinks.pop(
                               random.randint(0, len(other_users_drinks)-1)))

    return suggestions


def sort_drinks(mongo, sort_options):
    """ Sets the values for the 'sort_options' list

    Function uses the values from request.form to set the contents of
    'sort_options'. The function returns None as 'sort_options' is a 
    global  variable and is set from within this function.

    Args:
        param1 : Always 'mongo'
        param2 : The 'sort_options' list

    Returns:
        None
    """

    # Number Of Drinks To Display
    num_drinks_display = request.form['num_drinks_display']
    sort_options[0] = mongo.db.drinks.count() if num_drinks_display\
        == 'All' else int(num_drinks_display)
    sort_options[1] = num_drinks_display

    # Drinks Sort By
    sort_by = request.form['sort_by']
    sort_options[2] = sort_by
    sort_options[3] = 0

    # Drinks Sort Order
    sort_order = request.form['sort_order']
    sort_options[4] = 1 if sort_order == 'Ascending' else -1
    sort_options[5] = sort_order

    return None


def get_ingredients(dict):
    """ Create a list of ingredients and measures

    Form data is passed as a dictionary. The functions iterates through
    the key/value pairs and appends the ingredients and measures to its
    own list called ingredients.

    Args:
        param1 : Always 'mongo'
        param2 : The dictionary containing the ingredients

    Returns:
        A list of alternating measures and ingredients
    """

    ingredients = []
    for k, v in list(dict.items()):
        if ('ingredient' in k) or ('measure' in k):
            ingredients.append(v)

    return ingredients
