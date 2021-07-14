from flask import Flask, json
from flask import jsonify
from flask import request
import pandas as pd
import numpy as np
import pickle
from scipy.sparse.linalg import svds
from joblib import dump,load
#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)


#model = load("LoadedModels/rating_based_2.joblib")
#predicted_ratings_svd = pickle.load(open("LoadedModels/predicted_ratings_svd.dat", "rb"))
bakery_df = pd.read_csv('dataset/bakeries_location.csv')
#pivot_data = pickle.load(open("pivot_data.dat", "rb"))

def recommend_places(userID, pivot_data, pred_data, num_recommendations):
    user_index  = userID-1 #index starts at 0

    sorted_user_ratings = pivot_data.iloc[user_index].sort_values(ascending = False) #sort user ratings

    sorted_user_predictions = pred_data.iloc[user_index].sort_values(ascending = False)#sorted_user_predictions
    

    temp = pd.concat([sorted_user_ratings, sorted_user_predictions], axis = 1)
    temp.index.name = 'Recommended Places'
    temp['Bakery_Name']=bakery_df['name']
    temp['Types_bread']=bakery_df['types_of_bread']
    temp.columns = ['user_ratings', 'user_predictions','Bakery_Name','Types_bread']
    
    temp = temp.loc[temp.user_ratings == 0]
    temp = temp.sort_values('user_predictions', ascending = False)

    print('\n Below are the recommended places for user(user_id = {}):\n'. format(userID))
    return temp.head(num_recommendations)

@app.route("/recommendBakeries",methods=["POST"])
#@cross_origin()
def recommendBakeries():
    input=request.get_json()
    rating_df = pd.read_csv('dataset/userprofile_ratings.csv')
    #target=["name","placeID","types_of_bread",'user_ratings']

    userid_input= input["userID"]
    rating_input = input["rating"]
    placeID_input = input["placeID"]

    new_rating = [[userid_input, placeID_input, rating_input]]
    new_ratingDF = pd.DataFrame(new_rating, columns=['userID', 'placeID', 'rating'])
    new_ratingDF

    rating_df1=pd.concat([rating_df, new_ratingDF], ignore_index=True)

    pivot_data = rating_df1.pivot_table(index = 'userID', columns = 'placeID', values = 'rating').fillna(0)

    pivot_data['user_index'] = np.arange(0, pivot_data.shape[0],1)
    pivot_data.set_index(['user_index'], inplace = True)

    U,s, VT = svds(pivot_data, k = 10)
    sigma = np.diag(s)
    all_user_predicted_ratings = np.dot(np.dot(U,sigma), VT)

    pred_data = pd.DataFrame(all_user_predicted_ratings, columns = pivot_data.columns)

    userid_rating_input = input["userID_rating"]
    result = recommend_places(userid_rating_input, pivot_data, pred_data, 5)

    result1 = result.to_dict('records')
    return jsonify({ "result":result1})

if __name__=="__main__":
    app.run(debug=True)