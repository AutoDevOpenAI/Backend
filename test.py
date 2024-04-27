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

resource_client = ResourceManagementClient(credential, subscription_id)

print([i for i in resource_client.resource_groups.list()])
# for resource_group in resource_client.resource_groups.list():
#     print(resource_group.name)
