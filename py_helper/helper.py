import random
from flask import request, session


def get_suggestions(mongo, num_suggestions):
    """ Returns a specified number of drinks

    This function will find all drinks not submitted by the current
    user. Of those drinks, it will then randomly select and return a
    specified number of them.

    Args:
        mongo : Always 'mongo'
        num_suggestions : The number of drinks to return (int)

    Returns:
        A list of drinks, with each drink stored as a dictionary
    """

    if session.get('username') is not None:
        other_users_drinks = list(mongo.db.drinks.find({
            "userName": {"$nin": [session['username']]}}))
    else:
        other_users_drinks = []

    suggestions = []
    if len(other_users_drinks) > 3:
        while len(suggestions) < num_suggestions:
            suggestions.append(other_users_drinks.pop(
                               random.randint(0, len(other_users_drinks)-1)))

    return suggestions


def sort_drinks(mongo):
    """ Sets the values for the 'sort_options' session list

    Function uses the values from request.form to set the contents of
    'sort_options'. The function returns None as 'sort_options' is
    global and values are set from within this function.

    Args:
        mongo : Always 'mongo'

    Returns:
        None
    """

    # Number Of Drinks To Display
    num_drinks_display = request.form['num_drinks_display']
    session['sort_options'][0] = mongo.db.drinks.count() if num_drinks_display\
        == 'All' else int(num_drinks_display)
    session['sort_options'][1] = num_drinks_display

    # Drinks Sort By
    sort_by = request.form['sort_by']
    session['sort_options'][2] = sort_by
    session['sort_options'][3] = 0

    # Drinks Sort Order
    sort_order = request.form['sort_order']
    session['sort_options'][4] = 1 if sort_order == 'Ascending' else -1
    session['sort_options'][5] = sort_order

    session['sort_options'] = session['sort_options']

    return None


def get_ingredients(drink_dict):
    """ Create a list of ingredients and measures

    Form data is passed as a dictionary. The functions iterates through
    the key/value pairs and appends the ingredients and measures to its
    own list called ingredients.

    Args:
        drink_dict : The dictionary containing the ingredients

    Returns:
        A list of alternating measures and ingredients
    """

    ingredients = []
    for k, v in list(drink_dict.items()):
        if ('ingredient' in k) or ('measure' in k):
            ingredients.append(v)
            drink_dict.pop(k)

    return ingredients
