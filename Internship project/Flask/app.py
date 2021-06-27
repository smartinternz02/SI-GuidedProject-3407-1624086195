import numpy as np
import pandas as pd
from flask import Flask,render_template,request
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Uas2INotcbV0_vnRrKwTvtEqu_jw03g1YNDZmGsnh-Zj"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/Prediction')
def prediction():
    return render_template('web.html')
@app.route('/Home')
def my_home():
     return render_template('index.html')
 
    
@app.route('/predict',methods=['POST'])
def predict():
    input_features=[float(x) for x in request.form.values()]
    features_name=['sad','neutral','happy','step_count','calories_burned','hours_of_sleep','weight_kg']
    payload_scoring = {"input_data": [{"field": [features_name], "values": [input_features]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/4022b48f-76ed-4773-8aa6-b34a070d10c3/predictions?version=2021-06-27', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    if(pred == 0):
        result = "You are not fit"
    else:
        result = "You are fit"
    return render_template('web.html',prediction_text=result)
if __name__ =='__main__':
    app.run(debug=False)
