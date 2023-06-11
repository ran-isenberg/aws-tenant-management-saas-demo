import boto3
import cachetools


@cachetools.cached(cachetools.TTLCache(maxsize=50, ttl=360))
def get_boto3_client(aws_service: str, role_arn: str, external_id: str) -> boto3.client:
    # cool security action happens here
    return boto3.client(service_name=aws_service)
