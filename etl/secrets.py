import boto3
import os


def get_secret(name: str, source: str="envrionment") -> str:
    if source == "environment":
        secret = os.environ.get(name, None)
    elif source == "ssm":
        client = boto3.client("secretsmanager")
        secret = client.get_secret_value(
            SecretId=name
            )
    else:
        raise NotImplementedError(f"{source} is not a supported source")
    return secret

    
