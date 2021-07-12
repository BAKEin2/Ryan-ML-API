from flask import Flask, json
from flask import jsonify
from flask import request
import pandas as pd
import pickle

from joblib import dump,load
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

model = load("rating_based_2.joblib")
pred_data = pickle.load(open("pred_data.dat", "rb"))
pivot_data = pickle.load(open("pivot_data.dat", "rb"))
@app.route("/recommendBakeries",methods=["POST"])
#@cross_origin()
def recommend_places():
    input=request.get_json()
    pred_data = pickle.load(open("pred_data.dat", "rb"))
    pivot_data = pickle.load(open("pivot_data.dat", "rb"))
    #target=["name","placeID","types_of_bread",'user_ratings']
    '''
    userid_input= input["userID"]
    rating_input = input["rating"]
    placeID_input = input["placeID"]
    '''
    userid_input= input["userID"]
    pred_data = pred_data
    pivot_data = pivot_data
    num_recommendations_input= input["num_recommendations"]


    result=model.predict([[userid_input,pred_data,pivot_data,num_recommendations_input]])

    return jsonify({ "result:" : result})

if __name__=="__main__":
    app.run(debug=True)