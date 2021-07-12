from flask import Flask, json
from flask import jsonify
from flask import request
import pandas as pd

from joblib import dump,load
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

classifer=load("interests_location_based_2.joblib")
bakery_df = pd.read_csv('bakeries_location.csv')  

@app.route("/recommendInterestBakeries",methods=["POST"])
#@cross_origin()
def recommendInterestBakeries():
    input=request.get_json()

    target=["name","placeID","types_of_bread"]

    userID= input["userID"]
    longitude = input["longitude"]
    latitude = input["latitude"]

    '''
    placeID = input["placeID"]
    name = input["name"]
    bakery_longitude = input["longitude"]
    bakery_latitude = input["latitude"]
    '''

    interests = [[userID,longitude,latitude]]
    interests_df = pd.DataFrame(interests,columns=['userID','longitude','latitude'])
    '''    
    bakeries = [[placeID,name,bakery_longitude,bakery_latitude]]
    bakeries_extracted = pd.DataFrame(bakeries,columns=['placeID','name','bakery_longitude','bakery_latitude'])
    '''
    result=classifer.predict(interests_df)    

    return jsonify({ "result:" : target[result[0]] })

if __name__=="__main__":
    app.run(debug=True)