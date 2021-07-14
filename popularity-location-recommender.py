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

def recommend_restaurants(df, longitude, latitude):
    # Predict the cluster for longitude and latitude provided
    cluster = classifer.predict(np.array([longitude,latitude]).reshape(1,-1))[0]
    cluster1=int(cluster)
      
    # Get the best restaurant in this cluster
    return df[df['cluster']==cluster1].iloc[0:5][['placeID','name','types_of_bread', 'latitude','longitude']]

@app.route("/recommendPopularBakeries",methods=["POST"])
#@cross_origin()
def recommendPopularBakeries():
    input=request.get_json()
    pop_recommendations_df = pd.read_csv('dataset/pop_recommendations.csv').to_json()
    #target=["name","placeID","types_of_bread"]
    
    longitude_input = input["longitude"]
    latitude_input = input["latitude"]

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
    result=recommend_restaurants(pop_recommendations_df,longitude_input,latitude_input) 
    result1 = result.tolist()
    return jsonify({
        "result":[
            {"placeID" : result1[0][0][1], "name" : result1[0][0][2],"types_of_bread": result1[0][0][3],"latitude":result1[0][0][4],"longitude":result1[0][0][5]},
            {"placeID" : result1[0][1][1], "name" : result1[0][1][2],"types_of_bread": result1[0][1][3],"latitude":result1[0][1][4],"longitude":result1[0][1][5]},
            {"placeID" : result1[0][2][1], "name" : result1[0][2][2],"types_of_bread": result1[0][2][3],"latitude":result1[0][2][4],"longitude":result1[0][2][5]},
            {"placeID" : result1[0][3][1], "name" : result1[0][3][2],"types_of_bread": result1[0][3][3],"latitude":result1[0][3][4],"longitude":result1[0][3][5]},
            {"placeID" : result1[0][4][1], "name" : result1[0][4][2],"types_of_bread": result1[0][4][3],"latitude":result1[0][4][4],"longitude":result1[0][4][5]},
        ]
    })
        


if __name__=="__main__":
    app.run(debug=True)