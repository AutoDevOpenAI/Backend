from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError



app = Flask(__name__)
shared_data = {}

# Test route to ensure the API is working
@app.route('/')
def home():
    return "Welcome to the Flask API!"

# authentication
@app.route('/authentication', methods=['POST'])
def authenticate():
    # sample_data = {"message": "Authentified!"}
    aws_access_key_id = request.json.get('aws_access_key_id')
    aws_secret_access_key = request.json.get('aws_secret_access_key')
    shared_data["aws_access_key_id"] = aws_access_key_id
    shared_data["aws_secret_access_key"] = aws_secret_access_key
    iam = boto3.client(
        'iam',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    
    # Call AWS IAM to list users
    try:
        response = iam.list_users()
        user_names = [user['UserName'] for user in response['Users']]
        return jsonify(user_names)
    except Exception as e:
        return jsonify(error=str(e)), 400


@app.route('run_query',methods = ['GET'])
def run_query():
    query = request.json.get('query')
    cloudformation = boto3.client(
        'cloudformation',
        aws_access_key_id=shared_data["aws_access_key_id"],
        aws_secret_access_key=shared_data["aws_secret_access_key"]
    )

    #run query into gpt, get actual query we want, in terms of stack_name and template_body


    gpt_res = query

    stack_name = request.json.get('stack_name')
    template_body = request.json.get('template_body')  # JSON or YAML formatted string

    try:
        response = cloudformation.update_stack(
            StackName=stack_name,
            TemplateBody=template_body
        )
        return jsonify(response)
    except ClientError as e:
        return jsonify(error=str(e)), 400

if __name__ == '__main__':
    app.run(debug=True)
