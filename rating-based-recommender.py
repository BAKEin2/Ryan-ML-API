from flask import Flask, json
from flask import jsonify
from flask import request
import pandas as pd
import pickle

from joblib import dump,load
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)


model = load("LoadedModels/rating_based_2.joblib")
predicted_ratings_svd = pickle.load(open("LoadedModels/predicted_ratings_svd.dat", "rb"))
#pivot_data = pickle.load(open("pivot_data.dat", "rb"))

@app.route("/recommendBakeries",methods=["POST"])
#@cross_origin()
def recommend_places():
    input=request.get_json()
    bakery_df = pd.read_csv('dataset/bakeries_location.csv').to_json()
    #target=["name","placeID","types_of_bread",'user_ratings']
    '''
    userid_input= input["userID"]
    rating_input = input["rating"]
    placeID_input = input["placeID"]
    '''
    userid_input= input["userID"]
    user_ratings = predicted_ratings_svd[userid_input]
    bakery_df['rating'] = user_ratings
    bakery_df = bakery_df.sort_values(by=['rating'], ascending=False)
    bakery_df = pd.DataFrame(bakery_df[['name', 'types_of_bread', 'rating']].head())
    result=bakery_df.to_dict()

    return jsonify({
        "result":[
            {"name" : result[0][0][1], "types_of_bread" : result[0][0][2],"rating": result[0][0][3]},
            {"name" : result[0][1][1], "types_of_bread" : result[0][1][2],"rating": result[0][1][3]},
            {"name" : result[0][2][1], "types_of_bread" : result[0][2][2],"rating": result[0][2][3]},
            {"name" : result[0][3][1], "types_of_bread" : result[0][3][2],"rating": result[0][3][3]},
            {"name" : result[0][4][1], "types_of_bread" : result[0][4][2],"rating": result[0][4][3]},
        ]
    })

if __name__=="__main__":
    app.run(debug=True)