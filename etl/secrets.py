import boto3
import os
import json
from botocore.exceptions import ClientError


def get_secret(name: str, source: str="envrionment") -> dict:
    if source == "environment":
        value = os.environ.get(name, None)
        if value is None:
            raise ValueError("No such secret in the envrionment")
    elif source == "ssm":
        client = boto3.client("secretsmanager")
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise e
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
        else:
            secret = json.loads(base64.b64decode(get_secret_value_response['SecretBinary']))
            
    else:
        raise NotImplementedError(f"{source} is not a supported source")
    return secret

    
