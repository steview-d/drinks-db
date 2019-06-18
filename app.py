import os
from flask import Flask, redirect, render_template, request, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = 'h34dfuck'

@app.route("/")
def index():
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)