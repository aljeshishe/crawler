import base64
import logging
import time

import boto3
import requests
from dotenv import dotenv_values

log = logging.getLogger(__name__)


def dot_env_config():
    return dotenv_values()


def invoke_api_endpoint(service_name, timeout=30):
    client = boto3.client("apigatewayv2")
    response = client.get_apis()
    apis = response["Items"]
    api = next(api for api in apis if api["Name"] == service_name)
    url = api["ApiEndpoint"]

    print(f"Calling {url}")
    start_time = time.time()
    while time.time() - start_time < timeout:
        resp = requests.get(url)
        if resp.status_code == 200:
            print(f"OK")
            return
        if resp.status_code == 500:
            print("Response 500. Retrying...")
            continue
    resp.raise_for_status()


def invoke_function(function_name):
    print(f"Executing function={function_name}")
    client = boto3.client('lambda')
    r = client.invoke(FunctionName=function_name, LogType="Tail")

    logs = base64.b64decode(r["LogResult"]).decode("utf-8")
    print(f"Logs:\n{logs}")

    payload = r["Payload"].read()
    print(f"Payload:\n{payload}")
    if r.get('FunctionError') == 'Unhandled':
        print("Error!")
        exit(-1)
    print("OK")
