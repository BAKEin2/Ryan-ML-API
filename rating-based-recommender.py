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

    return jsonify({
        "result":[target[
            {"placeID" : result[0][0][1], "ratings" : result[0][0][2],"types_of_bread" : result[0][0][3]},
            {"placeID" : result[0][1][1], "ratings" : result[0][1][2],"types_of_bread" : result[0][1][3]},
            {"placeID" : result[0][2][1], "ratings" : result[0][2][2],"types_of_bread" : result[0][2][3]},
        ]]
    })

if __name__=="__main__":
    app.run(debug=True)