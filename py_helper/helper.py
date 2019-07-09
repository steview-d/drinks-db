import random
from flask import session

def get_suggestions(mongo,num_suggestions):
    """
        Function which returns a specified number of drinks.
        These drinks are chosen at random from all drinks in the db
        aside from those creted by the user requesting the suggestions.
    """
    try:
        other_users_drinks = list(mongo.db.drinks.find( { "userName": { "$nin": [ session['username'] ] } } ))
    except:
        other_users_drinks = []
    
    suggestions=[]
    if other_users_drinks:
        while len(suggestions) < num_suggestions:
            suggestions.append(other_users_drinks.pop(random.randint(0, len(other_users_drinks)-1)))

    return suggestions
       