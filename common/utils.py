import base64
import logging

import boto3
import requests

log = logging.getLogger(__name__)


def invoke_api_endpoint(service_name):
    client = boto3.client("apigatewayv2")
    response = client.get_apis()
    apis = response["Items"]
    api = next(api for api in apis if api["Name"] == service_name)
    url = api["ApiEndpoint"]
    print(f"Calling {url}")
    resp = requests.get(url)
    resp.raise_for_status()
    print(f"OK")


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
