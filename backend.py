import os
import re
import subprocess
from flask import Flask, request, jsonify
from openai import OpenAI
import boto3
import random
import string
import requests

client = OpenAI(
    api_key="sk-proj-blWbdsDl8v3N65dQjcVjT3BlbkFJn9OlhzKSWgOc7dKAvcqV")

app = Flask(__name__)
boto3.setup_default_session(
    aws_access_key_id='AKIA3IMIIKAEFMVXRX4Y',
    aws_secret_access_key='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',
    region_name='us-west-1'
)
cf_client = boto3.client('cloudformation')


@app.route('/create-s3', methods=['POST'])
def chat():
    data = request.json['query']
    categories = ["S3","DynamoDB","Lambda"]
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role": "system",  "content": f"You are a helpful assistant skilled in AWS services. Please categorize the following query into one of the following categories, and provide no other text. If there isn't a specific category directly in the query, choose the option that would best fit the use case. The categories are: {categories}"},
                                                  {"role": "user", "content": data}
                                              ])
    print(response)
    if response.choices[0].message.content == "S3":
        response = client.chat.completions.create(model="gpt-3.5-turbo",
                                                messages=[
                                                    {"role": "system",  "content": "You are a helpful assistant skilled in AWS services. Please create a detailed CloudFormation template for an S3 bucket. The template should include the following features: a unique bucket name with a prefix 'pearhackathon-' and the name from the prompt after, private access settings, enabled versioning, and a deletion policy set to retain the bucket when the stack is deleted. Include outputs for the bucket name. Make sure it is a YAML format and does not include any placeholders for unique AWS names/region etc - it should have generic naming convention."},
                                                    {"role": "user", "content": data}
                                                ])
    elif response.choices[0].message.content == "DynamoDB":
        response = client.chat.completions.create(model="gpt-3.5-turbo",
                                                messages=[
                                                    {"role": "system",  "content": "You are a helpful assistant skilled in AWS services. Please create a detailed CloudFormation template for an DynamoDB table. The template should include the following features: a unique bucket name with a prefix 'test-database-' and the name from the prompt - it should have generic naming convention."},
                                                    {"role": "user", "content": data}
                                                ])
    response_json = response.choices[0].message.content
    response_json = response_json[7:-3]
    print(response_json)
    filename = 'output.yaml'


    with open(filename, 'w') as file:
        file.write(response_json)

    with open(filename, 'r') as file:
        template_body = file.read()

    try:
        stack_name = ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(10))

        stack_name = 'Stack' + stack_name
        result = cf_client.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Capabilities=['CAPABILITY_IAM']
        )
        response_info = result['StackId']
        status = "Stack creation initiated successfully."
    except Exception as e:
        response_info = str(e)
        status = "Error creating stack."

    #post request
    edge_url = "http://127.0.0.1:5000/create-s3"
    keys = ['input','template','aws_url']
    edge_data = {}

    edge_data['input'] = data
    edge_data['template'] = response_json
    edge_data['aws_url'] = response_info
    edge_data['status'] = status

    requests.post(edge_url, json = edge_data)

    return jsonify({
        "stack_status": status,
        "response_info": response_info
    })


if __name__ == '__main__':
    app.run(debug=True)
