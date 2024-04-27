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

credential = ClientSecretCredential(client_id="768a5199-a38f-4630-b5d1-e3f0bb604b05",
                                    tenant_id="2cdd854f-3936-41b0-a9c1-70b6e605cf08",
                                    client_secret="1Lz8Q~ZDNARmWFiFE2AJPEpLayisGYq1vKYfEc.1"
                                    )

resource_client = ResourceManagementClient(credential, subscription_id)

print([i for i in resource_client.resource_groups.list()])
# for resource_group in resource_client.resource_groups.list():
#     print(resource_group.name)
