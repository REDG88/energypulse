import boto3
from flask import Flask, request, jsonify, render_template
import pandas as pd

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
    client = boto3.client('bedrock')
    response = client.invoke_model(
        ModelId='your-model-id',  # Replace with your Bedrock model ID
        Body={
            'input': prompt
        }
    )
    return response['output']

# Load your data (replace with your bucket and file name)
bucket_name = 'your-bucket-name'
file_key = 'your-file.csv'
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
    app.run(host='0.0.0.0', port=80)
