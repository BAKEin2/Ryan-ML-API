from flask import Flask, json
from flask import jsonify
from flask import request
import pandas as pd

from joblib import dump,load
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

classifer=load("popularity_location_based.joblib")

@app.route("/recommendPopularBakeries",methods=["POST"])
#@cross_origin()
def recommendInterestBakeries():
    input=request.get_json()

    target=["name","placeID","types_of_bread"]
    
    longitude = input["longitude"]
    latitude = input["latitude"]

    '''
    placeID = input["placeID"]
    name = input["name"]
    bakery_longitude = input["longitude"]
    bakery_latitude = input["latitude"]
    '''

    popularity = [[longitude,latitude]]
    popularity_df = pd.DataFrame(popularity,columns=['longitude','latitude'])
    '''    
    bakeries = [[placeID,name,bakery_longitude,bakery_latitude]]
    bakeries_extracted = pd.DataFrame(bakeries,columns=['placeID','name','bakery_longitude','bakery_latitude'])
    '''
    result=classifer.predict(popularity_df)    

    return jsonify({ "result:" : target[result[0]] })
        


if __name__=="__main__":
    app.run(debug=True)