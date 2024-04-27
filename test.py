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


subscription_id = "08c87e2a-61cf-43ec-bce5-6312d648f88a"
resource_group_name = "AutoDev"
location = "westus2"

credential = ClientSecretCredential(client_id="3173bcd6-ef08-478e-b883-822f707f23d0",
                                    tenant_id="2cdd854f-3936-41b0-a9c1-70b6e605cf08",
                                    client_secret="pYP8Q~ONWB0T1pJYivl6gKZPnoHOFbUarX4SyaA-"
                                    )
resource_client = ResourceManagementClient(credential, subscription_id)

for resource_group in resource_client.resource_groups.list():
    print(resource_group.name)
