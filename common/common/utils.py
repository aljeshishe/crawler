import logging

import boto3
import munc
import yaml

log = logging.getLogger(__name__)


def invoke_function(service, stage, function):
    function_name = f"{service}-{stage}-{function}"
    r = client.invoke(FunctionName=function_name,)
    payload = r["Payload"].read()
    if r.get('FunctionError') == 'Unhandled':
        log.error(f"Failed to run function={function_name}. Output:\n{payload}")
        raise Exception("Failed to run function")
