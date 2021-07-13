from flask import Flask, json
from flask import jsonify
from flask import request
import pandas as pd
import numpy as np

from joblib import dump,load
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

classifer=load("LoadedModels/popularity_location_based.joblib")

@app.route("/recommendPopularBakeries",methods=["POST"])
#@cross_origin()
def recommendPopularBakeries():
    input=request.get_json()
    pop_recommendations_df = pd.read_csv('dataset/pop_recommendations.csv').to_json()

    #target=["name","placeID","types_of_bread"]
    
    longitude = input["longitude"]
    latitude = input["latitude"]

    '''
    placeID = input["placeID"]
    name = input["name"]
    bakery_longitude = input["longitude"]
    bakery_latitude = input["latitude"]
    '''

      
    '''    
    bakeries = [[placeID,name,bakery_longitude,bakery_latitude]]
    bakeries_extracted = pd.DataFrame(bakeries,columns=['placeID','name','bakery_longitude','bakery_latitude'])
    ''' 
    result=classifer.predict([[longitude,latitude]])
    result1 = result.tolist()
    return jsonify({ "result:" : result1 })
        


if __name__=="__main__":
    app.run(debug=True)