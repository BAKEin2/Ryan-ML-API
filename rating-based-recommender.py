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
    bakery_df1 = bakery_df.sort_values(by=['rating'], ascending=False)
    result=bakery_df1[['name', 'types_of_bread', 'rating']].head()

    return jsonify({ "result:" : result})

if __name__=="__main__":
    app.run(debug=True)