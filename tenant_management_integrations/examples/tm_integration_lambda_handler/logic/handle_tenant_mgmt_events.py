from typing import List

from aws_lambda_powertools import Logger

from tenant_management_integrations.examples.tm_integration_lambda_handler.handlers.schemas.request_types import RequestModel
from tenant_management_integrations.examples.tm_integration_lambda_handler.logic.event_handlers.activate_handler import handle_activate_event
from tenant_management_integrations.examples.tm_integration_lambda_handler.logic.event_handlers.create_handler import handle_create_event
from tenant_management_integrations.examples.tm_integration_lambda_handler.logic.event_handlers.delete_handler import handle_delete_event
from tenant_management_integrations.examples.tm_integration_lambda_handler.logic.event_handlers.suspend_handler import handle_suspend_event
from tenant_management_integrations.examples.tm_integration_lambda_handler.logic.event_handlers.update_handler import handle_update_event
from tenant_management_integrations.schemas.common import ServicesEventType, TenantMgmtException
from tenant_management_integrations.schemas.sqs import ErrorType, HardenedSqsRecordModel, ServiceFailure, ServiceResponse
from tenant_management_integrations.tm_sdk import send_response_to_tenant_mgmt_sqs, verify_tenant_mgmt_request

logger = Logger()


def handle_events(tenants_requests: List[HardenedSqsRecordModel]) -> None:

    for request in tenants_requests:
        req_event: RequestModel = request.body

        try:
            logger.info('verifying request')
            verify_tenant_mgmt_request(
                msg=request,
                role_arn='role_arn',
            )

        except TenantMgmtException:
            error_str = 'failed to validate signature and token for tenant'
            logger.exception(error_str)
            _send_failure(message=f'{error_str} {req_event.tenant_id}', tenant_request=req_event)
            continue

        handle_event(req_event)


def handle_event(tenant_request: RequestModel) -> None:

    actions_mapping = {
        ServicesEventType.CREATE: handle_create_event,
        ServicesEventType.UPDATE: handle_update_event,
        ServicesEventType.DELETE: handle_delete_event,
        ServicesEventType.ACTIVATE: handle_activate_event,
        ServicesEventType.SUSPEND: handle_suspend_event,
    }
    try:
        action_handler = actions_mapping.get(tenant_request.event_type)
        action_handler(tenant_request)
        _send_success(tenant_request)
    except Exception:  # catch any unexpected exceptions that are not caught inside action_handler etc.
        error_str = 'failed to handle tenant event'
        logger.exception(error_str)
        _send_failure(message=f'{error_str} {tenant_request.tenant_id}', tenant_request=tenant_request)


def _send_success(tenant_request: RequestModel) -> None:

    logger.info('sending success response to tenant management SQS')
    response = ServiceResponse(tenant_id=tenant_request.tenant_id, request_id=tenant_request.request_id, service='my_service')
    if tenant_request.event_type in (ServicesEventType.CREATE, ServicesEventType.ACTIVATE):
        response.endpoint = 'https://my-endpoint.mycompany.com'
        response.api_endpoint = 'https://my-endpoint.mycompany.com/api'
    _send_response_to_tm_sqs(response)


def _send_failure(message: str, tenant_request: RequestModel) -> None:

    logger.info('sending failure response to tenant management SQS')
    response = ServiceResponse(tenant_id=tenant_request.tenant_id, request_id=tenant_request.request_id, service='my_service')
    response.failures = [ServiceFailure(error_type=ErrorType.GENERAL, message=message)]
    _send_response_to_tm_sqs(response)


def _send_response_to_tm_sqs(response: ServiceResponse) -> None:

    try:
        send_response_to_tenant_mgmt_sqs(
            response=response,
            tenant_mgmt_sqs_url='sqs_url',
            sqs_role_arn='my_role_arn',
            external_id='000',
        )
    except TenantMgmtException:
        logger.exception(
            'failed to send response to tenant management SQS',
            service=response.service,
            tenant_id=response.tenant_id,
            request_id=response.request_id,
            failures=response.failures,
        )
