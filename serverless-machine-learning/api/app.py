from flask import Flask, request, json
import boto3
import pickle

BUCKET_NAME = 'lambda-ml-bucket1'
MODEL_FILE_NAME = 'model.pkl'

app = Flask(__name__)

S3 = boto3.client('s3', region_name='us-east-1')

@app.route('/', methods=['POST'])
def index():    
    # Parse request body for model input 
    body_dict = request.get_json(silent=True)    
    data = body_dict['data']     
    
    # Load model
    model = load_model(MODEL_FILE_NAME)

# Make prediction 
    prediction = model.predict(data).tolist()

# Respond with prediction result
    result = {'prediction': prediction}    
   
    return json.dumps(result)

# To load the model from s3
def load_model(key):
    response = S3.get_object(Bucket=BUCKET_NAME, Key=key)
    model_str = response['Body'].read()
    model = pickle.loads(model_str)
    return model

def predict(data):
    model = load_model(MODEL_FILE_NAME)
    return model.predict(data).tolist()

if __name__ == '__main__':    
    # listen on all IPs 
    app.run(host='0.0.0.0')