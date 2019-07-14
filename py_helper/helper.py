import random
from flask import request, session

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
       
       
def sort_drinks(mongo, sort_options):
    """
        Text Here
    """
    # Number Of Drinks To Display
    num_drinks_display = request.form['num_drinks_display']
    sort_options[0]=mongo.db.drinks.count() if num_drinks_display\
        == 'All' else int(num_drinks_display)
    sort_options[1] = num_drinks_display
    
    # Drinks Sort By
    sort_by = request.form['sort_by']
    sort_options[2] = sort_by
    sort_options[3] = 0
    
    # Drinks Sort Order
    sort_order = request.form['sort_order']
    sort_options[4]=1 if sort_order=='Ascending' else -1
    sort_options[5]=sort_order
    
    return