import boto3
from flask import Flask, request, jsonify, render_template
import pandas as pd
import json

# Initialize Flask app
app = Flask(__name__)

# Load the CSV file from S3
def load_csv_from_s3(bucket_name, file_key):
    s3_client = boto3.client('s3')
    obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
    df = pd.read_csv(obj['Body'])
    return df

# Function to invoke the Bedrock model
def invoke_bedrock_model(prompt):
    client = boto3.client('bedrock-runtime', region_name='us-east-1')  # Use bedrock-runtime, specify region
    body = json.dumps({"inputText": prompt})  # JSON format for input
    response = client.invoke_model(
        modelId='amazon.titan-text-premier-v1:0',  # Replace with your Bedrock model ID
        contentType='application/json',
        body=body  # Pass the JSON formatted body
    )
    result = response['body'].read().decode('utf-8')  # Decode the response
    return result

# Load your data (replace with your bucket and file name)
bucket_name = 'energy-pulse-dataset'
file_key = 'energy_sector_data.csv'
data_frame = load_csv_from_s3(bucket_name, file_key)

# Home route to serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint for querying the agent
@app.route('/query', methods=['POST'])
def handle_query():
    user_query = request.json.get('query')
    query_type = request.json.get('type')

    # Construct the prompt for the Bedrock model
    prompt = f"{query_type}: {user_query}"

    # Invoke the Bedrock model and return the result
    result = invoke_bedrock_model(prompt)
    return jsonify(result)

# API endpoint for metrics
@app.route('/metrics', methods=['GET'])
def get_metrics():
    fault_counts = data_frame['Fault_Type'].value_counts().to_dict()
    return jsonify(fault_counts)

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8098)
