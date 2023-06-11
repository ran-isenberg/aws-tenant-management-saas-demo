from typing import Any, Dict, List

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from tenant_management_integrations.examples.tm_integration_lambda_handler.logic.handle_tenant_mgmt_events import handle_events
from tenant_management_integrations.schemas.sqs import HardenedSqsRecordModel
from tenant_management_integrations.tm_sdk import parse_tenant_mgmt_requests


def tm_integration(event: Dict[str, Any], context: LambdaContext) -> None:  # pylint: disable=unused-argument
    logger = Logger()

    tenants_requests: List[HardenedSqsRecordModel] = parse_tenant_mgmt_requests(event=event)
    logger.info('handling tenant management requests', requests_amount=len(tenants_requests))
    handle_events(tenants_requests)
    logger.info('finished handling tenant management requests', requests_amount=len(tenants_requests))
