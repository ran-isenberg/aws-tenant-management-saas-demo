from typing import Any, Dict, List

import boto3
import cachetools
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import ValidationError as ParseError
from aws_lambda_powertools.utilities.parser import parse
from botocore.exceptions import ClientError
from pydantic import ValidationError

from tenant_management_integrations.schemas.common import TenantMgmtException
from tenant_management_integrations.schemas.sqs import HardenedSqsModel, HardenedSqsRecordModel, ServiceResponse

logger = Logger()


def parse_tenant_mgmt_requests(event: Dict[str, Any]) -> List[HardenedSqsRecordModel]:
    try:
        logger.info('parsing tenant mgmt request')
        parsed_event: HardenedSqsModel = parse(event, model=HardenedSqsModel)
        logger.info(f'finished parsing tenant mgmt request, found {len(parsed_event.Records)} requests')
        return parsed_event.Records
    except ParseError as exc:
        error_str = f'failed to parse tenant management requests, exception={exc}'
        logger.error(error_str)
        raise TenantMgmtException(error_str) from exc


def verify_tenant_mgmt_request(msg: HardenedSqsRecordModel) -> bool:
    # imagine security magic here
    return True


def send_response_to_tenant_mgmt_sqs(
    response: ServiceResponse,
    tenant_mgmt_sqs_url: str,
    sqs_role_arn: str,
    external_id: str,
) -> None:

    logger.info('sending response to tenant mgmt SQS')
    msg_str = response.json()

    # assume role to gain access to sqs
    try:
        client = get_boto3_client('sqs', sqs_role_arn, external_id)
    except (ClientError, ValidationError, IndexError) as exc:
        error_str = f'failed to assume role for SQS access, exception={str(exc)}'
        logger.error(error_str)
        raise TenantMgmtException(error_str) from exc

    logger.info('sending response message to TM SQS')

    try:
        client.send_message(
            QueueUrl=tenant_mgmt_sqs_url,
            MessageBody=msg_str,
            MessageAttributes=_get_sqs_message_attributes(),
            MessageDeduplicationId=f'{response.request_id}{response.service}',
            MessageGroupId=response.tenant_id,
        )
    except ClientError as exc:
        error_str = f'failed to send response to tenant mgmt SQS, exception={str(exc)}'
        logger.error(error_str)
        raise TenantMgmtException(error_str) from exc


def _get_sqs_message_attributes() -> Dict[str, Any]:
    message_attributes = {}
    message_attributes['X-Correlation-ID'] = {
        'DataType': 'String',
        'StringValue': 'correlation',
    }
    message_attributes['X-Session-ID'] = {
        'DataType': 'String',
        'StringValue': 'session_id',
    }
    return message_attributes


@cachetools.cached(cachetools.TTLCache(maxsize=50, ttl=360))
def get_boto3_client(aws_service: str, role_arn: str, external_id: str) -> boto3.client:
    # cool security action happens here
    return boto3.client(service_name=aws_service)
