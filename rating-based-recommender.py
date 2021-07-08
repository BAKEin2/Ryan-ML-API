from flask import Flask, app
from flask import jsonify
from flask import request
from flask_cors import CORS

import tensorflow as tf
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

model = tf.keras.models.load_model("irisclassifier.h5")

@app.route("/classifyIris",methods=["POST"])
@cross_origin()
def classifyIris():
    input=request.get_json()

    target=["iris_setosa","Iris-versicolor","Iris-virginica"]

    sepalLength= input["sepalLength"]
    sepalWidth= input["sepalWidth"]
    petalLength= input["petalLength"]
    petalWidth= input["petalWidth"]

    result = model.predict([[sepalLength,sepalWidth,petalLength,petalWidth]])

    return jsonify({ "result" : target[np.argmax(result[0])] })

if __name__=="__main__":
    app.run(debug=False)