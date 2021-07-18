from flask import Flask, json
from flask import jsonify
from flask import request
import numpy as np
import pandas as pd
from scipy.sparse.linalg import svds

import pickle
from joblib import dump,load
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

interests_classifer=load("LoadedModels/interests_location_based_2.joblib")
popularity_classifer=load("LoadedModels/popularity_location_based.joblib")
bakery_df = pd.read_csv('dataset/bakeries_location.csv')


def recommend_interests_restaurants(df, longitude, latitude):
    # Predict the cluster for longitude and latitude provided
    cluster = interests_classifer.predict(np.array([longitude,latitude]).reshape(1,-1))[0]
    cluster1=int(cluster)
    print(cluster1)
    df.head()
    # Get the best restaurant in this cluster
    filtered_df = df[df['cluster']==cluster1]
    filtered_df.head()
    return filtered_df.iloc[0:5][['placeID','name','types_of_bread', 'latitude','longitude']]

def recommend_popular_restaurants(df, longitude, latitude):
    # Predict the cluster for longitude and latitude provided
    cluster = popularity_classifer.predict(np.array([longitude,latitude]).reshape(1,-1))[0]
    cluster1=int(cluster)
    print(cluster1)
    df.head()
    # Get the best restaurant in this cluster
    filtered_df = df[df['cluster']==cluster1]
    filtered_df.head()
    return filtered_df.iloc[0:5][['placeID','name','types_of_bread', 'latitude','longitude']]

def recommend_rating_places(userID, pivot_data, pred_data, num_recommendations):
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

@app.route("/recommendInterestBakeries",methods=["POST"])
def recommendInterestBakeries():
    input=request.get_json()
    bakery_df = pd.read_csv('dataset/bakery_df_extracted.csv')

    bread_interests=input["bread_interests"]
    longitude = input["longitude"]
    latitude = input["latitude"]
    bakery_df_checkinput= bakery_df['types_of_bread']==bread_interests
    bakery_df_selected_bread=bakery_df[bakery_df_checkinput]

    result=recommend_interests_restaurants(bakery_df_selected_bread,longitude,latitude) 
    result1 = result.to_dict('records')
    return jsonify({ "result":result1})

@app.route("/recommendPopularBakeries",methods=["POST"])
def recommendPopularBakeries():
    input=request.get_json()
    pop_recommendations_df = pd.read_csv('dataset/pop_recommendations.csv')

    longitude_input = input["longitude"]
    latitude_input = input["latitude"]

    result=recommend_popular_restaurants(pop_recommendations_df,longitude_input,latitude_input) 
    result1 = result.to_dict('records')
    return jsonify({ "result":result1})

@app.route("/recommendRatedBakeries",methods=["POST"])
def recommendRatedBakeries():
    input=request.get_json()
    rating_df = pd.read_csv('dataset/userprofile_ratings.csv')

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
    result = recommend_rating_places(userid_rating_input, pivot_data, pred_data, 5)

    result1 = result.to_dict('records')
    return jsonify({ "result":result1})

if __name__=="__main__":
    app.run(debug=True)