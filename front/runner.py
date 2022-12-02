import base64
from pathlib import Path

import boto3


def invoke_function(function_name):
    print(f"Executing function={function_name}")
    r = client.invoke(FunctionName=function_name, LogType="Tail")

    logs = base64.b64decode(r["LogResult"]).decode("utf-8").replace("\r", "\n")
    print(f"Logs:\n{logs}")

    payload = r["Payload"].read().decode("utf-8")
    print(f"Payload:\n{payload}")
    if r.get('FunctionError') == 'Unhandled':
        print("Error!")
        exit(-1)


if __name__ == "__main__":
    client = boto3.client('lambda')
    invoke_function("front-dev-api")
