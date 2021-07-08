import os
import numpy as np
import flask
import pickle
from flask import Flask, app , redirect, url_for, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
@cross_origin()
@app.route('/index')
@cross_origin()
def index():
    return flask.render_template('index.html')

def ClusterNumberPredictor(to_predict_list):
    to_predict= np.array(to_predict_list).reshape(1,2)
    loaded_model = pickle.load(open("model.pkl","rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/result',methods = ['POST'])
def result():
    if request.method =='POST':
        to_predict_list = request.form.values()
        to_predict_list = list(map(float, to_predict_list))
        result = ClusterNumberPredictor(to_predict_list)
        cluster_number = int(result)
        prediction = "You are in cluster number ${}".format(cluster_number)

        return render_template("result.html", prediction = prediction)
        


if __name__=="__main__":
    app.run(debug=False)