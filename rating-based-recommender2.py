from flask import Flask, json
from flask import jsonify
from flask import request
import pandas as pd

from joblib import dump,load
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

model=load("rating_based_2.joblib")

@app.route("/recommendBakeries",methods=["POST"])
#@cross_origin()
def recommendBakeries():
    input=request.get_json()

    target=["name","placeID","types_of_bread",'user_ratings']

    userid_input= input["userID"]
    rating_input = input["rating"]
    placeID_input = input["placeID"]

    result=model.predict([[userid_input,rating_input,placeID_input]])

    return jsonify({ "result:" : result})

if __name__=="__main__":
    app.run(debug=True)