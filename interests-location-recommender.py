from flask import Flask, json
from flask import jsonify
from flask import request

from joblib import dump,load
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

classifer=load("interest_location_based_2.joblib")

@app.route("/classifyBakeries",methods=["POST"])
#@cross_origin()
def classifyBakeries():
    input=request.get_json()

    target=["12", "14" , "24" , "35" , "57"]

    userid_input= input["userID"]
    interests_input = input["bread_interests"]
    longitude_input = input["longitude"]
    latitude_input = input["latitude"]

    result=classifer.predict([[userid_input,interests_input,longitude_input,latitude_input]])

    return jsonify({ "result" : target[result[0]] })

if __name__=="__main__":
    app.run(debug=False)