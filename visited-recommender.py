from flask import Flask, json
from flask import jsonify
from flask import request
import pandas as pd

from joblib import dump,load
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

model=load("rating_based_2.joblib")

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

    return jsonify({
        "result":[
            {"placeID" : result[0][0][1], "name" : result[0][0][2],"types_of_bread" : result[0][0][3]},
            {"placeID" : result[0][1][1], "name" : result[0][1][2],"types_of_bread" : result[0][1][3]},
            {"placeID" : result[0][2][1], "name" : result[0][2][2],"types_of_bread" : result[0][2][3]},
        ]
    })

if __name__=="__main__":
    app.run(debug=True)