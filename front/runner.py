import boto3
import requests


def invoke_function(service_name):
    client = boto3.client("apigatewayv2")
    response = client.get_apis()
    apis = response["Items"]
    api = next(api for api in apis if api["Name"] == service_name)
    url = api["ApiEndpoint"]
    print(f"Calling {url}")
    resp = requests.get(url)
    resp.raise_for_status()
    print(f"OK")



if __name__ == "__main__":
    client = boto3.client('lambda')
    invoke_function("dev-front")
