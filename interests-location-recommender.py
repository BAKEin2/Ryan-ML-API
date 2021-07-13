from flask import Flask, json
from flask import jsonify
from flask import request
import numpy as np
import pandas as pd

import pickle
from joblib import dump,load
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

classifer=load("LoadedModels/interests_location_based_2.joblib")
#pred_data = pickle.load(open("bakery_df_extracted.dat", "rb"))
#bakery_df = pd.read_csv('bakeries_location.csv')  

def recommend_restaurants(df, longitude, latitude):
    # Predict the cluster for longitude and latitude provided
    cluster = classifer.predict(np.array([longitude,latitude]).reshape(1,-1))[0]
    print(cluster)
      
    # Get the best restaurant in this cluster
    return df[df['cluster']==cluster].iloc[0:10][['placeID','name','types_of_bread', 'latitude','longitude'	]]

@app.route("/recommendInterestBakeries",methods=["POST"])
#@cross_origin()

def recommendInterestBakeries():
    input=request.get_json()
    bakery_df = pd.read_csv('dataset/bakeries_location.csv').to_json()
    #target=["name","placeID","types_of_bread"]

    #userID= input["userID"]
    bread_interests=input["bread_interests"]
    longitude = input["longitude"]
    latitude = input["latitude"]
    bakery_df_checkinput= pd.DataFrame([bakery_df['types_of_bread']==bread_interests])
    bakery_df_selected_bread=pd.DataFrame([bakery_df[bakery_df_checkinput]])
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
    result=recommend_restaurants(bakery_df_selected_bread,longitude,latitude) 
    return jsonify({ "result:" : result })

if __name__=="__main__":
    app.run(debug=True)