from flask import Flask, app
from flask import jsonify
from flask import request
from joblib import load
from get_tweets import get_related_tweets
from flask_cors import CORS

import tensorflow as tf
import cv2
import numpy as np


pipeline = load("user_visited_based_2.joblib")

# function to get results for a particular text query
def requestResults(name):
    # get the tweets text
    tweets = get_related_tweets(name)
    # get the prediction
    tweets['prediction'] = pipeline.predict(tweets['tweet_text'])
    # get the value counts of different labels predicted
    data = str(tweets.prediction.value_counts()) + '\n\n'
    return data + str(tweets)

app = Flask(__name__)
CORS(app)
# render default webpage
@app.route('/')
@cross_origin()
def home():
    return render_template('home.html')

# when the post method detect, then redirect to success function
@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def get_data():
    if request.method == 'POST':
        user = request.form['search']
        return redirect(url_for('success', name=user))

# get the data for the requested query
@app.route('/success/<name>')
@cross_origin()
def success(name):
    return "<xmp>" + str(requestResults(name)) + " </xmp> "

if __name__=="__main__":
    app.run(debug=False)