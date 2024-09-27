from flask import Flask, render_template, request
import boto3
import pandas as pd

app = Flask(__name__)

# Configure AWS Clients (Bedrock and QuickSight)
session = boto3.Session(region_name='us-east-1')
bedrock_client = session.client('bedrock')
quicksight_client = session.client('quicksight')

# Route to interact with Amazon Bedrock agent
@app.route('/agent', methods=['POST'])
def interact_agent():
    user_input = request.form['user_input']
    response = bedrock_client.invoke_model(
        modelId='amazon.titan-embed-text-v1',
        body={'input': user_input}
    )
    # Extract the output from Bedrock agent's response
    agent_output = response['result']['output']
    return render_template('dashboard.html', agent_output=agent_output)

# Dashboard route to visualize QuickSight data
@app.route('/dashboard')
def dashboard():
    # Fetching energy pulse data for QuickSight
    # Embed QuickSight Dashboard for visualization
    embed_url = quicksight_client.get_dashboard_embed_url(
        AwsAccountId='your-aws-account-id',
        DashboardId='your-dashboard-id',
        IdentityType='IAM'
    )
    return render_template('dashboard.html', embed_url=embed_url['EmbedUrl'])

# Home route
@app.route('/')
def home():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
