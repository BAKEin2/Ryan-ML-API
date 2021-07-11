from flask import Flask, json
from flask import jsonify
from flask import request

from joblib import dump,load
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

classifer=load("rating_based_2.joblib")

@app.route("/classifyBakeries",methods=["POST"])
#@cross_origin()
def classifyBakeries():
    input=request.get_json()

    target=["12", "14" , "24" , "35" , "57"]

    userid_input= input["userID"]
    rating_input = input["rating"]
    placeid_input = input["placeID"]

    result=classifer.predict([[userid_input,rating_input,placeid_input]])

    return jsonify({ "result" : target[result[0]] })

if __name__=="__main__":
    app.run(debug=False)