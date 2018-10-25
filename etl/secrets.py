import boto3
import os


def get_secret(name: str, source: str="envrionment") -> str:
    if source == "environment":
        secret = os.environ.get(name, None)
    elif source == "ssm":
        client = boto3.client("secretsmanager")
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=name
            )
        except boto3.ClientError as e:
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
            else:
                if 'SecretString' in get_secret_value_response:
                    secret = get_secret_value_response['SecretString']
                else:
                    secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    else:
        raise NotImplementedError(f"{source} is not a supported source")
    return secret

    
