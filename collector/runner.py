import base64
from pathlib import Path

import boto3
import munch as munch
import yaml


def invoke_function(function_name):
    print(f"Executing function={function_name}")
    r = client.invoke(FunctionName=function_name, LogType="Tail")

    logs = base64.b64decode(r["LogResult"]).decode("utf-8")
    print(f"Logs:\n{logs}")

    payload = r["Payload"].read()
    print(f"Payload:\n{payload}")
    if r.get('FunctionError') == 'Unhandled':
        print("Error!")
        exit(-1)
    print("OK")



if __name__ == "__main__":
    client = boto3.client('lambda')
    with Path("serverless.yml").open() as f:
        data = munch.munchify(yaml.safe_load(f))
    invoke_function(function_name="collector-stage5-function")
