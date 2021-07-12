from flask import Flask, json
from flask import jsonify
from flask import request
import pandas as pd

from joblib import dump,load
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

model=load("user_visited_based_2.joblib")

@app.route("/recommendVisitedBakeries",methods=["POST"])
#cross_origin()
def recommendVisitedBakeries():
    input=request.get_json()

    target=["rating","placeID"]

    userID= input["userID"]
    placeID = input["placeID"]
    transactions = input["transactions"]
    user_latitude= input["user_latitude"]
    user_longitude = input["user_longitude"]
    visited = [[userID,placeID,transactions,user_latitude,user_longitude]]
    visitedDF = pd.DataFrame(visited,columns=['userID','placeID','transactions','user_latitude,','user_longitude'])
    result=model.predict(visitedDF)

    return jsonify({ "result:" : result})

if __name__=="__main__":
    app.run(debug=True)