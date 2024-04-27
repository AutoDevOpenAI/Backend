import os
import re
import subprocess
import json
from flask import Flask, request, jsonify
from openai import OpenAI
from azure.identity import DefaultAzureCredential
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentMode
from azure.storage.blob import BlobServiceClient

client = OpenAI(
    api_key="sk-proj-tS1RI3kvkWo5sx46XBKuT3BlbkFJVGHxBFwtOJFmisgcY293")

app = Flask(__name__)

subscription_id = "08c87e2a-61cf-43ec-bce5-6312d648f88a"
resource_group_name = "AutoDev"
location = "westus2"
blob_service_connection_string = "DefaultEndpointsProtocol=https;AccountName=autodevopenai;AccountKey=OFR9Y7VeswLUMe/8yj6+Q4c9UYZYJBITD8PkjP+oUcw1XcL99GfloiHRQvF3dULIORpdrWkQQaGn+AStU0BnAQ==;EndpointSuffix=core.windows.net"

credential = ClientSecretCredential(client_id="55a4f942-b50f-46e0-8a0a-212c9a0a8b35",
                                    tenant_id="72f988bf-86f1-41af-91ab-2d7cd011db47",
                                    client_secret="39882f9d-73a8-4634-a0a9-7233f0fc5268"
                                    )
resource_client = ResourceManagementClient(credential, subscription_id)
blob_service_client = BlobServiceClient.from_connection_string(
    blob_service_connection_string)


@app.route('/create-s3', methods=['POST'])
def chat():
    data = request.json['query']
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role": "system",   "content": "You are a helpful assistant skilled in Azure services. Please create a detailed ARM template for deploying an Azure Blob Storage account. The template should include the following features: a unique storage account name incorporating a hash or unique string to ensure global uniqueness, private access settings, and enabled blob versioning. The storage account should be located in 'westus2'. Additionally, ensure the deletion policy is set to retain the blobs even when the resource group is deleted. Format the response in valid JSON and include outputs for the storage account name."},
                                                  {"role": "user", "content": data}
                                              ])

    response_json = response.choices[0].message.content

    filename = 'response.json'
    with open(filename, 'w') as file:
        file.write(response_json)

    deploy_template(filename)

    return jsonify(response_json)


def deploy_template(template_file):
    with open(template_file, 'r') as file:
        template = json.load(file)

    deployment_properties = {
        'mode': DeploymentMode.incremental,
        'template': template
    }

    deployment_async_operation = resource_client.deployments.begin_create_or_update(
        resource_group_name,
        'deployment_name',
        deployment_properties
    )

    deployment_async_operation.wait()

    # Upload the response file to Azure Blob Storage
    blob_client = blob_service_client.get_blob_client(
        container="templates", blob=template_file)
    with open(template_file, "rb") as data:
        blob_client.upload_blob(data)


if __name__ == '__main__':
    app.run(debug=True)
